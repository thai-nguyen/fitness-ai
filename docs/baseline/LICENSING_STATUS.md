# Repository Licensing Status

| Field | Value |
| --- | --- |
| Status | **PENDING** — Project Owner decision required |
| Date | 2026-11-25 |
| Finding | F-M03-004 |
| Related | PH00-TB-011 |

## Decision required

The Project Owner has **not** selected a repository license.

Engineering must **not** auto-create MIT, Apache, GPL, or other open-source license files without explicit PO approval.

Existing source-code ownership is preserved until a license is chosen.

## Separated licensing concerns

| Concern | Status |
| --- | --- |
| Application source-code licensing | **PENDING** PO selection |
| Third-party dependency licensing | Track via lockfiles (`requirements.lock.txt`, `pubspec.lock`); review before distribution |
| AI model licensing (e.g. Qwen) | **PENDING** separate assessment before production (M05+) |
| Exercise content licensing | **PENDING** production (OI-005); M04 uses **original synthetic fixtures only** (see `docs/architecture/EXERCISE_SCHEMA_AND_CATALOG_M04.md`) — external datasets **not ingested** |

## PH00-TB-011 split

| Sub-item | Status |
| --- | --- |
| Document local DB access (`psql` / container-only) | **Done** — see `docs/phase-00/LOCAL_DEV_RUNBOOK.md` |
| Add repository `LICENSE` file | **Blocked** on PO license selection |

Do not mark PH00-TB-011 complete until the LICENSE acceptance criterion is satisfied.
