# PH00-M03 Remediation Report

| Field | Value |
| --- | --- |
| Milestone | PH00-M03 — Engineering Foundation (remediation) |
| Date | 2026-11-25 |
| Prior review | **PASS WITH CONDITIONS** |
| Author | Engineering |
| Reviewer | Tech Lead |
| M02 checkpoint | `6ecbbaf4b24c0704c458290076f1b67086bbde53` (HEAD unchanged) |
| M03 commit | **NOT AUTHORIZED** / not performed |
| Push | **NO-GO** |
| M04 | **NO-GO** |

---

## 1. Executive summary

Focused remediation for F-M03-001..005. Local quality script fixed and executed (**exit 0**). Dependency/CI/licensing reviews completed without inventing a license. Interactive Windows Flutter runtime **partially validated** with PrintWindow UI captures for **success** and **unavailable** states plus live backend request logs; **in-window Retry click via injected input was not confirmed**. F-M03-001 remains **PENDING** human Retry confirmation per directive. M03 not self-accepted.

## 2. Finding-by-finding resolution

### F-M03-001 — Interactive Flutter runtime (MEDIUM) — **PARTIAL / PENDING**

| Item | Result |
| --- | --- |
| Preconditions (PG :15432 healthy, API :8080 live/ready) | **Met** |
| `flutter run -d windows --dart-define=API_BASE_URL=http://127.0.0.1:8080` | **Executed** — synced; VM service up |
| App starts / health route / DI / Cubit | **Observed** via UI capture + logs |
| Real FastAPI call | **Observed** — uvicorn `GET /health/ready 200` |
| Service/version/DB displayed | **Observed** — PrintWindow `health-ui-success.png` |
| Backend unavailable UI | **Observed** — `health-ui-error.png` (Status unavailable / Backend unreachable) |
| Retry restores success (interactive click) | **NOT CONFIRMED** — injected mouse clicks did not register on Flutter Windows controls |
| Unhandled exceptions | None observed in flutter-run logs |
| Readiness HTTP 503 when project Postgres stopped | **Executed** — `ready_ex_status=503`; Postgres restored healthy |

**F-M03-001 status: PENDING** until Project Owner/Tech Lead confirms interactive Retry (instructions in §3).

### F-M03-002 — Local quality script (MEDIUM) — **RESOLVED**

Fixed PowerShell native exit-code handling (`Invoke-Native` + `$LASTEXITCODE`). Executed successfully: **exit 0**. Negative probe confirmed non-zero failure path throws.

### F-M03-003 — Dependency reproducibility (LOW) — **RESOLVED (review)**

Lockfiles free of machine-specific absolute paths. Versions align with `pyproject.toml` / `pubspec.yaml`. CI install strategy compatible (`pip install -e ".[dev]"`, `flutter pub get`). No paid deps. No blanket upgrades. Vulnerability scanners not run (limitation).

### F-M03-004 — Repository LICENSE (LOW) — **RESOLVED (status recorded)**

No license invented. [`docs/baseline/LICENSING_STATUS.md`](../baseline/LICENSING_STATUS.md) records PENDING PO decision. PH00-TB-011 remains `IN_PROGRESS` (DB docs done; LICENSE blocked).

### F-M03-005 — GitHub Actions static validation (LOW) — **RESOLVED**

YAML parses (`yaml.safe_load` OK). Triggers, `contents: read`, free runners, Postgres service, no LAN/Ollama/deploy/secrets. Hosted execution **NOT_EXECUTED**.

## 3. Interactive runtime evidence

### Commands

```text
flutter run -d windows --dart-define=API_BASE_URL=http://127.0.0.1:8080
# also: direct exe apps/mobile/build/windows/x64/runner/Debug/fitness_ai_mobile.exe
```

### Artifacts (`scripts/runtime-evidence/`)

| File | Content |
| --- | --- |
| `flutter-run2.log` | Build OK, Syncing OK, Flutter run key commands, VM service URL |
| `health-ui-success.png` | Fitness AI; Status ready; service fitness-ai-backend; version 0.1.0; Database up; timestamp; Retry |
| `health-ui-error.png` | Status unavailable (red); Backend unreachable; Retry |
| `uvicorn.out.log` | Multiple `GET /health/ready` 200 from app |

### Manual verification instructions (for F-M03-001 close-out)

1. Ensure Postgres: `docker compose -f infrastructure/docker-compose.yml ps` → healthy on `127.0.0.1:15432`.
2. Start backend: see runbook (port **8080**).
3. Run: `cd apps/mobile` then
   `flutter run -d windows --dart-define=API_BASE_URL=http://127.0.0.1:8080`
4. Confirm UI shows **ready** / **fitness-ai-backend** / **0.1.0** / **Database: up**.
5. Stop **only** the fitness-ai uvicorn process (do not stop unrelated services).
6. Click **Retry** → expect **unavailable** / Backend unreachable.
7. Restart uvicorn; click **Retry** → expect success restored.
8. Optional: `docker compose -f infrastructure/docker-compose.yml stop postgres` → `GET /health/ready` returns **503**; `start postgres` restores ready.

Report confirmation to Tech Lead to clear F-M03-001.

## 4. Local quality script execution evidence

```text
Command: powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\local_quality.ps1
Exit code: 0

Included:
  ruff check / ruff format --check / pytest (9 passed)
  flutter pub get / dart format / flutter analyze / flutter test --exclude-tags e2e (6 passed)
  docker compose config

Not included in script (separate):
  flutter run interactive, --tags e2e, alembic, Ollama
```

Native failure handling probe: `Invoke-Native { cmd /c exit 7 }` → caught `FAILED (7)` (exit 2).

## 5. Dependency reproducibility review

| Check | Result |
| --- | --- |
| Absolute paths in locks | **None found** |
| Python | 3.12 documented; CI `3.12` |
| Flutter | 3.47.2 documented; CI flutter-action `3.47.2` |
| Backend pins | Match lock (FastAPI 0.115.6, SQLAlchemy 2.0.36, …) |
| Mobile pins | pubspec.lock present |
| Paid deps | None |
| Vuln scan | **Not executed** (limitation) |

## 6. Repository licensing status

**PENDING** PO selection. See `LICENSING_STATUS.md`. Application / dependency / model / exercise content licensing separated. No LICENSE file created.

## 7. CI static validation

| Check | Result |
| --- | --- |
| YAML structure | Valid |
| Permissions | `contents: read` |
| Runners | `ubuntu-latest` (free) |
| Postgres service | `postgres:16.6-alpine` |
| LAN / Ollama | Absent |
| Deploy / secrets / paid | Absent |
| Hosted run | **NOT_EXECUTED** |

## 8. Commands and actual results (remediation pass)

| Check | Result | New vs reused |
| --- | --- | --- |
| HEAD = M02 | `6ecbbaf…` | New confirm |
| PG healthy :15432 | healthy | New |
| `/health/live` `/health/ready` | 200 ready | New |
| Interactive flutter run | Synced; UI success capture | **New** |
| Unavailable UI capture | error PNG | **New** |
| Retry click interactive | Not confirmed | **New gap** |
| DB stop → ready 503 | 503 then restored | **New** |
| `local_quality.ps1` | exit 0 | **New** |
| Alembic current | `20261125_0001 (head)` | New |
| Secret heuristic | Doc/test LAN refs only (7 hits) | New |
| flutter analyze/tests | via quality script | New |
| Windows/APK builds | Prior M03 evidence | Reused |

## 9. Files modified

| Path | Change |
| --- | --- |
| `scripts/local_quality.ps1` | Native exit-code handling |
| `docs/baseline/LICENSING_STATUS.md` | **Created** |
| `docs/phase-00/PH00-M03-remediation-report.md` | **Created** (this file) |
| `docs/phase-00/PH00-M03-completion-report.md` | Remediation ref; checklist corrected |
| `docs/backlog/TECHNICAL_BACKLOG.md` | TB-011 clarification |
| `.gitignore` | runtime-evidence `*.log` |
| `scripts/runtime-evidence/*` | Local evidence (logs ignored; PNGs local) |

## 10. Remaining limitations and risks

- F-M03-001 Retry click not agent-confirmed on Windows Flutter
- Hosted CI not executed
- Dependency vulnerability scan not run
- LICENSE still PENDING
- Multi-monitor desktop made compositor screenshots unreliable; PrintWindow used instead

## 11. Updated backlog statuses

| ID | Status |
| --- | --- |
| PH00-TB-010 | `VALIDATED` (acceptance still PENDING Tech Lead) |
| PH00-TB-011 | `IN_PROGRESS` — DB docs done; LICENSE blocked on PO |
| PH00-TB-012+ | Unchanged / NO-GO |

## 12. M03 acceptance readiness

| Gate | Status |
| --- | --- |
| Quality script | Pass (exit 0) |
| Deps / CI static / licensing record | Pass |
| Interactive runtime | **Partial** — success + unavailable verified; **Retry pending human** |
| Recommend acceptance | **Conditional** — accept after F-M03-001 Retry confirmation (manual steps §3), or accept with explicit waiver of Retry interactive evidence |

Engineering does **not** mark M03 `ACCEPTED`.

## 13. Final Git working tree status

```text
HEAD: 6ecbbaf4b24c0704c458290076f1b67086bbde53 (M02)
Branch: main ahead of origin by 2
M03 files: uncommitted (authorized)
No M03 commit. No push.
```

**STOP.** Submit for Tech Lead final review.
