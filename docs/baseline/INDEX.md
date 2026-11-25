# Baseline Document Index

| Field | Value |
| --- | --- |
| Last updated | 2026-11-25 |
| Milestone | PH00-M01 **`ACCEPTED`** (Tech Lead 2026-11-25) |
| Authoritative package | Consolidated Baseline **APPROVED** 2026-11-25 (PO) |
| Next milestone | PH00-M02 — authorization **PENDING** |

## 1. Authoritative vs derived documents

| Class | Role | May engineering invent content? |
| --- | --- | --- |
| **Authoritative consolidated baseline** | Official replacement for unavailable historical originals | **No** — do not silently modify approved meaning |
| **Derived baseline** | Working summaries for execution | Yes, but must yield to authoritative package on conflict |
| **Operational trackers** | Status, risks, backlog, ADRs | Yes, under milestone authorization |

## 2. Authoritative source documents

| ID | Document | Path | Present? | Status |
| --- | --- | --- | --- | --- |
| AUTH-001 | Product Plan v1.0 (consolidated) | [`authoritative/PRODUCT_PLAN_V1.0.md`](authoritative/PRODUCT_PLAN_V1.0.md) | **Yes** | **APPROVED** (PO 2026-11-25) |
| AUTH-002 | PO Review Response (consolidated) | [`authoritative/PO_REVIEW_RESPONSE.md`](authoritative/PO_REVIEW_RESPONSE.md) | **Yes** | **APPROVED** (PO 2026-11-25) |
| AUTH-003 | Technical Implementation Plan v1.1 (consolidated) | [`authoritative/TECHNICAL_IMPLEMENTATION_PLAN_V1.1.md`](authoritative/TECHNICAL_IMPLEMENTATION_PLAN_V1.1.md) | **Yes** | **APPROVED** (PO 2026-11-25) |
| AUTH-004 | Baseline index | [`authoritative/BASELINE_INDEX.md`](authoritative/BASELINE_INDEX.md) | **Yes** | **APPROVED** (PO 2026-11-25) |

Approval evidence: [`authoritative/BASELINE_INDEX.md`](authoritative/BASELINE_INDEX.md) § Approval record (verbatim PO statement).

**Nature:** Approved consolidated replacements — **not** verbatim historical originals.

## 3. Derived baseline documents

| Document | Path | Consistency vs AUTH (2026-11-25) |
| --- | --- | --- |
| Project baseline | [`PROJECT_BASELINE.md`](PROJECT_BASELINE.md) | Reconciled |
| Approved technical direction | [`APPROVED_TECHNICAL_DIRECTION.md`](APPROVED_TECHNICAL_DIRECTION.md) | Reconciled; ADR-0001 still governs CI |
| MVP scope | [`MVP_SCOPE.md`](MVP_SCOPE.md) | Reconciled |
| Engineering principles | [`ENGINEERING_PRINCIPLES.md`](ENGINEERING_PRINCIPLES.md) | Aligned |
| Decision register | [`DECISION_REGISTER.md`](DECISION_REGISTER.md) | Includes D-006 baseline approval |
| Open issues register | [`OPEN_ISSUES.md`](OPEN_ISSUES.md) | OI-001 closure subject to validation pass |

## 4. Source-of-truth ownership

| Concern | Authoritative owner | Working document | Approver |
| --- | --- | --- | --- |
| Product scope / MVP | AUTH-001 + AUTH-002 | `MVP_SCOPE.md` | Product Owner |
| Technical direction | AUTH-003 + accepted ADRs | `APPROVED_TECHNICAL_DIRECTION.md` | Tech Lead |
| Architecture decisions | Accepted ADRs | `docs/architecture/` (M02+) | Tech Lead |
| Execution status | — | `docs/phase-00/execution-tracker.md` | Tech Lead |
| Agent governance | `AGENTS.md` + D-005 | — | Tech Lead |
| Consolidated baseline package | AUTH-001..004 | This index | Product Owner |

**Conflict rule:** Approved consolidated baseline wins over derived summaries for product/technical planning content. Accepted ADRs and the Phase 0 tracker win for execution-specific accepted decisions and live milestone authorization. System/security/tool constraints remain supreme (D-005).

## 5. Consistency validation

See [`../phase-00/PH00-M01-final-readiness-report.md`](../phase-00/PH00-M01-final-readiness-report.md).
