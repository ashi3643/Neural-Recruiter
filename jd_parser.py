#!/usr/bin/env python3
"""
jd_parser.py - Dynamic Job Description Parser
Parses any job description and extracts structured requirements for candidate ranking.
Supports both rule-based parsing and optional LLM-based parsing.
"""

import re
import json
import os
from typing import Dict, List, Optional, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from dataclasses import dataclass


@dataclass
class ParsedJobDescription:
    """Structured representation of a job description."""
    title: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_range: tuple[int, int]  # (min_years, max_years)
    role_type: str  # e.g., "ML Engineer", "Data Scientist", "Search Engineer"
    domain_keywords: List[str]
    seniority_level: str  # "junior", "mid", "senior", "lead", "principal"
    raw_text: str


class JDParser:
    """
    Parse job descriptions into structured requirements.
    Supports LLM-based parsing via Google Gemini API and rule-based fallback.
    """
    
    # Common role type patterns
    ROLE_PATTERNS = {
        'machine learning engineer': ['ml engineer', 'machine learning engineer', 'ml engineer'],
        'ai engineer': ['ai engineer', 'artificial intelligence engineer', 'applied ai engineer'],
        'data scientist': ['data scientist', 'senior data scientist', 'principal data scientist'],
        'search engineer': ['search engineer', 'retrieval engineer', 'information retrieval engineer'],
        'nlp engineer': ['nlp engineer', 'natural language processing engineer'],
        'recommendation engineer': ['recommendation engineer', 'recommendation systems engineer', 'recommender systems engineer'],
        'applied scientist': ['applied scientist', 'research scientist', 'ai research engineer'],
        'backend engineer': ['backend engineer', 'software engineer', 'full stack engineer'],
    }
    
    # Seniority patterns
    SENIORITY_PATTERNS = {
        'principal': ['principal', 'staff', 'lead'],
        'senior': ['senior', 'sr.', 'sr'],
        'mid': ['mid-level', 'mid level', 'intermediate'],
        'junior': ['junior', 'jr.', 'jr', 'entry-level', 'entry level'],
    }
    
    # Experience extraction patterns
    EXPERIENCE_PATTERNS = [
        r'(\d+)\s*[-–to]+\s*(\d+)\s*years?\s*(?:of\s*)?(?:experience|exp)',
        r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
        r'minimum\s*(?:of\s*)?(\d+)\s*years?',
    ]
    
    def __init__(self, use_llm: bool = False, api_key: Optional[str] = None):
        """
        Initialize JD parser.
        
        Args:
            use_llm: Whether to use LLM-based parsing (requires API key)
            api_key: Google Gemini API key (set via GEMINI_API_KEY env var)
        """
        self.use_llm = use_llm
        self.api_key = api_key
        
    def parse(self, job_description: str) -> ParsedJobDescription:
        """
        Parse a job description into structured requirements.
        Uses LLM parsing by default for true semantic understanding,
        with rule-based fallback if LLM unavailable.
        
        Args:
            job_description: Raw job description text
            
        Returns:
            ParsedJobDescription with structured requirements
        """
        # Try LLM parsing first (AI-powered approach)
        # Get API key from argument or environment
        api_key = self.api_key or os.environ.get('GEMINI_API_KEY')
        
        if api_key:
            try:
                return self._parse_with_llm(job_description, api_key)
            except Exception as e:
                print(f"[JD PARSER] LLM parsing failed: {e}, falling back to rule-based parsing")
        
        # Fallback to rule-based parsing
        return self._parse_with_rules(job_description)
    
    def _parse_with_rules(self, jd_text: str) -> ParsedJobDescription:
        """Parse JD using rule-based extraction."""
        jd_lower = jd_text.lower()
        
        # Extract title
        title = self._extract_title(jd_text)
        
        # Extract role type
        role_type = self._extract_role_type(jd_lower)
        
        # Extract seniority
        seniority = self._extract_seniority(jd_lower)
        
        # Extract experience range
        exp_range = self._extract_experience_range(jd_lower)
        
        # Extract skills
        required_skills, preferred_skills = self._extract_skills(jd_lower)
        
        # Extract domain keywords
        domain_keywords = self._extract_domain_keywords(jd_lower)
        
        return ParsedJobDescription(
            title=title,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            experience_range=exp_range,
            role_type=role_type,
            domain_keywords=domain_keywords,
            seniority_level=seniority,
            raw_text=jd_text
        )
    
    def _parse_with_llm(self, jd_text: str, api_key: str) -> ParsedJobDescription:
        """Parse JD using Google Gemini API (requires GEMINI_API_KEY)."""
        try:
            import google.generativeai as genai
            
            # Configure Gemini API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Create prompt for job description parsing
            prompt = f"""You are a professional job description parser. Extract structured information from the following job description and return a JSON object with exactly these fields:
- title: job title (string)
- required_skills: list of required technical skills (array of strings)
- preferred_skills: list of preferred/nice-to-have skills (array of strings)
- experience_min: minimum years of experience (integer)
- experience_max: maximum years of experience (integer or null)
- role_type: primary role category like "ML Engineer", "Data Scientist", "Search Engineer" (string)
- domain_keywords: list of domain-specific keywords (array of strings)
- seniority_level: one of "junior", "mid", "senior", "lead", "principal" (string)

Job Description:
{jd_text}

Respond with ONLY valid JSON, no additional text or markdown."""
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=1024,
                    response_mime_type="application/json",
                )
            )
            
            # Extract and parse JSON from response
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            parsed = json.loads(response_text)
            
            return ParsedJobDescription(
                title=parsed.get('title', ''),
                required_skills=parsed.get('required_skills', []),
                preferred_skills=parsed.get('preferred_skills', []),
                experience_range=(
                    parsed.get('experience_min', 0),
                    parsed.get('experience_max', 20)
                ),
                role_type=parsed.get('role_type', ''),
                domain_keywords=parsed.get('domain_keywords', []),
                seniority_level=parsed.get('seniority_level', 'mid'),
                raw_text=jd_text
            )
            
        except Exception as e:
            print(f"[JD PARSER] Gemini LLM parsing failed: {e}, falling back to rule-based")
            return self._parse_with_rules(jd_text)
    
    def _extract_title(self, jd_text: str) -> str:
        """Extract job title from JD."""
        lines = jd_text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line) < 100 and not line.startswith('#'):
                return line
        return "Unknown Position"
    
    def _extract_role_type(self, jd_lower: str) -> str:
        """Extract primary role type."""
        for role, patterns in self.ROLE_PATTERNS.items():
            for pattern in patterns:
                if pattern in jd_lower:
                    return role
        return "General Engineer"
    
    def _extract_seniority(self, jd_lower: str) -> str:
        """Extract seniority level."""
        for level, patterns in self.SENIORITY_PATTERNS.items():
            for pattern in patterns:
                if pattern in jd_lower:
                    return level
        return "mid"
    
    def _extract_experience_range(self, jd_lower: str) -> tuple[int, int]:
        """Extract experience range from JD."""
        for pattern in self.EXPERIENCE_PATTERNS:
            match = re.search(pattern, jd_lower)
            if match:
                if len(match.groups()) == 2:
                    return (int(match.group(1)), int(match.group(2)))
                else:
                    years = int(match.group(1))
                    return (years, years + 5)
        
        # Default range if not found
        return (0, 20)
    
    def _extract_skills(self, jd_lower: str) -> tuple[List[str], List[str]]:
        """Extract required and preferred skills."""
        # Common tech skills to look for
        tech_skills = [
            'python', 'java', 'javascript', 'typescript', 'go', 'rust', 'c++',
            'pytorch', 'tensorflow', 'keras', 'scikit-learn', 'pandas', 'numpy',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'fastapi',
            'sql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'docker', 'kubernetes', 'aws', 'gcp', 'azure',
            'machine learning', 'deep learning', 'nlp', 'computer vision',
            'embeddings', 'vector search', 'semantic search', 'rag',
            'sentence-transformers', 'hugging face', 'transformers',
            'faiss', 'pinecone', 'weaviate', 'qdrant', 'milvus', 'chroma',
            'bm25', 'information retrieval', 'learning to rank', 'ltr',
            'recommendation systems', 'collaborative filtering',
            'git', 'ci/cd', 'agile', 'scrum'
        ]
        
        found_skills = []
        for skill in tech_skills:
            # Use word boundary matching to avoid false matches (e.g., "go" in "algorithms")
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, jd_lower):
                found_skills.append(skill)
        
        # Simple heuristic: skills in "requirements" section are required
        # skills in "preferred" or "nice to have" are preferred
        required_section = jd_lower.split('preferred')[0].split('nice to have')[0]
        required = [s for s in found_skills if s in required_section]
        preferred = [s for s in found_skills if s not in required]
        
        return required, preferred
    
    def _extract_domain_keywords(self, jd_lower: str) -> List[str]:
        """Extract domain-specific keywords."""
        domain_keywords = [
            'search', 'retrieval', 'ranking', 'recommendation',
            'nlp', 'natural language', 'computer vision', 'speech',
            'robotics', 'autonomous', 'fintech', 'healthcare',
            'e-commerce', 'adtech', 'gaming', 'social media'
        ]
        
        return [kw for kw in domain_keywords if kw in jd_lower]


def parse_jd_from_file(file_path: str, use_llm: bool = False, api_key: Optional[str] = None) -> ParsedJobDescription:
    """
    Parse job description from a file.
    
    Args:
        file_path: Path to text file containing job description
        use_llm: Whether to use LLM-based parsing
        api_key: API key for LLM parsing
        
    Returns:
        ParsedJobDescription
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        jd_text = f.read()
    
    parser = JDParser(use_llm=use_llm, api_key=api_key)
    return parser.parse(jd_text)


def parse_jd_from_text(jd_text: str, use_llm: bool = False, api_key: Optional[str] = None) -> ParsedJobDescription:
    """
    Parse job description from text string.
    
    Args:
        jd_text: Job description text
        use_llm: Whether to use LLM-based parsing
        api_key: API key for LLM parsing
        
    Returns:
        ParsedJobDescription
    """
    parser = JDParser(use_llm=use_llm, api_key=api_key)
    return parser.parse(jd_text)


if __name__ == '__main__':
    # Test with sample JD
    sample_jd = """
    Senior Machine Learning Engineer - Search & Recommendation Systems
    
    We are looking for a Senior Machine Learning Engineer to join our team building 
    state-of-the-art search and recommendation systems. You will work on dense retrieval,
    semantic search, and learning-to-rank algorithms.
    
    Requirements:
    - 5-8 years of experience in machine learning
    - Strong Python skills
    - Experience with PyTorch or TensorFlow
    - Knowledge of vector databases (Pinecone, Weaviate, Qdrant)
    - Familiarity with sentence-transformers and embeddings
    - Understanding of BM25 and information retrieval metrics (NDCG, MRR)
    
    Preferred:
    - PhD in Computer Science or related field
    - Experience with large-scale recommendation systems
    - Knowledge of hybrid search architectures
    """
    
    parser = JDParser()
    parsed = parser.parse(sample_jd)
    
    print("Parsed Job Description:")
    print(f"Title: {parsed.title}")
    print(f"Role Type: {parsed.role_type}")
    print(f"Seniority: {parsed.seniority_level}")
    print(f"Experience Range: {parsed.experience_range[0]}-{parsed.experience_range[1]} years")
    print(f"Required Skills: {parsed.required_skills}")
    print(f"Preferred Skills: {parsed.preferred_skills}")
    print(f"Domain Keywords: {parsed.domain_keywords}")
