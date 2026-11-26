# AI Provider Design (PH00-M05)

| Field | Value |
| --- | --- |
| Provider | Ollama (Local AI First) |
| Model | `qwen3.5:9b` (exact tag verified) |
| Digest (smoke) | `56671c2ab9385f9cfcb404638e32cd62d88e3501d44822208363c010179a3c90` |
| Quantization | Q4_K_M |
| Implementation | `app/modules/ai_coach/providers/` |

## Contracts

`AIMessage`, `AIRequest`, `AIStructuredRequest`, `AIResponse`, `AIStreamEvent`, `AIUsage`, `AIProviderCapabilities`, structured `AIProviderError` codes.

Adapters: `OllamaProvider`, `FakeAIProvider` (tests).

No OpenAI/Anthropic/Gemini adapters. No LangChain.

## Config

See `.env.example`. LAN endpoints belong only in ignored local `.env` / process env — never committed defaults.

## Capability notes

Reported model capabilities include completion, vision, tools, thinking. M05 uses chat + `format=json` structured generation + streaming; thinking traces are disabled (`think=false`) and not persisted.
