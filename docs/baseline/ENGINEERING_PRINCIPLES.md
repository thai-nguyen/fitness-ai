# Engineering Principles

Authoritative principles for Phase 0 and subsequent implementation. Violations require Tech Lead review; product-scope violations also require Product Owner approval.

1. **Product-driven vertical-slice development** — Deliver thin, end-to-end slices over horizontal speculative layers.
2. **Safety-first AI architecture** — Guardrails, authorization, and evaluation are first-class, not afterthoughts.
3. **Deterministic business rules over probabilistic decisions where appropriate** — Especially fitness constraints and plan validity.
4. **No direct database mutations by the LLM** — Models propose; authorized services apply.
5. **User confirmation for training plan activation and material adjustments** — Material coaching changes are explicit.
6. **Offline-first workout tracking** — Local durability and sync semantics are core, not optional polish.
7. **Immutable training plan versions** — Version history is preserved; activation is controlled.
8. **Explicit module boundaries** — Modular monolith with clear ownership and interfaces.
9. **Minimal infrastructure** — Prefer approved simple building blocks; no premature scale architecture.
10. **No speculative abstractions** — Abstract only when a concrete second use case exists.
11. **Privacy by design** — Classify data, minimize collection, govern third-party AI providers.
12. **Automated testing from the beginning** — Tests and CI foundations start with the walking skeleton.
13. **Evidence-based milestone completion** — No fabricated results; statuses reflect real evidence.
14. **Preserve approved product requirements** — Do not silently expand or shrink MVP scope.
15. **Use synthetic data for technical proof of concepts** — No real health data in Phase 0 POCs.
