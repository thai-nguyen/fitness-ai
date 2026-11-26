"""Deterministic AI request safety / injection gate (not medical triage)."""

from __future__ import annotations

from dataclasses import dataclass

from app.modules.fitness_engine.domain.enums import Severity
from app.modules.fitness_engine.domain.results import ValidationIssue

INJECTION_MARKERS = (
    "ignore previous instructions",
    "ignore all instructions",
    "reveal system prompt",
    "reveal the system prompt",
    "override safety",
    "bypass validator",
    "execute sql",
    "drop table",
    "http://",
    "https://",
    "access other user",
    "another user's",
    "cross-user",
    "activate training plan",
    "activate the plan",
    "store this as system instruction",
)

UNSAFE_MEDICAL = (
    "diagnose",
    "prescription for",
    "train through chest pain",
    "ignore the pain",
)


@dataclass(frozen=True)
class AiSafetyResult:
    allowed: bool
    outcome: str  # PASSED|REJECTED|REVIEW_REQUIRED|UNSUPPORTED
    issues: tuple[ValidationIssue, ...]


def screen_ai_request(text: str, *, intent: str | None = None) -> AiSafetyResult:
    lowered = text.lower()
    issues: list[ValidationIssue] = []
    for marker in INJECTION_MARKERS:
        if marker in lowered:
            issues.append(
                ValidationIssue(
                    code="PROMPT_INJECTION_BLOCKED",
                    rule_id="BR-SAFE-002",
                    field="request",
                    severity=Severity.ERROR,
                    reason="request blocked by deterministic injection/authorization gate",
                )
            )
            return AiSafetyResult(False, "REJECTED", tuple(issues))
    for marker in UNSAFE_MEDICAL:
        if marker in lowered:
            issues.append(
                ValidationIssue(
                    code="UNSAFE_REQUEST_BLOCKED",
                    rule_id="BR-SAFE-002",
                    field="request",
                    severity=Severity.ERROR,
                    reason="unsupported medical/unsafe fitness request",
                )
            )
            return AiSafetyResult(False, "REVIEW_REQUIRED", tuple(issues))
    if intent == "unsupported":
        return AiSafetyResult(
            False,
            "UNSUPPORTED",
            (
                ValidationIssue(
                    code="UNSUPPORTED_INTENT",
                    rule_id="BR-ASSESS-002",
                    field="intent",
                    severity=Severity.ERROR,
                    reason="intent not supported in M05 POC",
                ),
            ),
        )
    return AiSafetyResult(True, "PASSED", ())
