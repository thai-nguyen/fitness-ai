"""Deterministic training volume calculation."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from app.modules.exercise_catalog.domain.models import ExerciseCatalog
from app.modules.fitness_engine.domain.draft import TrainingPlanDraft
from app.modules.fitness_engine.domain.enums import Severity
from app.modules.fitness_engine.domain.results import ValidationIssue

MIN_WORKING_SETS = 1
MAX_WORKING_SETS = 5
WEEKLY_PRIMARY_WARN = 20
WEEKLY_PRIMARY_ERROR = 30


@dataclass(frozen=True)
class VolumeSummary:
    exercise_count: int
    total_working_sets: int
    weekly_primary_sets: dict[str, float]
    weekly_secondary_sets: dict[str, float]


def summarize_volume(draft: TrainingPlanDraft, catalog: ExerciseCatalog) -> VolumeSummary:
    by_id = catalog.by_id()
    primary: dict[str, float] = defaultdict(float)
    secondary: dict[str, float] = defaultdict(float)
    exercise_count = 0
    total_sets = 0
    for session in draft.sessions:
        for item in session.exercises:
            exercise_count += 1
            total_sets += item.working_sets
            ex = by_id.get(item.exercise_id)
            if ex is None:
                continue
            for mg in ex.primary_muscle_groups:
                primary[mg.value] += item.working_sets
            for mg in ex.secondary_muscle_groups:
                # Explicit policy: secondary counted at 0.5
                secondary[mg.value] += item.working_sets * 0.5
    return VolumeSummary(
        exercise_count=exercise_count,
        total_working_sets=total_sets,
        weekly_primary_sets=dict(sorted(primary.items())),
        weekly_secondary_sets=dict(sorted(secondary.items())),
    )


def validate_working_sets(working_sets: int) -> ValidationIssue | None:
    if working_sets < MIN_WORKING_SETS or working_sets > MAX_WORKING_SETS:
        return ValidationIssue(
            code="INVALID_WORKING_SETS",
            rule_id="BR-VOL-001",
            field="working_sets",
            severity=Severity.ERROR,
            reason=f"working_sets must be {MIN_WORKING_SETS}-{MAX_WORKING_SETS}",
        )
    return None


def volume_issues(draft: TrainingPlanDraft, catalog: ExerciseCatalog) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for session in draft.sessions:
        for item in session.exercises:
            issue = validate_working_sets(item.working_sets)
            if issue:
                issues.append(
                    ValidationIssue(
                        code=issue.code,
                        rule_id=issue.rule_id,
                        field=issue.field,
                        severity=issue.severity,
                        reason=issue.reason,
                        entity_id=item.exercise_id,
                    )
                )
    summary = summarize_volume(draft, catalog)
    for muscle, sets in summary.weekly_primary_sets.items():
        if sets > WEEKLY_PRIMARY_ERROR:
            issues.append(
                ValidationIssue(
                    code="EXCESSIVE_VOLUME",
                    rule_id="BR-VOL-002",
                    field="weekly_primary_sets",
                    severity=Severity.ERROR,
                    reason=f"primary volume for {muscle} exceeds {WEEKLY_PRIMARY_ERROR}",
                    entity_id=muscle,
                )
            )
        elif sets > WEEKLY_PRIMARY_WARN:
            issues.append(
                ValidationIssue(
                    code="HIGH_VOLUME_WARNING",
                    rule_id="BR-VOL-002",
                    field="weekly_primary_sets",
                    severity=Severity.WARNING,
                    reason=f"primary volume for {muscle} exceeds soft cap {WEEKLY_PRIMARY_WARN}",
                    entity_id=muscle,
                )
            )
    return issues
