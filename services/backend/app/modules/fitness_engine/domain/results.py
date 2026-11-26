"""Structured results and validation issues."""

from __future__ import annotations

from dataclasses import dataclass

from app.modules.fitness_engine.domain.draft import TrainingPlanDraft
from app.modules.fitness_engine.domain.enums import GenerationOutcome, SafetyOutcome, Severity


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    rule_id: str
    field: str
    severity: Severity
    reason: str
    entity_id: str | None = None


@dataclass(frozen=True)
class SafetyScreenResult:
    outcome: SafetyOutcome
    issues: tuple[ValidationIssue, ...]
    guidance_category: str | None = None


@dataclass(frozen=True)
class SubstitutionResult:
    original_exercise_id: str
    replacement_exercise_id: str | None
    reason: str
    constraints: tuple[str, ...]
    valid: bool


@dataclass(frozen=True)
class GenerationResult:
    outcome: GenerationOutcome
    draft: TrainingPlanDraft | None
    issues: tuple[ValidationIssue, ...]
    safety: SafetyScreenResult | None
    warnings: tuple[ValidationIssue, ...] = ()
