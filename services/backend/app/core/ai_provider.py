"""Minimal AI provider configuration boundary (no chat/inference in M03)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.core.config import Settings


@dataclass(frozen=True)
class AiProviderConfig:
    provider: str
    base_url: str
    model: str


class AiProvider(Protocol):
    """Future adapter contract — intentionally tiny for M03."""

    @property
    def name(self) -> str: ...


def resolve_ai_provider_config(settings: Settings) -> AiProviderConfig:
    return AiProviderConfig(
        provider=settings.ai_provider,
        base_url=settings.ollama_base_url,
        model=settings.ollama_model,
    )
