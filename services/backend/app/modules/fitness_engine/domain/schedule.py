"""Deterministic schedule allocation."""

from __future__ import annotations

from dataclasses import dataclass

from app.modules.fitness_engine.domain.enums import Severity, Weekday
from app.modules.fitness_engine.domain.results import ValidationIssue
from app.modules.fitness_engine.domain.templates import TrainingTemplate

WEEKDAY_ORDER = (
    Weekday.MON,
    Weekday.TUE,
    Weekday.WED,
    Weekday.THU,
    Weekday.FRI,
    Weekday.SAT,
    Weekday.SUN,
)


@dataclass(frozen=True)
class ScheduleResult:
    days: tuple[Weekday, ...] | None
    issues: tuple[ValidationIssue, ...]


def _spread_score(days: list[Weekday]) -> int:
    """Higher is better: prefer gaps between consecutive selected days."""
    idxs = [WEEKDAY_ORDER.index(d) for d in days]
    if len(idxs) < 2:
        return 0
    return sum(idxs[i + 1] - idxs[i] for i in range(len(idxs) - 1))


def allocate_schedule(
    available: tuple[Weekday, ...],
    preferred: tuple[Weekday, ...],
    template: TrainingTemplate,
) -> ScheduleResult:
    available_set = list(dict.fromkeys(available))  # preserve order, unique
    if not available_set:
        return ScheduleResult(
            None,
            (
                ValidationIssue(
                    code="NO_AVAILABLE_DAYS",
                    rule_id="BR-SCHED-001",
                    field="available_training_days",
                    severity=Severity.ERROR,
                    reason="no available training days",
                ),
            ),
        )

    target = min(max(template.min_days, len(preferred) or template.min_days), template.max_days)
    target = min(target, len(available_set))
    if len(available_set) < template.min_days:
        return ScheduleResult(
            None,
            (
                ValidationIssue(
                    code="INSUFFICIENT_DAYS",
                    rule_id="BR-SCHED-003",
                    field="available_training_days",
                    severity=Severity.ERROR,
                    reason=(
                        f"need at least {template.min_days} days "
                        f"for template {template.template_id}"
                    ),
                ),
            ),
        )

    # Prefer preferred days first (stable order by WEEKDAY_ORDER), then fill
    preferred_ordered = [d for d in WEEKDAY_ORDER if d in preferred and d in available_set]
    remaining = [d for d in WEEKDAY_ORDER if d in available_set and d not in preferred_ordered]

    chosen = preferred_ordered[:target]
    if len(chosen) < target:
        # Choose remaining days maximizing spread (deterministic among equals via day order)
        pool = remaining
        while len(chosen) < target and pool:
            best = None
            best_score = -1
            for candidate in pool:
                trial = sorted(chosen + [candidate], key=lambda d: WEEKDAY_ORDER.index(d))
                score = _spread_score(trial)
                if score > best_score:
                    best_score = score
                    best = candidate
            assert best is not None
            chosen.append(best)
            pool = [d for d in pool if d != best]

    chosen_sorted = tuple(sorted(chosen, key=lambda d: WEEKDAY_ORDER.index(d)))
    return ScheduleResult(chosen_sorted, ())
