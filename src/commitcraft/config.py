from __future__ import annotations

from dataclasses import dataclass

from commitcraft.constants import DEFAULT_MAX_CONTEXT, DEFAULT_MODEL, DEFAULT_OLLAMA_URL


@dataclass(frozen=True)
class Config:
    model: str = DEFAULT_MODEL
    ollama_url: str = DEFAULT_OLLAMA_URL
    max_context: int = DEFAULT_MAX_CONTEXT
    debug: bool = False
