# Project Baseline

| Field | Value |
| --- | --- |
| Project | AI Personal Fitness Coach (fitness-ai) |
| Baseline ID | `BASELINE-2026-11-25-PH00-M01-CLOSURE` |
| Established | 2026-11-25 |
| Phase | PHASE-00 — Project Initialization & Technical Discovery |
| Milestone | PH00-M01 — Final closure validation |
| Status | PH00-M01 **`ACCEPTED`** by Tech Lead 2026-11-25 |
| Governing AUTH | Consolidated Baseline APPROVED by PO 2026-11-25 (not verbatim historical originals) |

## 1. Purpose

Shared starting point for Phase 0: repository state, approved direction, MVP boundaries, documentation layout, execution tracking, and known pending items.

## 2. Authorization boundary (current)

| Category | Status |
| --- | --- |
| Consolidated Baseline | **APPROVED** (PO) |
| PH00-M01 | **`ACCEPTED`** (Tech Lead 2026-11-25; basis = final readiness report) |
| Remaining M01 blockers | **None reported** |
| PH00-M02 authorization | **PENDING** (explicit GO required; not started) |
| PH00-M03+ | **NO-GO** until respective authorization |
| Production feature development | NO-GO |
| Unapproved infrastructure | NO-GO |

## 3. Repository snapshot

| Item | Observation |
| --- | --- |
| Remote | `https://github.com/thai-nguyen/fitness-ai.git` (`main`) |
| Application code | None (M03+) |
| CI workflows | None (M03; ADR-0001 accepted) |
| AUTH package | Four files under `docs/baseline/authoritative/` |
| Governance | `AGENTS.md` present (D-005) |

## 4. Direction summary

See [`APPROVED_TECHNICAL_DIRECTION.md`](APPROVED_TECHNICAL_DIRECTION.md) and AUTH-003.

- Flutter + pragmatic Clean Architecture + BLoC/Cubit + offline Drift/SQLite
- FastAPI modular monolith + PostgreSQL
- Hybrid AI + deterministic Fitness Engine + structured memory
- GitHub + GitHub Actions (ADR-0001)
- Offline-first workouts; immutable plan versions; user-confirmed AI recommendations

## 5. MVP summary

See [`MVP_SCOPE.md`](MVP_SCOPE.md) and AUTH-001/002.

## 6. Pending assumptions (remain pending after baseline approval)

Staffing/budget/timeline ROMs; fitness expert rules; content licensing; AI/auth/analytics providers; PG job POC; Nutrition Lite inclusion; market/regulatory research; measured POC/SLO/cost results.

## 7. Documentation

Index: [`INDEX.md`](INDEX.md). Phase 0 tracker: [`../phase-00/execution-tracker.md`](../phase-00/execution-tracker.md).

## 8. Synthetic data policy

Phase 0 POCs use synthetic data only. No production credentials. No real health data.
