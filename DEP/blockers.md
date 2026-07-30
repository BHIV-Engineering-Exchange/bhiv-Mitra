# Blockers — MITRA Phase 1 Convergence

## Active Blockers

### B1 — Cross-Origin Session Continuity
**Blocked on:** Raj Prajapati (Control Plane)
**Impact:** Phase 3 — full conversation continuity across separate VM deployments
**Details:**
`localStorage` is origin-bound. When Gurukul, Samruddhi, and SETU are deployed on separate VMs (separate origins), conversation history and session state do not transfer. Raj needs to provide a backend endpoint:
- `GET /api/session/{session_id}` — restore session and conversation history
- `POST /api/session/{session_id}/sync` — push local state to backend

**Frontend readiness:** `contextStore.js` already manages `sessionId` and sends it on every request. Once Raj's endpoint exists, `syncFromBackend()` can be wired in.

---

### B2 — Real-Time Execution State from TANTRA
**Blocked on:** Raj Prajapati + Ashmit (TANTRA Runtime)
**Impact:** Phase 4 — runtime awareness (no simulated frontend state)
**Details:**
The task requires all 7 runtime states to come from the backend. Currently, `ActivityIndicator` and `ExecutionStatusPanel` react to frontend-emitted events. They need a real-time stream (WebSocket or SSE) from TANTRA that pushes:
- `thinking` | `executing` | `capability_running` | `waiting` | `completed` | `failed` | `retrying`

**Frontend readiness:** `ExecutionStatusPanel.js` already handles `runtime.executing`, `runtime.waiting`, and all capability events. Only the transport (WS/SSE client) needs to be added once the endpoint exists.

---

### B3 — Backend LLM Bypass
**Blocked on:** Raj Prajapati / Vijay Dhawan
**Impact:** Success criterion — "All intelligence comes from UniGuru"
**Details:**
`backend/app/core/llm_bridge.py` directly imports and calls `AsyncOpenAI`, `AsyncGroq`, `google.generativeai`, and `MistralClient`. This bypasses UniGuru's intelligence APIs. **This is backend code — not Ashwini's responsibility to fix**, but it is flagged because the success criteria require all intelligence to route through UniGuru.

---

## Resolved Blockers

| ID  | Description                | Resolution                        | Date       |
|-----|----------------------------|-----------------------------------|------------|
| B4  | `src/config.js` missing   | Created `src/config.js`           | 2026-07-29 |
| B5  | uniguru.html URL typo     | Fixed `http.localhost` → `http://localhost` | 2026-07-29 |
| B6  | addMessage signature bug  | Fixed call in `ConversationPanel.js` | 2026-07-29 |
| B7  | Samruddhi page missing    | Created `pages/samruddhi.html`    | 2026-07-29 |
