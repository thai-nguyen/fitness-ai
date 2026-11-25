# Decision Register

| Field | Value |
| --- | --- |
| Last updated | 2026-11-25 |
| Milestone | PH00-M01 official acceptance recorded |

## Status values

`PROPOSED` · `ACCEPTED` · `ACCEPTED_WITH_CONSTRAINTS` · `REJECTED` · `SUPERSEDED` · `DEFERRED` · `PENDING`

## Decisions

| ID | Title | Status | ADR | Date | Notes |
| --- | --- | --- | --- | --- | --- |
| D-001 | Retain GitHub hosting; use GitHub Actions + PR workflow instead of GitLab CI | `ACCEPTED` | [ADR-0001](../adr/0001-github-hosting-and-github-actions.md) | 2026-11-25 | PO + Tech Lead. CI files deferred to M03. |
| D-002 | Flutter / FastAPI Modular Monolith / PostgreSQL / Hybrid AI stack | `ALIGNED` (planning direction) | M02 ADRs pending | 2026-11-25 | Confirmed against AUTH-003; detailed ADRs still M02 |
| D-003 | PostgreSQL-backed background jobs subject to M07 validation | `PROPOSED` | — | 2026-11-25 | Redis/Celery fallback only via ADR; **not** accepted by baseline approval |
| D-004 | Retain existing `docs/phase-00` documentation layout | `ACCEPTED` | — | 2026-11-25 | Matches AUTH-003 guidance |
| D-005 | `AGENTS.md` repo-specific governance with constraints | `ACCEPTED_WITH_CONSTRAINTS` | — | 2026-11-25 | No override of system/security/tool permissions; no global Cursor edits |
| D-006 | Consolidated Baseline (AUTH-001..004) as official replacement for unavailable historical originals | `ACCEPTED` | — | 2026-11-25 | PO explicit approval; pending assumptions remain pending |
| D-007 | PH00-M01 milestone acceptance | `ACCEPTED` | — | 2026-11-25 | Tech Lead; basis = final readiness report; M02 authorization remains PENDING |

## D-006 approval evidence

PO statement (2026-11-25):

> Tôi phê duyệt bộ 4 tài liệu Consolidated Baseline làm baseline thay thế chính thức cho dự án fitness-ai. Cho phép thực hiện PH00-M01 final closure validation. Giữ nguyên trạng thái pending của các giả định chưa được xác nhận.

Recorded in [`authoritative/BASELINE_INDEX.md`](authoritative/BASELINE_INDEX.md).

## Explicitly still pending / not accepted by D-006

- Team composition / staffing / 7 FTE / budget / 16-week commitment
- Fitness/nutrition numerical thresholds (expert)
- Exercise content licensing
- AI provider selection / data governance completion
- Managed authentication provider selection
- PostgreSQL durable queue feasibility (POC)
- Nutrition Lite inclusion beyond conditional spike
- Target market / regulatory / jurisdiction assumptions
- POC results, cost/latency benchmarks, SLOs as commitments
- Proposed ADRs other than ADR-0001

## Notes

- Accepted decisions do not authorize M02+ or CI implementation before authorized milestones.
