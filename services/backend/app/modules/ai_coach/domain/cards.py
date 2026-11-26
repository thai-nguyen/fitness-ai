"""Allowlisted recommendation card / action contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

ALLOWED_CARD_TYPES = frozenset(
    {"training_adjustment", "exercise_substitution", "preference_update", "info"}
)
ALLOWED_ACTION_TYPES = frozenset({"review_proposal", "accept_preference", "dismiss"})


@dataclass(frozen=True)
class RecommendationCard:
    type: str
    title: str
    proposal_id: str
    reason: str
    requires_confirmation: bool


@dataclass(frozen=True)
class RecommendationAction:
    type: str
    reference_id: str


def build_safe_cards(
    *,
    message: str,
    card_type: str,
    reason: str,
    requires_confirmation: bool = True,
    safety_status: str,
) -> dict[str, Any]:
    if card_type not in ALLOWED_CARD_TYPES:
        raise ValueError("unknown card type")
    proposal_id = f"synth_prop_{uuid4().hex[:12]}"
    card = RecommendationCard(
        type=card_type,
        title="Review a technical proposal",
        proposal_id=proposal_id,
        reason=reason,
        requires_confirmation=requires_confirmation,
    )
    action = RecommendationAction(type="review_proposal", reference_id=proposal_id)
    return {
        "response_id": f"synth_resp_{uuid4().hex[:12]}",
        "message": message,
        "cards": [card.__dict__],
        "actions": [action.__dict__],
        "safety_status": safety_status,
    }
