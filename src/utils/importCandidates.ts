import { Candidate } from '../types';

function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    const nextChar = line[i + 1];

    if (char === '"') {
      if (inQuotes && nextChar === '"') {
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (char === ',' && !inQuotes) {
      result.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }

  result.push(current.trim());
  return result;
}

function csvRowToCandidate(row: Record<string, string>): Candidate | null {
  try {
    return {
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
        current_company_size: row.current_company_size || '',
        current_industry: row.current_industry || '',
      },
      skills: JSON.parse(row.skills_json || '[]'),
      career_history: JSON.parse(row.career_json || '[]'),
      education: JSON.parse(row.education_json || '[]'),
      certifications: JSON.parse(row.certifications_json || '[]'),
      redrob_signals: JSON.parse(row.signals_json || '{}'),
    };
  } catch {
    return null;
  }
}

export async function parseCandidatesFile(file: File): Promise<Candidate[]> {
  const ext = file.name.toLowerCase();

  if (ext.endsWith('.jsonl')) {
    const text = await file.text();
    const candidates: Candidate[] = [];

    for (const line of text.split('\n')) {
      if (!line.trim()) continue;
      try {
        candidates.push(JSON.parse(line) as Candidate);
      } catch {
        // skip malformed lines
      }
    }

    return candidates;
  }

  if (ext.endsWith('.csv')) {
    const text = await file.text();
    const lines = text.split('\n').filter(line => line.trim());

    if (lines.length < 2) {
      return [];
    }

    const headers = parseCSVLine(lines[0]);
    const candidates: Candidate[] = [];

    for (let i = 1; i < lines.length; i++) {
      const values = parseCSVLine(lines[i]);
      if (values.length !== headers.length) continue;

      const row: Record<string, string> = {};
      headers.forEach((header, index) => {
        row[header] = values[index];
      });

      const candidate = csvRowToCandidate(row);
      if (candidate) {
        candidates.push(candidate);
      }
    }

    return candidates;
  }

  throw new Error('Unsupported file format. Please upload a .csv or .jsonl file.');
}
