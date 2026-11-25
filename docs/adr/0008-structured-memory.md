# ADR-0008 — Structured AI Memory in PostgreSQL

| Field | Value |
| --- | --- |
| Status | `ACCEPTED` (architectural direction); implementation details remain PENDING until POC/evidence |
| Date | 2026-11-25 |

## Decision

Structured memory records in PostgreSQL with provenance and user controls. **No** dedicated vector DB / custom RAG in MVP. Memory cannot override domain SoT.

## Alternatives

Vector DB now — deferred.

## Validation

M05 memory POC; isolation/deletion tests.

## Approval scope (2026-11-25)

**Accepted:** architectural principle / direction only (Tech Lead + Project Owner).
**Not accepted as proven:** feasibility, schemas, algorithms, or production readiness � remain PENDING for the validation milestones named in this ADR.
