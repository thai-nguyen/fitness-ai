# CR-20261125 — Zero-Cost First & Local AI First

| Field | Value |
| --- | --- |
| Status | `ACCEPTED` (Project Owner directive) |
| Date | 2026-11-25 |
| Approver | Project Owner |
| Related ADR | [ADR-0017](../adr/0017-zero-cost-local-ai-ollama.md) |
| Related decisions | D-010, D-011 |

## 1. Current decision (historical)

AUTH-003 planning text listed an **OpenAI adapter candidate** (subject to governance/POC) and did not mandate zero-cost-only development infrastructure.

## 2. Proposed / approved change

Adopt **Zero-Cost First** and **Local AI First** for all development, architecture, discovery, and POCs:

- Primary AI provider for Phase 0: **Ollama** (local), initial model **Qwen 3.5 9B** (tag to verify).
- No paid APIs/cloud/SaaS without explicit PO approval.
- Preserve hybrid AI architecture + provider abstraction; add Ollama adapter.
- Configurable endpoint/model via env; backend-only access to Ollama.

## 3. Technical rationale

PO operates an existing zero-cost Ollama server on the LAN. Paid cloud LLM spend is unnecessary for Phase 0 if local model feasibility is validated.

## 4. Product impact

- No Core MVP feature scope change.
- AI quality/latency may be constrained by local hardware until validated.
- Production AI hosting remains an open decision after POCs.

## 5. Effort impact

- M02: documentation/ADR updates (this CR).
- M05: expanded local-model evaluation matrix (already planned; now Ollama-specific).
- Avoids paid API integration work unless later approved.

## 6. Risks

Local capacity, model capability gaps, LAN availability, free-tier CI limits. Mitigate via M05 measurements and zero-cost fallback evaluation before any paid proposal.

## 7. Alternatives

Paid cloud LLM immediately — rejected by PO constraint. Direct mobile→Ollama — rejected for security.

## 8. Required approval

**Project Owner — granted** via Zero-Cost First / Local AI First directive (2026-11-25).

## 9. Baseline preservation

Consolidated Baseline files are **not** silently rewritten. This CR + ADR-0017 are the authoritative subsequent change records.
