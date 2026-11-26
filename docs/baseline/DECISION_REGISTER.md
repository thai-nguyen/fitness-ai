# Decision Register

| Field | Value |
| --- | --- |
| Last updated | 2026-11-25 |
| Milestone | PH00-M03 ACCEPTED WITH WAIVER; PH00-M04 authorized |

## Status values

`PROPOSED` · `ACCEPTED` · `ACCEPTED_WITH_CONSTRAINTS` · `REJECTED` · `SUPERSEDED` · `DEFERRED` · `PENDING` · `ALIGNED`

## Decisions

| ID | Title | Status | ADR | Date | Notes |
| --- | --- | --- | --- | --- | --- |
| D-001 | Retain GitHub hosting; use GitHub Actions + PR workflow instead of GitLab CI | `ACCEPTED` | [ADR-0001](../adr/0001-github-hosting-and-github-actions.md) | 2026-11-25 | Stay within free Actions limits |
| D-002 | Flutter / FastAPI Modular Monolith / PostgreSQL / Hybrid AI stack | `ACCEPTED` | ADR-0002..0005 foundation; 0006–0010/0012 direction | 2026-11-25 | PO confirmed TL ADR decisions |
| D-003 | PostgreSQL-backed background jobs subject to M07 validation | `PROPOSED` | ADR-0014 | 2026-11-25 | Redis/Celery deferred |
| D-004 | Retain existing `docs/phase-00` documentation layout | `ACCEPTED` | — | 2026-11-25 | |
| D-005 | `AGENTS.md` repo-specific governance with constraints | `ACCEPTED_WITH_CONSTRAINTS` | — | 2026-11-25 | |
| D-006 | Consolidated Baseline as official replacement | `ACCEPTED` | — | 2026-11-25 | Pending assumptions remain pending |
| D-007 | PH00-M01 milestone acceptance | `ACCEPTED` | — | 2026-11-25 | Commit `dc5f9d2` |
| D-008 | Proceed to PH00-M02 after M01 local checkpoint | `ACCEPTED` | — | 2026-11-25 | |
| D-009 | Architecture ADRs 0002–0016 content for review | `SUPERSEDED` | — | 2026-11-25 | Superseded by D-012 |
| D-010 | **Zero-Cost First** development constraint | `ACCEPTED` | [ADR-0017](../adr/0017-zero-cost-local-ai-ollama.md) | 2026-11-25 | PO directive; CR-20261125 |
| D-011 | **Ollama** as primary Phase 0 / development AI provider; Qwen 3.5 9B initial POC model | `ACCEPTED` (dev provider) | ADR-0017 | 2026-11-25 | Suitability PENDING M05 |
| D-012 | PH00-M02 acceptance + ADR approval scope | `ACCEPTED` | ADR-0002..0017 per register | 2026-11-25 | TL accept; PO ADR confirmation |
| D-013 | Proceed to PH00-M03 after M02 local checkpoint | `ACCEPTED` | — | 2026-11-25 | M03 commit NOT AUTHORIZED; push NO-GO |
| D-014 | Python deps via `pyproject.toml` + venv + `requirements.lock.txt` | `ACCEPTED` | — | 2026-11-25 | M03 implementation |
| D-015 | Sync SQLAlchemy 2.x for M03 health/DB access | `ACCEPTED` | — | 2026-11-25 | Async deferred |
| D-016 | Postgres host port `127.0.0.1:15432` (avoid Windows excluded ranges) | `ACCEPTED` | — | 2026-11-25 | Image `postgres:16.6-alpine` |
| D-017 | Backend listen port `8080` (avoid occupied `8000`) | `ACCEPTED` | — | 2026-11-25 | |
| D-018 | Provisional Android id `com.fitnessai.dev.fitness_ai_mobile` | `ACCEPTED` | — | 2026-11-25 | Dev only |
| D-019 | Mobile API base URL via `--dart-define=API_BASE_URL` | `ACCEPTED` | — | 2026-11-25 | |
| D-020 | PH00-M03 ACCEPTED WITH WAIVER (F-M03-001 Retry interactive) | `ACCEPTED` | [CR-20261125-B](../change-requests/CR-20261125-m03-retry-waiver.md) | 2026-11-25 | Retry not PASS/VERIFIED; regression still required |
| D-021 | Proceed to PH00-M04 after M03 local checkpoint | `ACCEPTED` | — | 2026-11-25 | M04 commit NOT AUTHORIZED; push NO-GO |
| D-022 | M04 fitness rules as versioned dataclass catalog (`m04-provisional-1`) | `ACCEPTED` | — | 2026-11-26 | Engineering; no expert approval claimed |
| D-023 | Fixture catalog as in-module synthetic `ExerciseDefinition` tuples (`fixture-v1`) | `ACCEPTED` | — | 2026-11-26 | No external dataset ingest |
| D-024 | Deterministic tie-break by ascending `exercise_id` | `ACCEPTED` | — | 2026-11-26 | Selector / substitution |
| D-025 | Structured `GenerationResult` / `ValidationIssue` domain errors | `ACCEPTED` | — | 2026-11-26 | No FastAPI coupling |
| D-026 | Duration estimate = sets×exec + rest + transitions + warm/cool | `ACCEPTED` | — | 2026-11-26 | Estimate ≠ actual |
| D-027 | Safety: any reported concern → REVIEW_REQUIRED (non-triage) | `ACCEPTED` | — | 2026-11-26 | Fail closed |
| D-028 | Evaluation scenarios module + pytest gate (≥30) | `ACCEPTED` | — | 2026-11-26 | Synthetic only |
| D-029 | PH00-M04 technical feasibility acceptance | `ACCEPTED` | — | 2026-11-26 | Provisional rules remain non-expert-approved; OI-003/005 preserved |
| D-030 | Proceed to PH00-M05 after M04 local checkpoint; Ollama synthetic inference authorized | `ACCEPTED` | — | 2026-11-26 | M05 commit NOT AUTHORIZED; push NO-GO; paid AI NO-GO |
| D-031 | Structured output via Ollama format=json + eligible candidate allowlist | `ACCEPTED` | — | 2026-11-26 | M05 technical decision |
| D-032 | Max 1 structured repair then deterministic fallback | `ACCEPTED` | — | 2026-11-26 | Configurable via AI_MAX_REPAIR_ATTEMPTS |
| D-033 | synthetic_ai_memory minimal PostgreSQL POC table | `ACCEPTED` | — | 2026-11-26 | Alembic 20261126_0002 |
| D-034 | Disable/persist-no thinking traces for user/eval paths | `ACCEPTED` | — | 2026-11-26 | think=false |
| D-035 | Live Ollama only via explicit evaluation modes | `ACCEPTED` | — | 2026-11-26 | Unit tests use FakeAIProvider |

## D-012 ADR approval scope

| Class | ADRs | Meaning |
| --- | --- | --- |
| Foundation accepted | 0001, 0002, 0003, 0004, 0005, 0017 | Bind M03 bootstrap |
| Direction accepted | 0006, 0007, 0008, 0009, 0010, 0012 | Principle accepted; impl PENDING |
| Remain proposed | 0011, 0013, 0014, 0015, 0016 | POC/business validation required |

## D-010 / D-011 approval evidence

Project Owner directive (2026-11-25): Zero-Cost First & Local AI First; existing Ollama server (Qwen 3.5 9B; reported base URL for ops config only). See [CR-20261125](../change-requests/CR-20261125-zero-cost-local-ai.md).

## Explicitly still pending

- Team / budget / timeline ROM commitments
- Fitness/nutrition numerical thresholds (expert)
- Exercise content licensing
- **Qwen/Ollama capability & production readiness** (M05)
- Managed/self-hosted **auth** vendor selection (prefer zero-cost)
- Analytics / object storage production choices (prefer zero-cost)
- PostgreSQL durable queue feasibility (M07)
- Nutrition Lite inclusion
- Target market / regulatory assumptions
- **Production hosting** (paid cloud needs PO approval)
- Paid cloud AI (not approved)

## Notes

- Accepted zero-cost constraint binds all milestones until PO changes it.
- M02 local commit authorized after validation; push remains NO-GO.
