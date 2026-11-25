# ADR-0002 — Modular Monolith Backend

| Field | Value |
| --- | --- |
| Status | `ACCEPTED` |
| Date | 2026-11-25 |
| Related | AUTH-003, PH00-M02 |

## Context

Need clear module boundaries without microservice ops cost for MVP.

## Decision

Build a **modular monolith** (FastAPI) with separately runnable API and worker processes from one codebase.

## Alternatives

Microservices now — rejected (deferred). Modular monolith — selected. Single ball-of-mud — rejected.

## Rationale

Matches approved direction; supports vertical slices; defers distribution complexity.

## Consequences

Strict module import rules required. Extract services later only with evidence.

## Risks / validation

Boundary erosion — enforce in review/CI lint later. M03 skeleton demonstrates module packaging.

## Related requirements

ARCH-*, Core MVP multi-capability product.

## Approval (2026-11-25)

ACCEPTED by Tech Lead with Project Owner confirmation for PH00-M03 foundation bootstrap.
