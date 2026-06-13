#!/usr/bin/env python3
"""
semantic_reranker.py - Semantic Embeddings Layer for Neural Recruiter
Implements semantic similarity-based reranking using sentence-transformers.
This adds the "AI layer" on top of the heuristic core for top-K candidates.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class SemanticRerankResult:
    """Result of semantic reranking."""
    candidate_id: str
    original_score: float
    semantic_score: float
    combined_score: float
    original_rank: int
    new_rank: int


class SemanticReranker:
    """
    Semantic reranker using sentence-transformers for top-K candidates.
    
    This implements the "AI layer" that reranks the top-K candidates from
    the heuristic scorer using semantic similarity between job description
    and candidate profiles.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', enable_embeddings: bool = False):
        """
        Initialize semantic reranker.
        
        Args:
            model_name: Name of sentence-transformers model
            enable_embeddings: Whether to enable actual embeddings (requires sentence-transformers)
        """
        self.model_name = model_name
        self.enable_embeddings = enable_embeddings
        self.model = None
        
        if enable_embeddings:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(model_name)
                print(f"[SEMANTIC] Loaded model: {model_name}")
            except ImportError:
                print("[SEMANTIC] sentence-transformers not installed. Using fallback keyword-based similarity.")
                self.enable_embeddings = False
    
    def embed_text(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector or None if embeddings disabled
        """
        if not self.enable_embeddings or not self.model:
            return None
        
        return self.model.encode(text).tolist()
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        if self.enable_embeddings and self.model:
            # Use actual embeddings
            emb1 = self.model.encode(text1)
            emb2 = self.model.encode(text2)
            
            # Cosine similarity
            import numpy as np
            dot_product = np.dot(emb1, emb2)
            norm1 = np.linalg.norm(emb1)
            norm2 = np.linalg.norm(emb2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        else:
            # Fallback: keyword-based similarity
            return self._keyword_similarity(text1.lower(), text2.lower())
    
    def _keyword_similarity(self, text1: str, text2: str) -> float:
        """
        Compute keyword-based similarity as fallback.
        
        Args:
            text1: First text (lowercase)
            text2: Second text (lowercase)
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def build_candidate_text(self, candidate: Dict[str, Any]) -> str:
        """
        Build text representation of candidate for embedding.
        
        Args:
            candidate: Candidate dictionary
            
        Returns:
            Combined text string
        """
        profile = candidate.get('profile', {})
        headline = profile.get('headline', '')
        summary = profile.get('summary', '')
        title = profile.get('current_title', '')
        
        # Add skills
        skills = candidate.get('skills', [])
        skill_text = ' '.join([s.get('name', '') for s in skills])
        
        # Add career descriptions
        career = candidate.get('career_history', [])
        career_text = ' '.join([c.get('description', '') for c in career])
        
        return f"{headline} {summary} {title} {skill_text} {career_text}"
    
    def rerank_top_k(
        self,
        ranked_candidates: List[tuple[str, float, Dict[str, Any]]],
        job_description: str,
        k: int = 50,
        semantic_weight: float = 0.3
    ) -> List[SemanticRerankResult]:
        """
        Rerank top-K candidates using semantic similarity.
        
        Args:
            ranked_candidates: List of (candidate_id, original_score, components, candidate)
            job_description: Job description text
            k: Number of top candidates to rerank
            semantic_weight: Weight for semantic score in combined score (0.0 to 1.0)
            
        Returns:
            List of SemanticRerankResult with reranked results
        """
        if k > len(ranked_candidates):
            k = len(ranked_candidates)
        
        # Extract top-K candidates
        top_k = ranked_candidates[:k]
        
        # Compute semantic similarity for each candidate
        results = []
        for rank_idx, (cid, orig_score, components, candidate) in enumerate(top_k):
            candidate_text = self.build_candidate_text(candidate)
            semantic_score = self.compute_similarity(job_description, candidate_text)
            
            # Combined score: weighted average of original and semantic
            combined_score = (1 - semantic_weight) * orig_score + semantic_weight * semantic_score
            
            results.append(SemanticRerankResult(
                candidate_id=cid,
                original_score=orig_score,
                semantic_score=semantic_score,
                combined_score=combined_score,
                original_rank=rank_idx + 1,
                new_rank=0  # Will be set after sorting
            ))
        
        # Sort by combined score
        results.sort(key=lambda x: x.combined_score, reverse=True)
        
        # Update new ranks
        for i, result in enumerate(results):
            result.new_rank = i + 1
        
        return results
    
    def rerank_all(
        self,
        ranked_candidates: List[tuple[str, float, Dict[str, Any]]],
        job_description: str,
        semantic_weight: float = 0.3
    ) -> List[SemanticRerankResult]:
        """
        Rerank all candidates using semantic similarity.
        
        Args:
            ranked_candidates: List of (candidate_id, original_score, components, candidate)
            job_description: Job description text
            semantic_weight: Weight for semantic score in combined score (0.0 to 1.0)
            
        Returns:
            List of SemanticRerankResult with reranked results
        """
        return self.rerank_top_k(ranked_candidates, job_description, k=len(ranked_candidates), semantic_weight=semantic_weight)


def integrate_semantic_reranking(
    ranked_candidates: List[tuple[str, float, Dict[str, Any]]],
    job_description: str,
    enable_semantic: bool = True,
    top_k: int = 50,
    semantic_weight: float = 0.3
) -> List[tuple[str, float, Dict[str, Any]]]:
    """
    Integrate semantic reranking into the ranking pipeline.
    
    Args:
        ranked_candidates: List of (candidate_id, original_score, components, candidate)
        job_description: Job description text
        enable_semantic: Whether to enable semantic reranking
        top_k: Number of top candidates to rerank
        semantic_weight: Weight for semantic score in combined score
        
    Returns:
        Updated list of (candidate_id, new_score, components, candidate)
    """
    if not enable_semantic:
        return ranked_candidates
    
    reranker = SemanticReranker(enable_embeddings=True)
    
    # Rerank top-K
    reranked_results = reranker.rerank_top_k(ranked_candidates, job_description, top_k, semantic_weight)
    
    # Create mapping of candidate_id -> new_score
    score_map = {r.candidate_id: r.combined_score for r in reranked_results}
    
    # Update scores for top-K candidates
    updated_ranked = []
    for cid, orig_score, components, candidate in ranked_candidates:
        if cid in score_map:
            updated_ranked.append((cid, score_map[cid], components, candidate))
        else:
            # Keep original score for candidates outside top-K
            updated_ranked.append((cid, orig_score, components, candidate))
    
    # Re-sort by new scores
    updated_ranked.sort(key=lambda x: x[1], reverse=True)
    
    return updated_ranked


if __name__ == '__main__':
    # Test semantic reranker
    test_candidates = [
        {
            'candidate_id': 'CAND_001',
            'profile': {
                'headline': 'Senior Machine Learning Engineer',
                'summary': 'Expert in search and recommendation systems',
                'current_title': 'ML Engineer'
            },
            'skills': [{'name': 'PyTorch'}, {'name': 'embeddings'}],
            'career_history': [{'description': 'Built vector search systems'}]
        },
        {
            'candidate_id': 'CAND_002',
            'profile': {
                'headline': 'Software Engineer',
                'summary': 'Backend developer with Python experience',
                'current_title': 'Backend Engineer'
            },
            'skills': [{'name': 'Python'}, {'name': 'Django'}],
            'career_history': [{'description': 'Built REST APIs'}]
        }
    ]
    
    test_jd = "Senior Machine Learning Engineer for search and recommendation systems"
    
    ranked = [('CAND_001', 0.9, {}, test_candidates[0]), ('CAND_002', 0.7, {}, test_candidates[1])]
    
    reranker = SemanticReranker(enable_embeddings=False)  # Use keyword similarity for testing
    results = reranker.rerank_top_k(ranked, test_jd, k=2)
    
    print("Semantic Reranking Test Results:")
    for r in results:
        print(f"  {r.candidate_id}: orig={r.original_score:.2f}, semantic={r.semantic_score:.2f}, combined={r.combined_score:.2f}, rank {r.original_rank}->{r.new_rank}")
