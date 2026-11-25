# Baseline Index — fitness-ai

## Approval record (2026-11-25)

| Field | Value |
| --- | --- |
| Status | **APPROVED** as official Consolidated Baseline replacement |
| Approver | Project Owner |
| Approval date | 2026-11-25 |
| Nature | Approved consolidated replacements — **not** verbatim historical originals |

**Project Owner explicit approval (verbatim):**

> Tôi phê duyệt bộ 4 tài liệu Consolidated Baseline làm baseline thay thế chính thức cho dự án fitness-ai. Cho phép thực hiện PH00-M01 final closure validation. Giữ nguyên trạng thái pending của các giả định chưa được xác nhận.

English paraphrase for registry use: The PO approves the four Consolidated Baseline documents as the official replacement baseline for fitness-ai; authorizes PH00-M01 final closure validation; and requires pending/unconfirmed assumptions to remain pending.

This approval does **not** convert pending assumptions, conditional requirements, proposed ADRs, or unvalidated technical decisions into accepted commitments.

---

Package provenance (unchanged): Prepared from available conversation summaries and decisions, not verbatim historical originals. Existing repository tracker and accepted ADRs remain authoritative for execution status and specific accepted decisions.

## Document register
| ID | File | Owner | Status |
|---|---|---|---|
| AUTH-001 | [PRODUCT_PLAN_V1.0.md](PRODUCT_PLAN_V1.0.md) | PO | Proposed reconstructed replacement |
| AUTH-002 | [PO_REVIEW_RESPONSE.md](PO_REVIEW_RESPONSE.md) | PO | Proposed reconstructed replacement |
| AUTH-003 | [TECHNICAL_IMPLEMENTATION_PLAN_V1.1.md](TECHNICAL_IMPLEMENTATION_PLAN_V1.1.md) | TL | Proposed reconstructed replacement |
| INDEX | BASELINE_INDEX.md | PO + TL | Proposed |

Deposit together under docs/baseline/authoritative/ (or update existing index to point to that directory). Retain original files if later recovered, record provenance and reconcile conflicts. Do not overwrite historical evidence. Existing repository tracker and accepted ADRs remain authoritative for execution and specific decisions.

## Authority and precedence
System/security/tool constraints first. Explicit owner-approved changes and accepted ADRs govern their subject; PO Review governs scope conflicts with early Product Plan; Technical Plan governs engineering direction within product scope; Product Plan governs vision/roadmap. AGENTS governs repository-specific execution within those boundaries. Backlog and tracker govern task IDs/status/authorization; completion reports are evidence, not approval. Escalate unresolved conflicts, do not silently choose. No document here authorizes M02 or commits resources.

## Decision register summary
| Decision | Status | Meaning |
|---|---|---|
| D-001 / ADR-0001 GitHub + GitHub Actions + PRs | ACCEPTED | Explicit owner approval in conversation; repo synchronization pending verification; CI implementation M03 |
| D-005 AGENTS governance | ACCEPTED WITH CONSTRAINTS | TL decision; no override of system/security/tool permissions or global config changes |
| Core MVP, offline P0, basic adaptation, plan versions, hybrid AI | ALIGNED PLANNING DIRECTION | PO/TL prior alignment; consolidated replacement ratification pending |
| Flutter/FastAPI modular monolith/PostgreSQL/structured memory | ALIGNED PLANNING DIRECTION | Detailed ADR review pending M02 |
| PG durable queue | PROPOSED | Reliability POC; Redis/Celery fallback requires ADR |
| Managed auth, AI/analytics providers, hosting, admin framework | PROPOSED | Feasibility/governance/need assessment |
| Nutrition Lite | CONDITIONAL | Spike only now; value/rules/capacity approval after alpha |
| Advanced nutrition, billing, wearables, social, running | DEFERRED | Later roadmap, not MVP |
| Microservices/K8s/Kafka/vector DB/multi-agent/custom RAG | DEFERRED | No speculative infrastructure |
| 16 weeks, 7 FTE, estimates, cost, metrics, market | PENDING APPROVAL / HYPOTHESES | No commitment or measured results |
| Fitness/nutrition thresholds, content rights, legal/provider policies | PENDING EVIDENCE | Expert/legal/provider review required |

## Current execution state (reported, not independently verified)
PH00-M01 implemented/remediation validated in part, pending final acceptance. F-M01-001 blocked on approved baseline replacement; F-M01-002 ADR update pending verification; F-M01-003–006 conditional report-level pass. OI-002 decision approved; close only after repo validation. M02–M09 NOT_STARTED / unauthorized. No commit/push/merge authorized. Existing agent report says 18 unique tasks; reconcile actual IDs, fields, dependencies/cycles before acceptance. GitHub remote and AGENTS presence are agent-reported, not verified here.

## Ratification and handoff
1. Project Owner explicitly approves these four reconstructed files as replacement baseline (not original documents), or requests corrections.
2. Agent deposits files, records provenance/approval evidence and reconciles derived docs, accepted ADR-0001 and D-005. Preserve history; report contradictions, no silent scope changes.
3. Validate actual file presence, links, unique task IDs, dependencies/cycles, required fields, Git diff including untracked docs, gitignore, secret scan and unauthorized scope. Report commands/results/limitations.
4. Update F-M01-001 and OI-001 only after evidence and reviewer acceptance; synchronize ADR-0001/OI-002. Submit final M01 report.
5. TL reviews repository evidence and explicitly accepts M01, then separately authorizes M02. No automatic progression.

## Known reconstruction limitations
Available context is a detailed summary rather than full historical text; individual original story wording, exact feature mappings, ADR numbering and original estimates may differ. Historical feature ranges preserved where known; repository IDs control technical tasks. No actual POCs, expert rules, licensing, market research, budget, staffing, provider agreements or deployment evidence supplied. New editorial choices: English, consolidated cross-references, explicit status taxonomy, safety gate ordering, repository ID reconciliation, and correction of illustrative cost arithmetic. These are proposed documentation clarifications, not additional product scope.
