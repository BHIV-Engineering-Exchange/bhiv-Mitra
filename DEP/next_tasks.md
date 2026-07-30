# Next Tasks — MITRA Phase 1 → Phase 2

## Immediate (Unblocked)

1. **Landing & Dashboard pages** — Create proper landing and dashboard HTML shells for Gurukul, Samruddhi, and SETU with richer content and navigation. MITRA is already embedded; pages just need more realistic product UI.

2. **Wire `MessageRenderer` into `ConversationPanel`** — Replace inline `innerHTML` bubble creation in `ConversationPanel` with calls to `MessageRenderer.render()`. This is a refactor, not a behaviour change.

3. **Wire `ExecutionStatusPanel` into `MITRAWindow`** — Add `ExecutionStatusPanel` as an optional panel in the companion window alongside the existing `HealthPanel` and `ActivityIndicator`.

4. **Screenshot capture** — Take the 10 required screenshots per the evidence packet naming convention and place them in `evidence_packet/screenshots/`.

## Blocked (Requires Team Members)

5. **Cross-origin session continuity** — Requires Raj to expose a backend session-fetch/restore endpoint. Once available, `contextStore.syncFromBackend(sessionId)` can be implemented.

6. **Real-time execution state stream** — Requires Raj + Ashmit to expose a WebSocket or SSE endpoint from TANTRA that pushes `Executing`, `Waiting`, `Capability Running`, `Completed`, `Failed`, `Retrying` events. The `ExecutionStatusPanel` already handles these events.

7. **Desktop-wide floating mode** — Phase 2 feature. Architecture is ready (dock controller, floating CSS). Implementation requires Electron or similar desktop shell.
