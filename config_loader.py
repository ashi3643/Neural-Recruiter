#!/usr/bin/env python3
"""
config_loader.py - Configuration Loader for Neural Recruiter
Loads configuration from config.yaml and provides access to all parameters.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import date


class Config:
    """Configuration container for Neural Recruiter."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to config.yaml file. If None, looks for config.yaml in current directory.
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        else:
            config_path = Path(config_path)
        
        self.config_path = config_path
        self._config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    # System Configuration
    @property
    def current_date(self) -> date:
        """Get current date from config."""
        date_str = self._config.get('system', {}).get('current_date', '2026-06-11')
        return date.fromisoformat(date_str)
    
    @property
    def mode(self) -> str:
        """Get system mode (demo or submission)."""
        return self._config.get('system', {}).get('mode', 'submission')
    
    @property
    def enable_honeypot_detection(self) -> bool:
        """Check if honeypot detection is enabled."""
        return self._config.get('system', {}).get('enable_honeypot_detection', True)
    
    @property
    def enable_domain_penalties(self) -> bool:
        """Check if domain penalties are enabled."""
        return self._config.get('system', {}).get('enable_domain_penalties', True)
    
    @property
    def enable_consulting_penalties(self) -> bool:
        """Check if consulting penalties are enabled."""
        return self._config.get('system', {}).get('enable_consulting_penalties', True)
    
    # Scoring Weights
    @property
    def weights(self) -> Dict[str, float]:
        """Get scoring weights."""
        return self._config.get('weights', {})
    
    # Title Tiers
    @property
    def tier_a_titles(self) -> set:
        """Get Tier A title set."""
        return set(self._config.get('title_tiers', {}).get('tier_a', []))
    
    @property
    def tier_c_titles(self) -> set:
        """Get Tier C title set."""
        return set(self._config.get('title_tiers', {}).get('tier_c', []))
    
    # Consulting Firms
    @property
    def consulting_firms(self) -> set:
        """Get consulting firms set."""
        return set(self._config.get('consulting_firms', []))
    
    # Core AI Skills
    @property
    def core_ai_skills(self) -> set:
        """Get core AI skills set."""
        return set(self._config.get('core_ai_skills', []))
    
    @property
    def default_jd_semantic_keywords(self) -> list:
        """Get default JD semantic keywords list."""
        return self._config.get('default_jd_semantic_keywords', [])
    
    # Domain Penalties
    @property
    def penalty_domains(self) -> List[str]:
        """Get penalty domains list."""
        return self._config.get('penalty_domains', [])
    
    # Preferred Locations
    @property
    def preferred_locations(self) -> set:
        """Get preferred locations set."""
        return set(self._config.get('preferred_locations', []))
    
    # Honeypot Thresholds
    @property
    def career_duration_tolerance(self) -> float:
        """Get career duration tolerance."""
        return self._config.get('honeypot', {}).get('career_duration_tolerance', 0.35)
    
    @property
    def minimum_career_months(self) -> int:
        """Get minimum career months for timeline check."""
        return self._config.get('honeypot', {}).get('minimum_career_months', 24)
    
    @property
    def expert_zero_threshold(self) -> int:
        """Get expert skills with 0 months threshold."""
        return self._config.get('honeypot', {}).get('expert_zero_threshold', 3)
    
    @property
    def expert_skills_threshold(self) -> int:
        """Get expert skills threshold."""
        return self._config.get('honeypot', {}).get('expert_skills_threshold', 8)
    
    @property
    def expert_endorsements_threshold(self) -> int:
        """Get expert endorsements threshold."""
        return self._config.get('honeypot', {}).get('expert_endorsements_threshold', 5)
    
    # Experience Scoring
    @property
    def default_experience_range(self) -> tuple[int, int]:
        """Get default experience range."""
        exp_config = self._config.get('experience', {})
        return (
            exp_config.get('default_min_years', 6),
            exp_config.get('default_max_years', 8)
        )
    
    # Behavioral Scoring
    @property
    def inactive_severe_threshold(self) -> int:
        """Get severe inactivity threshold."""
        return self._config.get('behavioral', {}).get('inactive_severe', 365)
    
    @property
    def inactive_moderate_threshold(self) -> int:
        """Get moderate inactivity threshold."""
        return self._config.get('behavioral', {}).get('inactive_moderate', 180)
    
    @property
    def response_rate_threshold(self) -> float:
        """Get response rate threshold."""
        return self._config.get('behavioral', {}).get('response_rate_threshold', 0.05)
    
    @property
    def notice_period_thresholds(self) -> Dict[str, int]:
        """Get notice period thresholds."""
        return {
            'excellent': self._config.get('behavioral', {}).get('notice_period_excellent', 15),
            'good': self._config.get('behavioral', {}).get('notice_period_good', 30),
            'fair': self._config.get('behavioral', {}).get('notice_period_fair', 60),
        }
    
    @property
    def behavioral_multipliers(self) -> Dict[str, float]:
        """Get behavioral multipliers."""
        return {
            'inactive_severe': self._config.get('behavioral', {}).get('inactive_severe_multiplier', 0.10),
            'inactive_moderate': self._config.get('behavioral', {}).get('inactive_moderate_multiplier', 0.30),
            'low_response': self._config.get('behavioral', {}).get('low_response_multiplier', 0.40),
        }
    
    # GitHub Scoring
    @property
    def github_thresholds(self) -> Dict[str, Any]:
        """Get GitHub scoring thresholds."""
        return {
            'no_github': self._config.get('github', {}).get('no_github_score', 0.25),
            'excellent': self._config.get('github', {}).get('excellent_threshold', 70),
            'good': self._config.get('github', {}).get('good_threshold', 50),
            'fair': self._config.get('github', {}).get('fair_threshold', 30),
            'poor': self._config.get('github', {}).get('poor_threshold', 10),
        }
    
    # Output Configuration
    @property
    def default_top_n(self) -> int:
        """Get default top N candidates."""
        return self._config.get('output', {}).get('default_top_n', 100)
    
    @property
    def include_components(self) -> bool:
        """Get include components flag."""
        return self._config.get('output', {}).get('include_components', False)
    
    @property
    def save_cache(self) -> bool:
        """Get save cache flag."""
        return self._config.get('output', {}).get('save_cache', True)
    
    def reload(self):
        """Reload configuration from file."""
        self._config = self._load_config()


# Global config instance
_global_config: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """
    Get global configuration instance.
    
    Args:
        config_path: Optional path to config file
        
    Returns:
        Config instance
    """
    global _global_config
    if _global_config is None:
        _global_config = Config(config_path)
    return _global_config


def reset_config():
    """Reset global configuration instance."""
    global _global_config
    _global_config = None


if __name__ == '__main__':
    # Test config loading
    config = get_config()
    print("Configuration loaded successfully:")
    print(f"  Current date: {config.current_date}")
    print(f"  Mode: {config.mode}")
    print(f"  Tier A titles: {len(config.tier_a_titles)} titles")
    print(f"  Consulting firms: {len(config.consulting_firms)} firms")
    print(f"  Core AI skills: {len(config.core_ai_skills)} skills")
    print(f"  Preferred locations: {len(config.preferred_locations)} locations")
    print(f"  Weights: {config.weights}")
