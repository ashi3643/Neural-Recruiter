#!/usr/bin/env python3
"""
rank.py — India Runs Hackathon: Track 01 Candidate Ranking
Usage: python rank.py --candidates candidates.jsonl --out submission.csv
       python rank.py --candidates candidates.csv --jd job_description.txt --out submission.csv
Runtime: ~60–90 seconds on CPU for 100K candidates. No network, no GPU needed.
"""

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path
from typing import Optional

# Import dynamic JD parser and CSV utilities
from jd_parser import parse_jd_from_file, parse_jd_from_text, ParsedJobDescription
from csv_utils import import_candidates_from_csv, export_ranked_results, load_cached_ranking, save_ranking_cache
from config_loader import get_config
from semantic_reranker import integrate_semantic_reranking

# ── LOAD CONFIGURATION ────────────────────────────────────────────────────────

# Load configuration from config.yaml
config = get_config()

# Use config values (backwards compatibility with old variable names)
TIER_A_TITLES = config.tier_a_titles
TIER_C_TITLES = config.tier_c_titles
CONSULTING_FIRMS = config.consulting_firms
CORE_AI_SKILLS = config.core_ai_skills
PREFERRED_LOCATIONS = config.preferred_locations
TODAY = config.current_date
CORE_JD_SEMANTIC_KEYWORDS = config.default_jd_semantic_keywords


# ── TITLE TIER ────────────────────────────────────────────────────────────────

def get_title_tier_and_score(title: str) -> tuple[str, float]:
    t = title.lower()
    
    # If we have a parsed JD, check if title matches JD role type
    if PARSED_JD and PARSED_JD.role_type:
        jd_role = PARSED_JD.role_type.lower()
        if any(k in t for k in [jd_role, jd_role.replace(' ', ''), jd_role.replace('-', ' ')]):
            return 'A', 1.0
    
    # Default tier checks
    if any(k in t for k in TIER_A_TITLES):
        return 'A', 1.0
    if any(k in t for k in TIER_C_TITLES):
        return 'C', 0.01
    # Everything else = Tier B (technical, but adjacent to AI)
    return 'B', 0.40


# ── HONEYPOT DETECTION ────────────────────────────────────────────────────────

def is_honeypot(candidate: dict) -> bool:
    if not config.enable_honeypot_detection:
        return False
        
    profile = candidate['profile']
    career = candidate.get('career_history', [])
    skills = candidate.get('skills', [])
    education = candidate.get('education', [])
    certifications = candidate.get('certifications', [])

    # 1. Career history longer than stated years of experience
    career_total_months = sum(r.get('duration_months', 0) for r in career)
    profile_months = profile.get('years_of_experience', 0) * 12
    tolerance = 1.0 + config.career_duration_tolerance
    if career_total_months > profile_months * tolerance and career_total_months > config.minimum_career_months:
        return True

    # 2. Multiple expert-proficiency skills with 0 months duration
    expert_zero = sum(
        1 for s in skills
        if s.get('proficiency') == 'expert' and s.get('duration_months', 1) == 0
    )
    if expert_zero >= config.expert_zero_threshold:
        return True

    # 3. Too many "expert" skills with near-zero endorsements
    expert_skills = [s for s in skills if s.get('proficiency') == 'expert']
    total_endorsements = sum(s.get('endorsements', 0) for s in skills)
    if len(expert_skills) >= config.expert_skills_threshold and total_endorsements < config.expert_endorsements_threshold:
        return True

    # 4. Education end year in the future
    current_year = TODAY.year
    for edu in education:
        if edu.get('end_year', 0) > current_year:
            return True

    # 5. Certification year in the future
    for cert in certifications:
        if cert.get('year', 0) > current_year:
            return True

    return False


# ── SCORING COMPONENTS ────────────────────────────────────────────────────────

def score_skills(skills: list, tier: str) -> float:
    """Skill depth: proficiency × duration, weighted toward core JD skills."""
    PROF = {'expert': 1.0, 'advanced': 0.75, 'intermediate': 0.5, 'beginner': 0.25}
    total = 0.0
    for s in skills:
        name = s.get('name', '').lower()
        if any(k in name for k in CORE_AI_SKILLS):
            prof = PROF.get(s.get('proficiency', 'beginner'), 0.25)
            duration_frac = min(s.get('duration_months', 1), 36) / 36
            total += prof * duration_frac
    # Tier B: must have some core AI skills to rank, otherwise suppress
    if tier == 'B' and total < 0.3:
        return 0.0  # triggers suppression in main scorer
    return min(total / 3.0, 1.0)  # normalise: 3 strong skills = perfect score


def score_career_quality(career: list) -> float:
    """Career quality: product company ratio, AI role ratio, trajectory."""
    if not career:
        return 0.3

    total_months = max(sum(r.get('duration_months', 0) for r in career), 1)

    # Consulting firm penalty
    if config.enable_consulting_penalties:
        consulting_months = sum(
            r.get('duration_months', 0) for r in career
            if any(f in r.get('company', '').lower() for f in CONSULTING_FIRMS)
        )
        consulting_ratio = consulting_months / total_months
        if consulting_ratio >= 1.0:  # Entire career at consulting = hard disqualifier
            return 0.05
        product_score = 1.0 - consulting_ratio
    else:
        product_score = 1.0

    # AI/ML role ratio in career
    AI_ROLE_KEYWORDS = {
        'ml', 'machine learning', 'ai ', 'nlp', 'deep learning',
        'data scientist', 'applied scientist', 'search', 'recommendations',
        'retrieval', 'ranking', 'research engineer',
    }
    ai_months = sum(
        r.get('duration_months', 0) for r in career
        if any(kw in r.get('title', '').lower() for kw in AI_ROLE_KEYWORDS)
    )
    ai_months = max(ai_months, 0)
    ai_ratio = min(ai_months / 36, 1.0)  # 3+ years in AI roles = full credit

    # Career trajectory: is most recent role AI-focused?
    recent_ai = any(
        any(kw in r.get('title', '').lower() for kw in AI_ROLE_KEYWORDS)
        for r in career[:2]
    )
    trajectory_bonus = 0.15 if recent_ai else 0.0

    return min(0.50 * product_score + 0.35 * ai_ratio + trajectory_bonus, 1.0)


def score_experience(yoe: float) -> float:
    """Experience range: uses dynamic JD requirements if available, else defaults to config range."""
    if PARSED_JD and PARSED_JD.experience_range:
        min_exp, max_exp = PARSED_JD.experience_range
        # Sweet spot is within JD range
        if min_exp <= yoe <= max_exp:
            return 1.0
        # Close to range
        elif min_exp - 1 <= yoe < min_exp:
            return 0.85
        elif max_exp < yoe <= max_exp + 2:
            return 0.85
        # Further away
        elif min_exp - 2 <= yoe < min_exp - 1:
            return 0.65
        elif max_exp + 2 < yoe <= max_exp + 4:
            return 0.60
        else:
            return 0.20
    else:
        # Default: use config default range
        min_exp, max_exp = config.default_experience_range
        if min_exp <= yoe <= max_exp:
            return 1.0
        elif min_exp - 1 <= yoe < min_exp:
            return 0.85
        elif max_exp < yoe <= max_exp + 2:
            return 0.85
        elif min_exp - 2 <= yoe < min_exp - 1:
            return 0.65
        elif max_exp + 2 < yoe <= max_exp + 4:
            return 0.60
        else:
            return 0.20


def score_behavioral(signals: dict) -> tuple[float, float]:
    """Returns (behavioral_score, multiplier). Multiplier is applied to total score."""
    try:
        last_active = date.fromisoformat(signals.get('last_active_date', '2020-01-01'))
        days_inactive = (TODAY - last_active).days
    except (ValueError, TypeError):
        days_inactive = 365

    # Recency — highly inactive = multiplier kill switch
    recency = max(0.0, 1.0 - days_inactive / 180.0)

    # Response rate
    rr = signals.get('recruiter_response_rate', 0.5)

    # Notice period (using config thresholds)
    notice = signals.get('notice_period_days', 60)
    notice_thresholds = config.notice_period_thresholds
    notice_score = 1.0 if notice <= notice_thresholds['excellent'] else \
                    0.85 if notice <= notice_thresholds['good'] else \
                    0.60 if notice <= notice_thresholds['fair'] else 0.35

    # Interview completion
    icr = signals.get('interview_completion_rate', 0.5)

    # Open to work bonus
    open_bonus = 0.10 if signals.get('open_to_work_flag', False) else 0.0

    score = (0.35 * recency + 0.30 * rr + 0.20 * notice_score + 0.15 * icr) + open_bonus
    score = min(score, 1.0)

    # Multiplier — severely penalise ghosts and non-responders (using config)
    multipliers = config.behavioral_multipliers
    if days_inactive > config.inactive_severe_threshold:
        mult = multipliers['inactive_severe']
    elif days_inactive > config.inactive_moderate_threshold:
        mult = multipliers['inactive_moderate']
    elif rr < config.response_rate_threshold:
        mult = multipliers['low_response']
    else:
        mult = 1.0

    return score, mult


def score_location(profile: dict, signals: dict) -> float:
    """Location fit for India-based Redrob team."""
    loc = profile.get('location', '').lower()
    country = profile.get('country', '').lower()

    if any(city in loc for city in PREFERRED_LOCATIONS):
        return 1.0
    if 'india' in country or 'india' in loc:
        return 0.80 if signals.get('willing_to_relocate', False) else 0.60
    return 0.35 if signals.get('willing_to_relocate', False) else 0.15


def score_github(signals: dict) -> float:
    """
    Enhanced GitHub activity scoring as a coding-hygiene proxy for an AI engineer.
    Considers activity score, repository relevance, and contribution patterns.
    """
    gh = signals.get('github_activity_score', -1)
    thresholds = config.github_thresholds
    
    # Base score from activity level
    if gh == -1:
        return thresholds['no_github']
    elif gh >= thresholds['excellent']:
        base_score = 1.00
    elif gh >= thresholds['good']:
        base_score = 0.80
    elif gh >= thresholds['fair']:
        base_score = 0.60
    elif gh >= thresholds['poor']:
        base_score = 0.40
    else:
        base_score = 0.20
    
    # Bonus for relevant repositories (if data available)
    repo_bonus = 0.0
    repos = signals.get('github_repositories', [])
    if repos:
        # Check for AI/ML relevant repositories
        ai_keywords = ['machine learning', 'deep learning', 'nlp', 'computer vision', 
                      'reinforcement learning', 'transformer', 'embedding', 'vector',
                      'search', 'recommendation', 'retrieval', 'ranking']
        relevant_repos = sum(1 for repo in repos if any(kw in repo.lower() for kw in ai_keywords))
        if relevant_repos > 0:
            repo_bonus = min(relevant_repos * 0.05, 0.15)  # Max 0.15 bonus
    
    # Bonus for recent activity (if data available)
    recent_bonus = 0.0
    last_commit = signals.get('github_last_commit_date')
    if last_commit:
        try:
            from datetime import datetime
            last_commit_date = datetime.fromisoformat(last_commit.replace('Z', '+00:00'))
            days_since_commit = (TODAY - last_commit_date.date()).days
            if days_since_commit <= 30:
                recent_bonus = 0.10
            elif days_since_commit <= 90:
                recent_bonus = 0.05
        except Exception:
            pass
    
    final_score = min(base_score + repo_bonus + recent_bonus, 1.0)
    return final_score


def score_skills_with_assessment(skills: list, signals: dict, tier: str) -> float:
    """Skills depth combo score incorporating base skills plus validated Redrob assessments."""
    base_score = score_skills(skills, tier)
    if tier == 'B' and base_score == 0.0:
        return 0.0

    scores = signals.get('skill_assessment_scores', {}) if isinstance(signals, dict) else {}
    if not scores:
        assessment_score = 0.50
    else:
        relevant_scores = []
        for s, score in scores.items():
            s_lower = s.lower()
            if any(k in s_lower for k in ['python', 'machine learning', 'data science', 'ai ', 'nlp', 'deep learning', 'pytorch', 'tensorflow', 'algorithms', 'software', 'sql', 'retrieval', 'search']):
                try:
                    relevant_scores.append(float(score))
                except (ValueError, TypeError):
                    pass
        if not relevant_scores:
            assessment_score = 0.50
        else:
            assessment_score = min(sum(relevant_scores) / len(relevant_scores) / 100.0, 1.0)

    combined_score = 0.70 * base_score + 0.30 * assessment_score
    return min(combined_score, 1.0)


def score_jd_semantic_fit(candidate: dict, use_embeddings: bool = True) -> float:
    """
    Evaluates the semantic fit of the candidate's headline, summary, and career description.
    Uses sentence-transformers embeddings by default for true semantic understanding.
    Falls back to keyword matching if embeddings unavailable.
    """
    profile = candidate.get('profile', {})
    headline = (profile.get('headline') or '').lower()
    summary = (profile.get('summary') or '').lower()
    
    text = f"{headline} {summary} {profile.get('current_title', '').lower()}"
    
    for role in candidate.get('career_history', []):
        title = (role.get('title') or '').lower()
        desc = (role.get('description') or '').lower()
        text += f" {title} {desc}"
    
    # Try semantic embeddings first (AI-powered approach)
    if use_embeddings:
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np
            
            # Load model lazily (only when needed)
            if not hasattr(score_jd_semantic_fit, '_model'):
                score_jd_semantic_fit._model = SentenceTransformer('all-MiniLM-L6-v2')
                # Pre-compute JD embedding if available
                if PARSED_JD:
                    jd_text = PARSED_JD.title + ' ' + ' '.join(PARSED_JD.required_skills)
                    score_jd_semantic_fit._jd_embedding = score_jd_semantic_fit._model.encode(jd_text)
                else:
                    # Use default keywords as fallback JD text
                    jd_text = ' '.join(CORE_JD_SEMANTIC_KEYWORDS)
                    score_jd_semantic_fit._jd_embedding = score_jd_semantic_fit._model.encode(jd_text)
            
            # Compute candidate embedding and similarity
            candidate_embedding = score_jd_semantic_fit._model.encode(text)
            jd_embedding = score_jd_semantic_fit._jd_embedding
            
            # Cosine similarity
            dot_product = np.dot(candidate_embedding, jd_embedding)
            norm_candidate = np.linalg.norm(candidate_embedding)
            norm_jd = np.linalg.norm(jd_embedding)
            
            if norm_candidate > 0 and norm_jd > 0:
                similarity = dot_product / (norm_candidate * norm_jd)
                return float(similarity)
        except ImportError:
            print("[SEMANTIC] sentence-transformers not available, falling back to keyword matching")
            use_embeddings = False
        except Exception as e:
            print(f"[SEMANTIC] Embedding computation failed: {e}, falling back to keyword matching")
            use_embeddings = False
    
    # Fallback: keyword-based matching
    match_count = 0
    unique_matches = set()
    for kw in CORE_JD_SEMANTIC_KEYWORDS:
        count = text.count(kw)
        if count > 0:
            match_count += count
            unique_matches.add(kw)
            
    unique_ratio = min(len(unique_matches) / 6.0, 1.0)
    freq_score = min(match_count / 15.0, 1.0)
    
    return 0.60 * unique_ratio + 0.40 * freq_score


def get_domain_penalty_multiplier(candidate: dict) -> float:
    """Returns a multiplier (0.5 or 1.0) if candidate is from a disqualifying/irrelevant domain."""
    if not config.enable_domain_penalties:
        return 1.0
        
    profile = candidate.get('profile', {})
    headline = (profile.get('headline') or '').lower()
    summary = (profile.get('summary') or '').lower()
    title = (profile.get('current_title') or '').lower()
    
    text = f"{headline} {summary} {title}"
    
    penalty_hits = sum(1 for d in config.penalty_domains if d in text)
    if penalty_hits >= 1:
        search_hits = sum(1 for kw in ['search', 'retrieval', 'recommend', 'ranking'] if kw in text)
        if search_hits < 2:
            return 0.50
    return 1.0


# ── REASONING GENERATION ─────────────────────────────────────────────────────

def generate_reasoning(candidate: dict, score: float, components: dict) -> str:
    """Per-candidate reasoning using only facts from the profile, with skill-to-requirement mapping."""
    p = candidate['profile']
    sig = candidate['redrob_signals']
    title = p.get('current_title', 'Unknown')
    yoe = p.get('years_of_experience', 0)
    rr = sig.get('recruiter_response_rate', 0)
    notice = sig.get('notice_period_days', 0)
    loc = p.get('location', 'Unknown')

    # Top relevant skills
    PROF = {'expert': 3, 'advanced': 2, 'intermediate': 1, 'beginner': 0}
    ai_skills = sorted(
        [s for s in candidate.get('skills', [])
         if any(k in s.get('name', '').lower() for k in CORE_AI_SKILLS)],
        key=lambda s: PROF.get(s.get('proficiency', 'beginner'), 0),
        reverse=True
    )
    skill_str = ', '.join(s['name'] for s in ai_skills[:3]) if ai_skills else 'general tech skills'

    # Skill-to-requirement mapping if JD is available
    skill_match_str = ''
    if PARSED_JD and PARSED_JD.required_skills:
        candidate_skill_names = {s.get('name', '').lower() for s in candidate.get('skills', [])}
        matched_skills = [skill for skill in PARSED_JD.required_skills if skill.lower() in candidate_skill_names]
        match_count = len(matched_skills)
        total_required = len(PARSED_JD.required_skills)
        if match_count > 0:
            skill_match_str = f' | matches {match_count}/{total_required} JD requirements: {", ".join(matched_skills[:3])}'

    # Build concern string
    concerns = []
    exp_score = components.get('experience')
    if exp_score is not None and exp_score < 0.6:
        concerns.append(f'{yoe:.1f}y outside 5-9y range')
    try:
        last_active = date.fromisoformat(sig.get('last_active_date', ''))
        days = (TODAY - last_active).days
        if days > 60:
            concerns.append(f'inactive {days}d')
    except Exception:
        pass
    if notice > 60:
        concerns.append(f'{notice}d notice')

    concern_str = f'; concern: {", ".join(concerns)}' if concerns else ''

    return (
        f'{title}, {yoe:.1f}y exp; skills: {skill_str}{skill_match_str}; '
        f'response_rate={rr:.2f}; {loc}{concern_str}.'
    )


# ── MAIN SCORER ───────────────────────────────────────────────────────────────

WEIGHTS = config.weights

# Global JD data (can be updated dynamically)
PARSED_JD: Optional[ParsedJobDescription] = None

def update_jd_keywords(jd: ParsedJobDescription):
    """Update global JD keywords based on parsed job description."""
    global PARSED_JD, CORE_JD_SEMANTIC_KEYWORDS
    
    PARSED_JD = jd
    
    # Build dynamic keyword list from parsed JD
    CORE_JD_SEMANTIC_KEYWORDS = jd.required_skills + jd.preferred_skills + jd.domain_keywords
    
    # Add standard IR/search keywords if role type matches
    if any(role in jd.role_type.lower() for role in ['search', 'retrieval', 'recommendation', 'ml', 'ai']):
        CORE_JD_SEMANTIC_KEYWORDS.extend([
            'retrieval', 'ranking', 'recommendation', 'search', 'dense retrieval', 
            'hybrid search', 'hybrid retrieval', 'vector search', 'embeddings', 
            'sentence transformers', 'bm25', 'information retrieval', 'learning to rank', 
            'ltr', 'reranking', 'ndcg', 'mrr', 'map', 'evaluat', 'ab test', 'a/b test',
            'pinecone', 'weaviate', 'qdrant', 'milvus', 'faiss', 'chroma'
        ])

def compute_score(candidate: dict) -> tuple[float, dict]:
    """Returns (final_score, component_dict). Score 0 = disqualified."""

    # 1. Honeypot check
    if is_honeypot(candidate):
        return 0.0, {
            'career_quality': 0, 'skills_depth': 0, 'jd_semantic_fit': 0,
            'title_alignment': 0, 'experience_range': 0, 'experience': 0,
            'behavioral_availability': 0, 'location_fit': 0, 'github_signal': 0,
        }

    profile = candidate.get('profile', {})
    signals = candidate.get('redrob_signals', {})
    career = candidate.get('career_history', [])
    skills = candidate.get('skills', [])

    # 2. Title tier gate
    tier, title_score = get_title_tier_and_score(profile.get('current_title', ''))
    
    # 3. Skills depth with assessment
    skill_score = score_skills_with_assessment(skills, signals, tier)
    
    # Suppressed adjacent tech roles if no AI skills
    career_score = score_career_quality(career)
    exp_score = score_experience(profile.get('years_of_experience', 0))
    behav_score, behav_mult = score_behavioral(signals)
    loc_score = score_location(profile, signals)
    github_score = score_github(signals)

    if tier == 'C':
        return 0.01, {
            'career_quality': career_score, 'skills_depth': skill_score, 'jd_semantic_fit': 0,
            'title_alignment': title_score, 'experience_range': exp_score, 'experience': exp_score,
            'behavioral_availability': behav_score, 'location_fit': loc_score, 'github_signal': github_score,
            'reason': f'keyword_stuffer:{profile.get("current_title", "")}'
        }

    if tier == 'B' and skill_score == 0.0:
        return 0.05, {
            'career_quality': career_score, 'skills_depth': 0, 'jd_semantic_fit': 0,
            'title_alignment': title_score, 'experience_range': exp_score, 'experience': exp_score,
            'behavioral_availability': behav_score, 'location_fit': loc_score, 'github_signal': github_score,
            'reason': f'tech_no_ai_skills:{profile.get("current_title", "")}'
        }

    # 4. Score normal components
    semantic_score = score_jd_semantic_fit(candidate, use_embeddings=True)
    domain_mult = get_domain_penalty_multiplier(candidate)

    # 5. Weighted sum
    raw = (
        WEIGHTS['career_quality']          * career_score +
        WEIGHTS['skills_depth']            * skill_score +
        WEIGHTS['jd_semantic_fit']         * semantic_score +
        WEIGHTS['title_alignment']         * title_score +
        WEIGHTS['experience_range']        * exp_score +
        WEIGHTS['behavioral_availability'] * behav_score +
        WEIGHTS['location_fit']            * loc_score +
        WEIGHTS['github_signal']           * github_score
    )

    final = round(raw * behav_mult * domain_mult, 4)

    components = {
        'career_quality': career_score,
        'skills_depth': skill_score,
        'jd_semantic_fit': semantic_score,
        'title_alignment': title_score,
        'experience_range': exp_score,
        'experience': exp_score,  # Keep for reasoning compatibility
        'behavioral_availability': behav_score,
        'location_fit': loc_score,
        'github_signal': github_score,
    }
    return final, components


# ── ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Rank candidates for any job description (dynamic JD support)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with default JD (hardcoded for AI Engineer role)
  python rank.py --candidates candidates.jsonl --out submission.csv
  
  # Dynamic JD from file
  python rank.py --candidates candidates.jsonl --jd job_description.txt --out submission.csv
  
  # CSV input instead of JSONL
  python rank.py --candidates candidates.csv --jd job_description.txt --out submission.csv
  
  # Use LLM for JD parsing (requires GEMINI_API_KEY env var)
  python rank.py --candidates candidates.jsonl --jd job_description.txt --use-llm --out submission.csv
  
  # Load from cache if available
  python rank.py --candidates candidates.jsonl --jd job_description.txt --use-cache --out submission.csv
        """
    )
    parser.add_argument('--candidates', default='candidates.jsonl',
                        help='Path to candidates file (JSONL or CSV)')
    parser.add_argument('--jd', default=None,
                        help='Path to job description file (text). If not provided, uses default hardcoded JD')
    parser.add_argument('--jd-text', default=None,
                        help='Job description as text string (alternative to --jd file)')
    parser.add_argument('--use-llm', action='store_true',
                        help='Use LLM (Gemini) for JD parsing (requires GEMINI_API_KEY env var)'}]
    parser.add_argument('--use-cache', action='store_true',
                        help='Use cached ranking if available (saves time)')
    parser.add_argument('--out', default='submission.csv',
                        help='Output CSV path')
    parser.add_argument('--top', type=int, default=100,
                        help='Number of candidates to output (default: 100)')
    parser.add_argument('--include-components', action='store_true',
                        help='Include scoring component breakdown in output')
    parser.add_argument('--enable-semantic-reranking', action='store_true', default=True,
                        help='Enable semantic embeddings reranking for top-K candidates (default: True)')
    parser.add_argument('--disable-semantic-reranking', action='store_true',
                        help='Disable semantic embeddings reranking')
    parser.add_argument('--semantic-top-k', type=int, default=50,
                        help='Number of top candidates to semantically rerank (default: 50)')
    parser.add_argument('--semantic-weight', type=float, default=0.3,
                        help='Weight for semantic score in combined score (default: 0.3)')
    args = parser.parse_args()

    # Parse job description if provided
    parsed_jd = None
    if args.jd:
        print(f'Loading job description from {args.jd}...', flush=True)
        parsed_jd = parse_jd_from_file(args.jd, use_llm=args.use_llm)
        update_jd_keywords(parsed_jd)
        print(f'  Title: {parsed_jd.title}')
        print(f'  Role Type: {parsed_jd.role_type}')
        print(f'  Experience Range: {parsed_jd.experience_range[0]}-{parsed_jd.experience_range[1]} years')
        print(f'  Required Skills: {parsed_jd.required_skills}')
    elif args.jd_text:
        print('Parsing job description from text...', flush=True)
        parsed_jd = parse_jd_from_text(args.jd_text, use_llm=args.use_llm)
        update_jd_keywords(parsed_jd)
        print(f'  Title: {parsed_jd.title}')
        print(f'  Role Type: {parsed_jd.role_type}')
        print(f'  Experience Range: {parsed_jd.experience_range[0]}-{parsed_jd.experience_range[1]} years')
        print(f'  Required Skills: {parsed_jd.required_skills}')
    else:
        print('Using default hardcoded JD (AI Engineer role)', flush=True)

    # Load candidates
    candidates_path = Path(args.candidates)
    if not candidates_path.exists():
        print(f'ERROR: {args.candidates} not found.', file=sys.stderr)
        sys.exit(1)

    # Check cache first if requested
    cache_path = Path(args.out).with_suffix('.cache.csv')
    if args.use_cache and cache_path.exists():
        print(f'Loading cached ranking from {cache_path}...', flush=True)
        cached = load_cached_ranking(str(cache_path))
        if cached:
            print(f'Loaded {len(cached)} cached candidates', flush=True)
            # Export to requested output format
            export_ranked_results(cached, args.out, include_components=args.include_components)
            print(f'\n[DONE] {args.out} written from cache.')
            sys.exit(0)

    print(f'Loading candidates from {args.candidates}...', flush=True)
    
    # Detect file format and load accordingly
    if candidates_path.suffix == '.csv':
        candidates = import_candidates_from_csv(str(candidates_path))
    else:
        # Assume JSONL
        candidates = []
        with open(candidates_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    candidates.append(json.loads(line))
    
    print(f'Loaded {len(candidates):,} candidates', flush=True)

    print('Scoring...', flush=True)
    scored = []
    for i, c in enumerate(candidates):
        if i % 10000 == 0 and i > 0:
            print(f' {i:,} done...', flush=True)
        score, components = compute_score(c)
        scored.append((c['candidate_id'], score, components, c))

    # Apply semantic reranking if enabled (default: True)
    enable_semantic = not args.disable_semantic_reranking
    if enable_semantic and parsed_jd:
        print(f'[SEMANTIC RERANKING] Top {args.semantic_top_k} candidates...', flush=True)
        jd_text = parsed_jd.title + ' ' + ' '.join(parsed_jd.required_skills)
        scored = integrate_semantic_reranking(
            scored,
            jd_text,
            enable_semantic=True,
            top_k=args.semantic_top_k,
            semantic_weight=args.semantic_weight
        )
        print(f'[SEMANTIC RERANKING] Complete', flush=True)
    elif enable_semantic and not parsed_jd:
        print(f'[SEMANTIC RERANKING] Using default JD keywords for semantic scoring', flush=True)
        jd_text = ' '.join(CORE_JD_SEMANTIC_KEYWORDS)
        scored = integrate_semantic_reranking(
            scored,
            jd_text,
            enable_semantic=True,
            top_k=args.semantic_top_k,
            semantic_weight=args.semantic_weight
        )
        print(f'[SEMANTIC RERANKING] Complete', flush=True)

    # Sort by score desc, tie-break by candidate_id asc (per spec)
    scored.sort(key=lambda x: (-x[1], x[0]))

    top_n = scored[:args.top]

    print(f'Generating reasoning for top {args.top}...', flush=True)
    rows = []
    for rank_idx, (cid, score, components, candidate) in enumerate(top_n):
        rank = rank_idx + 1
        reasoning = generate_reasoning(candidate, score, components)
        
        if args.include_components:
            rows.append({
                'candidate_id': cid,
                'rank': rank,
                'score': score,
                'reasoning': reasoning,
                **components
            })
        else:
            rows.append({
                'candidate_id': cid,
                'rank': rank,
                'score': score,
                'reasoning': reasoning,
            })

    out_path = Path(args.out)
    print(f'Writing {out_path}...', flush=True)
    
    if args.include_components:
        fieldnames = ['candidate_id', 'rank', 'score', 'reasoning', 
                     'career_quality', 'skills_depth', 'jd_semantic_fit',
                     'title_alignment', 'experience_range', 'behavioral_availability',
                     'location_fit', 'github_signal']
        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f, fieldnames=['candidate_id', 'rank', 'score', 'reasoning']
            )
            writer.writeheader()
            writer.writerows(rows)

    # Save cache for future runs
    save_ranking_cache(rows, str(cache_path), metadata={
        'jd_title': parsed_jd.title if parsed_jd else 'default',
        'timestamp': str(date.today()),
        'candidates_file': str(candidates_path),
    })

    print(f'\n[DONE] {out_path} written.')
    print(f'[CACHE] Saved to {cache_path}')
    print(f'\nTop 5 candidates:')
    for r in rows[:5]:
        print(f" #{r['rank']} {r['candidate_id']} score={r['score']} {r['reasoning'][:80]}...")
