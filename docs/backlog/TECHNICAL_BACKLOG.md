# Technical Backlog — Phase 0

| Field | Value |
| --- | --- |
| Last updated | 2026-11-25 |
| Source | PH00-M01 assessment + remediation |
| PH00-M01 | **`ACCEPTED`** (Tech Lead 2026-11-25) |
| Authorization note | PH00-M02 GO active for TB-008/009 design only. TB-010+ remain unauthorized until later milestone GOs |
| Product feature IDs | Historical families exist in AUTH-001 (e.g. ONB/AI/TRN/WKT); technical tasks use `PH00-TB-*` only. Full product↔task traceability deferred to M09 — **do not invent** missing mappings |

## Status vocabulary

`NOT_STARTED` · `IN_PROGRESS` · `BLOCKED` · `IMPLEMENTED` · `VALIDATED` · `ACCEPTED` · `DEFERRED`

## Priority

`P0` (critical path) · `P1` · `P2`

## Tasks

### PH00-TB-001

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-001 |
| Parent milestone | PH00-M01 |
| Description | Deposit authoritative Product Plan v1.0, PO Review Response, and TIP v1.1 into `docs/baseline/authoritative/` |
| Priority | P0 |
| Dependencies | None (external input) |
| Deliverables | Three authoritative files at expected paths; baseline index updated |
| Acceptance criteria | Files present; INDEX lists Present=Yes; derived docs consistency review recorded |
| Responsible role | Project Owner / Tech Lead (deposit); Engineering (index update) |
| Required reviewer | Tech Lead |
| Status | `VALIDATED` (AUTH deposited + PO-approved 2026-11-25; see readiness report) |

### PH00-TB-002

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-002 |
| Parent milestone | PH00-M01 |
| Description | Confirm ADR-0001 (GitHub hosting + GitHub Actions + PR workflow) |
| Priority | P0 |
| Dependencies | PH00-TB-001 preferred for TIP reconciliation; not strictly required for ADR confirmation |
| Deliverables | ADR-0001 status updated by approver; decision register D-001 updated |
| Acceptance criteria | ADR-0001 `ACCEPTED` or explicitly `REJECTED` with alternate CR; no CI files created in M01 |
| Responsible role | Project Owner (confirm) / Tech Lead |
| Required reviewer | Tech Lead (+ Project Owner) |
| Status | `VALIDATED` (ADR-0001 / D-001 `ACCEPTED`; CI implementation still deferred to M03) |

### PH00-TB-003

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-003 |
| Parent milestone | PH00-M01 |
| Description | Establish repository governance via root `AGENTS.md` |
| Priority | P0 |
| Dependencies | None |
| Deliverables | `AGENTS.md` at repository root covering required governance sections |
| Acceptance criteria | File present; references SoT hierarchy; marks missing AUTH docs as pending; usable for authorized M01 work |
| Responsible role | Engineering |
| Required reviewer | Tech Lead |
| Status | `IMPLEMENTED` |

### PH00-TB-004

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-004 |
| Parent milestone | PH00-M01 |
| Description | Complete Phase 0 technical backlog with required fields and integrity validation |
| Priority | P0 |
| Dependencies | None |
| Deliverables | This backlog file; uniqueness/dependency validation evidence |
| Acceptance criteria | All tasks have required fields; no duplicate IDs; no circular deps; no unauthorized active future milestones |
| Responsible role | Engineering |
| Required reviewer | Tech Lead |
| Status | `IMPLEMENTED` |

### PH00-TB-005

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-005 |
| Parent milestone | PH00-M01 |
| Description | Validate and remediate `.gitignore` for monorepo safety |
| Priority | P0 |
| Dependencies | None |
| Deliverables | Updated `.gitignore`; `git check-ignore` evidence |
| Acceptance criteria | Secrets/caches ignored; `.env.example`, lockfiles, migrations, docs, CI paths, source not ignored |
| Responsible role | Engineering |
| Required reviewer | Tech Lead |
| Status | `IMPLEMENTED` |

### PH00-TB-006

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-006 |
| Parent milestone | PH00-M01 |
| Description | Documentation consistency validation (links, SoT, naming, statuses) |
| Priority | P1 |
| Dependencies | PH00-TB-003 |
| Deliverables | Remediation report section; docs index updates |
| Acceptance criteria | Relative links resolve; no duplicate authoritative docs; milestone status consistent; structure retained |
| Responsible role | Engineering |
| Required reviewer | Tech Lead |
| Status | `IMPLEMENTED` |

### PH00-TB-007

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-007 |
| Parent milestone | PH00-M01 |
| Description | Reconcile derived baseline documents against deposited authoritative sources |
| Priority | P0 |
| Dependencies | PH00-TB-001 |
| Deliverables | Consistency report; updated derived docs or CR list |
| Acceptance criteria | Each derived claim traced or marked conflict; F-M01-001 cleared |
| Responsible role | Engineering |
| Required reviewer | Tech Lead |
| Status | `VALIDATED` (derived docs reconciled to AUTH in final closure validation) |

### PH00-TB-008

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-008 |
| Parent milestone | PH00-M02 |
| Description | Produce system architecture, bounded contexts, domain model, lifecycles, AI architecture, data ownership, repo architecture |
| Priority | P0 |
| Dependencies | PH00-M01 `ACCEPTED`; PH00-TB-001 preferred; explicit M02 GO |
| Deliverables | Architecture docs under `docs/architecture/` + ADRs + M02 completion report |
| Acceptance criteria | Per PH00-M02 acceptance criteria in Tech Lead brief |
| Responsible role | Engineering (Architect) |
| Required reviewer | Tech Lead |
| Status | `IMPLEMENTED` (design; M02 acceptance PENDING) |

### PH00-TB-009

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-009 |
| Parent milestone | PH00-M02 |
| Description | Author remaining architecture ADRs (Flutter, modular monolith, monorepo, PostgreSQL, hybrid AI, offline, versioning, jobs, etc.) |
| Priority | P0 |
| Dependencies | PH00-TB-008 |
| Deliverables | ADR files with unique IDs; decision register updates |
| Acceptance criteria | Required ADR topics covered; statuses `PROPOSED` until approved |
| Responsible role | Engineering |
| Required reviewer | Tech Lead |
| Status | `IMPLEMENTED` (ADR-0002..0016 `PROPOSED`) |

### PH00-TB-010

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-010 |
| Parent milestone | PH00-M03 |
| Description | Bootstrap approved monorepo: Flutter app, FastAPI modular monolith, local Postgres/Alembic, testing + CI foundations, walking skeleton |
| Priority | P0 |
| Dependencies | PH00-M02 `ACCEPTED`; ADR-0001 confirmed (or alternate CI decision); PH00-TB-008 |
| Deliverables | Runnable walking skeleton; CI workflows; local-dev docs |
| Acceptance criteria | Apps boot; migrations apply; CI green on PR; no deferred infra introduced |
| Responsible role | Engineering |
| Required reviewer | Tech Lead |
| Status | `VALIDATED` (engineering evidence in PH00-M03 completion report; Tech Lead acceptance PENDING) |

### PH00-TB-010-A (subtask)

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-010-A |
| Parent | PH00-TB-010 |
| Description | Optional read-only Ollama `/api/tags` connectivity check (no generation) |
| Status | `VALIDATED` (LAN reachable; exact tag `qwen3.5:9b` present) |

### PH00-TB-011

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-011 |
| Parent milestone | PH00-M03 |
| Description | Add project LICENSE and document DB client access (`psql` or container-only) |
| Priority | P2 |
| Dependencies | PH00-TB-010 (can parallelize LICENSE with legal input) |
| Deliverables | LICENSE file; local-dev note |
| Acceptance criteria | License approved by owner; local DB access documented |
| Responsible role | Engineering (+ Legal for LICENSE) |
| Required reviewer | Tech Lead |
| Status | `IN_PROGRESS` — DB access documented in runbook; **LICENSE blocked on PO decision** (see `docs/baseline/LICENSING_STATUS.md`). Do not mark complete until LICENSE criterion is met. |

### PH00-TB-012

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-012 |
| Parent milestone | PH00-M04 |
| Description | Define exercise catalog schema, training templates, fitness constraints, deterministic validation interfaces |
| Priority | P0 |
| Dependencies | PH00-TB-008 |
| Deliverables | Schema/contracts docs; pending expert-rule list; pure-domain engine + tests |
| Acceptance criteria | Interfaces defined; expert-pending rules explicitly listed; no invented medical approvals |
| Responsible role | Engineering |
| Required reviewer | Tech Lead (+ Domain Expert for rules) |
| Status | `ACCEPTED` (technical feasibility; expert rule approval still OI-003 — not EXPERT_APPROVED) |

### PH00-TB-013

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-013 |
| Parent milestone | PH00-M04 |
| Description | Assess exercise content sources and licensing |
| Priority | P0 |
| Dependencies | None (can start analysis in M04 authorization) |
| Deliverables | Licensing assessment memo |
| Acceptance criteria | Sources listed; license risk rated; go/no-go for content use |
| Responsible role | Product Owner / Legal (+ Engineering support) |
| Required reviewer | Tech Lead / Legal |
| Status | `ACCEPTED` for M04 technical assessment (synthetic fixtures only); production content go/no-go still OI-005; app LICENSE still OI-014 |

### PH00-TB-014

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-014 |
| Parent milestone | PH00-M05 |
| Description | AI technical POCs against **Ollama/Qwen 3.5 9B** (ADR-0017): structured JSON/schema, plan generation, exercise ID grounding, tool-calling or app-controlled routing fallback, memory, cards, streaming, safety, VI/EN quality, latency/TPS/concurrency/resources, timeout recovery |
| Priority | P0 |
| Dependencies | PH00-TB-012; synthetic datasets; verified Ollama model tag/endpoint |
| Deliverables | Ollama adapter POC; measurement evidence (no fabrication); limitation report if gaps |
| Acceptance criteria | Real measurements; no paid AI APIs; LLM cannot mutate DB; safety eval executed; zero-cost alts considered before any paid proposal |
| Responsible role | Engineering (AI Systems) |
| Required reviewer | Tech Lead |
| Status | `VALIDATED` (engineering evidence in PH00-M05 completion report; Tech Lead acceptance PENDING) |

### PH00-TB-015

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-015 |
| Parent milestone | PH00-M06 |
| Description | Offline workout POC: local persistence, pending events, restart recovery, sync, idempotency, duplicates, account isolation, conflicts |
| Priority | P0 |
| Dependencies | PH00-TB-010; workout lifecycle from PH00-TB-008 |
| Deliverables | POC + tests demonstrating sync invariants |
| Acceptance criteria | Business state vs sync state separated; idempotency proven; conflict cases covered |
| Responsible role | Engineering (Mobile) |
| Required reviewer | Tech Lead |
| Status | `NOT_STARTED` |

### PH00-TB-016

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-016 |
| Parent milestone | PH00-M07 |
| Description | PostgreSQL-backed background job reliability POC |
| Priority | P1 |
| Dependencies | PH00-TB-010 |
| Deliverables | POC + concurrent worker tests |
| Acceptance criteria | Claim/lease/retry/cancel/crash recovery evidenced; Celery/Redis still deferred unless CR |
| Responsible role | Engineering (Backend) |
| Required reviewer | Tech Lead |
| Status | `NOT_STARTED` |

### PH00-TB-017

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-017 |
| Parent milestone | PH00-M08 |
| Description | Security, privacy, consent, deletion, AI provider governance, analytics privacy, evaluation dataset, acceptance criteria |
| Priority | P0 |
| Dependencies | PH00-TB-008; PH00-TB-014 findings |
| Deliverables | Threat model; data classification; policies; eval dataset |
| Acceptance criteria | Criteria reviewable; sensitive boundaries clear; provider governance documented |
| Responsible role | Engineering (+ Privacy/Legal as needed) |
| Required reviewer | Tech Lead |
| Status | `NOT_STARTED` |

### PH00-TB-018

| Field | Value |
| --- | --- |
| Task ID | PH00-TB-018 |
| Parent milestone | PH00-M09 |
| Description | Phase 0 exit review: evidence pack, ADR updates, risks, backlog, traceability, re-estimate, Go/No-Go |
| Priority | P0 |
| Dependencies | PH00-TB-008 through PH00-TB-017 completed, validated, or explicitly deferred |
| Deliverables | Exit review report + formal recommendation |
| Acceptance criteria | Evidence-based; unresolved blockers listed; no fabricated results |
| Responsible role | Engineering |
| Required reviewer | Tech Lead (+ Product Owner for product Go/No-Go) |
| Status | `NOT_STARTED` |

## Dependency graph (acyclic)

```text
PH00-TB-001 → PH00-TB-007
PH00-TB-003 → PH00-TB-006
PH00-TB-001 (preferred) → PH00-TB-002
PH00-M01 ACCEPTED + M02 GO → PH00-TB-008 → PH00-TB-009
PH00-TB-008 → PH00-TB-012
PH00-TB-008 → PH00-TB-010 → PH00-TB-015
PH00-TB-010 → PH00-TB-016
PH00-TB-012 → PH00-TB-014
PH00-TB-008 + PH00-TB-014 → PH00-TB-017
PH00-TB-008..017 → PH00-TB-018
```

## Integrity notes

- Task IDs are unique (`PH00-TB-001` … `PH00-TB-018`).
- No circular dependencies in the graph above.
- Only M01 tasks may be `IN_PROGRESS` / `IMPLEMENTED` / `BLOCKED` under current authorization.
- M02–M09 tasks remain `NOT_STARTED` (not authorized).
- No Product Owner feature IDs invented.
