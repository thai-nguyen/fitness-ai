# Open Issues Register

| Field | Value |
| --- | --- |
| Last updated | 2026-11-26 |
| Milestone | PH00-M04 (includes M03 outstanding verification tracking) |

## Status values

`OPEN` · `BLOCKED` · `IN_PROGRESS` · `RESOLVED` · `DEFERRED`

## Issues

| ID | Title | Severity | Status | Related | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| OI-003 | Domain expert unavailable for fitness rule sign-off | High | `OPEN` | M04 | Product Owner | Identify expert before M04 acceptance |
| OI-004 | Local model suitability / production AI readiness (Ollama/Qwen) + governance | High | `OPEN` | ADR-0017; M05 / M08 | Tech Lead | Run M05 matrix; production hosting still pending |
| OI-005 | Exercise content licensing undecided | High | `OPEN` | M04 | PO / Legal | Licensing assessment |
| OI-006 | External Cursor GitLab workflow rule vs GitHub PR workflow | Medium | `OPEN` | D-005 / ADR-0001 | Tech Lead / Engineering | Report-only under D-005 constraints |
| OI-008 | Staffing / budget / timeline ROM not approved | Medium | `OPEN` | AUTH-003 §8 | PO / Sponsor | Keep pending; re-estimate after POCs |
| OI-009 | Managed auth provider not selected | Medium | `OPEN` | AUTH-003 | Tech Lead | Feasibility POC |
| OI-010 | PG durable job queue feasibility unproven | Medium | `OPEN` | M07 / D-003 | Tech Lead | M07 POC |
| OI-011 | Nutrition Lite inclusion undecided | Medium | `OPEN` | AUTH-001/002 | PO | Spike only; post-alpha decision |
| OI-012 | Target market / regulatory assumptions unverified | Medium | `OPEN` | AUTH-001 | PO | Research |
| OI-013 | M03 interactive Retry Recovery verification outstanding | Medium | `OPEN` | F-M03-001; D-020; CR-20261125-B | Eng / PO | Future regression; must not be marked PASS/VERIFIED |
| OI-014 | Repository LICENSE pending owner decision | Medium | `OPEN` | F-M03-004; PH00-TB-011; `LICENSING_STATUS.md` | PO | Select license; do not invent LICENSE file |
| OI-015 | Hosted GitHub Actions execution not performed | Low | `OPEN` | F-M03-005; ADR-0001 | Eng | Run hosted workflow when push authorized |
| OI-016 | Clean-environment dependency reproducibility follow-up | Low | `OPEN` | F-M03-003; R-009 | Eng | Re-verify from clean checkout / fresh venv |
| OI-017 | Dependency vulnerability scanning pending | Low | `OPEN` | M03 remediation outstanding; R-023 | Eng | Run free local/OSS scan before production gate |

## Resolved

| ID | Title | Resolution | Date |
| --- | --- | --- | --- |
| OI-001 | Consolidated Baseline deposits missing | Four files deposited + PO approval 2026-11-25; consistency validation passed in final readiness report | 2026-11-25 |
| OI-002 | GitHub vs GitLab CI | ADR-0001 / D-001 `ACCEPTED` | 2026-11-25 |
| OI-007 | Derived vs AUTH consistency unverified | Reconciled during PH00-M01 final closure validation | 2026-11-25 |
