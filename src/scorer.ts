import { Candidate, ScoreComponents, ScoringResult, SignalWeights, JobDescriptionConfig } from './types';

// ── CONSTANTS ─────────────────────────────────────────────────────────────────

const TIER_A_TITLES = [
  'ml engineer', 'machine learning engineer', 'senior machine learning engineer',
  'ai engineer', 'senior ai engineer', 'applied scientist', 'applied ml engineer',
  'applied ai engineer', 'nlp engineer', 'search engineer', 'ranking engineer',
  'retrieval engineer', 'recommendations engineer', 'recommendation systems engineer',
  'research engineer', 'ai research engineer', 'deep learning engineer',
  'data scientist', 'senior data scientist', 'principal data scientist',
  'staff machine learning engineer', 'junior ml engineer', 'ml researcher'
];

const TIER_C_TITLES = [
  'hr manager', 'hr executive', 'human resources', 'recruitment manager',
  'operations manager', 'operations executive', 'content writer', 'copywriter',
  'accountant', 'financial analyst', 'finance manager',
  'civil engineer', 'mechanical engineer', 'electrical engineer',
  'marketing manager', 'marketing executive', 'digital marketing',
  'sales executive', 'sales manager', 'business development',
  'graphic designer', 'ui designer', 'ux designer',
  'customer support', 'customer success',
  'business analyst', 'project manager'
];

const CONSULTING_FIRMS = [
  'tcs', 'tata consultancy', 'infosys', 'wipro', 'accenture', 'cognizant',
  'capgemini', 'hcl technologies', 'hcltech', 'tech mahindra', 'mphasis',
  'ltimindtree', 'mindtree', 'l&t infotech', 'hexaware', 'niit technologies',
  'mastech', 'syntel', 'zensar', 'birlasoft', 'infosonics', 'sonata software',
  'genpact', 'deloitte', 'ey', 'ernst & young', 'pwc', 'kpmg', 'cognizant technology solutions'
];

const CORE_AI_SKILLS = [
  'sentence transformers', 'sentence-transformers', 'embeddings', 'text embeddings',
  'dense retrieval', 'semantic search', 'vector search', 'vector similarity',
  'faiss', 'pinecone', 'qdrant', 'weaviate', 'milvus', 'opensearch',
  'elasticsearch', 'chroma', 'pgvector', 'redis vector',
  'rag', 'retrieval augmented generation', 'hybrid retrieval', 'bm25',
  'information retrieval', 'ranking system', 'recommendation system',
  'learning to rank', 'ltr', 'lambdamart', 'reranking',
  'ndcg', 'mrr', 'map', 'precision@k', 'recall@k', 'ranking evaluation',
  'pytorch', 'tensorflow', 'hugging face', 'transformers', 'bert', 'roberta',
  'mlflow', 'kubeflow', 'triton', 'torchserve', 'bentoml'
];

const PREFERRED_LOCATIONS = [
  'pune', 'noida', 'bengaluru', 'bangalore', 'hyderabad',
  'mumbai', 'delhi', 'gurgaon', 'gurugram', 'ncr', 'new delhi',
  'chennai', 'kolkata', 'ahmedabad', 'india'
];

const TODAY = new Date('2026-06-11');

// ── TITLE TIER ────────────────────────────────────────────────────────────────

export function get_title_tier_and_score(title: string): { tier: 'A' | 'B' | 'C'; score: number } {
  const t = title.toLowerCase().trim();
  if (TIER_A_TITLES.some(k => t.includes(k))) {
    return { tier: 'A', score: 1.0 };
  }
  if (TIER_C_TITLES.some(k => t.includes(k))) {
    return { tier: 'C', score: 0.01 };
  }
  return { tier: 'B', score: 0.40 };
}

// ── HONEYPOT DETECTION ────────────────────────────────────────────────────────

export function detect_honeypot(candidate: Candidate): { is_honeypot: boolean; reasons: string[] } {
  const profile = candidate.profile;
  const career = candidate.career_history || [];
  const skills = candidate.skills || [];
  const education = candidate.education || [];
  const certifications = candidate.certifications || [];
  const reasons: string[] = [];
  const currentYear = 2026;

  // 1. Career history longer than stated years of experience
  const career_total_months = career.reduce((sum, r) => sum + (r.duration_months || 0), 0);
  const profile_months = (profile.years_of_experience || 0) * 12;
  if (career_total_months > profile_months * 1.35 && career_total_months > 24) {
    reasons.push(`Timeline Paradox: Stated experience is ${profile.years_of_experience} yrs, but combined career history sums to ${Math.round(career_total_months / 12)} yrs.`);
  }

  // 2. Multiple expert-proficiency skills with 0 months duration
  const expert_zero = skills.filter(
    s => s.proficiency === 'expert' && (s.duration_months || 0) === 0
  ).length;
  if (expert_zero >= 3) {
    reasons.push(`Faked expert skills: Claimed ${expert_zero} "expert" skills with 0 months of experience.`);
  }

  // 3. Too many expert skills with near-zero endorsements
  const expert_skills_count = skills.filter(s => s.proficiency === 'expert').length;
  const total_endorsements = skills.reduce((sum, s) => sum + (s.endorsements || 0), 0);
  if (expert_skills_count >= 8 && total_endorsements < 5) {
    reasons.push(`Lack of Verified Endorsements: Claims ${expert_skills_count} expert skills with only ${total_endorsements} total peer endorsements.`);
  }

  // 4. Education end year in the future
  for (const edu of education) {
    if (edu.end_year > currentYear) {
      reasons.push(`Future Academic Timeline: Stated degree completion year (${edu.end_year}) is in the future.`);
      break;
    }
  }

  // 5. Certification year in the future
  for (const cert of certifications) {
    if (cert.year > currentYear) {
      reasons.push(`Future Credentials: Certification year (${cert.year}) is in the future.`);
      break;
    }
  }

  return {
    is_honeypot: reasons.length > 0,
    reasons
  };
}

// ── SCORING COMPONENTS ────────────────────────────────────────────────────────

export function score_skills(candidate: Candidate, tier: 'A' | 'B' | 'C'): number {
  const skills = candidate.skills || [];
  let total = 0.0;
  
  const PROF: Record<string, number> = {
    'expert': 1.0,
    'advanced': 0.75,
    'intermediate': 0.5,
    'beginner': 0.25
  };

  for (const s of skills) {
    const name = s.name.toLowerCase();
    if (CORE_AI_SKILLS.some(k => name.includes(k))) {
      const prof = PROF[s.proficiency] || 0.25;
      const duration_frac = Math.min(s.duration_months || 1, 36) / 36;
      total += prof * duration_frac;
    }
  }

  // Tier B: must have some core AI skills to rank, otherwise suppress
  if (tier === 'B' && total < 0.3) {
    return 0.0;
  }

  return Math.min(total / 3.0, 1.0);
}

export function score_skills_with_assessment(candidate: Candidate, tier: 'A' | 'B' | 'C'): number {
  const skills = candidate.skills || [];
  let total = 0.0;
  
  const PROF: Record<string, number> = {
    'expert': 1.0,
    'advanced': 0.75,
    'intermediate': 0.5,
    'beginner': 0.25
  };

  for (const s of skills) {
    const name = s.name.toLowerCase();
    if (CORE_AI_SKILLS.some(k => name.includes(k))) {
      const prof = PROF[s.proficiency] || 0.25;
      const duration_frac = Math.min(s.duration_months || 1, 36) / 36;
      total += prof * duration_frac;
    }
  }

  const base_score = Math.min(total / 3.0, 1.0);

  // Tier B: must have some core AI skills to rank, otherwise suppress
  if (tier === 'B' && total < 0.3) {
    return 0.0;
  }

  // Defensive checks for signals and skill assessment scores
  const signals = candidate.redrob_signals;
  if (!signals || !signals.skill_assessment_scores) {
    return 0.70 * base_score + 0.30 * 0.50; // default neutral assessment score
  }

  const scores = signals.skill_assessment_scores;
  const score_keys = Object.keys(scores || {});
  if (score_keys.length === 0) {
    return 0.70 * base_score + 0.30 * 0.50; // default neutral assessment score
  }

  const relevant_scores: number[] = [];
  const relevance_keywords = ['python', 'machine learning', 'data science', 'ai ', 'nlp', 'deep learning', 'pytorch', 'tensorflow', 'algorithms', 'software', 'sql', 'retrieval', 'search'];
  for (const k of score_keys) {
    const k_lower = k.toLowerCase();
    if (relevance_keywords.some(kw => k_lower.includes(kw))) {
      const val = Number(scores[k]);
      if (!isNaN(val)) {
        relevant_scores.push(val);
      }
    }
  }

  const assessment_score = relevant_scores.length > 0
    ? Math.min(relevant_scores.reduce((sum, v) => sum + v, 0) / relevant_scores.length / 100.0, 1.0)
    : 0.50;

  return 0.70 * base_score + 0.30 * assessment_score;
}

const CORE_JD_SEMANTIC_KEYWORDS = [
  'retrieval', 'ranking', 'recommendation', 'search', 'dense retrieval', 
  'hybrid search', 'hybrid retrieval', 'vector search', 'embeddings', 
  'sentence transformers', 'bm25', 'information retrieval', 'learning to rank', 
  'ltr', 'reranking', 'ndcg', 'mrr', 'map', 'evaluat', 'ab test', 'a/b test',
  'pinecone', 'weaviate', 'qdrant', 'milvus', 'faiss', 'chroma'
];

function extractKeywordsFromJD(jdConfig: JobDescriptionConfig): string[] {
  // Extract keywords from JD description and requirements
  const jdText = (
    `${jdConfig.title} ${jdConfig.description} ${jdConfig.core_requirements.join(' ')}`
  ).toLowerCase();
  
  // Extract key phrases from JD
  const keywords = new Set<string>();
  
  // Add explicit requirements that appear in the JD
  const technicalTerms = [
    'retrieval', 'ranking', 'recommendation', 'search', 'embeddings',
    'vector', 'dense', 'hybrid', 'semantic', 'ai', 'ml', 'machine learning',
    'nlp', 'python', 'pytorch', 'tensorflow', 'distributed', 'scale',
    'production', 'system design', 'architecture', 'infrastructure'
  ];
  
  for (const term of technicalTerms) {
    if (jdText.includes(term)) {
      keywords.add(term);
    }
  }
  
  // Extract any multi-word phrases from core requirements
  for (const req of jdConfig.core_requirements) {
    const words = req.toLowerCase().split(/\s+/);
    if (words.length >= 2) {
      // Extract bigrams and trigrams
      for (let i = 0; i < words.length - 1; i++) {
        const phrase = words.slice(i, i + 2).join(' ');
        if (phrase.length > 5) keywords.add(phrase);
      }
    }
  }
  
  // If no keywords extracted, fall back to defaults
  if (keywords.size === 0) {
    return CORE_JD_SEMANTIC_KEYWORDS;
  }
  
  // Merge with default keywords for completeness
  return Array.from(new Set([...keywords, ...CORE_JD_SEMANTIC_KEYWORDS]));
}

export function score_jd_semantic_fit(candidate: Candidate, jdConfig?: JobDescriptionConfig): number {
  const profile = candidate.profile;
  const headline = (profile.headline || '').toLowerCase();
  const summary = (profile.summary || '').toLowerCase();
  
  let text = `${headline} ${summary} ${profile.current_title || ''}`;
  
  const career = candidate.career_history || [];
  for (const role of career) {
    text += ` ${(role.title || '').toLowerCase()} ${(role.description || '').toLowerCase()}`;
  }
  
  // Use dynamic JD keywords if jdConfig provided, otherwise use defaults
  const keywords = jdConfig ? extractKeywordsFromJD(jdConfig) : CORE_JD_SEMANTIC_KEYWORDS;
  
  let match_count = 0;
  const unique_matches = new Set<string>();
  
  for (const kw of keywords) {
    if (text.includes(kw)) {
      unique_matches.add(kw);
      let idx = text.indexOf(kw);
      while (idx !== -1) {
        match_count++;
        idx = text.indexOf(kw, idx + kw.length);
      }
    }
  }
  
  const unique_ratio = Math.min(unique_matches.size / Math.max(keywords.length / 4, 6.0), 1.0);
  const freq_score = Math.min(match_count / Math.max(keywords.length * 2, 15.0), 1.0);
  
  return 0.60 * unique_ratio + 0.40 * freq_score;
}

const PENALTY_DOMAINS = [
  'computer vision', 'computervision', 'speech recognition', 'robotics',
  'image classification', 'object detection', 'text-to-speech', 'text to speech',
  'tts', 'lidar', 'autonomous vehicles', 'autonomous driving'
];

export function get_domain_penalty_multiplier(candidate: Candidate): number {
  const profile = candidate.profile;
  const headline = (profile.headline || '').toLowerCase();
  const summary = (profile.summary || '').toLowerCase();
  const title = (profile.current_title || '').toLowerCase();
  
  const text = `${headline} ${summary} ${title}`;
  
  const has_penalty_domain = PENALTY_DOMAINS.some(d => text.includes(d));
  if (has_penalty_domain) {
    const search_hits = ['search', 'retrieval', 'recommend', 'ranking'].filter(kw => text.includes(kw)).length;
    if (search_hits < 2) {
      return 0.50;
    }
  }
  return 1.0;
}

export function score_career_quality(candidate: Candidate): number {
  const career = candidate.career_history || [];
  if (career.length === 0) {
    return 0.3;
  }

  const total_months = Math.max(career.reduce((sum, r) => sum + (r.duration_months || 0), 0), 1);

  // Consulting firm penalty
  const consulting_months = career.reduce((sum, r) => {
    const is_consulting = CONSULTING_FIRMS.some(f => r.company.toLowerCase().includes(f));
    return sum + (is_consulting ? (r.duration_months || 0) : 0);
  }, 0);

  const consulting_ratio = consulting_months / total_months;
  if (consulting_ratio >= 1.0) {
    return 0.05;
  }
  const product_score = 1.0 - consulting_ratio;

  // AI role ratio
  const AI_ROLE_KEYWORDS = [
    'ml', 'machine learning', 'ai ', 'nlp', 'deep learning',
    'data scientist', 'applied scientist', 'search', 'recommendations',
    'retrieval', 'ranking', 'research engineer'
  ];
  const ai_months = career.reduce((sum, r) => {
    const is_ai = AI_ROLE_KEYWORDS.some(k => r.title.toLowerCase().includes(k));
    return sum + (is_ai ? (r.duration_months || 0) : 0);
  }, 0);

  const ai_ratio = Math.min(Math.max(ai_months, 0) / 36, 1.0);

  // Trace recent AI roles
  const recent_roles = career.slice(0, 2);
  const recent_ai = recent_roles.some(r => 
    AI_ROLE_KEYWORDS.some(k => r.title.toLowerCase().includes(k))
  );
  const trajectory_bonus = recent_ai ? 0.15 : 0.0;

  return Math.min(0.50 * product_score + 0.35 * ai_ratio + trajectory_bonus, 1.0);
}

export function score_experience_range(yoe: number): number {
  if (yoe >= 6.0 && yoe <= 8.0) return 1.0;
  if (yoe >= 5.0 && yoe < 6.0) return 0.85;
  if (yoe > 8.0 && yoe <= 9.0) return 0.85;
  if (yoe >= 4.0 && yoe < 5.0) return 0.65;
  if (yoe > 9.0 && yoe <= 11.0) return 0.60;
  if (yoe >= 3.0 && yoe < 4.0) return 0.40;
  if (yoe > 11.0 && yoe <= 14.0) return 0.45;
  return 0.20;
}

export function score_behavioral_availability(candidate: Candidate): { score: number; multiplier: number } {
  const signals = candidate.redrob_signals;
  
  let days_inactive = 365;
  try {
    const last_active = new Date(signals.last_active_date || '2020-01-01');
    days_inactive = Math.floor((TODAY.getTime() - last_active.getTime()) / (1000 * 3600 * 24));
  } catch (e) {
    days_inactive = 365;
  }

  // Recency
  const recency = Math.max(0.0, 1.0 - days_inactive / 180.0);

  // Response rate
  const rr = signals.recruiter_response_rate || 0.5;

  // Notice period
  const notice = signals.notice_period_days || 60;
  const notice_score = notice <= 15 ? 1.0 : notice <= 30 ? 0.85 : notice <= 60 ? 0.60 : 0.35;

  // Interview completion
  const icr = signals.interview_completion_rate || 0.5;

  // Open to work bonus
  const open_bonus = signals.open_to_work_flag ? 0.10 : 0.0;

  const score = (0.35 * recency + 0.30 * rr + 0.20 * notice_score + 0.15 * icr) + open_bonus;
  const final_score = Math.min(score, 1.0);

  // Multiplier
  let mult = 1.0;
  if (days_inactive > 365) {
    mult = 0.10;
  } else if (days_inactive > 180) {
    mult = 0.30;
  } else if (rr < 0.05) {
    mult = 0.40;
  }

  return { score: final_score, multiplier: mult };
}

export function score_location(candidate: Candidate): number {
  const loc = (candidate.profile.location || '').toLowerCase();
  const country = (candidate.profile.country || '').toLowerCase();
  const willing_to_relocate = candidate.redrob_signals.willing_to_relocate;

  if (PREFERRED_LOCATIONS.some(city => loc.includes(city) && city !== 'india')) {
    return 1.0;
  }
  if (country.includes('india') || loc.includes('india')) {
    return willing_to_relocate ? 0.80 : 0.60;
  }
  return willing_to_relocate ? 0.35 : 0.15;
}

export function score_github(candidate: Candidate): number {
  const gh = candidate.redrob_signals.github_activity_score;
  if (gh === -1) return 0.25;
  if (gh >= 70) return 1.00;
  if (gh >= 50) return 0.80;
  if (gh >= 30) return 0.60;
  if (gh >= 10) return 0.40;
  return 0.20;
}

// ── REASONING GENERATION ─────────────────────────────────────────────────────

export function generate_reasoning(candidate: Candidate, score: number, components: ScoreComponents): string {
  const p = candidate.profile;
  const sig = candidate.redrob_signals;
  const title = p.current_title || 'Unknown';
  const yoe = p.years_of_experience || 0;
  const rr = sig.recruiter_response_rate || 0;
  const notice = sig.notice_period_days || 0;
  const loc = p.location || 'Unknown';

  const PROF: Record<string, number> = { 'expert': 3, 'advanced': 2, 'intermediate': 1, 'beginner': 0 };
  const ai_skills = [...(candidate.skills || [])]
    .filter(s => CORE_AI_SKILLS.some(k => s.name.toLowerCase().includes(k)))
    .sort((a, b) => (PROF[b.proficiency] || 0) - (PROF[a.proficiency] || 0));

  const skill_str = ai_skills.length > 0
    ? ai_skills.slice(0, 3).map(s => s.name).join(', ')
    : 'general tech skills';

  const concerns: string[] = [];
  const exp_score = components.experience_range;
  if (exp_score < 0.6) {
    concerns.push(`${yoe.toFixed(1)}y outside 5-9y range`);
  }
  
  try {
    const last_active = new Date(sig.last_active_date || '2020-01-01');
    const days = Math.floor((TODAY.getTime() - last_active.getTime()) / (1000 * 3600 * 24));
    if (days > 60) {
      concerns.push(`inactive ${days}d`);
    }
  } catch (e) {}

  if (notice > 60) {
    concerns.push(`${notice}d notice`);
  }

  const concern_str = concerns.length > 0 ? `; concern: ${concerns.join(', ')}` : '';

  return `${title}, ${yoe.toFixed(1)}y exp; skills: ${skill_str}; response_rate=${rr.toFixed(2)}; ${loc}${concern_str}.`;
}

// ── MAIN TS COMPUTE SCORER ───────────────────────────────────────────────────

export function compute_score(candidate: Candidate, weights: SignalWeights, jdConfig?: JobDescriptionConfig): ScoringResult {
  // 1. Honeypot check
  const { is_honeypot, reasons } = detect_honeypot(candidate);
  if (is_honeypot) {
    return {
      candidate_id: candidate.candidate_id,
      candidate,
      score: 0.0,
      components: {
        title_alignment: 0,
        skills_depth: 0,
        career_quality: 0,
        experience_range: 0,
        behavioral_availability: 0,
        location_fit: 0,
        github_signal: 0,
        jd_semantic_fit: 0,
      },
      is_honeypot: true,
      honeypot_reasons: reasons,
      disqualified: true,
      disqualification_reason: 'Flagged as Honeypot Candidate: Contains impossible timelines or faked profiles.',
      multiplier: 0,
      reasoning: `Flagged Honeypot: ${reasons.join(' ')}`
    };
  }

  // 2. Title tier gate
  const title_align_info = get_title_tier_and_score(candidate.profile.current_title);
  const tier = title_align_info.tier;
  const title_align = title_align_info.score;

  // 3. Pre-score skills with assessment (used for Tier B suppression matching Python)
  const skills = score_skills_with_assessment(candidate, tier);

  // Suppressed adjacent tech roles if no AI skills
  const career = score_career_quality(candidate);
  if (tier === 'C') {
    return {
      candidate_id: candidate.candidate_id,
      candidate,
      score: 0.0100,
      components: {
        title_alignment: title_align,
        skills_depth: skills,
        career_quality: career,
        experience_range: score_experience_range(candidate.profile.years_of_experience),
        behavioral_availability: score_behavioral_availability(candidate).score,
        location_fit: score_location(candidate),
        github_signal: score_github(candidate),
        jd_semantic_fit: 0,
      },
      is_honeypot: false,
      honeypot_reasons: [],
      disqualified: true,
      disqualification_reason: `Keyword Stuffer detected with non-AI title "${candidate.profile.current_title}". Score suppressed to floor (0.01).`,
      multiplier: 1.0,
      reasoning: `Disqualified: Keyword stuffer. Title "${candidate.profile.current_title}" does not map to ML/AI/Data Science core roles.`
    };
  }

  if (tier === 'B' && skills === 0.0) {
    return {
      candidate_id: candidate.candidate_id,
      candidate,
      score: 0.0500,
      components: {
        title_alignment: title_align,
        skills_depth: 0,
        career_quality: career,
        experience_range: score_experience_range(candidate.profile.years_of_experience),
        behavioral_availability: score_behavioral_availability(candidate).score,
        location_fit: score_location(candidate),
        github_signal: score_github(candidate),
        jd_semantic_fit: 0,
      },
      is_honeypot: false,
      honeypot_reasons: [],
      disqualified: true,
      disqualification_reason: `Adjacent engineering title "${candidate.profile.current_title}" without any core AI/Retrieval/Ranking skills. Score suppressed to (0.05).`,
      multiplier: 1.0,
      reasoning: `Disqualified: Adjacent role without AI background. Title is "${candidate.profile.current_title}" with zero vector search or ML expertise.`
    };
  }

  // 4. Score normal components
  const exp = score_experience_range(candidate.profile.years_of_experience);
  const behav_detail = score_behavioral_availability(candidate);
  const availability = behav_detail.score;
  const multiplier = behav_detail.multiplier;
  const loc = score_location(candidate);
  const github = score_github(candidate);
  const jd_semantic_fit = score_jd_semantic_fit(candidate, jdConfig);

  const comps: ScoreComponents = {
    title_alignment: title_align,
    skills_depth: skills,
    career_quality: career,
    experience_range: exp,
    behavioral_availability: availability,
    location_fit: loc,
    github_signal: github,
    jd_semantic_fit: jd_semantic_fit,
  };

  // 5. Weighted score (matching target weights)
  const rawScore = (weights.career_quality * career) +
                   (weights.skills_depth * skills) +
                   (weights.title_alignment * title_align) +
                   (weights.behavioral_availability * availability) +
                   (weights.experience_range * exp) +
                   (weights.location_fit * loc) +
                   (weights.github_signal * github) +
                   (weights.jd_semantic_fit * jd_semantic_fit);

  const domain_mult = get_domain_penalty_multiplier(candidate);
  const finalScore = rawScore * multiplier * domain_mult;
  const finalScoreRounded = Math.round(finalScore * 10000) / 10000;

  const reasoning = generate_reasoning(candidate, finalScoreRounded, comps);

  return {
    candidate_id: candidate.candidate_id,
    candidate,
    score: Math.max(0.0150, finalScoreRounded),
    components: comps,
    is_honeypot: false,
    honeypot_reasons: [],
    disqualified: false,
    multiplier,
    reasoning
  };
}
