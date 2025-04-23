"""
Data types used for the Aider MCP server.
"""

from pydantic import BaseModel
from typing import List, Optional, Dict


class AICodeParams(BaseModel):
    """Parameters for the AI coding session."""
    architect: bool = True
    prompt: str
    model: str
    editor_model: Optional[str] = None
    editable_context: List[str]
    readonly_context: List[str] = []
    settings: Optional[Dict] = None
    use_git: bool = True