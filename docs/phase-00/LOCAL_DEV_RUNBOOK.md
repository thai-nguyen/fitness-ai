# Local Development Runbook (PH00-M03)

Zero-Cost First / Local AI First. No paid services.

## Selected toolchain (this workstation)

| Tool | Version |
| --- | --- |
| Flutter | 3.47.2 (stable) |
| Dart | 3.13.2 |
| Python | 3.12.10 |
| Docker / Compose | 29.9.2 / v5.6.1 |
| PostgreSQL image | `postgres:16.6-alpine` |
| Backend host port | `8080` |
| Postgres host port | `127.0.0.1:15432` → container `5432` |

Provisional Android application id: `com.fitnessai.dev.fitness_ai_mobile` (development only).

## Prerequisites

1. Copy `.env.example` → `.env` (gitignored). Do **not** put private LAN Ollama addresses in committed files.
2. Start PostgreSQL only:

```powershell
docker compose -f infrastructure/docker-compose.yml up -d
docker compose -f infrastructure/docker-compose.yml ps
```

## Backend

```powershell
cd services\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
$env:DATABASE_URL="postgresql+psycopg://fitness:fitness_dev_only@127.0.0.1:15432/fitness_ai"
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Checks:

- `GET http://127.0.0.1:8080/health/live`
- `GET http://127.0.0.1:8080/health/ready`

## Mobile

```powershell
cd apps\mobile
flutter pub get
# Windows desktop (validated on this host):
flutter run -d windows --dart-define=API_BASE_URL=http://127.0.0.1:8080
# Android emulator:
flutter run -d emulator-5554 --dart-define=API_BASE_URL=http://10.0.2.2:8080
# Physical Android device (use your *dev machine* LAN IP, not Ollama IP unless same host):
flutter run --dart-define=API_BASE_URL=http://<DEV_LAN_IP>:8080
```

Debug Android cleartext for local HTTP is enabled only under `android/app/src/debug`.

## Ollama (optional M03 connectivity)

Configure in local `.env`:

```text
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://192.168.8.54:11434
OLLAMA_MODEL=<tag from /api/tags>
```

Optional read-only check: `GET /api/tags` with a short timeout. Not required for app startup or tests. Capability validation is **M05**.

## Local quality gate

```powershell
.\scripts\local_quality.ps1
```

## Safe shutdown

```powershell
docker compose -f infrastructure/docker-compose.yml stop
# Do NOT use down -v unless intentionally destroying project volume fitness_ai_pg_data
```

## Known limitations

- Android SDK licenses may be unaccepted — APK build can be blocked until `flutter doctor --android-licenses`.
- iOS build not validated on Windows.
- GitHub Actions YAML exists but hosted execution awaits push authorization.
- Host port `55432` was avoided due to Windows excluded port ranges; use `15432`.
