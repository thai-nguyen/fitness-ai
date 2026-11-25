# ADR-0006 — Hybrid AI with Single Orchestrator

| Field | Value |
| --- | --- |
| Status | `ACCEPTED` (architectural direction); implementation details remain PENDING until POC/evidence |
| Date | 2026-11-25 |

## Decision

Hybrid AI: deterministic paths + LLM conversation/personalization via **one** orchestrator. No multi-agent platform.

## Alternatives

Multi-agent — deferred. LLM-only — rejected (safety).

## Consequences

Tool allowlist; structured validation; Fitness Engine final plan safety authority.

## Validation

M05 POCs; M08 eval.

## Approval scope (2026-11-25)

**Accepted:** architectural principle / direction only (Tech Lead + Project Owner).
**Not accepted as proven:** feasibility, schemas, algorithms, or production readiness � remain PENDING for the validation milestones named in this ADR.
