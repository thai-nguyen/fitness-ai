# Risk Register

| Field | Value |
| --- | --- |
| Last updated | 2026-11-25 |
| Owner | Engineering / Tech Lead |
| Status | Updated during PH00-M01 remediation |

## Severity scale

`Low` · `Medium` · `High` · `Critical`

## Risks

| ID | Risk | Severity | Likelihood | Impact | Mitigation / next step | Status | Target |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-001 | TIP / Product Plan / PO Review not in repo → requirement drift | High | Low | High | Consolidated Baseline deposited + PO-approved 2026-11-25; derived docs reconciled | Mitigated | Monitor AUTH vs derived drift |
| R-002 | Hosting/CI mismatch delays foundation | Medium | Low | Medium | ADR-0001 / D-001 `ACCEPTED`; implement Actions in M03 only | Mitigated (decision); implementation pending M03 | M03 |
| R-003 | Fitness business rules lack domain expert approval | High | Medium | High | Gate M04 rule acceptance | Open | M04 |
| R-004 | Exercise content licensing blocks catalog | High | Unknown | High | M04 licensing assessment | Open | M04 |
| R-005 | AI provider data governance unsuitable | High | Medium | High | M05/M08 assessment; synthetic-only POCs | Open | M05/M08 |
| R-006 | Offline sync complexity underestimated | High | Medium | High | M06 POC | Open | M06 |
| R-007 | PG-backed jobs insufficient vs Celery/Redis | Medium | Medium | Medium | M07 POC; CR only if evidenced | Open | M07 |
| R-008 | Scope creep during discovery | Medium | Medium | Medium | Milestone authorization + CR process + AGENTS.md | Mitigating | Ongoing |
| R-009 | Missing version pins cause environment drift | Low | Medium | Low | Pin in M03 | Open | M03 |
| R-010 | No automated tests yet | Medium | High | Medium | Testing foundations in M03 | Open | M03+ |
| R-011 | External GitLab Cursor rule conflicts with GitHub workflow | Low | High | Low | AGENTS.md §16; OI-006; do not edit global rules | Mitigating | Ongoing |
| R-012 | M02 started without AUTH docs increases rework | Medium | Low | Medium | AUTH deposited; keep M02 NO-GO until M01 `ACCEPTED` + explicit GO | Mitigating | Pre-M02 |
| R-013 | Baseline ROM (FTE/budget/dates) treated as commitments | High | Medium | High | D-006 explicitly keeps pending assumptions pending | Open | Ongoing |
| R-014 | Fitness rules / licensing / provider gaps block M04–M08 | High | Medium | High | OI-003..005, OI-009 | Open | M04–M08 |

## Closed risks

_None._
