# Risk Register

| Field | Value |
| --- | --- |
| Last updated | 2026-11-26 |
| Owner | Engineering / Tech Lead |
| Status | Updated PH00-M04 tracker remediation (outstanding M03 verification refs) |

## Severity scale

`Low` · `Medium` · `High` · `Critical`

## Risks

| ID | Risk | Severity | Likelihood | Impact | Mitigation | Owner | Validation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-001 | AUTH drift | High | Low | High | Approved Consolidated Baseline + indexes | TL | Ongoing | Mitigated |
| R-002 | CI delay | Medium | Low | Medium | ADR-0001; workflows M03 | Eng | M03 | Mitigated (decision) |
| R-003 | Unvalidated fitness rules | Critical | Medium | Critical | Fitness Engine + expert gate; no invented thresholds | PO/Expert | M04 | Open |
| R-004 | Content licensing | High | Unknown | High | M04 assessment | PO/Legal | M04 | Open |
| R-005 | AI provider governance / paid leakage | High | Medium | High | ADR-0017 zero-cost; Ollama-only Phase 0; no paid APIs without PO | TL | M05/M08 | Mitigating |
| R-006 | Offline data loss / dup sync | Critical | Medium | Critical | ADR-0009; M06 POC | Eng | M06 | Open |
| R-007 | PG job queue inadequacy | Medium | Medium | Medium | ADR-0014; M07 POC | Eng | M07 | Open |
| R-008 | Scope creep | Medium | Medium | Medium | AGENTS + CR | TL | Ongoing | Mitigating |
| R-009 | Env drift / clean-env reproducibility gap | Low | Medium | Low | Pin M03; track OI-016 (F-M03-003 follow-up) | Eng | M03+ | Open |
| R-010 | Missing automated tests | Medium | High | Medium | M03 foundations | Eng | M03+ | Open |
| R-011 | Cursor GitLab rule conflict | Low | High | Low | D-005 | Eng | Ongoing | Mitigating |
| R-012 | M02 without baseline | Medium | Low | Medium | M01 accepted + AUTH | TL | Done | Closed |
| R-013 | ROM as commitment | High | Medium | High | D-006 pending list | PO | Ongoing | Open |
| R-014 | Provider/rules gaps block later Ms | High | Medium | High | OI register | TL/PO | M04–M08 | Open |
| R-015 | AI hallucination / unsafe plan | Critical | Medium | Critical | Hybrid AI + Fitness Engine final validation | AI/TL | M05/M08 | Open |
| R-016 | Incorrect memory / SoT override | High | Medium | High | ADR-0008; memory ≠ domain truth | AI | M05 | Open |
| R-017 | Cross-user data leakage | Critical | Low | Critical | Tool authZ; tests | Eng | M05/M08 | Open |
| R-018 | Plan version conflicts / stale apply | High | Medium | High | ADR-0010; recommendation guards | Eng | M02 design / M03+ | Mitigating |
| R-019 | AI cost overrun | High | Medium | Medium | Usage monitor; budgets | TL | M05 metrics | Open |
| R-020 | Provider availability | Medium | Medium | Medium | Fallback UX | Eng | M05 | Open |
| R-021 | Architecture complexity creep | Medium | Medium | Medium | Minimal infra; ADR discipline | TL | M02 review | Mitigating |
| R-022 | Local Ollama/Qwen capacity or capability insufficient | Medium | Medium | Medium | M05 live hybrid OK (CONDITIONAL GO Phase 0); chat latency variance remains; production bar still unmet | AI/TL | M05 | Mitigating |
| R-023 | Free-tier CI/push/notification limits; hosted Actions unrun; vuln scan pending | Medium | Medium | Medium | Document limits; OI-015 (F-M03-005 hosted NOT_EXECUTED); OI-017 vuln scan | Eng | M03+ | Open |
| R-024 | LAN Ollama outage / misconfig blocks AI POCs | Medium | Medium | Medium | Env config; health checks; deterministic fallbacks | Eng | M05 | Open |
| R-025 | Waived M03 Retry Recovery regresses unnoticed | Medium | Medium | Medium | OI-013 / F-M03-001; D-020 — not PASS; schedule regression | Eng | Post-M03 | Open |
| R-026 | Missing repository LICENSE blocks redistribution clarity | Medium | High | Medium | OI-014 / PH00-TB-011 / LICENSING_STATUS; PO decision | PO | Ongoing | Open |

## Closed

| ID | Resolution |
| --- | --- |
| R-012 | M01 accepted; AUTH present; M02 authorized after commit `dc5f9d2` |
