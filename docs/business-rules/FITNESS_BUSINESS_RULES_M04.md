# Fitness Business Rules Catalog (PH00-M04)

| Field | Value |
| --- | --- |
| Rule set version | `m04-provisional-1` |
| Status | Technical feasibility only — **not** expert-approved |
| Authoritative implementation | `services/backend/app/modules/fitness_engine/domain/rules.py` |
| Related | PH00-TB-012, ADR-0007, OI-003 |

## Review vocabulary

| Kind | Meaning |
| --- | --- |
| `TECHNICAL_INVARIANT` | Structural / fail-closed engineering constraint |
| `PROVISIONAL_FITNESS_RULE` | Numeric or programming heuristic for synthetic tests only |
| `EXPERT_REVIEW_REQUIRED` | Must not be treated as production fitness guidance |
| `EXPERT_APPROVED` | **None** in M04 — do not fabricate |

Sources marked `SOURCE_PENDING` have no fabricated citations.

## Inventory

Full structured fields (ID, name, description, rationale, inputs, behavior, hard/soft, source, review status, implementation ref, test ref, limitations) live in code:

`app/modules/fitness_engine/domain/rules.py` → `RULES`

| Rule ID | Kind | Hard/Soft | Summary |
| --- | --- | --- | --- |
| BR-ASSESS-001 | TECHNICAL_INVARIANT | hard | Required assessment fields |
| BR-ASSESS-002 | PROVISIONAL_FITNESS_RULE | hard | Supported goals only |
| BR-ASSESS-003 | TECHNICAL_INVARIANT | hard | Assessment completeness |
| BR-SCOPE-001 | EXPERT_REVIEW_REQUIRED | hard | Beginner/intermediate only |
| BR-SCOPE-002 | EXPERT_REVIEW_REQUIRED | hard | Adult eligibility |
| BR-SCHED-001 | TECHNICAL_INVARIANT | hard | ≥1 available day |
| BR-SCHED-002 | TECHNICAL_INVARIANT | hard | Unique days |
| BR-SCHED-003 | PROVISIONAL_FITNESS_RULE | hard | ≤5 days/week fixture |
| BR-SCHED-004 | TECHNICAL_INVARIANT | hard | Preferred ⊆ available |
| BR-SCHED-005 | EXPERT_REVIEW_REQUIRED | soft | Prefer spaced days |
| BR-DUR-001 | PROVISIONAL_FITNESS_RULE | hard | 20–90 min session window |
| BR-DUR-002 | TECHNICAL_INVARIANT | hard | Estimate must fit max duration |
| BR-SEL-001 | TECHNICAL_INVARIANT | hard | Equipment hard filter |
| BR-SEL-002 | TECHNICAL_INVARIANT | hard | Active catalog only |
| BR-SEL-003 | EXPERT_REVIEW_REQUIRED | hard | Difficulty vs experience |
| BR-SEL-004 | TECHNICAL_INVARIANT | hard | Exclusions / restriction tags |
| BR-VOL-001 | PROVISIONAL_FITNESS_RULE | hard | Working sets 1–5 |
| BR-VOL-002 | EXPERT_REVIEW_REQUIRED | soft/hard | Weekly primary volume warn/error |
| BR-INT-001 | TECHNICAL_INVARIANT | hard | Rep range / rest validity |
| BR-INT-002 | EXPERT_REVIEW_REQUIRED | hard | Beginner RPE ≤7 |
| BR-SAFE-001 | TECHNICAL_INVARIANT | hard | Explicit adult eligibility |
| BR-SAFE-002 | EXPERT_REVIEW_REQUIRED | hard | Reported concerns block generation |
| BR-SAFE-003 | TECHNICAL_INVARIANT | hard | Missing safety config fail-closed |
| BR-SUB-001 | TECHNICAL_INVARIANT | hard | Substitution constraints |
| BR-VAL-001 | TECHNICAL_INVARIANT | hard | Independent draft validation |

## Expert review requirements

All `PROVISIONAL_FITNESS_RULE` and `EXPERT_REVIEW_REQUIRED` rows require domain-expert review before any production use. OI-003 remains `OPEN`. A technically validated draft is **not** a production-approved workout prescription.

## Schedule hard vs soft

See [`../architecture/SCHEDULE_CONSTRAINTS_M04.md`](../architecture/SCHEDULE_CONSTRAINTS_M04.md). BR-SCHED-005 spacing is soft; template `min_days` and availability are hard.

## Traceability metrics

Executable metrics: `app/modules/fitness_engine/domain/traceability.py` (see remediation report F-M04-006).
