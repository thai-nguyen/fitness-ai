# Cost & Provider Governance (Zero-Cost First)

| Field | Value |
| --- | --- |
| Owner | Engineering / Project Owner |
| Version | 0.1 |
| Status | `ACCEPTED` constraint (PO); provider matrix living doc |
| Related | ADR-0017, D-010, CR-20261125 |

## 1. Rule

No paid API, cloud infrastructure, SaaS subscription, or billable service without **explicit Project Owner approval**.

Prefer: local hardware, open-source, free tooling, self-hosted options.

## 2. Approved for Phase 0 development (AI)

| Service | Purpose | Cost class | Notes |
| --- | --- | --- | --- |
| Ollama + Qwen 3.5 9B | LLM inference for POCs | **Zero** (local) | Base URL/model via env; verify tag/capabilities before impl |
| FastAPI backend gateway | AuthZ boundary to AI | Local OSS | Mobile must not call Ollama directly |

## 3. Preferred zero-cost stack (non-AI)

| Need | Preferred | Paid alternative (requires PO approval) |
| --- | --- | --- |
| Mobile | Flutter | — |
| API | FastAPI | — |
| DB | PostgreSQL (local/Docker) | Managed cloud PG |
| Offline | SQLite / Drift | — |
| Containers | Docker Engine | Managed K8s |
| Object storage | Local filesystem / self-hosted MinIO | S3 billable |
| Auth | Local/self-hosted OIDC options (evaluate) | Auth0/Firebase paid tiers |
| Monitoring | Open-source (e.g. basic OTel/self-host) | SaaS APM |
| CI | GitHub Actions **free limits** / self-hosted runners | Paid minutes |
| AI eval | Local harness | Paid eval SaaS |

## 4. Proposal template (mandatory before any external paid service)

For every proposed external service document:

1. Purpose
2. Free/open-source alternative
3. Expected **development** cost
4. Potential **production** cost
5. Usage limits
6. Approval requirements (PO)

Do **not** assume free tiers remain free at production scale.

## 5. Explicitly not approved (unless PO later approves)

OpenAI / Anthropic / Gemini paid APIs; paid cloud GPU; Redis Cloud; managed Kafka; commercial vector DBs; Kubernetes cloud control planes; other billable SaaS.
