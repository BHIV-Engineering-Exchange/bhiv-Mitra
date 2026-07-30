# Bucket & Replay Integration

## Bucket Stages

Every TANTRA execution records two stages to Bucket:

### 1. `tantra_execution`
```json
{
  "trace_id": "trace_abc123",
  "capability_type": "email",
  "action": "send_message",
  "status": "completed",
  "decision": "ALLOW",
  "latency_ms": 245.67,
  "integrity_hash": "sha256...",
  "state_timeline": [...],
  "invocation_count": 1,
  "failure_count": 0
}
```

### 2. `tantra_insightflow`
```json
{
  "trace_id": "trace_abc123",
  "events": [...],
  "execution_started_at": "2026-07-29T...",
  "execution_completed_at": "2026-07-29T...",
  "total_latency_ms": 245.67,
  "status": "completed",
  "telemetry_hash": "sha256..."
}
```

## Replay Support

### ReplayMetadata
Stored alongside execution artifacts:
```python
@dataclass
class ReplayMetadata:
    original_trace_id: str
    replay_count: int = 0
    last_replayed_at: Optional[str] = None
    replay_hash: Optional[str] = None
    integrity_verified: bool = False
```

### Replay Flow
1. Load trace from Bucket via `BucketService.get_trace_logs(trace_id)`
2. Extract original request from `mitra_request_log` stage
3. Reconstruct `ExecutionRequest` with replay context
4. Execute through TANTRA Runtime
5. Record replay in Replay Registry
6. Compare original vs replayed integrity hashes

## Integrity Verification

Every `ExecutionResult` computes a SHA-256 integrity hash:
```python
canonical = {
    "trace_id": trace_id,
    "status": status,
    "decision": decision,
    "invocation_count": len(invocations),
    "failure_count": len(failures),
    "completed_at": completed_at,
}
return hashlib.sha256(json.dumps(canonical, sort_keys=True).encode()).hexdigest()
```

This hash is stored in Bucket and can be verified during replay.
