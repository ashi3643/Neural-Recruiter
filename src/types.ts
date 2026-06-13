export interface CareerRole {
  company: string;
  title: string;
  start_date: string;
  end_date: string;
  duration_months: number;
  is_current: boolean;
  industry: string;
  company_size: string;
  description: string;
}

export interface EducationEntry {
  institution: string;
  degree: string;
  field_of_study: string;
  start_year: number;
  end_year: number;
  grade: string;
  tier: 'tier_1' | 'tier_2' | 'tier_3' | 'tier_4' | 'unknown';
}

export interface SkillEntry {
  name: string;
  proficiency: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  endorsements: number;
  duration_months: number;
}

export interface CertificationEntry {
  name: string;
  issuer: string;
  year: number;
}

export interface RedrobSignals {
  open_to_work_flag: boolean;
  last_active_date: string;
  recruiter_response_rate: number;
  avg_response_time_hours: number;
  notice_period_days: number;
  github_activity_score: number;
  interview_completion_rate: number;
  offer_acceptance_rate: number;
  skill_assessment_scores: Record<string, number>;
  profile_completeness_score: number;
  applications_submitted_30d: number;
  saved_by_recruiters_30d: number;
  willing_to_relocate: boolean;
  preferred_work_mode: string;
  expected_salary_range_inr_lpa: { min: number; max: number };
  verified_email: boolean;
  verified_phone: boolean;
  linkedin_connected: boolean;
}

export interface Candidate {
  candidate_id: string;
  profile: {
    name: string;
    headline: string;
    summary: string;
    location: string;
    country: string;
    years_of_experience: number;
    current_title: string;
    current_company: string;
    current_company_size: string;
    current_industry: string;
    avatar_url?: string;
  };
  career_history: CareerRole[];
  education: EducationEntry[];
  skills: SkillEntry[];
  certifications: CertificationEntry[];
  redrob_signals: RedrobSignals;
  
  // Custom metadata for visualization purposes
  tag?: 'superstar' | 'keyword_stuffer' | 'honeypot' | 'ghost' | 'plain_language' | 'normal';
}

export interface ScoreComponents {
  title_alignment: number;
  skills_depth: number;
  career_quality: number;
  experience_range: number;
  behavioral_availability: number;
  location_fit: number;
  github_signal: number;
  jd_semantic_fit: number;
}

export interface SignalWeights {
  career_quality: number;
  skills_depth: number;
  title_alignment: number;
  behavioral_availability: number;
  experience_range: number;
  location_fit: number;
  github_signal: number;
  jd_semantic_fit: number;
}

export interface JobDescriptionConfig {
  title: string;
  company: string;
  experience_range: string;
  location: string;
  description: string;
  core_requirements: string[];
}

export interface ScoringResult {
  candidate_id: string;
  candidate: Candidate;
  score: number;
  components: ScoreComponents;
  is_honeypot: boolean;
  honeypot_reasons: string[];
  disqualified: boolean;
  disqualification_reason?: string;
  multiplier: number;
  reasoning: string;
}
