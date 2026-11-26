"""Versioned prompt loader for M05."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path


def _prompts_root() -> Path:
    # services/backend/app/modules/ai_coach/domain/prompts.py -> repo/ai/prompts
    return Path(__file__).resolve().parents[6] / "ai" / "prompts"


@lru_cache
def load_prompt(relative_path: str) -> str:
    path = _prompts_root() / relative_path
    return path.read_text(encoding="utf-8")


SYS_COACH = "v1/sys_coach.txt"
PERSONALIZE = "v1/personalize_plan.txt"
