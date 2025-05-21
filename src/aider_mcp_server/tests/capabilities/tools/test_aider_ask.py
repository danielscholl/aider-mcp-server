"""Tests for the aider_ask tool."""

import os
from dotenv import load_dotenv

from aider_mcp_server.capabilities.tools.aider_ask import ask_question


def setup_module(module):
    load_dotenv()


def test_ask_question_simple():
    """Ensure a basic prompt returns a non-empty string."""
    response = ask_question("Say hello")
    assert isinstance(response, str)
    assert response
