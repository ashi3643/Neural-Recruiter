#!/usr/bin/env python3
"""
ab_test_comparison.py - A/B Test Comparison: Keyword vs Semantic Scoring
Compares ranking quality between keyword-based and semantic embedding-based scoring.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Set
from datetime import date

# Import ranking components
from rank import (
    compute_score, score_jd_semantic_fit, PARSED_JD, 
    CORE_JD_SEMANTIC_KEYWORDS, config, TODAY
)
from jd_parser import parse_jd_from_file, ParsedJobDescription
from evaluation import evaluate_ranking, create_synthetic_ground_truth, print_evaluation_report


def score_candidates_keyword(candidates: List[Dict[str, Any]]) -> List[tuple]:
    """Score candidates using keyword-based semantic fit (old approach)."""
    scored = []
    for candidate in candidates:
        # Temporarily disable embeddings for keyword scoring
        score, components = compute_score(candidate)
        scored.append((candidate['candidate_id'], score, components, candidate))
    return scored


def score_candidates_semantic(candidates: List[Dict[str, Any]], jd: ParsedJobDescription) -> List[tuple]:
    """Score candidates using semantic embeddings (new approach)."""
    # Update global JD for semantic scoring
    from rank import update_jd_keywords
    update_jd_keywords(jd)
    
    scored = []
    for candidate in candidates:
        # Use embeddings-enabled scoring
        score, components = compute_score(candidate)
        scored.append((candidate['candidate_id'], score, components, candidate))
    return scored


def compare_rankings(
    keyword_ranked: List[tuple],
    semantic_ranked: List[tuple],
    top_k: int = 100
) -> Dict[str, Any]:
    """Compare keyword vs semantic rankings."""
    keyword_ids = [c[0] for c in keyword_ranked[:top_k]]
    semantic_ids = [c[0] for c in semantic_ranked[:top_k]]
    
    # Calculate overlap
    keyword_set = set(keyword_ids)
    semantic_set = set(semantic_ids)
    overlap = keyword_set.intersection(semantic_set)
    
    # Rank correlation (Spearman-like)
    keyword_rank_map = {cid: i for i, cid in enumerate(keyword_ids)}
    semantic_rank_map = {cid: i for i, cid in enumerate(semantic_ids)}
    
    # Calculate average rank change for overlapping candidates
    rank_changes = []
    for cid in overlap:
        keyword_rank = keyword_rank_map[cid]
        semantic_rank = semantic_rank_map[cid]
        rank_changes.append(semantic_rank - keyword_rank)
    
    avg_rank_change = sum(rank_changes) / len(rank_changes) if rank_changes else 0
    
    return {
        'top_k': top_k,
        'keyword_top_ids': keyword_ids,
        'semantic_top_ids': semantic_ids,
        'overlap_count': len(overlap),
        'overlap_percentage': len(overlap) / top_k * 100,
        'avg_rank_change': avg_rank_change,
        'rank_changes': rank_changes
    }


def run_ab_test(
    candidates_path: str,
    jd_path: str,
    top_k: int = 100
) -> Dict[str, Any]:
    """Run A/B test comparing keyword vs semantic scoring."""
    
    print("=" * 70)
    print("A/B TEST: Keyword vs Semantic Scoring")
    print("=" * 70)
    
    # Load candidates
    print(f"\n[1/4] Loading candidates from {candidates_path}...")
    candidates = []
    candidates_file = Path(candidates_path)
    
    if candidates_file.suffix == '.csv':
        from csv_utils import import_candidates_from_csv
        candidates = import_candidates_from_csv(candidates_path)
    else:
        with open(candidates_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    candidates.append(json.loads(line))
    
    print(f"Loaded {len(candidates):,} candidates")
    
    # Parse JD
    print(f"\n[2/4] Parsing job description from {jd_path}...")
    jd = parse_jd_from_file(jd_path, use_llm=False)  # Use rule-based for consistency
    print(f"JD Title: {jd.title}")
    print(f"Role Type: {jd.role_type}")
    print(f"Required Skills: {len(jd.required_skills)}")
    
    # Score with keyword approach (disable embeddings)
    print(f"\n[3/4] Scoring with keyword-based semantic fit...")
    # Temporarily modify to force keyword scoring
    original_semantic_func = score_jd_semantic_fit
    
    def keyword_only_semantic(candidate: dict, use_embeddings: bool = False) -> float:
        """Force keyword-only scoring."""
        return original_semantic_func(candidate, use_embeddings=False)
    
    # Monkey-patch for keyword scoring
    import rank
    rank.score_jd_semantic_fit = keyword_only_semantic
    
    keyword_ranked = score_candidates_keyword(candidates)
    keyword_ranked.sort(key=lambda x: (-x[1], x[0]))
    
    # Restore original function
    rank.score_jd_semantic_fit = original_semantic_func
    
    print(f"Keyword scoring complete. Top score: {keyword_ranked[0][1]:.4f}")
    
    # Score with semantic approach (enable embeddings)
    print(f"\n[4/4] Scoring with semantic embeddings...")
    semantic_ranked = score_candidates_semantic(candidates, jd)
    semantic_ranked.sort(key=lambda x: (-x[1], x[0]))
    
    print(f"Semantic scoring complete. Top score: {semantic_ranked[0][1]:.4f}")
    
    # Compare rankings
    print(f"\n" + "=" * 70)
    print("COMPARISON RESULTS")
    print("=" * 70)
    
    comparison = compare_rankings(keyword_ranked, semantic_ranked, top_k)
    
    print(f"\nTop {top_k} Candidates:")
    print(f"  Overlap: {comparison['overlap_count']}/{top_k} ({comparison['overlap_percentage']:.1f}%)")
    print(f"  Average Rank Change: {comparison['avg_rank_change']:+.2f}")
    
    # Show top 10 from each approach
    print(f"\nTop 10 Keyword-Based:")
    for i, (cid, score, _, _) in enumerate(keyword_ranked[:10]):
        print(f"  {i+1:2d}. {cid} (score: {score:.4f})")
    
    print(f"\nTop 10 Semantic-Based:")
    for i, (cid, score, _, _) in enumerate(semantic_ranked[:10]):
        print(f"  {i+1:2d}. {cid} (score: {score:.4f})")
    
    # Show candidates that moved significantly
    print(f"\nSignificant Rank Changes (|change| >= 5):")
    significant_changes = [
        (cid, comparison['rank_changes'][i]) 
        for i, cid in enumerate(comparison['overlap']) 
        if abs(comparison['rank_changes'][i]) >= 5
    ]
    significant_changes.sort(key=lambda x: abs(x[1]), reverse=True)
    
    for cid, change in significant_changes[:10]:
        print(f"  {cid}: {change:+d} positions")
    
    # Evaluation metrics (using synthetic ground truth)
    print(f"\n" + "=" * 70)
    print("EVALUATION METRICS (Synthetic Ground Truth)")
    print("=" * 70)
    
    # Create synthetic ground truth from semantic ranking (top 20%)
    ground_truth = create_synthetic_ground_truth(
        [{'candidate_id': c[0], 'score': c[1]} for c in semantic_ranked],
        top_n_percent=0.2
    )
    
    print(f"\nKeyword-Based Ranking Evaluation:")
    keyword_eval = evaluate_ranking(
        [{'candidate_id': c[0], 'score': c[1]} for c in keyword_ranked],
        ground_truth,
        k_values=[10, 20, 50, 100]
    )
    print_evaluation_report(keyword_eval)
    
    print(f"\nSemantic-Based Ranking Evaluation:")
    semantic_eval = evaluate_ranking(
        [{'candidate_id': c[0], 'score': c[1]} for c in semantic_ranked],
        ground_truth,
        k_values=[10, 20, 50, 100]
    )
    print_evaluation_report(semantic_eval)
    
    return {
        'comparison': comparison,
        'keyword_evaluation': keyword_eval,
        'semantic_evaluation': semantic_eval,
        'keyword_ranked': keyword_ranked,
        'semantic_ranked': semantic_ranked
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A/B test comparison: Keyword vs Semantic scoring'
    )
    parser.add_argument('--candidates', default='candidates.jsonl',
                        help='Path to candidates file')
    parser.add_argument('--jd', default='sample_job_description.txt',
                        help='Path to job description file')
    parser.add_argument('--top-k', type=int, default=100,
                        help='Number of top candidates to compare')
    parser.add_argument('--output', default='ab_test_results.json',
                        help='Output file for results')
    
    args = parser.parse_args()
    
    results = run_ab_test(args.candidates, args.jd, args.top_k)
    
    # Save results
    with open(args.output, 'w') as f:
        # Convert to serializable format
        serializable_results = {
            'comparison': results['comparison'],
            'keyword_evaluation': results['keyword_evaluation'],
            'semantic_evaluation': results['semantic_evaluation'],
            'top_10_keyword': [(c[0], float(c[1])) for c in results['keyword_ranked'][:10]],
            'top_10_semantic': [(c[0], float(c[1])) for c in results['semantic_ranked'][:10]]
        }
        json.dump(serializable_results, f, indent=2)
    
    print(f"\nResults saved to {args.output}")
