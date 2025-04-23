"""
Tool for listing available Aider models.
"""

from typing import List
from aider.models import fuzzy_match_models


def list_models(substring: str) -> List[str]:
    """
    List available Aider models filtered by substring.
    
    Args:
        substring: Substring to filter models by
        
    Returns:
        List of matching model names
    """
    try:
        matches = fuzzy_match_models(substring)
        return matches
    except Exception as e:
        print(f"Error in list_models: {str(e)}")
        return []