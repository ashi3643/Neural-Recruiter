import express, { Request, Response } from 'express';
import path from 'path';
import fs from 'fs';
import readline from 'readline';
import { createServer as createViteServer } from 'vite';
import { GoogleGenAI } from '@google/genai';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Initialize Express
const app = express();
const PORT = 3000;

app.use(express.json());

// Helper function to parse CSV line with quoted field support
function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = '';
  let inQuotes = false;
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    const nextChar = line[i + 1];
    
    if (char === '"') {
      if (inQuotes && nextChar === '"') {
        // Escaped quote inside quoted field
        current += '"';
        i++;
      } else {
        // Toggle quote state
        inQuotes = !inQuotes;
      }
    } else if (char === ',' && !inQuotes) {
      // Field separator
      result.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }
  
  // Add last field
  result.push(current.trim());
  
  return result;
}

// Helper function to read candidates from file (JSONL or CSV)
async function readCandidatesFromFile(filePath: string): Promise<any[]> {
  const candidates: any[] = [];
  const ext = path.extname(filePath).toLowerCase();

  if (ext === '.jsonl') {
    const fileStream = fs.createReadStream(filePath);
    const rl = readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity
    });

    for await (const line of rl) {
      if (line.trim()) {
        try {
          candidates.push(JSON.parse(line));
        } catch (e) {
          console.warn("Failed to parse line in JSONL file:", e);
        }
      }
    }
  } else if (ext === '.csv') {
    const fileStream = fs.createReadStream(filePath, { encoding: 'utf-8' });
    const rl = readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity,
    });

    let headers: string[] | null = null;
    let rowIndex = 0;

    for await (const line of rl) {
      if (!line.trim()) continue;

      if (!headers) {
        headers = parseCSVLine(line);
        continue;
      }

      rowIndex++;
      const values = parseCSVLine(line);
      if (!headers || values.length !== headers.length) {
        console.warn(`Skipping malformed CSV row ${rowIndex + 1}`);
        continue;
      }

      const row: Record<string, string> = {};
      headers.forEach((header, index) => {
        row[header] = values[index];
      });

      try {
        candidates.push({
          candidate_id: row.candidate_id || '',
          profile: {
            name: row.name || '',
            current_title: row.current_title || '',
            current_company: row.current_company || '',
            headline: row.headline || '',
            summary: row.summary || '',
            years_of_experience: parseFloat(row.years_of_experience || '0'),
            location: row.location || '',
            country: row.country || '',
          },
          skills: JSON.parse(row.skills_json || '[]'),
          career_history: JSON.parse(row.career_json || '[]'),
          education: JSON.parse(row.education_json || '[]'),
          certifications: JSON.parse(row.certifications_json || '[]'),
          redrob_signals: JSON.parse(row.signals_json || '{}'),
        });
      } catch (e) {
        console.warn(`Failed to parse CSV row ${rowIndex + 1}:`, e);
      }
    }
  } else {
    console.warn(`Unsupported file format: ${ext}`);
  }

  return candidates;
}

// API Endpoint: Retrieve candidate count without loading full payload
app.get('/api/candidates/count', async (req: Request, res: Response) => {
  try {
    const filePath = (req.query.file as string) || process.env.CANDIDATES_FILE || 'candidates.csv';
    const candidatesPath = path.join(process.cwd(), filePath);

    if (!fs.existsSync(candidatesPath)) {
      return res.status(200).json({ count: 0, file: filePath });
    }

    const ext = path.extname(candidatesPath).toLowerCase();
    if (ext === '.jsonl') {
      let count = 0;
      const fileStream = fs.createReadStream(candidatesPath);
      const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });
      for await (const line of rl) {
        if (line.trim()) count++;
      }
      return res.status(200).json({ count, file: filePath });
    }

    const candidates = await readCandidatesFromFile(candidatesPath);
    return res.status(200).json({ count: candidates.length, file: filePath });
  } catch (err: any) {
    console.error("Failed to count candidates:", err);
    return res.status(500).json({ error: "Failed to count candidates." });
  }
});

// API Endpoint: Retrieve candidates dynamically from file
app.get('/api/candidates', async (req: Request, res: Response) => {
  try {
    // Support dynamic file path via query parameter
    const filePath = (req.query.file as string) || process.env.CANDIDATES_FILE || 'candidates.csv';
    const candidatesPath = path.join(process.cwd(), filePath);
    
    if (!fs.existsSync(candidatesPath)) {
      console.warn(`${filePath} not found on disk. Client should fall back to internal mock list.`);
      return res.status(200).json({ candidates: [] });
    }

    const candidates = await readCandidatesFromFile(candidatesPath);
    return res.status(200).json({ candidates });
  } catch (err: any) {
    console.error("Failed to parse candidates file server-side:", err);
    return res.status(500).json({ error: "Failed to read candidates database." });
  }
});

// API Endpoint: Upload and parse job description file
app.post('/api/upload-jd', async (req: Request, res: Response) => {
  try {
    const { jdText, jdFile } = req.body;
    
    if (jdText) {
      // Direct JD text provided
      return res.status(200).json({ jdText, source: 'text' });
    }
    
    if (jdFile) {
      // JD file path provided
      const jdPath = path.join(process.cwd(), jdFile);
      if (!fs.existsSync(jdPath)) {
        return res.status(404).json({ error: "Job description file not found" });
      }
      
      const jdText = fs.readFileSync(jdPath, 'utf-8');
      return res.status(200).json({ jdText, source: 'file' });
    }
    
    return res.status(400).json({ error: "No JD text or file provided" });
  } catch (err: any) {
    console.error("Failed to process job description:", err);
    return res.status(500).json({ error: "Failed to process job description" });
  }
});

// API Endpoint: Upload candidate file
app.post('/api/upload-candidates', async (req: Request, res: Response) => {
  try {
    const { filePath } = req.body;
    
    if (!filePath) {
      return res.status(400).json({ error: "No file path provided" });
    }
    
    const candidatesPath = path.join(process.cwd(), filePath);
    if (!fs.existsSync(candidatesPath)) {
      return res.status(404).json({ error: "Candidate file not found" });
    }
    
    const candidates = await readCandidatesFromFile(candidatesPath);
    return res.status(200).json({ candidates, source: filePath });
  } catch (err: any) {
    console.error("Failed to process candidate file:", err);
    return res.status(500).json({ error: "Failed to process candidate file" });
  }
});

// Initialize server-side Gemini CLIENT using @google/genai SDK
const getGeminiClient = (): GoogleGenAI | null => {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey || apiKey === "MY_GEMINI_API_KEY") {
    console.warn("GEMINI_API_KEY is not configured or left as default in preview. Graceful mock fallbacks will be triggered.");
    return null;
  }
  return new GoogleGenAI({
    apiKey: apiKey,
    httpOptions: {
      headers: {
        'User-Agent': 'aistudio-build' // mandatory telemetry header from guidelines
      }
    }
  });
};

// API Endpoint: Candidate critique pre-screening evaluator powered by Gemini AI
app.post('/api/candidate-critique', async (req: Request, res: Response) => {
  try {
    const { candidateName, title, experience, skills, history } = req.body;
    
    const ai = getGeminiClient();
    if (!ai) {
      // Fallback response if API key is not present/unconfigured, allowing perfect offline evaluations
      return res.status(200).json({
        critique: `### AI Pre-Screening Evaluation for ${candidateName} (Mock Mode)\n\n` +
          `**1. Relevancy Assessment:**\n` +
          `- Stated title "${title}" with ${experience} years experience fits target profile definitions.\n` +
          `- Stated skills: ${skills.slice(0, 4).join(', ')} provide adequate background.\n\n` +
          `**2. Critical Technical Questions Suggested:**\n` +
          `- *"What specific multi-stage scaling choices did you adopt to optimize query latency for those vectors?"*\n` +
          `- *"Given your noticeable ${experience} years of experience, how do you handle online search metrics drifts?"*\n\n` +
          `**3. Outreach Pitch:**\n` +
          `- "Hi ${candidateName}, we saw your excellent history as a ${title} and think your hands-on ML expertise matches what we build at Redrob AI."`
      });
    }

    const systemInstruction = 
      "You are an elite, senior tech recruiter specialized in evaluating founding AI & Search Engineers for startup positions. " +
      "Provide a highly objective, professional, and scannable performance assessment. Speak directly to technical merits, product-vs-consulting ratios, " +
      "skill depth, and possible red flags. Do not use generic prose or marketing fluff. Use Markdown formatting with scannable headers.";

    const prompt = 
      `Analyze this candidate for the "Senior AI Engineer" position at Redrob AI. The candidate must have hands-on experience shipping ranking, search, or retrieval systems (embeddings, vector DBs, hybrid search, ranking metrics) at product-centric platforms, with 5-9 years experience.\n\n` +
      `Candidate Profile:\n` +
      `- Name: ${candidateName}\n` +
      `- Title: ${title}\n` +
      `- Experience: ${experience} years\n` +
      `- Stated Skills: ${skills.join(', ')}\n` +
      `- Recent Work Milestones:\n${history.join('\n')}\n\n` +
      `Generate your response strictly matching these 3 sections with these exact labels:\n` +
      `**1. Relevancy Assessment:** (Detailed analysis of core search metrics, and product-vs-consulting alignment)\n` +
      `**2. Critical Technical Questions Suggested:** (Provide 2 precise, deep-dive technical questions targeting their actual stated work history)\n` +
      `**3. Outreach Pitch:** (Provide a short personalized 2-sentence outreach proposal citing their specific company work history)`;

    // Call Gemini using gemini-2.5-flash (available on free tier for this project)
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: {
        systemInstruction,
        temperature: 0.2 // ultra low temperature for exact, factual evaluations
      }
    });

    const critiqueText = response.text || "Assessment could not be compiled.";

    return res.status(200).json({ critique: critiqueText });
  } catch (error: any) {
    console.error("Gemini server-side evaluation error:", error);
    return res.status(500).json({ error: "Failed to generate AI pre-screening criticism." });
  }
});

// Boot full-stack development configuration (Express + Vite Middleware integration)
async function startServer() {
  if (process.env.NODE_ENV !== "production") {
    // In development mode, Vite acts as a middleware to handle assets dynamically
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    // Serve static files in production mode
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req: Request, res: Response) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on port ${PORT} in ${process.env.NODE_ENV || 'development'} mode.`);
  });
}

startServer();
