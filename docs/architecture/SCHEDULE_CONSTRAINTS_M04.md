# Schedule Constraints (PH00-M04)

| Field | Value |
| --- | --- |
| Implementation | `fitness_engine/domain/schedule.py`, `templates.py`, `assessment.py` |
| Rule set | `m04-provisional-1` |

## Hard constraints

| Rule | Behavior |
| --- | --- |
| BR-SCHED-001 | At least one available training day; sessions must be within availability (validator) |
| BR-SCHED-002 | Unique days (no duplicates) |
| BR-SCHED-003 | Fixture max frequency ≤5; template `min_days` must be satisfiable |
| BR-SCHED-004 | Preferred days ⊆ available days |
| Template min/max days | `allocate_schedule` fails with `INSUFFICIENT_DAYS` when availability < template.min_days — **not** silently relaxed |

## Soft preferences

| Rule | Behavior |
| --- | --- |
| BR-SCHED-005 | Prefer spaced (non-consecutive) days when multiple candidates exist (`_spread_score`) |

Consecutive days are **allowed** when availability forces them. Soft spacing is a provisional heuristic (`EXPERT_REVIEW_REQUIRED`), not a hard rest prescription.

## Provisional fitness assumptions

- Soft spacing does **not** model physiology, fatigue, or week-boundary wrap-around rest science.
- Plans are single-week technical drafts; no multi-week calendar / timezone infrastructure.
- Numeric frequency caps remain provisional fixtures until expert review (OI-003).

## Limitations

- No prohibition on consecutive days as a hard rule in M04.
- Week-boundary spacing (Sun→Mon) is not specially modeled beyond ordered weekday indices Mon–Sun.
