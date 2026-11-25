# System Architecture — Core MVP

| Field | Value |
| --- | --- |
| Owner | Engineering (Architect) |
| Version | 0.1 |
| Status | `PROPOSED` (PH00-M02) |
| Related | AUTH-003, ADR-0001..0015, PH00-TB-008 |
| Assumptions | Zero-Cost First (ADR-0017); Ollama for Phase 0 AI; PG job queue subject to M07; production hosting pending |
| Open decisions | Auth provider (prefer self-hosted/free); analytics (OSS); production AI hosting; multi-device conflict; Qwen suitability |

## 1. Scope

Architecture for Core MVP: auth/onboarding, exercise catalog, personalized plans with immutable versions, offline-first workouts, AI coach with structured memory and recommendation cards, basic adaptive coaching, progress, reminders, minimal admin, security/privacy/AI safety.

## 2. System context

```mermaid
C4Context
title System Context — fitness-ai Core MVP
Person(user, "End User", "Trains with mobile app")
Person(admin, "Administrator", "Minimal catalog/ops admin")
System(fitness, "AI Personal Fitness Coach", "Mobile + modular monolith backend")
System_Ext(idp, "Auth Provider", "Prefer local/self-hosted OIDC — vendor TBD")
System_Ext(ollama, "Ollama + Qwen 3.5 9B", "LAN inference — Phase 0 primary; via backend only")
System_Ext(push, "FCM / APNs", "Reminders when enabled — evaluate free tiers")
System_Ext(obj, "Object Storage", "Local FS / self-hosted MinIO preferred")
System_Ext(analytics, "Product Analytics", "Privacy-safe — prefer OSS/self-host")
System_Ext(obs, "Observability", "Open-source / self-host preferred")
Rel(user, fitness, "Uses")
Rel(admin, fitness, "Administers")
Rel(fitness, idp, "OIDC")
Rel(fitness, ollama, "LLM via adapter (not public)")
Rel(fitness, push, "Push")
Rel(fitness, obj, "Private objects")
Rel(fitness, analytics, "Events")
Rel(fitness, obs, "Telemetry")
```

| Actor / system | Status |
| --- | --- |
| Flutter mobile | Confirmed |
| FastAPI modular monolith + worker | Confirmed shape; bootstrap M03 |
| PostgreSQL (local/Docker) | Confirmed |
| Local SQLite (Drift) | Confirmed |
| GitHub + GitHub Actions | **ACCEPTED** (ADR-0001); stay within **free** limits / self-hosted runners if needed |
| Ollama (Qwen 3.5 9B) | **Approved development AI** (ADR-0017); suitability **PENDING** POC |
| Auth / analytics / object storage | Prefer zero-cost/self-host; paid requires PO approval |
| FCM/APNs | When notifications required; check free tier limits |
| Minimal admin web | Confirmed need; OSS stack |
| Production cloud hosting | **PENDING** PO decision |

## 3. Container architecture

```mermaid
C4Container
title Containers
Person(user, "User")
Person(adminUser, "Admin")
Container(mobile, "Flutter App", "Dart", "UI, BLoC, Drift/SQLite, offline sync")
Container(admin, "Admin Web", "Minimal", "Catalog/users/ops — when authorized")
Container(api, "API Process", "FastAPI", "REST/OpenAPI, SSE chat")
Container(worker, "Worker Process", "Same codebase", "Jobs, outbox consumers")
ContainerDb(pg, "PostgreSQL", "Source of truth")
ContainerDb(sqlite, "SQLite", "On-device workout durability")
System_Ext(ext, "External Providers")
Rel(user, mobile, "Uses")
Rel(adminUser, admin, "Uses")
Rel(mobile, api, "HTTPS REST / SSE")
Rel(admin, api, "HTTPS")
Rel(api, pg, "SQL")
Rel(worker, pg, "SQL")
Rel(mobile, sqlite, "Local R/W")
Rel(api, ext, "Adapters")
Rel(worker, ext, "Push / LLM jobs")
```

**Trade-off:** API and worker are separately deployable processes from one modular monolith codebase — not microservices.

## 4. Backend module map

```mermaid
flowchart LR
  subgraph presentation
    API[API / SSE]
  end
  subgraph application
    AppServices[Application Services]
  end
  subgraph domain
    Identity
    Profile
    Exercise
    Training
    FitnessEngine[Fitness Engine]
    Workout
    Recovery
    Progress
    Coaching
    Notification
    Administration
  end
  subgraph platform
    Jobs[Job / Outbox]
    Audit
    AIUsage[AI Usage]
  end
  API --> AppServices
  AppServices --> Identity
  AppServices --> Profile
  AppServices --> Exercise
  AppServices --> Training
  AppServices --> FitnessEngine
  AppServices --> Workout
  AppServices --> Recovery
  AppServices --> Progress
  AppServices --> Coaching
  AppServices --> Notification
  AppServices --> Administration
  AppServices --> Jobs
  Coaching --> FitnessEngine
  Coaching --> Training
  Workout --> Training
```

**Rules:** Domain modules do not import infrastructure. No cross-module repository access. Cross-context collaboration via application services / explicit events (limited outbox).

## 5. Core runtime interactions

```mermaid
sequenceDiagram
  participant M as Mobile
  participant A as API
  participant D as Domain/App Services
  participant P as PostgreSQL
  participant W as Worker
  participant L as LLM Adapter
  M->>A: Authenticated request
  A->>D: Use case
  D->>P: Read/write SoT
  alt Async generation / reminders
    D->>P: Enqueue job / outbox
    W->>P: Claim job
    W->>L: Provider call (if needed)
    W->>P: Persist result
  end
  A-->>M: Response / SSE
```

## 6. Trust & deployment boundaries

| Boundary | Notes |
| --- | --- |
| Device | Local SQLite; secrets in secure storage; no other-user data |
| TLS edge | Mobile/admin → API |
| AuthN/Z | OIDC tokens; ownership checks on every mutation |
| Provider edge | LLM/auth/push/storage via adapters; no raw PII in analytics; **backend-only** Ollama |
| Data plane | PostgreSQL authoritative for server state |
| Cost plane | Local/zero-cost first; production hosting **PENDING** (see ADR-0017) |

Full local vs production split: [`ZERO_COST_DEPLOYMENT_BOUNDARIES.md`](ZERO_COST_DEPLOYMENT_BOUNDARIES.md).

Environments: local / staging / prod separation (M03+). No production health data in nonprod.

## 7. Sync vs async

| Sync | Async (jobs / limited outbox) |
| --- | --- |
| Profile reads/writes, workout sync batch ack, plan activate, recommendation accept | Plan generation, reminder fan-out, deletion workflows, heavy AI generation |

Job implementation **PROPOSED** PG durable queue — validate M07.

## 8. Failure isolation

- Provider outage: existing plans/workouts remain usable; AI degraded UX.
- Worker crash: lease/retry (M07).
- Mobile offline: local durability (M06).
- Invalid AI output: reject/repair/fallback; never activate unvalidated plans.

## 9. Validation requirements

Walkthroughs in `DESIGN_WALKTHROUGHS.md`. M03 walking skeleton. M05–M07 POCs for AI/offline/jobs.
