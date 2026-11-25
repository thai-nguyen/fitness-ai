# Architecture Decision Records

## Status values

`PROPOSED` · `ACCEPTED` · `ACCEPTED_WITH_CONSTRAINTS` · `DEPRECATED` · `SUPERSEDED` · `REJECTED`

## Index

| ADR | Title | Status | Milestone |
| --- | --- | --- | --- |
| [0001](0001-github-hosting-and-github-actions.md) | GitHub hosting + GitHub Actions | `ACCEPTED` | M01 |
| [0002](0002-modular-monolith.md) | Modular monolith | `ACCEPTED` | M02 → M03 |
| [0003](0003-monorepo.md) | Monorepo layout | `ACCEPTED` | M02 → M03 |
| [0004](0004-flutter-clean-architecture.md) | Flutter Clean Architecture + BLoC | `ACCEPTED` | M02 → M03 |
| [0005](0005-postgresql.md) | PostgreSQL SoT | `ACCEPTED` | M02 → M03 |
| [0006](0006-hybrid-ai.md) | Hybrid AI orchestrator | `ACCEPTED` (direction); impl PENDING | M02 / M05 |
| [0007](0007-fitness-engine.md) | Deterministic Fitness Engine | `ACCEPTED` (direction); impl PENDING | M02 / M04 |
| [0008](0008-structured-memory.md) | Structured AI memory | `ACCEPTED` (direction); impl PENDING | M02 / M05 |
| [0009](0009-offline-first-workout.md) | Offline-first workouts | `ACCEPTED` (direction); impl PENDING | M02 / M06 |
| [0010](0010-immutable-plan-versions.md) | Immutable plan versions | `ACCEPTED` (direction); impl PENDING | M02+ |
| [0011](0011-limited-outbox.md) | Limited transactional outbox | `PROPOSED` | M07 |
| [0012](0012-ai-provider-abstraction.md) | AI provider abstraction | `ACCEPTED` (direction); chat/tools PENDING M05 | M02 / M05 |
| [0013](0013-managed-authentication.md) | Managed OIDC auth | `PROPOSED` | Auth spike |
| [0014](0014-postgresql-job-queue.md) | PG job queue | `PROPOSED` (M07 evidence required) | M07 |
| [0015](0015-health-data-governance.md) | Health-adjacent governance | `PROPOSED` | M08 |
| [0016](0016-ai-evaluation.md) | AI evaluation strategy | `PROPOSED` | M05/M08 |
| [0017](0017-zero-cost-local-ai-ollama.md) | Zero-Cost First & Local AI (Ollama) | `ACCEPTED` | M02 (PO) |

## Approval summary (2026-11-25)

| Scope | ADRs |
| --- | --- |
| Fully accepted foundation | 0001, 0002, 0003, 0004, 0005, 0017 |
| Accepted architectural direction only | 0006, 0007, 0008, 0009, 0010, 0012 |
| Remain `PROPOSED` | 0011, 0013, 0014, 0015, 0016 |

Evidence: Tech Lead PH00-M02 final review + Project Owner confirmation (2026-11-25). Model suitability and production readiness remain PENDING (M05).
