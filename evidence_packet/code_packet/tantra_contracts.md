# TANTRA Contracts Documentation

## ExecutionRequest

The canonical execution request — the ONLY supported execution interface.

```python
@dataclass
class ExecutionRequest:
    trace_metadata: TraceMetadata      # Deterministic trace_id
    context: ExecutionContext           # Platform, user, enforcement
    capability_type: CapabilityType    # whatsapp, email, etc.
    action: str                        # Operation to execute
    payload: Dict[str, Any]            # Operation data
    action_data: Dict[str, Any]        # Full action data
    timeout_seconds: int = 30          # Execution timeout
    max_retries: int = 3               # Retry limit
    priority: int = 0                  # Execution priority
    created_at: str                    # ISO timestamp
```

## ExecutionResult

The canonical execution result returned by TANTRA Runtime.

```python
@dataclass
class ExecutionResult:
    trace_metadata: TraceMetadata      # Same trace_id
    status: ExecutionStatus            # Terminal state
    decision: ExecutionDecision        # Enforcement verdict
    response_data: Dict[str, Any]      # Execution output
    invocations: List[CapabilityInvocation]  # What was executed
    failures: List[FailureContract]    # What went wrong
    replay_metadata: Optional[ReplayMetadata]  # For replay
    telemetry: Dict[str, Any]          # InsightFlow data
    total_latency_ms: float            # End-to-end latency
    integrity_hash: str                # SHA-256 integrity
```

## ExecutionStatus

11 lifecycle states with deterministic transitions:

```
PENDING → DISPATCHED → IN_PROGRESS → COMPLETED
                       → FAILED
                       → BLOCKED
                       → DELAYED
                       → REWRITE
                       → CANCELLED
                       → TIMED_OUT
                       → TERMINATED
```

## CapabilityType

Enum of supported execution capabilities:

```python
class CapabilityType(str, Enum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    TELEGRAM = "telegram"
    INSTAGRAM = "instagram"
    CALENDAR = "calendar"
    REMINDER = "reminder"
    EMS = "ems"
    DEVICE_GATEWAY = "device_gateway"
    ECOSYSTEM_PRODUCT = "ecosystem_product"
    LLM_INVOCATION = "llm_invocation"
    CUSTOM = "custom"
```

## Integrity

Every `ExecutionResult` computes a SHA-256 integrity hash from:
- trace_id
- status
- decision
- invocation_count
- failure_count
- completed_at

This hash is stored in Bucket for tamper detection and replay verification.
