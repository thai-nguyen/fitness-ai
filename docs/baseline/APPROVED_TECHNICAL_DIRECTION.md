# Approved Technical Direction

| Field | Value |
| --- | --- |
| Source | AUTH-003 TIP v1.1 Consolidated Baseline + accepted ADRs |
| Captured / reconciled | 2026-11-25 (PH00-M01 final closure) |
| AUTH package | APPROVED by PO 2026-11-25 (consolidated replacement, not verbatim original) |
| Change control | Material deviations require Change Request / ADR |

## Mobile

| Decision | Choice | Status |
| --- | --- | --- |
| Framework | Flutter | Aligned planning direction |
| Architecture style | Pragmatic Clean Architecture | Aligned; detailed ADR in M02 |
| State management | BLoC / Cubit | Aligned |
| Navigation | GoRouter | Aligned |
| DI | GetIt | Aligned |
| Networking | Dio | Aligned |
| Offline persistence | Drift / SQLite | Aligned; offline-first workouts P0 |

## Backend

| Decision | Choice | Status |
| --- | --- | --- |
| Language | Python | Aligned |
| API framework | FastAPI modular monolith | Aligned |
| Database | PostgreSQL | Aligned |
| ORM / migrations / schemas | SQLAlchemy / Alembic / Pydantic | Aligned |
| API style | REST/OpenAPI; SSE for chat | Aligned planning |
| Background jobs | PostgreSQL durable queue | **PROPOSED** — M07 POC; Redis/Celery only via ADR |
| Auth | Managed OIDC | **PROPOSED** — provider selection pending |

## AI

| Decision | Choice | Status |
| --- | --- | --- |
| Shape | Hybrid AI; single lightweight orchestrator | Aligned |
| Domain | Deterministic Fitness Domain Engine | Aligned |
| Generation | Template-first + LLM personalization + validation | Aligned |
| Memory | Structured persistent memory (PostgreSQL first) | Aligned; semantic retrieval deferred |
| Providers | LLM provider abstraction + **Ollama adapter (Phase 0)** | **ADR-0017**: Ollama primary for dev/POCs; Qwen 3.5 9B initial model (suitability **PENDING** M05). Paid cloud AI **not** approved. AUTH-003 OpenAI-candidate wording superseded for Phase 0 by CR-20261125 (baseline file preserved). |
| Safety | Guardrails, tool authorization, evaluation | Aligned; numerical thresholds **pending expert** |

Hard constraints: no LLM direct DB mutations; user confirmation for plan activation / material adjustments; memory cannot override authoritative domain records.

## Infrastructure

| Decision | Choice | Status |
| --- | --- | --- |
| Hosting VCS | **GitHub** | **ACCEPTED** (ADR-0001 / D-001) |
| CI | **GitHub Actions** + PR workflow | **ACCEPTED**; workflow files in **M03 only** |
| Containers | Docker Engine (local) | Zero-cost preference |
| Object storage | Local FS / self-hosted MinIO preferred; billable S3 needs PO approval | ADR-0017 |
| Push | FCM / APNs when required — check free-tier limits | Aligned planning |
| Observability | Prefer OSS / self-hosted | Zero-cost preference |
| Admin | Minimal web admin (OSS stack) | **PROPOSED** when needed |
| Cost governance | Zero-Cost First | **ADR-0017 / D-010 ACCEPTED** |

## Explicitly deferred / forbidden without approval

Microservices, Kubernetes, Redis, Celery, Kafka, multi-agent architecture, dedicated vector database, custom RAG, advanced event streaming / generic event platform, Terraform unless justified, complex generic rule engines, **paid cloud AI APIs**, **paid cloud infra/SaaS** (unless PO explicitly approves).

## Alignment notes post-AUTH deposit

| Item | Status |
| --- | --- |
| Prior GitLab CI wording | **Superseded** by ADR-0001 |
| AUTH-003 OpenAI adapter candidate | **Superseded for Phase 0 execution** by ADR-0017 / CR-20261125 (historical text preserved) |
| Monorepo layout names | Design in M02; bootstrap M03 (AUTH-003 target layout) |
| Timeline/budget/FTE ROM in AUTH-003 | **PENDING** — not commitments |
| Ollama/Qwen suitability | **PENDING** M05 evidence |
| POC acceptance criteria in AUTH-003 | Require real evidence in M05–M07 |
