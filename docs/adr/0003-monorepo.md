# ADR-0003 — Monorepo Layout

| Field | Value |
| --- | --- |
| Status | `ACCEPTED` |
| Date | 2026-11-25 |

## Context

Mobile, backend, AI eval assets, and docs must version together for MVP.

## Decision

Use a **single Git monorepo** with `apps/`, `services/backend/`, `ai/`, `docs/`, `infrastructure/` as in `REPOSITORY_ARCHITECTURE.md`. Preserve existing `docs/phase-00`.

## Alternatives

Polyrepo — rejected for Phase 0/MVP coordination cost.

## Consequences

Clear ownership paths; CI path filters later (M03). No scaffolding in M02.

## Validation

M03 bootstrap matches layout.

## Approval (2026-11-25)

ACCEPTED by Tech Lead with Project Owner confirmation for PH00-M03 foundation bootstrap.
