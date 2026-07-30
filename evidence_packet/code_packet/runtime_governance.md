# Runtime Governance

## Health Validation

Each capability type has independent health tracking:
- Rolling window of last 100 latencies
- Status: HEALTHY, DEGRADED, UNHEALTHY
- Auto-degrades after 5+ consecutive failures

## Retry Policy

Configurable per capability type:

| Strategy | Behavior |
|----------|----------|
| NONE | No retries |
| LINEAR | 100ms, 200ms, 300ms... |
| EXPONENTIAL | 100ms, 200ms, 400ms, 800ms... |

Default: 3 retries with exponential backoff, max 5s delay.

## Cancellation

Cooperative cancellation via `CancellationToken`:
```python
POST /api/tantra/cancel/{trace_id}?reason=user_requested
```

Checks cancellation at:
- Precondition validation
- Before each retry attempt

## Failure Propagation

Every failure generates a `FailureContract` with:
- failure_id (deterministic SHA-256)
- failure_type and failure_code
- capability_type and trace_id
- is_retryable flag
- Full context for debugging

## Observability Hooks

Every execution generates InsightFlow telemetry events:
- execution.received
- enforcement.evaluated
- capability.dispatched
- capability.completed
- execution.failed
- execution.completed
- bucket.logged
