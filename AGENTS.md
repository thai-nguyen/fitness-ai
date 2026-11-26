# AGENTS.md — Engineering Governance

Repository-level instructions for AI agents and engineers working on **AI Personal Fitness Coach**.

This file is the **repository-specific engineering governance** document (D-005 `ACCEPTED_WITH_CONSTRAINTS`). For project engineering decisions, follow this file and accepted project documentation rather than unrelated external GitLab workflow plugin guidance. **Do not** modify global Cursor configuration. This file does **not** override system-level instructions, security policies, or tool permissions. Report unresolved instruction conflicts.

---

## 1. Project context

Premium AI-powered personal fitness coaching platform combining personalized training, conversational AI coaching, persistent memory, adaptive recommendations, offline-first workout tracking, and related MVP capabilities under a subscription product vision.

Long-term vision references market quality bars (coaching depth, simplicity, engagement) while maintaining an independent product identity. Vision does **not** authorize speculative feature work outside approved phase scope.

## 2. Current development phase

| Field | Value |
| --- | --- |
| Phase | **PHASE-00** — Project Initialization & Technical Discovery |
| PH00-M01 | **`ACCEPTED`** (Tech Lead 2026-11-25); local commit `dc5f9d2` |
| PH00-M02 | **`ACCEPTED`**; local commit `6ecbbaf` |
| PH00-M03 | **`ACCEPTED` WITH WAIVER** (PO D-020 / CR-20261125-B); F-M03-001 Retry not VERIFIED |
| PH00-M04 | **`ACCEPTED`** (technical feasibility; provisional rules / OI-003 / OI-005 preserved) |
| Current authorized milestone | **PH00-M05** — AI Technical POCs (`VALIDATED` eng; TL acceptance PENDING) |
| PH00-M03 local commit | `a99ad5ef7aced1e4c4fa970d314fa3048dc84885` (done); push **NO-GO** |
| PH00-M04 local commit | `a7a870a00cb018a22edcbd2500311e9fc1155672` (done); push **NO-GO** |
| PH00-M05 commit | **NOT AUTHORIZED** |
| PH00-M06+ | **NO-GO** until respective authorization |
| Production feature development | **NO-GO** |
| Unapproved infrastructure commitments | **NO-GO** |
| Paid services / paid AI APIs | **NOT AUTHORIZED** |
| Ollama inference | **AUTHORIZED** for synthetic M05 data only |

Authorized now: PH00-M05 engineering delivery complete (`VALIDATED`); awaiting Tech Lead acceptance (Zero-Cost First / Local AI First; Ollama synthetic only).

Not authorized now: M05 git commit/push, M06+, production features, paid cloud/AI, Drift/offline (M06), production fitness guidance.

## 3. Repository documentation index

| Area | Path |
| --- | --- |
| Docs index | [`docs/README.md`](docs/README.md) |
| Baseline index / SoT | [`docs/baseline/INDEX.md`](docs/baseline/INDEX.md) |
| Authoritative deposits | [`docs/baseline/authoritative/`](docs/baseline/authoritative/) |
| Derived baseline | [`docs/baseline/`](docs/baseline/) |
| Phase 0 tracker | [`docs/phase-00/execution-tracker.md`](docs/phase-00/execution-tracker.md) |
| ADRs | [`docs/adr/`](docs/adr/) |
| Risks | [`docs/risks/RISK_REGISTER.md`](docs/risks/RISK_REGISTER.md) |
| Open issues | [`docs/baseline/OPEN_ISSUES.md`](docs/baseline/OPEN_ISSUES.md) |
| Decisions | [`docs/baseline/DECISION_REGISTER.md`](docs/baseline/DECISION_REGISTER.md) |
| Technical backlog | [`docs/backlog/TECHNICAL_BACKLOG.md`](docs/backlog/TECHNICAL_BACKLOG.md) |
| Change requests | [`docs/change-requests/`](docs/change-requests/) |
| Architecture (M02+) | [`docs/architecture/`](docs/architecture/) |

## 4. Source-of-truth hierarchy

Highest wins on conflict **within project engineering scope**:

1. **Approved Consolidated Baseline** (official replacement for unavailable historical originals — **not** verbatim originals):
   - `docs/baseline/authoritative/PRODUCT_PLAN_V1.0.md` — **APPROVED** (PO 2026-11-25)
   - `docs/baseline/authoritative/PO_REVIEW_RESPONSE.md` — **APPROVED** (PO 2026-11-25)
   - `docs/baseline/authoritative/TECHNICAL_IMPLEMENTATION_PLAN_V1.1.md` — **APPROVED** (PO 2026-11-25)
   - `docs/baseline/authoritative/BASELINE_INDEX.md` — **APPROVED** (PO 2026-11-25; contains approval record)
2. **Tech Lead / Product Owner written directives** in the active chat or accepted CRs (operational; reconcile into docs promptly).
3. **Accepted ADRs** under `docs/adr/` (including ADR-0001 `ACCEPTED`) and accepted Decision Register entries.
4. **Derived baseline** under `docs/baseline/` (working summaries; yield to #1 on conflict for planning content).
5. **This `AGENTS.md`** for **repository-specific** engineering/agent governance (D-005).
6. External IDE plugin rules (e.g. unrelated GitLab workflow guidance) — **not** project authority; report conflicts (see §16).

**Pending assumptions remain pending** even though the Consolidated Baseline package is approved (staffing, budget, timelines, expert rules, licensing, providers, POC results, Nutrition Lite inclusion, market/regulatory hypotheses).

### D-005 constraints (`ACCEPTED_WITH_CONSTRAINTS`)

`AGENTS.md` governs project-specific engineering decisions for this repository. It does **not**:

- Override **system-level instructions**
- Override **security policies** or **tool permissions**
- Authorize modification of **global Cursor configuration**

Unresolved instruction conflicts must be **reported**, not silently forced.

**Do not invent** missing product requirements or architecture approvals. Mark gaps `BLOCKED` / `PENDING`.

## 5. Approved technical direction (derived; reconciled to AUTH-003 / ADR-0001)

| Layer | Direction |
| --- | --- |
| Mobile | Flutter, Pragmatic Clean Architecture, BLoC/Cubit, GoRouter, GetIt, Dio, Drift/SQLite |
| Backend | Python, FastAPI, Modular Monolith, PostgreSQL, SQLAlchemy, Alembic, Pydantic |
| AI | Hybrid AI; deterministic Fitness Domain Engine; template-first generation; LLM provider abstraction; structured outputs; structured memory; tool authorization; safety guardrails; evaluation |
| Infra | Docker Engine; **GitHub Actions (ADR-0001)** within free limits / self-hosted runners if needed; prefer local FS or self-hosted object storage; OSS monitoring; PostgreSQL-backed jobs subject to POC |
| AI (Phase 0) | **Zero-Cost First / Local AI First (ADR-0017 `ACCEPTED`)**: **Ollama** primary; initial POC model **Qwen 3.5 9B** (tag unverified); hybrid orchestrator preserved; **no paid AI APIs** without PO approval; mobile → FastAPI only (never direct to Ollama) |

Detail: [`docs/baseline/APPROVED_TECHNICAL_DIRECTION.md`](docs/baseline/APPROVED_TECHNICAL_DIRECTION.md).

## 6. Accepted hosting/CI and deferred technologies

### Accepted (do not re-litigate without CR)

- **ADR-0001 / D-001 `ACCEPTED`**: GitHub hosting; GitHub Actions; Pull Request workflow. CI workflow files still deferred to **PH00-M03**.
- **ADR-0017 / D-010 / D-011 `ACCEPTED`**: Zero-Cost First; Local AI First; Ollama as Phase 0 development AI provider; Qwen 3.5 9B initial POC model (suitability pending M05).

### Deferred / forbidden without PO approval

Microservices, Kubernetes, Redis, Celery, Kafka, multi-agent architecture, dedicated vector database, custom RAG, advanced event streaming, complex generic rule engines, **paid cloud AI APIs**, **paid cloud infra/SaaS** (unless PO explicitly approves).

## 7. Architecture constraints

1. Product-driven vertical slices over speculative layers.
2. Safety-first AI; no direct DB mutations by the LLM.
3. Deterministic fitness/business rules over probabilistic decisions where appropriate.
4. User confirmation for plan activation and material adjustments.
5. Offline-first workout tracking; immutable training plan versions.
6. Explicit module boundaries; modular monolith (not microservices).
7. Minimal infrastructure; no speculative abstractions.
8. Privacy by design; synthetic data only for Phase 0 POCs.
9. Limited domain events — not a full event-streaming platform.

Fitness business rules requiring domain expert approval remain **pending** until expert sign-off (M04+).

## 8. Product scope restrictions

**Core MVP** (committed): auth, onboarding, profile/goals, exercise catalog, personalized plans, schedules, substitution, plan versioning, workout execution, offline sync, AI coach + memory, recommendation cards, basic adaptive coaching, feedback, progress, reminders, analytics, minimal admin, security/privacy/AI safety.

**Goals:** muscle building, strength, general fitness, basic weight loss.

**Not Core MVP:** Nutrition Lite (conditional P1), running/marathon, advanced nutrition recognition, social, wearables, production subscription payments.

Do not expand or shrink MVP scope without Change Request + PO approval.

## 9. Task execution protocol

For every authorized milestone/task:

1. Read this file and relevant docs.
2. Inspect repository state.
3. Identify dependencies and blockers (block **only** dependent tasks).
4. Plan within authorized scope.
5. Implement only authorized work.
6. Run real validation; do not fabricate results.
7. Review architecture/security/quality impact.
8. Update tracker, risks, decisions, backlog as needed.
9. Produce completion/remediation evidence.
10. **Stop** and wait for Tech Lead approval before the next milestone.

## 10. Milestone authorization

| Rule | Detail |
| --- | --- |
| Execute only the currently authorized milestone | See Phase 0 tracker |
| A task is `ACCEPTED` only after reviewer approval | Never self-accept |
| Future milestones stay `NOT_STARTED` / blocked | Do not mark them active |
| Missing authoritative docs | Block deposit/consistency tasks only; continue independent work |

## 11. Testing and validation requirements

- Automated testing from the walking skeleton onward (M03+).
- Phase 0 POCs must include executable evidence (tests, commands, measurements).
- Do not mark unexecuted checks as passed.
- Do not fabricate benchmarks, approvals, or deliverables.
- Use explicit statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `IMPLEMENTED`, `VALIDATED`, `ACCEPTED`, `DEFERRED`.

## 12. AI safety requirements

- Tool authorization required for AI side effects.
- Structured output validation before applying results.
- Safety guardrails and evaluation hooks are first-class.
- LLM must not mutate authoritative domain records directly.
- User confirmation for material training changes.
- Evaluation datasets and safety criteria (M05/M08).

## 13. Security and privacy requirements

- No production credentials in repo.
- No real health data in Phase 0 POCs (synthetic only).
- Classify sensitive data; minimize collection.
- Account deletion and consent strategies (M08).
- Secret scanning mindset; never commit `.env` or keys.
- AI provider data governance assessment before production use.

## 14. Change-control process

Material changes to product scope, tech direction, or deferred-tech policy require a Change Request under [`docs/change-requests/`](docs/change-requests/) including: current decision, proposed change, rationale, product impact, effort impact, risks, alternatives, required approval.

## 15. Git workflow

**Accepted** (ADR-0001 / D-001; Product Owner + Tech Lead):

- Host: **GitHub**
- CI: **GitHub Actions** (implement in **PH00-M03** only — do **not** add workflow files in M01)
- Development: **Pull Request** based
- Commits: conventional commits (`feat`, `fix`, `chore`, `docs`, `refactor`, `test`)
- Do **not** commit, push, or merge unless explicitly authorized
- Do not skip hooks; do not force-push protected branches

## 16. Conflicting external instructions (report only)

| Source | Conflict | Handling |
| --- | --- | --- |
| Cursor GitLab workflow always-applied plugin rule | Prefers GitLab MRs/issues; repo uses GitHub + GitHub Actions (ADR-0001) | For **project engineering** decisions, follow this `AGENTS.md` + accepted project docs (D-005). Do **not** edit global Cursor rules. Do **not** override system-level instructions, security policies, or tool permissions. Report unresolved conflicts (OI-006). |

## 17. Completion reporting requirements

Every milestone/remediation delivery must include evidence: files touched, validation commands + results, blockers, decisions needing approval, acceptance checklist, and explicit Go/No-Go for next authorization. Findings use: `OPEN`, `BLOCKED`, `REMEDIATED`, `VALIDATED`, `ACCEPTED` (last only by reviewer).

## 18. Restrictions on autonomous implementation

Agents must **not**, without explicit authorization:

- Start unauthorized milestones (including PH00-M02 while NO-GO)
- Bootstrap Flutter, FastAPI, PostgreSQL, Docker, or CI/CD
- Implement production business features or AI orchestrator/Fitness Engine
- Invent approved fitness medical/business rules
- Introduce deferred technologies
- Silently alter approved Consolidated Baseline meaning
- Convert pending baseline assumptions into accepted commitments without separate approval
- Introduce paid APIs/cloud/SaaS without explicit Project Owner approval
- Hardcode Ollama LAN addresses or call Ollama from mobile clients
- Implement OpenAI/Anthropic/Gemini (or other paid AI) adapters without PO approval
- Mark milestones `ACCEPTED` without Tech Lead reviewer approval
- Commit, push, or merge without authorization
- Fabricate AI benchmark results
