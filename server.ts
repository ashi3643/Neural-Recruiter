import express, { Request, Response } from 'express';
import path from 'path';
import { createServer as createViteServer } from 'vite';
import { GoogleGenAI } from '@google/genai';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Initialize Express
const app = express();
const PORT = 3000;

app.use(express.json());

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

    // Call Gemini using the recommended model gemini-3.5-flash
    const response = await ai.models.generateContent({
      model: 'gemini-3.5-flash',
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
