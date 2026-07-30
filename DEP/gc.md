# GC — Governance Compliance

## Architecture Compliance

| Principle                                | Compliant | Notes                                                            |
|------------------------------------------|-----------|------------------------------------------------------------------|
| No frontend orchestration               | ✅ Yes    | All logic proxied through `controlPlane.js` → backend `/api/assistant` |
| No local execution logic                | ✅ Yes    | Capabilities dispatched to backend via `/api/mitra/evaluate`     |
| No direct LLM integrations in frontend  | ✅ Yes    | Frontend never calls OpenAI/Groq/Gemini directly                |
| Intelligence from UniGuru via Raj        | ⚠️ Partial | Frontend correctly routes through Raj. Backend `llm_bridge.py` calls LLM providers directly — this is Raj's responsibility |
| Execution state from TANTRA             | ⚠️ Partial | `ActivityIndicator` + `ExecutionStatusPanel` handle events. Real-time stream from TANTRA not yet available |
| Single canonical component              | ✅ Yes    | One `<mitra-companion>` Web Component, zero product-specific forks |
| Session ID sent on every request        | ✅ Yes    | `controlPlane.js` includes `session_id` from `contextStore`     |
| No UI paths that bypass runtime         | ✅ Yes    | All message/capability paths go through `RuntimeService` → `controlPlane` → backend |

## Security

| Check                   | Status  | Detail                                                    |
|-------------------------|---------|-----------------------------------------------------------|
| API key in requests     | ✅ Yes  | `X-API-Key` header sent on every backend call             |
| Shadow DOM isolation    | ✅ Yes  | Companion uses `attachShadow({ mode: 'open' })`          |
| User input sanitization | ✅ Yes  | `MessageRenderer.escapeForRole()` escapes user input HTML |
