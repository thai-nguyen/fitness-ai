# AI Personal Fitness Coach

Premium AI-powered personal fitness coaching platform.

Combines personalized training, conversational AI coaching, persistent user memory, adaptive recommendations, and offline-first workout tracking.

## Current phase

**PHASE-00 — Project Initialization & Technical Discovery**

| Milestone | Status |
| --- | --- |
| PH00-M01 | `ACCEPTED` — commit `dc5f9d2` |
| PH00-M02 | `ACCEPTED` — commit `6ecbbaf` |
| PH00-M03 | Walking Skeleton `IMPLEMENTED` — acceptance **PENDING**; **no M03 commit** |
| PH00-M04+ | **NO-GO** |

Constraints: **Zero-Cost First**, **Local AI First** (Ollama / Qwen 3.5 9B). Git **push NO-GO**. Paid services **NOT AUTHORIZED**.

## Walking Skeleton (M03)

`Flutter → FastAPI → PostgreSQL` health check path.

Quick start: [`docs/phase-00/LOCAL_DEV_RUNBOOK.md`](docs/phase-00/LOCAL_DEV_RUNBOOK.md)

```powershell
docker compose -f infrastructure/docker-compose.yml up -d
cd services\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
$env:DATABASE_URL="postgresql+psycopg://fitness:fitness_dev_only@127.0.0.1:15432/fitness_ai"
alembic upgrade head
uvicorn app.main:app --host 127.0.0.1 --port 8080
# other terminal:
cd apps\mobile
flutter pub get
flutter run -d windows --dart-define=API_BASE_URL=http://127.0.0.1:8080
```

Local quality: `.\scripts\local_quality.ps1`

## Approved stack

| Layer | Direction |
| --- | --- |
| Mobile | Flutter, Clean Architecture, BLoC/Cubit, GoRouter, GetIt, Dio |
| Backend | Python, FastAPI modular monolith, PostgreSQL, SQLAlchemy (sync M03), Alembic, Pydantic |
| AI | Hybrid direction; Ollama config boundary only in M03 (no chat) |
| Infra | Docker Compose (Postgres), GitHub Actions workflow definitions |

## Repository layout

```text
apps/mobile/           Flutter Walking Skeleton
services/backend/      FastAPI foundation
infrastructure/        docker-compose.yml
scripts/               local_quality.ps1
docs/                  baseline, architecture, phase-00
.github/workflows/     quality.yml (hosted run pending push)
```

## Documentation

| Area | Path |
| --- | --- |
| Governance | [`AGENTS.md`](AGENTS.md) |
| Docs index | [`docs/README.md`](docs/README.md) |
| Local runbook | [`docs/phase-00/LOCAL_DEV_RUNBOOK.md`](docs/phase-00/LOCAL_DEV_RUNBOOK.md) |
| M03 completion | [`docs/phase-00/PH00-M03-completion-report.md`](docs/phase-00/PH00-M03-completion-report.md) |

## Change control

Do not change product scope or introduce deferred/paid technologies without an approved Change Request.
