# Module Design Unit (MDU)

## TANTRA Package Structure

```
app/tantra/
├── __init__.py          # Package exports
├── contracts.py         # Canonical execution contracts (8 dataclasses)
├── runtime.py           # Sole execution engine (TantraRuntime)
├── state_machine.py     # Deterministic lifecycle (ExecutionStateMachine)
├── governance.py        # Runtime governance (health, retry, cancel)
├── registry.py          # Constitutional registry integration (9 registries)
├── insightflow.py       # Observability telemetry (InsightFlow)
└── api.py               # FastAPI endpoints (/api/tantra/*)
```

## Contract Hierarchy

```
ExecutionRequest
├── TraceMetadata        # Deterministic trace_id, span_id
├── ExecutionContext     # Platform, user, enforcement, policy
├── CapabilityType       # Enum: whatsapp, email, telegram, etc.
└── action, payload      # Operation-specific data

ExecutionResult
├── TraceMetadata        # Same trace_id follows through
├── ExecutionStatus      # Terminal state
├── ExecutionDecision    # Enforcement verdict
├── CapabilityInvocation # What was executed
├── FailureContract      # What went wrong
├── ReplayMetadata       # For replay support
└── integrity_hash       # SHA-256 integrity
```

## State Machine

```
PENDING -> DISPATCHED -> IN_PROGRESS -> COMPLETED
                       -> FAILED
                       -> BLOCKED
                       -> CANCELLED
                       -> TIMED_OUT
                       -> TERMINATED
```

## Data Flow

1. Orchestrator creates ExecutionRequest from legacy parameters
2. TANTRA Runtime validates preconditions via Governance
3. Enforcement gate applied via state machine
4. Capability Executor dispatches to platform executor
5. Gateway Auth token issued and verified
6. Result recorded to Bucket with integrity hash
7. InsightFlow telemetry captured
8. Constitutional Registry updated
9. ExecutionResult returned to orchestrator
