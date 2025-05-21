"""Utility to ask a simple question using an LLM model."""

from __future__ import annotations

import os
from dotenv import load_dotenv

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - openai may not be installed
    OpenAI = None  # type: ignore


def ask_question(prompt: str, model: str | None = None) -> str:
    """Send ``prompt`` to the specified model and return the response text."""

    load_dotenv()
    if model is None:
        model = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")

    if OpenAI is None:
        raise RuntimeError("openai package is not available")

    client = OpenAI(api_key=api_key)

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    content = resp.choices[0].message.content
    return content.strip() if content else ""
