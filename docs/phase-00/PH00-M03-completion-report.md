# PH00-M03 Completion Report — Engineering Foundation

| Field | Value |
| --- | --- |
| Milestone | PH00-M03 — Engineering Foundation (Walking Skeleton) |
| Date | 2026-11-25 |
| Author | Engineering |
| Reviewer | Tech Lead |
| Status | **`ACCEPTED` WITH WAIVER** (Project Owner) |
| Accepted by | Project Owner (Tech Lead review + PO waiver) |
| Acceptance date | 2026-11-25 |
| Waiver | [`CR-20261125-B`](../change-requests/CR-20261125-m03-retry-waiver.md) / D-020 |
| Remediation | [`PH00-M03-remediation-report.md`](PH00-M03-remediation-report.md) |
| M03 commit | Authorized local commit after validation; push **NO-GO** |
| Push | **NO-GO** |

---

## 1. Executive summary

PH00-M02 was closed and locally committed. PH00-M03 delivers a minimal **Flutter → FastAPI → PostgreSQL** Walking Skeleton with health UI, readiness API, Alembic baseline, Docker Compose Postgres, local quality scripts, and GitHub Actions workflow definitions — under **Zero-Cost First** / **Local AI First**. Ollama is optional (config + read-only `/api/tags`); app startup and tests do not require it. **M03 is not self-accepted. No M03 commit/push. M04 NO-GO.**

## 2. M02 closure and local commit SHA

| Field | Value |
| --- | --- |
| M02 status | `ACCEPTED` |
| M02 commit | `6ecbbaf4b24c0704c458290076f1b67086bbde53` |
| Message | `docs: finalize architecture baseline and close PH00-M02` |
| M01 ancestor | `dc5f9d2ece2875b41f4822f1a037897d259aaffc` preserved |
| Push | Not performed (`main` ahead of origin by 2 after M02) |

## 3. M03 authorized scope

In scope: monorepo bootstrap, Flutter health feature, FastAPI health/DB, Postgres Compose, Alembic empty baseline, env config, AI config boundary, tests, CI YAML, docs.
Out of scope: product features, AI chat/benchmarks, Drift/offline, auth, Redis/Celery, paid services, M03 commit, M04+.

## 4. Actual toolchain inventory

| Tool | Result |
| --- | --- |
| Git | 2.52.0.windows.1 |
| Flutter | 3.47.2 stable |
| Dart | 3.13.2 |
| Python | 3.12.10 |
| pip | 26.3 (venv) |
| Docker | 29.9.2 |
| Compose | v5.6.1 |
| Android SDK | 37.0.0 present; licenses previously warned — **APK debug build succeeded** |
| Java (Flutter config) | OpenJDK 21.0.8 |
| Devices | Windows desktop, Chrome, Edge available; no emulator required for Windows validation |
| Disk (D:) | ~525 GB free |
| Port conflicts | Host `8000` occupied (unrelated); Postgres `5433` used by unrelated `ai-postgres` — avoided |

## 5. Selected dependency versions

**Backend (pinned in `services/backend/pyproject.toml`):** FastAPI 0.115.6, Uvicorn 0.34.0, Pydantic 2.10.4, pydantic-settings 2.7.0, SQLAlchemy 2.0.36, psycopg[binary] 3.2.3, Alembic 1.14.0, httpx 0.28.1, pytest 8.3.4, ruff 0.8.4. Lock: `requirements.lock.txt`.

**Mobile:** flutter_bloc 9.1.0, go_router 14.8.1, get_it 8.0.3, dio 5.7.0, equatable 2.0.7, bloc_test 10.0.0, mocktail 1.0.4, flutter_lints ^6.0.0. Lock: `pubspec.lock`.

**Infra:** `postgres:16.6-alpine` (pinned).

**Dependency management rationale:** project-local venv + `pyproject.toml` editable install + freeze lock — simple, reproducible, no extra package manager.

## 6. Repository structure

```text
apps/mobile/
services/backend/
infrastructure/docker-compose.yml
scripts/local_quality.ps1
.github/workflows/quality.yml
.env.example
docs/phase-00/LOCAL_DEV_RUNBOOK.md
```

No admin portal, no empty future domain modules, no Ollama container.

## 7. Flutter foundation

- Clean Architecture health feature (`domain` / `data` / `presentation`)
- Cubit + GoRouter + GetIt + Dio
- Health screen: app name, backend status, service/version, DB status, last check, retry
- API base URL via `--dart-define=API_BASE_URL`
- Debug-only Android cleartext; provisional id `com.fitnessai.dev.fitness_ai_mobile`
- Windows debug build **executed**; Android debug APK **executed**

## 8. Backend foundation

- FastAPI app factory, structured logging, typed settings
- `GET /health/live`, `GET /health/ready` (503 if DB down), `GET /version`
- Sync SQLAlchemy + `SELECT 1` readiness
- Ollama **not** required for readiness

## 9. PostgreSQL and migrations

- Compose service `fitness-ai-postgres`, volume `fitness_ai_pg_data`, bind `127.0.0.1:15432`
- Empty baseline revision `20261125_0001`
- Validated: `alembic upgrade head`, `alembic current`, `alembic heads`

## 10. Local infrastructure

| Check | Result |
| --- | --- |
| `docker compose config` | OK |
| `docker compose up -d` | OK (after port change from blocked `55432`) |
| Health | `healthy` |
| Unrelated containers | Not stopped/removed |

## 11. Environment configuration

- `.env.example` with placeholders; `.env` created locally and **gitignored** (`git check-ignore` confirmed)
- Defaults use loopback for Ollama URL — **no** `192.168.8.54` in runtime defaults/source

## 12. Ollama connectivity (optional)

| Check | Result |
| --- | --- |
| `GET http://192.168.8.54:11434/api/tags` | HTTP **200**, inventory accessible |
| Exact Qwen tag | **`qwen3.5:9b` present** |
| Local `127.0.0.1:11434` | Also HTTP 200 on this workstation |
| Generation / benchmarks | **Not executed** (M05) |

Connectivity ≠ model quality or production suitability.

## 13. AI provider boundary

`AI_PROVIDER`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL` + minimal `AiProviderConfig` / protocol stub. No chat, tools, memory, RAG, or cloud adapters.

## 14. Local quality gates

| Area | Commands | Result |
| --- | --- | --- |
| Backend lint | `ruff check app tests` | exit 0 |
| Backend format | `ruff format --check` | exit 0 |
| Backend tests | `pytest -q` | **9 passed** |
| Mobile format | `dart format --set-exit-if-changed .` | exit 0 |
| Mobile analyze | `flutter analyze` | No issues |
| Mobile unit/widget | `flutter test --exclude-tags e2e` | **6 passed** |
| Compose | `docker compose config` | OK |
| Script | `scripts/local_quality.ps1` | **Executed exit 0** (remediation) |

## 15. GitHub Actions

- File: `.github/workflows/quality.yml`
- Jobs: backend (with Postgres service) + mobile; `workflow_dispatch` + path-filtered PR
- No Ollama/LAN, no deploy, no paid runners, `permissions: contents: read`
- **Hosted execution:** NOT EXECUTED (push unauthorized) — YAML present only

## 16. End-to-end Walking Skeleton results

### Historical (initial completion — retained)

Interactive Flutter UI session was originally **overstated** as covered by builds/widget/e2e Dio only. Corrected below after F-M03-001 remediation.

### Corrected status (post-remediation)

| Step | Status | Evidence |
| --- | --- | --- |
| 1 Postgres running | **Executed** | compose ps healthy :15432 |
| 2 Backend starts | **Executed** | uvicorn on 8080 |
| 3 `/health/live` | **Executed** | `{"status":"ok",...}` |
| 4 `/health/ready` | **Executed** | `database: up` |
| 5 DB connectivity | **Executed** | readiness + pytest + 503-on-DB-stop |
| 6 Alembic | **Executed** | upgrade/current/heads |
| 7 Flutter interactive start (Windows) | **Executed** | `flutter run -d windows`; PrintWindow success UI |
| 8 Flutter→backend readiness (live UI) | **Executed** | success PNG + uvicorn access log |
| 9 Success render (interactive) | **Executed** | `scripts/runtime-evidence/health-ui-success.png` |
| 10 Error when backend down (interactive) | **Executed** | `health-ui-error.png` |
| 11 Retry after recovery (interactive click) | **PENDING** | Injected clicks did not register; widget Retry covered in tests; **manual confirmation required** |
| 12 Tests independent of Ollama | **Executed** | quality script / pytest / flutter unit |

See [`PH00-M03-remediation-report.md`](PH00-M03-remediation-report.md) §3 for manual Retry instructions.

## 17. Test commands and actual results

```text
# Backend
ruff check app tests          → 0
pytest -q                     → 9 passed
alembic upgrade head/current  → 0 / 20261125_0001

# Mobile
flutter analyze               → No issues
flutter test --exclude-tags e2e → 6 passed
flutter test --tags e2e       → 2 passed (live backend)
flutter build windows --debug → success
flutter build apk --debug     → success (app-debug.apk)
```

## 18. Zero-cost compliance

OSS libraries only; local Docker Postgres; existing Ollama hardware; no paid APIs/SaaS/runners; CI free-tier oriented. Production cost remains PENDING.

## 19. Security and secret validation

| Check | Result |
| --- | --- |
| `.env` ignored | Yes |
| Credentialed URLs in commits | Placeholders in `.env.example` only |
| Private LAN in source defaults | Absent |
| Doc ops references to LAN | Allowed in ADR/architecture docs |
| Heuristic scan | Doc LAN hits + example placeholders; **not** a full audit |
| Health responses | No credentials/stack traces/paths leaked |

## 20. Files created or modified (M03 working tree; uncommitted)

Apps/mobile, services/backend, infrastructure, scripts, `.github/workflows/quality.yml`, `.env.example`, README/AGENTS/tracker/backlog/decisions/runbook/this report. `.env` local only.

## 21. Backlog task statuses

| ID | Status |
| --- | --- |
| PH00-TB-010 | `VALIDATED` (acceptance PENDING) |
| PH00-TB-010-A | `VALIDATED` (Ollama tags) |
| PH00-TB-011 | `IN_PROGRESS` (runbook DB notes; LICENSE pending owner) |
| PH00-TB-012+ | Unchanged / not started (later milestones) |

## 22. Implementation decisions and rationale

See D-014..D-019: sync SQLAlchemy, ports 15432/8080, dart-define config, pyproject+venv lock, provisional app id.

## 23. Decisions made without explicit prior detail

- Chose host port **15432** after Windows excluded-range blocked **55432**
- Chose backend **8080** because **8000** occupied by unrelated process
- Included Windows platform in `flutter create` for local validation on this host
- Added tagged e2e Dio tests for live client-path evidence

## 24. Pending assumptions

Auth vendor; AI suitability beyond tags; fitness rules; licensing/LICENSE text; production hosting/cost; offline sync; job queue; Nutrition Lite; budgets/timelines.

## 25. Known limitations

- Hosted GitHub Actions not executed
- Interactive Retry click not agent-confirmed (F-M03-001 pending)
- Android licenses previously warned (APK still built)
- iOS not validated on Windows
- Empty Alembic baseline ≠ domain schema readiness
- Secret scan heuristic-only
- Dependency vulnerability scan not run

## 26. Remaining risks and blockers

| Item | Notes |
| --- | --- |
| F-M03-001 Retry interactive | Pending human confirmation |
| M03 Tech Lead final acceptance | Gate |
| LICENSE (TB-011) | Awaiting PO |
| Model capability | M05 |
| Port exclusion ranges on Windows | Documented |
| Unrelated services on host | Must not be disrupted |

## 27. M03 acceptance checklist

- [x] M02 checkpoint successful
- [x] Flutter foundation builds (Windows + Android debug APK)
- [x] FastAPI starts
- [x] PostgreSQL connectivity
- [x] Alembic tooling
- [x] Mobile health ↔ backend (e2e client + widget states + interactive success/error UI)
- [ ] Interactive Retry click **VERIFIED** — **WAIVED** by PO (D-020); must **not** be marked PASS/VERIFIED
- [x] Local quality script executed (exit 0)
- [x] Quality checks passed
- [x] Env externalized; secrets not committed
- [x] No LAN hardcoded in source defaults
- [x] Ollama not mandatory for startup
- [x] CI workflow definitions exist (hosted run pending)
- [x] Local docs/runbook
- [x] Licensing status recorded (LICENSE file still PENDING PO)
- [x] No unauthorized product features / paid services
- [x] Project Owner **ACCEPT WITH WAIVER** M03 (2026-11-25)

## 28. Recommendation for M03 acceptance

**ACCEPTED WITH WAIVER** (PO). F-M03-001 Retry Recovery remains non-PASS; future regression testing still required. F-M03-002 accepted; F-M03-003 accepted with limitations; F-M03-004 license pending; F-M03-005 static CI accepted (hosted NOT_EXECUTED).

## 29. Readiness for PH00-M04

**NO-GO** until M03 `ACCEPTED` + explicit M04 authorization. Fitness Engine / content work must not start under this report.

## 30. Final Git working tree status

After M02 commit `6ecbbaf`, M03 artifacts remain **uncommitted** by authorization. Branch ahead of origin by 2 (M01+M02). No push.

**STOP.** Awaiting Tech Lead M03 review. No M03 commit. No push. No M04.
