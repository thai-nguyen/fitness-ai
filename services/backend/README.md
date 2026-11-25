# fitness-ai backend (PH00-M03)

Minimal FastAPI foundation: health endpoints, PostgreSQL connectivity, Alembic, AI config boundary.

## Quick start

```powershell
cd services/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e ".[dev]"
# From repo root: copy .env.example -> .env, start Compose postgres, then:
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

See [`docs/phase-00/LOCAL_DEV_RUNBOOK.md`](../../docs/phase-00/LOCAL_DEV_RUNBOOK.md).
