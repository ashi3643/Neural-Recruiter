#!/usr/bin/env python3
"""
csv_utils.py - CSV Import/Export Utilities for Candidate Ranking
Handles CSV import for candidate data and export for ranked results.
"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


def import_candidates_from_csv(csv_path: str) -> List[Dict[str, Any]]:
    """
    Import candidate data from CSV file.
    
    Expected CSV format:
    - candidate_id, name, current_title, current_company, headline, summary,
      years_of_experience, location, country, skills_json, career_json, signals_json
    
    Args:
        csv_path: Path to CSV file with candidate data
        
    Returns:
        List of candidate dictionaries in the same format as JSONL
    """
    candidates = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            candidate = {
                'candidate_id': row.get('candidate_id', ''),
                'profile': {
                    'name': row.get('name', ''),
                    'current_title': row.get('current_title', ''),
                    'current_company': row.get('current_company', ''),
                    'headline': row.get('headline', ''),
                    'summary': row.get('summary', ''),
                    'years_of_experience': float(row.get('years_of_experience', 0)),
                    'location': row.get('location', ''),
                    'country': row.get('country', ''),
                },
                'skills': json.loads(row.get('skills_json', '[]')),
                'career_history': json.loads(row.get('career_json', '[]')),
                'education': json.loads(row.get('education_json', '[]')),
                'certifications': json.loads(row.get('certifications_json', '[]')),
                'redrob_signals': json.loads(row.get('signals_json', '{}')),
            }
            candidates.append(candidate)
    
    return candidates


def export_candidates_to_csv(candidates: List[Dict[str, Any]], csv_path: str) -> None:
    """
    Export candidate data to CSV file.
    
    Args:
        candidates: List of candidate dictionaries
        csv_path: Output CSV file path
    """
    fieldnames = [
        'candidate_id', 'name', 'current_title', 'current_company', 
        'headline', 'summary', 'years_of_experience', 'location', 'country',
        'skills_json', 'career_json', 'education_json', 'certifications_json', 'signals_json'
    ]
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for candidate in candidates:
            profile = candidate.get('profile', {})
            row = {
                'candidate_id': candidate.get('candidate_id', ''),
                'name': profile.get('name', ''),
                'current_title': profile.get('current_title', ''),
                'current_company': profile.get('current_company', ''),
                'headline': profile.get('headline', ''),
                'summary': profile.get('summary', ''),
                'years_of_experience': profile.get('years_of_experience', 0),
                'location': profile.get('location', ''),
                'country': profile.get('country', ''),
                'skills_json': json.dumps(candidate.get('skills', [])),
                'career_json': json.dumps(candidate.get('career_history', [])),
                'education_json': json.dumps(candidate.get('education', [])),
                'certifications_json': json.dumps(candidate.get('certifications', [])),
                'signals_json': json.dumps(candidate.get('redrob_signals', {})),
            }
            writer.writerow(row)


def export_ranked_results(
    ranked_candidates: List[Dict[str, Any]], 
    output_path: str,
    include_components: bool = False
) -> None:
    """
    Export ranked results to CSV file.
    
    Args:
        ranked_candidates: List of tuples (candidate_id, rank, score, reasoning, components)
        output_path: Output CSV file path
        include_components: Whether to include scoring component breakdown
    """
    if include_components:
        fieldnames = ['candidate_id', 'rank', 'score', 'reasoning', 
                     'career_quality', 'skills_depth', 'jd_semantic_fit',
                     'title_alignment', 'experience_range', 'behavioral_availability',
                     'location_fit', 'github_signal']
    else:
        fieldnames = ['candidate_id', 'rank', 'score', 'reasoning']
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in ranked_candidates:
            # Handle both dictionary (from cache) and tuple (from new ranking) inputs
            if isinstance(item, dict):
                # Item is already a dictionary (from cache)
                row = item
            else:
                # Item is a tuple (from new ranking)
                if len(item) == 4:
                    cid, rank, score, reasoning = item
                    components = {}
                else:
                    cid, rank, score, reasoning, components = item
                
                row = {
                    'candidate_id': cid,
                    'rank': rank,
                    'score': score,
                    'reasoning': reasoning,
                }
                
                if include_components and components:
                    row.update(components)
            
            writer.writerow(row)


def load_cached_ranking(cache_path: str) -> Optional[List[Dict[str, Any]]]:
    """
    Load previously cached ranking results.
    
    Args:
        cache_path: Path to cached CSV file
        
    Returns:
        List of ranked candidates or None if cache doesn't exist
    """
    if not Path(cache_path).exists():
        return None
    
    ranked = []
    with open(cache_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ranked.append(row)
    
    return ranked


def save_ranking_cache(
    ranked_candidates: List[Dict[str, Any]], 
    cache_path: str,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Save ranking results to cache with metadata.
    
    Args:
        ranked_candidates: List of ranked candidates
        cache_path: Output cache file path
        metadata: Optional metadata (JD hash, timestamp, etc.)
    """
    export_ranked_results(ranked_candidates, cache_path)
    
    # Save metadata separately
    if metadata:
        metadata_path = cache_path.replace('.csv', '_metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)


def convert_jsonl_to_csv(jsonl_path: str, csv_path: str) -> None:
    """
    Convert JSONL candidate file to CSV format.
    
    Args:
        jsonl_path: Input JSONL file path
        csv_path: Output CSV file path
    """
    candidates = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                candidates.append(json.loads(line))
    
    export_candidates_to_csv(candidates, csv_path)
    print(f"Converted {len(candidates)} candidates from {jsonl_path} to {csv_path}")


def convert_csv_to_jsonl(csv_path: str, jsonl_path: str) -> None:
    """
    Convert CSV candidate file to JSONL format.
    
    Args:
        csv_path: Input CSV file path
        jsonl_path: Output JSONL file path
    """
    candidates = import_candidates_from_csv(csv_path)
    
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for candidate in candidates:
            f.write(json.dumps(candidate) + '\n')
    
    print(f"Converted {len(candidates)} candidates from {csv_path} to {jsonl_path}")


def create_ranking_summary(ranked_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create summary statistics for ranked results.
    
    Args:
        ranked_candidates: List of ranked candidates
        
    Returns:
        Dictionary with summary statistics
    """
    if not ranked_candidates:
        return {}
    
    scores = [float(c.get('score', 0)) for c in ranked_candidates]
    
    summary = {
        'total_candidates': len(ranked_candidates),
        'timestamp': datetime.now().isoformat(),
        'score_statistics': {
            'min': min(scores),
            'max': max(scores),
            'mean': sum(scores) / len(scores),
            'median': sorted(scores)[len(scores) // 2],
        },
        'top_10_avg': sum(scores[:10]) / min(10, len(scores)),
    }
    
    return summary


if __name__ == '__main__':
    # Test conversion between JSONL and CSV
    import sys
    
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        
        if input_file.endswith('.jsonl'):
            convert_jsonl_to_csv(input_file, output_file)
        elif input_file.endswith('.csv'):
            convert_csv_to_jsonl(input_file, output_file)
        else:
            print("Unknown input format. Use .jsonl or .csv")
    else:
        print("Usage: python csv_utils.py <input_file> <output_file>")
