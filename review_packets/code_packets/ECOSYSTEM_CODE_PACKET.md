# Ecosystem Adapters Code Packet

**Subsystem:** Ecosystem Adapters  
**Date:** July 2025  
**Status:** Production Ready

---

## Entry Files

| File | Purpose |
|------|---------|
| `backend/app/ecosystem/base_adapter.py` | Canonical adapter interface |
| `backend/app/ecosystem/adapter_registry.py` | Adapter discovery and management |

---

## Files Changed

### 1. `backend/app/ecosystem/base_adapter.py` (UNCHANGED)

**Purpose:** Define canonical interface for all BHIV product adapters

**Key Classes:**
- `BaseBHIVAdapter` - Abstract base class
- `IntegrationManifest` - Product integration contract
- `IntegrationRequest` - Canonical request format
- `IntegrationResponse` - Canonical response format
- `AdapterHealth` - Health tracking

**Integration Impact:**
- All adapters follow canonical interface
- All adapters are discoverable via registry
- All adapters provide health checks

### 2. `backend/app/ecosystem/adapter_registry.py` (UNCHANGED)

**Purpose:** Central registry for all BHIV product adapters

**Key Features:**
- Singleton pattern for single instance
- Lazy instantiation of adapters
- Health monitoring per adapter
- Discovery of all registered products

**Integration Impact:**
- All 11 products are registered
- All adapters are discoverable
- Health status is trackable

### 3. Individual Adapter Files (UNCHANGED)

| Adapter | File | Product |
|---------|------|---------|
| UniGuru | `backend/app/ecosystem/adapters/uniguru_adapter.py` | Learning & Education |
| Gurukul | `backend/app/ecosystem/adapters/gurukul_adapter.py` | Knowledge & Curriculum |
| SETU | `backend/app/ecosystem/adapters/setu_adapter.py` | Bridge Platform |
| Samruddhi | `backend/app/ecosystem/adapters/samruddhi_adapter.py` | Prosperity Platform |
| Namami Gange | `backend/app/ecosystem/adapters/namami_gange_adapter.py` | River Conservation |
| SVACS | `backend/app/ecosystem/adapters/svacs_adapter.py` | Validation Service |
| UCCIS | `backend/app/ecosystem/adapters/uccis_adapter.py` | Integration Service |
| NYAI | `backend/app/ecosystem/adapters/nyai_adapter.py` | AI Platform |
| Brahmanda | `backend/app/ecosystem/adapters/brahmanda_adapter.py` | Universe Platform |
| Bucket | `backend/app/ecosystem/adapters/bucket_adapter.py` | Storage Platform |
| TANTRA | `backend/app/ecosystem/adapters/tantra_adapter.py` | Framework Platform |

---

## Integration Points

### Adapter Interface

```python
class BaseBHIVAdapter(ABC):
    @property
    @abstractmethod
    def product_name(self) -> str:
        """Name of the BHIV product this adapter connects to."""
        ...

    @abstractmethod
    def _create_manifest(self) -> IntegrationManifest:
        """Define the canonical integration manifest for this product."""
        ...

    @abstractmethod
    async def query(self, request: IntegrationRequest) -> IntegrationResponse:
        """Query data from the BHIV product."""
        ...

    @abstractmethod
    async def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        """Execute an action on the BHIV product."""
        ...

    async def health_check(self) -> Dict[str, Any]:
        """Check adapter health status."""
        return self._health.to_dict()
```

### Registry Interface

```python
class AdapterRegistry:
    def register_adapter_class(self, product_name: str, adapter_class: Type[BaseBHIVAdapter]):
        """Register an adapter class (lazy instantiation)."""

    def get_adapter(self, product_name: str) -> Optional[BaseBHIVAdapter]:
        """Get or instantiate an adapter for a BHIV product."""

    def list_products(self) -> List[str]:
        """List all registered BHIV products."""

    async def health_check_all(self) -> Dict[str, Any]:
        """Get health status of all active adapters."""
```

---

## Data Structures

### IntegrationManifest

```python
class IntegrationManifest:
    product_name: str
    protocol: IntegrationProtocol
    base_url: Optional[str]
    capabilities: List[AdapterCapability]
    auth_type: str
    timeout_seconds: int
    retry_count: int
    rate_limit_per_minute: int
    event_topics: List[str]
    created_at: str
    version: str
```

### IntegrationRequest

```python
class IntegrationRequest:
    action: str
    payload: Dict[str, Any]
    trace_id: str
    source_product: str
    target_product: str
    user_id: Optional[str]
    session_id: Optional[str]
    authority_token: Optional[str]
    timestamp: str
```

### IntegrationResponse

```python
class IntegrationResponse:
    success: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    trace_id: str
    source_product: str
    latency_ms: float
    timestamp: str
```

---

## Usage Examples

### Query Product

```python
from app.ecosystem.adapter_registry import AdapterRegistry

registry = AdapterRegistry()
adapter = registry.get_adapter("UniGuru")

request = IntegrationRequest(
    action="get_courses",
    payload={"user_id": "123"},
    trace_id="abc123",
    source_product="mitra",
    target_product="UniGuru",
)

response = await adapter.query(request)
```

### Execute Product Action

```python
from app.ecosystem.adapter_registry import AdapterRegistry

registry = AdapterRegistry()
adapter = registry.get_adapter("Gurukul")

request = IntegrationRequest(
    action="enroll_course",
    payload={"course_id": "456"},
    trace_id="def456",
    source_product="mitra",
    target_product="Gurukul",
    user_id="123",
)

response = await adapter.execute(request)
```

### Health Check

```python
from app.ecosystem.adapter_registry import AdapterRegistry

registry = AdapterRegistry()
health = await registry.health_check_all()
```

---

## Testing

### Unit Tests

```bash
cd backend
python -m pytest tests/test_ecosystem.py -v
```

### Integration Tests

```bash
cd backend
python -m pytest tests/test_end_to_end.py -v
```

---

**Code Packet Prepared By:** Integration Team  
**Last Updated:** July 2025