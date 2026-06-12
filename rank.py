#!/usr/bin/env python3
"""
rank.py — India Runs Hackathon: Track 01 Candidate Ranking
Usage: python rank.py --candidates candidates.jsonl --out submission.csv
Runtime: ~60–90 seconds on CPU for 100K candidates. No network, no GPU needed.
"""

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

# ── CONSTANTS ─────────────────────────────────────────────────────────────────

TIER_A_TITLES = {
    # Direct matches — the JD's ideal role types
    'ml engineer', 'machine learning engineer', 'senior machine learning engineer',
    'ai engineer', 'senior ai engineer', 'applied scientist', 'applied ml engineer',
    'applied ai engineer', 'nlp engineer', 'search engineer', 'ranking engineer',
    'retrieval engineer', 'recommendations engineer', 'recommendation systems engineer',
    'research engineer', 'ai research engineer', 'deep learning engineer',
    'data scientist', 'senior data scientist', 'principal data scientist',
    'staff machine learning engineer', 'junior ml engineer', 'ml researcher',
}

TIER_C_TITLES = {
    # Non-technical keyword stuffers — should never rank in top 100
    'hr manager', 'hr executive', 'human resources', 'recruitment manager',
    'operations manager', 'operations executive', 'content writer', 'copywriter',
    'accountant', 'financial analyst', 'finance manager',
    'civil engineer', 'mechanical engineer', 'electrical engineer',
    'marketing manager', 'marketing executive', 'digital marketing',
    'sales executive', 'sales manager', 'business development',
    'graphic designer', 'ui designer', 'ux designer',
    'customer support', 'customer success',
    'business analyst',  # with no tech background — see career gate below
    'project manager',   # same
}

CONSULTING_FIRMS = {
    'tcs', 'tata consultancy', 'infosys', 'wipro', 'accenture', 'cognizant',
    'capgemini', 'hcl technologies', 'hcltech', 'tech mahindra', 'mphasis',
    'ltimindtree', 'mindtree', 'l&t infotech', 'hexaware', 'niit technologies',
    'mastech', 'syntel', 'zensar', 'birlasoft', 'infosonics', 'sonata software',
    'genpact', 'deloitte', 'ey', 'ernst & young', 'pwc', 'kpmg', 'cognizant technology solutions',
}

CORE_AI_SKILLS = {
    # Vector/semantic retrieval
    'sentence transformers', 'sentence-transformers', 'embeddings', 'text embeddings',
    'dense retrieval', 'semantic search', 'vector search', 'vector similarity',
    # Vector DBs
    'faiss', 'pinecone', 'qdrant', 'weaviate', 'milvus', 'opensearch',
    'elasticsearch', 'chroma', 'pgvector', 'redis vector',
    # Retrieval / ranking systems
    'rag', 'retrieval augmented generation', 'hybrid retrieval', 'bm25',
    'information retrieval', 'ranking system', 'recommendation system',
    'learning to rank', 'ltr', 'lambdamart', 'reranking',
    # Evaluation
    'ndcg', 'mrr', 'map', 'precision@k', 'recall@k', 'ranking evaluation',
    # Core ML frameworks (for AI engineers who write code)
    'pytorch', 'tensorflow', 'hugging face', 'transformers', 'bert', 'roberta',
    # MLOps (production experience signal)
    'mlflow', 'kubeflow', 'triton', 'torchserve', 'bentoml',
}

PREFERRED_LOCATIONS = {
    'pune', 'noida', 'bengaluru', 'bangalore', 'hyderabad',
    'mumbai', 'delhi', 'gurgaon', 'gurugram', 'ncr', 'new delhi',
    'chennai', 'kolkata', 'ahmedabad', 'india',
}

TODAY = date(2026, 6, 11)


# ── TITLE TIER ────────────────────────────────────────────────────────────────

def get_title_tier_and_score(title: str) -> tuple[str, float]:
    t = title.lower()
    if any(k in t for k in TIER_A_TITLES):
        return 'A', 1.0
    if any(k in t for k in TIER_C_TITLES):
        return 'C', 0.01
    # Everything else = Tier B (technical, but adjacent to AI)
    return 'B', 0.40


# ── HONEYPOT DETECTION ────────────────────────────────────────────────────────

def is_honeypot(candidate: dict) -> bool:
    profile = candidate['profile']
    career = candidate.get('career_history', [])
    skills = candidate.get('skills', [])
    education = candidate.get('education', [])
    certifications = candidate.get('certifications', [])

    # 1. Career history longer than stated years of experience
    career_total_months = sum(r.get('duration_months', 0) for r in career)
    profile_months = profile.get('years_of_experience', 0) * 12
    if career_total_months > profile_months * 1.35 and career_total_months > 24:
        return True

    # 2. Multiple expert-proficiency skills with 0 months duration
    expert_zero = sum(
        1 for s in skills
        if s.get('proficiency') == 'expert' and s.get('duration_months', 1) == 0
    )
    if expert_zero >= 3:
        return True

    # 3. Too many "expert" skills with near-zero endorsements
    expert_skills = [s for s in skills if s.get('proficiency') == 'expert']
    total_endorsements = sum(s.get('endorsements', 0) for s in skills)
    if len(expert_skills) >= 8 and total_endorsements < 5:
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
    consulting_months = sum(
        r.get('duration_months', 0) for r in career
        if any(f in r.get('company', '').lower() for f in CONSULTING_FIRMS)
    )
    consulting_ratio = consulting_months / total_months
    if consulting_ratio >= 1.0:  # Entire career at consulting = hard disqualifier
        return 0.05
    product_score = 1.0 - consulting_ratio

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
    """Experience range: 6–8 years is the JD sweet spot."""
    if 6.0 <= yoe <= 8.0:    return 1.0
    elif 5.0 <= yoe < 6.0:   return 0.85
    elif 8.0 < yoe <= 9.0:   return 0.85
    elif 4.0 <= yoe < 5.0:   return 0.65
    elif 9.0 < yoe <= 11.0:  return 0.60
    elif 3.0 <= yoe < 4.0:   return 0.40
    elif 11.0 < yoe <= 14.0: return 0.45
    else:                    return 0.20   # <3 or >14 years


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

    # Notice period (<30 days preferred, >90 days penalised)
    notice = signals.get('notice_period_days', 60)
    notice_score = 1.0 if notice <= 15 else 0.85 if notice <= 30 else 0.60 if notice <= 60 else 0.35

    # Interview completion
    icr = signals.get('interview_completion_rate', 0.5)

    # Open to work bonus
    open_bonus = 0.10 if signals.get('open_to_work_flag', False) else 0.0

    score = (0.35 * recency + 0.30 * rr + 0.20 * notice_score + 0.15 * icr) + open_bonus
    score = min(score, 1.0)

    # Multiplier — severely penalise ghosts and non-responders
    if days_inactive > 365:
        mult = 0.10
    elif days_inactive > 180:
        mult = 0.30
    elif rr < 0.05:
        mult = 0.40
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
    """GitHub activity as a coding-hygiene proxy for an AI engineer."""
    gh = signals.get('github_activity_score', -1)
    if gh == -1:   return 0.25   # No GitHub = mild concern for engineering role
    elif gh >= 70: return 1.00
    elif gh >= 50: return 0.80
    elif gh >= 30: return 0.60
    elif gh >= 10: return 0.40
    else:          return 0.20


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


CORE_JD_SEMANTIC_KEYWORDS = [
    'retrieval', 'ranking', 'recommendation', 'search', 'dense retrieval', 
    'hybrid search', 'hybrid retrieval', 'vector search', 'embeddings', 
    'sentence transformers', 'bm25', 'information retrieval', 'learning to rank', 
    'ltr', 'reranking', 'ndcg', 'mrr', 'map', 'evaluat', 'ab test', 'a/b test',
    'pinecone', 'weaviate', 'qdrant', 'milvus', 'faiss', 'chroma'
]

def score_jd_semantic_fit(candidate: dict) -> float:
    """Evaluates the semantic fit of the candidate's headline, summary, and career description."""
    profile = candidate.get('profile', {})
    headline = (profile.get('headline') or '').lower()
    summary = (profile.get('summary') or '').lower()
    
    text = f"{headline} {summary} {profile.get('current_title', '').lower()}"
    
    for role in candidate.get('career_history', []):
        title = (role.get('title') or '').lower()
        desc = (role.get('description') or '').lower()
        text += f" {title} {desc}"
        
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


PENALTY_DOMAINS = [
    'computer vision', 'computervision', 'speech recognition', 'robotics', 
    'image classification', 'object detection', 'text-to-speech', 'text to speech', 
    'tts', 'lidar', 'autonomous vehicles', 'autonomous driving'
]

def get_domain_penalty_multiplier(candidate: dict) -> float:
    """Returns a multiplier (0.5 or 1.0) if candidate is from a disqualifying/irrelevant domain."""
    profile = candidate.get('profile', {})
    headline = (profile.get('headline') or '').lower()
    summary = (profile.get('summary') or '').lower()
    title = (profile.get('current_title') or '').lower()
    
    text = f"{headline} {summary} {title}"
    
    penalty_hits = sum(1 for d in PENALTY_DOMAINS if d in text)
    if penalty_hits >= 1:
        search_hits = sum(1 for kw in ['search', 'retrieval', 'recommend', 'ranking'] if kw in text)
        if search_hits < 2:
            return 0.50
    return 1.0


# ── REASONING GENERATION ─────────────────────────────────────────────────────

def generate_reasoning(candidate: dict, score: float, components: dict) -> str:
    """Per-candidate reasoning using only facts from the profile."""
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
        f'{title}, {yoe:.1f}y exp; skills: {skill_str}; '
        f'response_rate={rr:.2f}; {loc}{concern_str}.'
    )


# ── MAIN SCORER ───────────────────────────────────────────────────────────────

WEIGHTS = {
    'career_quality': 0.20,
    'skills_depth': 0.22,
    'jd_semantic_fit': 0.15,
    'title_alignment': 0.15,
    'experience_range': 0.10,
    'behavioral_availability': 0.10,
    'location_fit': 0.04,
    'github_signal': 0.04,
}

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
    semantic_score = score_jd_semantic_fit(candidate)
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
    parser = argparse.ArgumentParser(description='Rank candidates for Redrob AI Engineer JD')
    parser.add_argument('--candidates', default='candidates.jsonl',
                        help='Path to candidates.jsonl')
    parser.add_argument('--out', default='submission.csv',
                        help='Output CSV path (your_team_id.csv)')
    parser.add_argument('--top', type=int, default=100,
                        help='Number of candidates to output (default: 100)')
    args = parser.parse_args()

    candidates_path = Path(args.candidates)
    if not candidates_path.exists():
        print(f'ERROR: {args.candidates} not found.', file=sys.stderr)
        sys.exit(1)

    print(f'Loading candidates from {args.candidates}...', flush=True)
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

    # Sort by score desc, tie-break by candidate_id asc (per spec)
    scored.sort(key=lambda x: (-x[1], x[0]))

    top_n = scored[:args.top]

    print(f'Generating reasoning for top {args.top}...', flush=True)
    rows = []
    for rank_idx, (cid, score, components, candidate) in enumerate(top_n):
        rank = rank_idx + 1
        reasoning = generate_reasoning(candidate, score, components)
        rows.append({
            'candidate_id': cid,
            'rank': rank,
            'score': score,
            'reasoning': reasoning,
        })

    out_path = Path(args.out)
    print(f'Writing {out_path}...', flush=True)
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f, fieldnames=['candidate_id', 'rank', 'score', 'reasoning']
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f'\n✓ Done. {out_path} written.')
    print(f'\nTop 5 candidates:')
    for r in rows[:5]:
        print(f" #{r['rank']} {r['candidate_id']} score={r['score']} {r['reasoning'][:80]}...")
