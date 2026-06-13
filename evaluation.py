#!/usr/bin/env python3
"""
evaluation.py - Evaluation Metrics for Neural Recruiter
Implements precision@k, NDCG@k, and other ranking evaluation metrics.
"""

import math
from typing import List, Dict, Any, Set


def precision_at_k(relevant_items: Set[str], ranked_items: List[str], k: int) -> float:
    """
    Calculate Precision@K metric.
    
    Args:
        relevant_items: Set of relevant item IDs (ground truth)
        ranked_items: List of ranked item IDs (predicted ranking)
        k: Number of top items to consider
        
    Returns:
        Precision@K score (0.0 to 1.0)
    """
    if k == 0:
        return 0.0
    
    top_k = ranked_items[:k]
    relevant_in_top_k = sum(1 for item in top_k if item in relevant_items)
    
    return relevant_in_top_k / k


def recall_at_k(relevant_items: Set[str], ranked_items: List[str], k: int) -> float:
    """
    Calculate Recall@K metric.
    
    Args:
        relevant_items: Set of relevant item IDs (ground truth)
        ranked_items: List of ranked item IDs (predicted ranking)
        k: Number of top items to consider
        
    Returns:
        Recall@K score (0.0 to 1.0)
    """
    if not relevant_items:
        return 0.0
    
    top_k = ranked_items[:k]
    relevant_in_top_k = sum(1 for item in top_k if item in relevant_items)
    
    return relevant_in_top_k / len(relevant_items)


def dcg_at_k(relevance_scores: List[float], k: int) -> float:
    """
    Calculate Discounted Cumulative Gain at K.
    
    Args:
        relevance_scores: List of relevance scores (higher = more relevant)
        k: Number of top items to consider
        
    Returns:
        DCG@K score
    """
    if k == 0:
        return 0.0
    
    relevance_scores = relevance_scores[:k]
    dcg = 0.0
    
    for i, rel in enumerate(relevance_scores):
        if rel > 0:
            dcg += rel / math.log2(i + 2)  # log2(i+2) because i is 0-indexed
    
    return dcg


def ndcg_at_k(relevance_scores: List[float], k: int) -> float:
    """
    Calculate Normalized Discounted Cumulative Gain at K.
    
    Args:
        relevance_scores: List of relevance scores (higher = more relevant)
        k: Number of top items to consider
        
    Returns:
        NDCG@K score (0.0 to 1.0)
    """
    if k == 0:
        return 0.0
    
    dcg = dcg_at_k(relevance_scores, k)
    
    # Ideal DCG: sort relevance scores in descending order
    ideal_scores = sorted(relevance_scores, reverse=True)
    idcg = dcg_at_k(ideal_scores, k)
    
    if idcg == 0:
        return 0.0
    
    return dcg / idcg


def mean_reciprocal_rank(relevant_items: Set[str], ranked_items: List[str]) -> float:
    """
    Calculate Mean Reciprocal Rank (MRR).
    
    Args:
        relevant_items: Set of relevant item IDs (ground truth)
        ranked_items: List of ranked item IDs (predicted ranking)
        
    Returns:
        MRR score (0.0 to 1.0)
    """
    if not relevant_items:
        return 0.0
    
    for i, item in enumerate(ranked_items):
        if item in relevant_items:
            return 1.0 / (i + 1)
    
    return 0.0


def average_precision(relevant_items: Set[str], ranked_items: List[str]) -> float:
    """
    Calculate Average Precision (AP).
    
    Args:
        relevant_items: Set of relevant item IDs (ground truth)
        ranked_items: List of ranked item IDs (predicted ranking)
        
    Returns:
        Average Precision score (0.0 to 1.0)
    """
    if not relevant_items:
        return 0.0
    
    precisions = []
    num_relevant = 0
    
    for i, item in enumerate(ranked_items):
        if item in relevant_items:
            num_relevant += 1
            precision = num_relevant / (i + 1)
            precisions.append(precision)
    
    if not precisions:
        return 0.0
    
    return sum(precisions) / len(relevant_items)


def evaluate_ranking(
    ranked_candidates: List[Dict[str, Any]],
    ground_truth_relevant: Set[str],
    k_values: List[int] = [5, 10, 20, 50, 100]
) -> Dict[str, Any]:
    """
    Evaluate ranking performance using multiple metrics.
    
    Args:
        ranked_candidates: List of ranked candidates with candidate_id and score
        ground_truth_relevant: Set of candidate IDs that are actually relevant
        k_values: List of k values for precision@k and recall@k
        
    Returns:
        Dictionary with all evaluation metrics
    """
    ranked_ids = [c['candidate_id'] for c in ranked_candidates]
    relevance_scores = [c.get('score', 0.0) for c in ranked_candidates]
    
    results = {
        'total_ranked': len(ranked_candidates),
        'total_relevant': len(ground_truth_relevant),
        'relevant_in_ranked': sum(1 for cid in ranked_ids if cid in ground_truth_relevant),
    }
    
    # Precision@K and Recall@K for each k
    for k in k_values:
        results[f'precision@{k}'] = precision_at_k(ground_truth_relevant, ranked_ids, k)
        results[f'recall@{k}'] = recall_at_k(ground_truth_relevant, ranked_ids, k)
    
    # NDCG@K for each k
    for k in k_values:
        results[f'ndcg@{k}'] = ndcg_at_k(relevance_scores, k)
    
    # MRR and MAP
    results['mrr'] = mean_reciprocal_rank(ground_truth_relevant, ranked_ids)
    results['map'] = average_precision(ground_truth_relevant, ranked_ids)
    
    return results


def print_evaluation_report(results: Dict[str, Any]) -> None:
    """Print a formatted evaluation report."""
    print("=" * 60)
    print("RANKING EVALUATION REPORT")
    print("=" * 60)
    print(f"Total candidates ranked: {results['total_ranked']}")
    print(f"Total relevant candidates: {results['total_relevant']}")
    print(f"Relevant candidates in ranking: {results['relevant_in_ranked']}")
    print()
    
    print("Precision@K:")
    for k in [5, 10, 20, 50, 100]:
        if f'precision@{k}' in results:
            print(f"  Precision@{k:3d}: {results[f'precision@{k}']:.4f}")
    
    print()
    print("Recall@K:")
    for k in [5, 10, 20, 50, 100]:
        if f'recall@{k}' in results:
            print(f"  Recall@{k:3d}:    {results[f'recall@{k}']:.4f}")
    
    print()
    print("NDCG@K:")
    for k in [5, 10, 20, 50, 100]:
        if f'ndcg@{k}' in results:
            print(f"  NDCG@{k:3d}:     {results[f'ndcg@{k}']:.4f}")
    
    print()
    print(f"Mean Reciprocal Rank (MRR): {results['mrr']:.4f}")
    print(f"Mean Average Precision (MAP): {results['map']:.4f}")
    print("=" * 60)


def create_synthetic_ground_truth(
    ranked_candidates: List[Dict[str, Any]],
    top_n_percent: float = 0.2
) -> Set[str]:
    """
    Create synthetic ground truth by treating top N% of ranked candidates as relevant.
    Useful for self-evaluation when no ground truth is available.
    
    Args:
        ranked_candidates: List of ranked candidates
        top_n_percent: Percentage of top candidates to consider as relevant (0.0 to 1.0)
        
    Returns:
        Set of candidate IDs considered relevant
    """
    n_relevant = max(1, int(len(ranked_candidates) * top_n_percent))
    return {c['candidate_id'] for c in ranked_candidates[:n_relevant]}


if __name__ == '__main__':
    # Example usage with synthetic data
    ranked_candidates = [
        {'candidate_id': f'CAND_{i}', 'score': 1.0 - (i * 0.01)}
        for i in range(100)
    ]
    
    # Create synthetic ground truth (top 20% are relevant)
    ground_truth = create_synthetic_ground_truth(ranked_candidates, top_n_percent=0.2)
    
    # Evaluate
    results = evaluate_ranking(ranked_candidates, ground_truth)
    print_evaluation_report(results)
