# Governance Contract (GC)

## Constitutional Principles

1. **Sole Execution Runtime**: TANTRA is the ONLY execution runtime for MITRA. No direct execution paths are permitted.

2. **Fail-Closed**: Missing enforcement verdict → BLOCK. Missing bucket artifact → BLOCK. Kill switch → TERMINATE.

3. **Immutable Policy**: RL signals can adjust confidence but never override enforcement decisions.

4. **Gateway Auth**: Every executor call requires an HMAC-signed gateway token from TANTRA.

5. **Complete Traceability**: Every execution generates a deterministic SHA-256 trace_id that follows it through every stage.

6. **Bucket as Truth**: MongoDB stores every stage with integrity hashes for replay and governance.

7. **Observability**: No execution is invisible. InsightFlow captures every lifecycle event.

## Registry Participation

TANTRA integrates with constitutional registries as a governed orchestration layer:
- **Execution Registry**: Records every execution attempt
- **Capability Registry**: Validates capability availability
- **Replay Registry**: Stores replay metadata
- **Review Registry**: Tracks governance review states

TANTRA does NOT own these registries — it orchestrates through them.

## Enforcement Hierarchy

```
EnforcementVerdict (frozen dataclass)
  -> TANTRA Runtime (applies verdict)
    -> Capability Executor (validates gateway auth)
      -> Platform Executor (real-world action)
```

No component may override the enforcement verdict.
