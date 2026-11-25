# PH00-M01 — Repository Assessment

| Field | Value |
| --- | --- |
| Assessment date | 2026-11-25 |
| Assessor | Engineering (under Tech Lead supervision) |
| Repository path | `D:\Project\fitness-ai` |
| Status | `VALIDATED` |

## 1. Executive finding

The repository is a **greenfield** project. Prior to M01 deliverables it contained a single tracked file (`.gitignore`) and one commit. No application code, architecture docs, CI, or ADRs existed. Phase 0 discovery documentation can be established without migration debt.

## 2. Version control

| Check | Result |
| --- | --- |
| Git repository | Yes |
| Branch | `main` |
| Upstream | `origin/main` (`https://github.com/thai-nguyen/fitness-ai.git`) |
| Commit history | `3fe03eb` — Initial commit (2026-11-25) by Nguyễn Đức Thái |
| Pre-M01 tracked files | `.gitignore` only |
| Working tree before M01 docs | Clean except subsequent M01 documentation work |

## 3. Pre-existing files and configurations

### 3.1 `.gitignore` (pre-M01)

- Content is a **Flutter engine / Flutter repository contributor** style ignore list (references `/bin/cache/`, `/packages/flutter/`, `/dev/bots/`, etc.).
- Suitable for contributing to the Flutter SDK; **not** well-aligned with an application monorepo (Python, Docker, `.env`, IDE, coverage for backend).
- M01 action: replace with an application-monorepo-oriented ignore file covering Flutter apps, Python, Docker, secrets, and IDE artifacts (reversible baseline hygiene).

### 3.2 Missing expected project artifacts

| Artifact | Present? |
| --- | --- |
| `README.md` | No (created in M01) |
| `docs/` | No (created in M01) |
| TIP v1.1 | No |
| ADRs | No |
| `apps/` / `backend/` / `mobile/` / packages | No |
| `docker-compose` / Dockerfiles | No |
| `.gitlab-ci.yml` | No |
| GitHub Actions workflows | No |
| `AGENTS.md` / Cursor rules in repo | No |
| `pyproject.toml` / `pubspec.yaml` | No |
| Tests | No |
| LICENSE | No |

## 4. Skills, instructions, and external conventions

| Source | Observation |
| --- | --- |
| In-repo agent instructions | None |
| Workspace Cursor rule (external) | GitLab workflow conventions plugin rule (`conventional commits`, GitLab issue refs, MR preferences) is active in the Cursor environment but **not** stored in this repository |
| Conflict signal | Approved CI is **GitLab CI**, remote is **GitHub**, workspace assistant rule assumes GitLab workflow |

## 5. Architecture decisions found in repository

None. No ADR directory, architecture markdown, or code that implies architecture.

Direction for Phase 0 is taken from the authorized Tech Lead / PO brief (TIP v1.1 alignment) and recorded under `docs/baseline/`.

## 6. Conflicts, gaps, and duplication

### Conflicts / misalignments

| ID | Description | Impact | Recommendation |
| --- | --- | --- | --- |
| C-001 | Remote hosting is GitHub; approved CI is GitLab CI | CI bootstrap in M03 ambiguous | **Superseded 2026-11-25:** ADR-0001 / D-001 `ACCEPTED` (GitHub + GitHub Actions + PRs). Historical finding retained. |
| C-002 | Cursor workspace GitLab workflow rule vs GitHub remote | Commit/MR workflow guidance may not match hosting | Tracked as OI-006; handled under D-005 constraints (report conflicts; do not modify global Cursor rules) |
| C-003 | Pre-M01 `.gitignore` targets Flutter SDK layout | Noise / missed ignores for Python secrets | Fixed in M01 baseline hygiene |

### Missing information

| ID | Description | Blocks |
| --- | --- | --- |
| G-001 | Canonical TIP v1.1 file not in repo | Precise requirement traceability (soft-blocks M02 polish; hard for M09) |
| G-002 | No prescribed monorepo directory names in brief | M03 bootstrap plan |
| G-003 | AI provider shortlist / credentials policy unspecified | M05 / M08 |
| G-004 | Exercise content source and licensing unspecified | M04 |
| G-005 | No LICENSE / org legal defaults | Distribution / content reuse |
| G-006 | Target Flutter / Python version pins not formally approved | M03 (local observation only for now) |

### Duplication

None detected (insufficient prior documentation to duplicate).

## 7. Local developer environment (observation only)

| Tool | Observed |
| --- | --- |
| OS | Windows 10 (build 19045) |
| Python | 3.12.10 |
| Flutter | 3.47.2 stable / Dart 3.13.2 |
| Docker | 29.9.2 |
| `psql` | Not on PATH |
| `gh` | Not installed |

These observations do **not** pin project versions. Version pins are an M03 decision under Tech Lead approval.

## 8. Security & privacy observations

- No secrets, `.env`, or credential files found
- No user/health data present
- Public/private visibility of GitHub remote not verified (`gh` unavailable); treat as potentially sensitive once code lands
- Recommendation: ensure remote visibility and secret scanning before any real credentials or provider keys are introduced (M03+)

## 9. Assessment conclusion

| Question | Answer |
| --- | --- |
| Safe to document baseline? | Yes |
| Safe to begin M02 after acceptance? | Yes, with G-001 preferred resolved |
| Safe to begin production features? | No (authorization NO-GO) |
| Migration / cleanup debt? | Minimal (gitignore only) |

**Recommendation:** Accept M01 after Tech Lead review, deposit TIP v1.1, resolve hosting/CI (C-001), then authorize PH00-M02.
