# PH00-M02 Remediation Report

| Field | Value |
| --- | --- |
| Milestone | PH00-M02 — Architecture & Domain Modelling (remediation) |
| Date | 2026-11-25 |
| Author | Engineering (Architect) |
| Reviewer | Tech Lead |
| Prior review | **PASS WITH CONDITIONS** |
| This deliverable | Focused remediation of F-M02-001..006 |
| M02 status | Remediation complete — milestone **`ACCEPTED`** (Tech Lead 2026-11-25) |
| Findings F-M02-001..006 | **`ACCEPTED`** |
| M02 commit | Authorized after validation (Part A closure) |
| Push | **NO-GO** |
| M03 | **GO** after successful M02 checkpoint |
| M01 checkpoint | Preserved — `dc5f9d2ece2875b41f4822f1a037897d259aaffc` |

---

## 1. Executive summary

Conditional findings F-M02-001 through F-M02-006 are addressed with documentation-only changes. **Actual ADR file count is 17** (ADR-0001..0017), including ADR-0017 `ACCEPTED`. Product architecture coverage clarifies that Product Plan `AUTH-*` means the **Authentication feature family**, not baseline document IDs. Content-level secret heuristics found **documentation-only** LAN endpoint references (no application/runtime config; no apps exist). Mermaid diagrams were reviewed manually; automated render unavailable. Zero-cost local vs production boundaries are explicit. ADR readiness classifies each ADR as A/B/C for Tech Lead approval before M03. **M02 is not marked ACCEPTED.** No commit, push, bootstrap, paid services, or AI/model execution.

---

## 2. Finding-by-finding resolution

### F-M02-001 — ADR validation consistency (MEDIUM) — **RESOLVED**

| Check | Result |
| --- | --- |
| Enumerate ADR files | 17 files `docs/adr/NNNN-*.md` |
| Unique IDs | 17 unique (`0001`–`0017`) |
| ADR-0017 present | **Yes** — `0017-zero-cost-local-ai-ollama.md` |
| ADR register | `docs/adr/README.md` lists 0001–0017; ACCEPTED = 0001, 0017 |
| D-010 / D-011 | Present `ACCEPTED` in `DECISION_REGISTER.md` with PO evidence |
| CR-20261125 | Present `docs/change-requests/CR-20261125-zero-cost-local-ai.md` |
| Document links | Relative MD link check: **0 broken** (78 checked) |
| Stale evidence | Completion report validation appendix corrected (was “16”; actual **17**) |

**Root cause of stale “16”:** inventory used a glob that missed `0010`–`0017` style matches in an earlier pass; re-enumeration with `????-*.md` yields **17**.

### F-M02-002 — Product architecture coverage (MEDIUM) — **RESOLVED**

| Clarification | |
| --- | --- |
| Baseline `AUTH-001..004` | Authoritative **documents** under `docs/baseline/authoritative/` |
| Product Plan `AUTH-001–006` | **Authentication feature family** |

Updated [`TRACEABILITY_MATRIX.md`](../architecture/TRACEABILITY_MATRIX.md) with Core MVP P0 coverage rows (family, priority, context, component, tech task, milestone, status, dependency). Full user-story mapping remains deferred to **M09**. No invented product feature IDs.

**Ambiguities called out:** minimal admin subset (Partial); analytics without dedicated Product Plan family ID (mapped under Platform without inventing IDs).

### F-M02-003 — Secret and configuration validation (MEDIUM) — **RESOLVED (heuristic)**

Content-level heuristic scan of tracked/untracked text-like files (see §8). **No** API keys, tokens, passwords, private keys, or credentialed connection strings detected. **Two** hits: documented Ollama LAN example host in ADR-0017 and AI_ARCHITECTURE — labeled ops-docs-only; **not** application source or committed runtime config (no apps/config files exist). Prefer env vars (`OLLAMA_BASE_URL`, `OLLAMA_MODEL`) — reiterated in boundaries doc. **Not** a comprehensive security audit.

### F-M02-004 — Mermaid review (LOW) — **RESOLVED (manual)**

Manual review of **14** Mermaid blocks under `docs/architecture/` (+ 1 new in ZERO_COST_DEPLOYMENT_BOUNDARIES). See §9. Automated rendering not available — limitation recorded. No paid tools added.

### F-M02-005 — Zero-cost deployment boundaries (MEDIUM) — **RESOLVED**

New [`ZERO_COST_DEPLOYMENT_BOUNDARIES.md`](../architecture/ZERO_COST_DEPLOYMENT_BOUNDARIES.md); linked from system architecture. Local vs production PENDING topics documented; backend-only Ollama; no paid fallback; offline independence; CI cannot assume LAN access. No AI integration or benchmarks executed.

### F-M02-006 — ADR readiness for M03 (MEDIUM) — **RESOLVED (recommendation)**

New [`ADR_READINESS_FOR_M03.md`](../architecture/ADR_READINESS_FOR_M03.md). ADR-0001 and ADR-0017 preserved `ACCEPTED`. Proposed ADRs **not** auto-accepted. Classification A/B/C + M03 block flags submitted for Tech Lead.

---

## 3. Evidence and validation commands

Executed on Windows PowerShell from repo root `D:\Project\fitness-ai` (2026-11-25).

```powershell
# ADR inventory
Get-ChildItem docs\adr\????-*.md | Sort-Object Name
# ACTUAL_COUNT=17 UNIQUE=17 HAS_0017=True

git rev-parse HEAD
# dc5f9d2ece2875b41f4822f1a037897d259aaffc
git merge-base --is-ancestor dc5f9d2ece2875b41f4822f1a037897d259aaffc HEAD
# exit 0
git status -sb
# main...origin/main [ahead 1]; M02 docs modified/untracked — not committed

# Backlog uniqueness across docs/**/*.md
# UNIQUE_COUNT=18 (PH00-TB-001 .. PH00-TB-018)

# Relative Markdown links under docs/
# CHECKED=78 BROKEN=0

# Secret heuristic (pattern for keys/tokens/passwords/private keys/credential URLs/LAN:11434)
# SCAN_FILES=59 HIT_COUNT=2 (doc-only LAN references; values not printed here beyond file:line)

# Unauthorized implementation
# apps/backend/services/.github/workflows → absent
```

Decision/CR spot-check: D-010, D-011 `ACCEPTED`; CR-20261125 present; ADR-0017 links D-010/D-011.

---

## 4. Actual ADR inventory

| # | File | Status (file/register) |
| --- | --- | --- |
| 1 | `0001-github-hosting-and-github-actions.md` | `ACCEPTED` |
| 2 | `0002-modular-monolith.md` | `PROPOSED` |
| 3 | `0003-monorepo.md` | `PROPOSED` |
| 4 | `0004-flutter-clean-architecture.md` | `PROPOSED` |
| 5 | `0005-postgresql.md` | `PROPOSED` |
| 6 | `0006-hybrid-ai.md` | `PROPOSED` |
| 7 | `0007-fitness-engine.md` | `PROPOSED` |
| 8 | `0008-structured-memory.md` | `PROPOSED` |
| 9 | `0009-offline-first-workout.md` | `PROPOSED` |
| 10 | `0010-immutable-plan-versions.md` | `PROPOSED` |
| 11 | `0011-limited-outbox.md` | `PROPOSED` |
| 12 | `0012-ai-provider-abstraction.md` | `PROPOSED` |
| 13 | `0013-managed-authentication.md` | `PROPOSED` |
| 14 | `0014-postgresql-job-queue.md` | `PROPOSED` (M07 evidence) |
| 15 | `0015-health-data-governance.md` | `PROPOSED` |
| 16 | `0016-ai-evaluation.md` | `PROPOSED` |
| 17 | `0017-zero-cost-local-ai-ollama.md` | `ACCEPTED` |

**Actual count: 17. Unique IDs: 17. Gaps in numbering: none.**

---

## 5. ADR readiness classification

Summary (full table in [`ADR_READINESS_FOR_M03.md`](../architecture/ADR_READINESS_FOR_M03.md)):

| Class | ADRs | Meaning |
| --- | --- | --- |
| **A** | 0001, 0017 | Approved baseline / PO — keep `ACCEPTED` |
| **B** | 0002, 0003, 0004, 0005 (+ soft 0009, 0010, 0012) | TL decision recommended before M03 layout/skeleton |
| **C** | 0006 detail beyond 0017, 0007, 0008, 0011, 0013–0016 | POC/business validation; do not auto-accept |

**Does not block M03 skeleton if TL accepts B-set direction:** 0007–0008, 0011, 0014–0016. Auth vendor (0013) can use stub/dev auth for skeleton.

---

## 6. Core MVP architecture coverage

See [`TRACEABILITY_MATRIX.md`](../architecture/TRACEABILITY_MATRIX.md). Covered P0 families: Authentication, Onboarding, Exercise library, Training, Workout/offline, AI Coach, Recovery feedback, Progress, Notifications, Ops/privacy; Admin and analytics marked **Partial** with open clarifications. Nutrition Lite / entitlement / progressive overload remain non-P0.

---

## 7. Zero-cost deployment boundaries

Documented in [`ZERO_COST_DEPLOYMENT_BOUNDARIES.md`](../architecture/ZERO_COST_DEPLOYMENT_BOUNDARIES.md):

- **Local:** Flutter, FastAPI, PostgreSQL, Ollama LAN, Qwen 3.5 9B POC, local secrets/env, optional worker — no paid cloud.
- **Production:** hosting, capacity, security/availability, ops cost, model suitability — all **PENDING**.
- Backend-only Ollama; configurable endpoint/model; timeouts/failures without paid fallback; offline workouts independent of AI; synthetic early POC data; no assumption GitHub-hosted runners reach private LAN.

---

## 8. Secret scan scope and limitations

| Item | Detail |
| --- | --- |
| Scope | Recursive text-like files under repo (extensions: md, py, dart, yml/yaml, env, toml, json, ts/js, sh, ps1, txt, ini, cfg); excluded `.git` |
| File count | **59** |
| Method | PowerShell regex heuristic for keys, tokens, passwords, private key headers, credentialed DB URLs, common cloud key prefixes, LAN host/`11434` |
| Hits | **2** — `docs/adr/0017-...md` L15; `docs/architecture/AI_ARCHITECTURE.md` L73 — **documentation** LAN URL examples |
| Application/runtime config | None present (no apps, no committed `.env`) |
| Limitations | Heuristic only; does not decode binaries, history blobs, or cloud secret stores; not a penetration test or full secret-scanning product |
| Claim | **Not** a comprehensive security audit |

Secret **values** are not reproduced in this report beyond file/line pointers.

---

## 9. Mermaid review results

| Document | Diagrams | Manual findings |
| --- | --- | --- |
| SYSTEM_ARCHITECTURE | C4Context, C4Container, flowchart modules, sequence | Syntax OK for Mermaid+C4; **C4 may not render** without C4 plugin — limitation. Module edges acyclic (Coaching→Engine/Training only). |
| BOUNDED_CONTEXTS | flowchart TB context map | Acyclic; matches narrative “no cycles”. |
| DOMAIN_MODEL | erDiagram | Consistent with aggregates; relationships readable. |
| DOMAIN_LIFECYCLES | 3× stateDiagram-v2 | Transitions match tables; business≠sync preserved (sync described in prose, not mixed into workout business chart). |
| AI_ARCHITECTURE | flowchart Ollama boundary; 2× sequence | Backend-only path correct; env-config note present. |
| OFFLINE_SYNC | sequence | Matches sync protocol section. |
| ZERO_COST_DEPLOYMENT_BOUNDARIES | flowchart local+LAN | Aligns with ADR-0017. |

**Automated rendering:** not executed (no Mermaid CLI/CI renderer installed; paid tools disallowed). Manual review only.

**Minor non-blocking note:** SYSTEM_ARCHITECTURE C4 diagrams depend on Mermaid C4 support in the viewer; if unsupported, treat as conceptual and keep flowchart/sequence as primary readable diagrams.

---

## 10. Files modified (remediation + prior M02 working tree)

### Created / updated in this remediation pass

| Path | Change |
| --- | --- |
| `docs/phase-00/PH00-M02-remediation-report.md` | **Created** (this report) |
| `docs/architecture/TRACEABILITY_MATRIX.md` | Coverage matrix + AUTH glossary |
| `docs/architecture/ZERO_COST_DEPLOYMENT_BOUNDARIES.md` | **Created** |
| `docs/architecture/ADR_READINESS_FOR_M03.md` | **Created** |
| `docs/architecture/README.md` | Index + remediation link |
| `docs/architecture/SYSTEM_ARCHITECTURE.md` | Link to deployment boundaries |
| `docs/phase-00/PH00-M02-completion-report.md` | Remediation reference + corrected validation |

### Broader uncommitted M02 design set (unchanged intent; still not committed)

Architecture pack, ADR-0002..0017, CR-20261125, trackers/AGENTS/risks/decisions — see `git status`. **No M02 commit.**

---

## 11. Remaining blockers and risks

| Item | Severity | Notes |
| --- | --- | --- |
| M02 Tech Lead final acceptance | Gate | Required before M03 |
| TL accept/amend B-class ADRs (0002–0005…) | Medium | Recommended before foundation layout |
| Qwen/Ollama suitability | Medium | M05; R-022 class |
| Auth vendor (prefer zero-cost) | Medium | ADR-0013; stub OK for early M03 |
| PG job queue feasibility | Medium | M07; ADR-0014 |
| Multi-device offline conflict | Medium | M06 OPEN |
| Production hosting/cost | Medium | PENDING; paid needs PO |
| Minimal admin / analytics ID clarity | Low | Partial coverage; clarify at gates |

No new unauthorized implementation. M01 commit intact; branch ahead of origin by 1 (M01 only).

---

## 12. Proposed M03 foundation scope (no implementation)

After M02 `ACCEPTED` + explicit M03 **GO** only:

1. Flutter skeleton (Clean Architecture / BLoC / routing smoke)
2. FastAPI skeleton + modular package layout
3. PostgreSQL local (Docker Compose Engine)
4. SQLAlchemy + Alembic plumbing
5. GitHub Actions basic quality gates within free limits (**no** hosted-runner Ollama LAN dependency)
6. Local unit + API smoke tests
7. `.env.example` only — `DATABASE_URL`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL`
8. AI provider **config boundary** (adapter interface; no live model benchmark required at bootstrap)
9. Basic structured logging (stdlib/OSS)

**Version pins:** select Flutter/Dart, Python, PostgreSQL, SQLAlchemy, Alembic, Drift/Dio at M03 start (not pinned in M02).

**Deferred:** Redis, Celery, vector DB, advanced monitoring SaaS, production hosting, paid AI, LAN Ollama on GitHub-hosted runners.

**Not started in this remediation.**

---

## 13. Recommendation for M02 acceptance

**ACCEPTED** by Tech Lead (2026-11-25) with Project Owner ADR confirmation. F-M02-001..006 `ACCEPTED`. Historical limitations preserved (secret heuristic; Mermaid manual-only). M03 authorized after M02 local checkpoint.

Limitations that remain recorded (not erased): secret scan is heuristic-only; Mermaid not auto-rendered; business rules / production infra / AI suitability / provider choices / budget remain PENDING.
