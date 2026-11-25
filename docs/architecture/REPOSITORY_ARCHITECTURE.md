# Repository / Monorepo Architecture

| Field | Value |
| --- | --- |
| Owner | Engineering |
| Version | 0.1 |
| Status | `ACCEPTED` (layout direction ADR-0003); bootstrap in **PH00-M03** |
| Related | AUTH-003 §2, ADR-0003 (monorepo) |
| Note | **Document only** — do not create app scaffolding in M02 |

## 1. Target layout

```text
fitness-ai/
  AGENTS.md
  README.md
  .gitignore
  .env.example                 # M03
  .github/workflows/           # M03 (ADR-0001)
  apps/
    mobile/                    # Flutter
    admin/                     # Minimal admin when needed
  services/
    backend/                   # FastAPI modular monolith
  ai/
    prompts/
    schemas/
    evaluations/
  infrastructure/              # Compose, deploy notes — minimal
  scripts/
  tests/                       # Cross-cutting integration
  docs/                        # Existing structure preserved
```

Preserve `docs/phase-00/` as established.

## 2. Flutter boundaries

```text
apps/mobile/
  lib/
    app/           # router, DI, bootstrap
    core/          # network, db, sync, security, design system
    features/<feature>/{presentation,application,domain,data}
```

Dependency direction: `presentation → application → domain ← data`.
`data` implements domain ports. Features do not import other features' data layers.

## 3. Backend boundaries

```text
services/backend/
  app/
    main.py
    modules/<context>/{domain,application,infrastructure,api}
    platform/{jobs,audit,auth,config}
  alembic/
  tests/
```

- Domain: entities, invariants, Fitness Engine
- Application: use cases, DTOs, transactions
- Infrastructure: SQLAlchemy, providers
- API: FastAPI routers

**No** cross-module infrastructure imports. Compose at application root.

## 4. Shared code rules

| Allowed | Forbidden |
| --- | --- |
| OpenAPI contracts / schemas package if justified | Dumping unrelated code into `shared/` |
| `ai/schemas` for structured outputs | Mobile importing backend internals |
| Documented design tokens export | Circular feature dependencies |

## 5. Testing boundaries

- Domain unit tests per module
- Application tests with fakes
- API contract tests
- Flutter bloc/widget tests
- Integration against real PG in CI (M03)
- AI eval harness under `ai/evaluations` (M05/M08)

## 6. Naming

- Python: `snake_case` modules; contexts match bounded context names
- Dart: `snake_case` files; features match product areas
- Events: `domain.action` (`training.plan_activated`)

## 7. Abstraction rule

Introduce interfaces only with a second concrete need or test seam — no speculative frameworks.
