# API Samples

This directory contains sample request and response payloads from the MITRA backend API.

## Sample 1 — Health Check

**Request:**
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "3.0.0"
}
```

---

## Sample 2 — Send Message

**Request:**
```
POST /api/assistant
Content-Type: application/json
X-API-Key: bhiv-enterprise-key

{
  "version": "3.0.0",
  "input": {
    "message": "What can MITRA do?"
  },
  "context": {
    "platform": "web",
    "device": "desktop",
    "session_id": "mitra-session-1722230400000-abc123"
  }
}
```

**Response:**
```json
{
  "final_output": {
    "reason": "MITRA can help you with tasks across the BHIV ecosystem, including Gurukul, Samruddhi, and SETU..."
  },
  "trace_id": "trace-xyz-001",
  "session_id": "mitra-session-1722230400000-abc123"
}
```

---

## Sample 3 — Capability Execution

**Request:**
```
POST /api/mitra/evaluate
Content-Type: application/json
X-API-Key: bhiv-enterprise-key

{
  "input": {
    "message": "Execute capability: analyze"
  },
  "context": {
    "platform": "web",
    "device": "desktop",
    "session_id": "mitra-session-1722230400000-abc123"
  }
}
```

**Response:**
```json
{
  "response": "Analysis capability executed successfully.",
  "trace_id": "trace-xyz-002",
  "execution": {
    "status": "completed",
    "capability": "analyze"
  }
}
```

---

## Live API Samples

See the backend directory for live captured JSON:
- `backend/MITRA_CONTROL_PLANE_LIVE_JSON.json`
- `backend/email_execution_response.json`
- `backend/whatsapp_execution_response.json`
- `backend/FULL_SYSTEM_TRACE.json`
