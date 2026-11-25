# AI Personal Fitness Coach

Premium AI-powered personal fitness coaching platform.

Combines personalized training, conversational AI coaching, persistent user memory, adaptive recommendations, and offline-first workout tracking.

## Current phase

**PHASE-00 — Project Initialization & Technical Discovery**

- **PH00-M01:** `ACCEPTED` (Tech Lead 2026-11-25)
- **PH00-M02:** authorization **PENDING** (do not start without explicit GO)
- Authorized generally for Phase 0 when milestones are GO: discovery, architecture documentation, technical POCs, reversible engineering foundation
- Not authorized: full production feature development, unapproved infrastructure, unauthorized milestones

## Approved stack (TIP v1.1)

| Layer | Direction |
| --- | --- |
| Mobile | Flutter, Pragmatic Clean Architecture, BLoC/Cubit, GoRouter, GetIt, Dio, Drift/SQLite |
| Backend | Python, FastAPI, Modular Monolith, PostgreSQL, SQLAlchemy, Alembic, Pydantic |
| AI | Hybrid architecture, deterministic Fitness Domain Engine, template-first generation, LLM provider abstraction |
| Infra | Docker, **GitHub Actions** (ADR-0001 `ACCEPTED`; implement in M03), basic observability; S3/FCM/APNs when required |

## Repository status

Greenfield baseline established under **PH00-M01**. Application code and walking skeleton are deferred to **PH00-M03**.

## Documentation

Start at [`AGENTS.md`](AGENTS.md) (governance) and [`docs/README.md`](docs/README.md).

| Area | Path |
| --- | --- |
| Agent / engineering governance | [`AGENTS.md`](AGENTS.md) |
| Baseline index / SoT | [`docs/baseline/INDEX.md`](docs/baseline/INDEX.md) |
| Authoritative deposits | [`docs/baseline/authoritative/`](docs/baseline/authoritative/) (**APPROVED** Consolidated Baseline 2026-11-25) |
| Project baseline | [`docs/baseline/`](docs/baseline/) |
| Phase 0 tracker | [`docs/phase-00/execution-tracker.md`](docs/phase-00/execution-tracker.md) |
| Architecture (M02+) | [`docs/architecture/`](docs/architecture/) |
| ADRs | [`docs/adr/`](docs/adr/) |
| Risks | [`docs/risks/RISK_REGISTER.md`](docs/risks/RISK_REGISTER.md) |
| Backlog | [`docs/backlog/TECHNICAL_BACKLOG.md`](docs/backlog/TECHNICAL_BACKLOG.md) |
| Change requests | [`docs/change-requests/`](docs/change-requests/) |

## Local tooling observed (developer workstation)

Captured during PH00-M01 assessment (not a project commitment):

- Python 3.12.10
- Flutter 3.47.2 (stable) / Dart 3.13.2
- Docker 29.9.2
- `psql` CLI not on PATH
- GitHub CLI (`gh`) not installed

## Change control

Do not change product scope, approved technology direction, or introduce deferred technologies without an approved Change Request. See [`docs/change-requests/README.md`](docs/change-requests/README.md).
