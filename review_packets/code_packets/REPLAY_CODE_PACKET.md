# Replay System Code Packet

**Subsystem:** Replay System  
**Date:** July 2025  
**Status:** Production Ready

---

## Entry Files

| File | Purpose |
|------|---------|
| `backend/app/replay/harness.py` | Trace replay and DR proof |
| `backend/app/api/replay.py` | Replay API endpoints |

---

## Files Changed

### 1. `backend/app/replay/harness.py` (ENHANCED)

**Purpose:** Disaster recovery replay proof generation

**Key Changes:**
- Added `DisasterRecoveryProof` dataclass
- Added `replay_with_dr_proof()` method
- Added `get_dr_proofs()` for proof retrieval
- Added `verify_dr_proof_integrity()` for verification
- Added `get_dr_summary()` for metrics

**Integration Impact:**
- System recoverability is now verifiable
- DR proofs are integrity-verified
- Recovery time is now measurable

### 2. `backend/app/api/replay.py` (ENHANCED)

**Purpose:** Replay API endpoints with DR proof support

**Key Changes:**
- Added `/api/replay/{trace_id}/dr-proof` endpoint
- Added `/api/replay/dr-proofs` endpoint
- Added `/api/replay/dr-proof/{trace_id}` endpoint
- Added `/api/replay/verify-dr-proof/{trace_id}` endpoint
- Added `/api/replay/dr-summary` endpoint

**Integration Impact:**
- DR proofs are now API-accessible
- DR proof verification is now possible
- DR metrics are now available

---

## Integration Points

### Replay Flow

```
Request Trace ID
    ↓
[Load Original Trace]
    ↓
[Extract Original Request]
    ↓
[Apply Modifications]
    ↓
[Replay Through Pipeline]
    ↓
[Generate DR Proof]
    ↓
[Return Proof]
```

### Disaster Recovery Proof

```python
@dataclass
class DisasterRecoveryProof:
    proof_id: str
    trace_id: str
    original_stages_count: int
    replayed_successfully: bool
    original_hash: str
    replayed_hash: str
    integrity_match: bool
    timestamp: str
    recovery_time_ms: float
    error: Optional[str] = None
```

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/replay/{trace_id}` | POST | Replay trace |
| `/api/replay/{trace_id}/stages` | GET | Get trace stages |
| `/api/replay/compare` | POST | Compare traces |
| `/api/replay/{trace_id}/dr-proof` | POST | Generate DR proof |
| `/api/replay/dr-proofs` | GET | Get all DR proofs |
| `/api/replay/dr-proof/{trace_id}` | GET | Get DR proof by trace_id |
| `/api/replay/verify-dr-proof/{trace_id}` | POST | Verify DR proof |
| `/api/replay/dr-summary` | GET | Get DR summary |

---

## Usage Examples

### Generate DR Proof

```python
from app.replay.harness import ReplayHarness

harness = ReplayHarness()

proof = await harness.replay_with_dr_proof(
    trace_id="abc123",
    modifications={"input.message": "Modified message"}
)

print(proof.replayed_successfully)
print(proof.recovery_time_ms)
```

### Verify DR Proof

```python
from app.replay.harness import ReplayHarness

harness = ReplayHarness()

proof = harness.get_dr_proof_by_trace_id("abc123")
is_valid = harness.verify_dr_proof_integrity(proof)

print(is_valid)
```

### Get DR Summary

```python
from app.replay.harness import ReplayHarness

harness = ReplayHarness()

summary = harness.get_dr_summary()
print(summary)
```

---

## Code Changes Summary

### Modified Files
- `backend/app/replay/harness.py`
- `backend/app/api/replay.py`

### Added Classes
- `DisasterRecoveryProof` - DR proof dataclass

### Added Methods
- `replay_with_dr_proof()` - Generate DR proof
- `get_dr_proofs()` - Retrieve DR proofs
- `get_dr_proof_by_trace_id()` - Get proof by trace_id
- `verify_dr_proof_integrity()` - Verify proof integrity
- `get_dr_summary()` - Get DR metrics

### Added Endpoints
- `/api/replay/{trace_id}/dr-proof`
- `/api/replay/dr-proofs`
- `/api/replay/dr-proof/{trace_id}`
- `/api/replay/verify-dr-proof/{trace_id}`
- `/api/replay/dr-summary`

---

## Testing

### Unit Tests

```bash
cd backend
python -m pytest tests/test_replay.py -v
```

### Integration Tests

```bash
cd backend
python -m pytest tests/test_end_to_end.py -v
```

---

**Code Packet Prepared By:** Replay Team  
**Last Updated:** July 2025