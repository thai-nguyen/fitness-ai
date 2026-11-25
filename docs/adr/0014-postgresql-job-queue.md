# ADR-0014 — PostgreSQL Durable Job Queue (Proposed)

| Field | Value |
| --- | --- |
| Status | `PROPOSED` |
| Date | 2026-11-25 |

## Decision (proposal)

Prefer PostgreSQL-backed jobs with atomic claim/leases. Redis/Celery remain deferred unless M07 evidence forces CR.

## Validation

**PH00-M07** reliability POC — do not treat as ACCEPTED until evidence.
