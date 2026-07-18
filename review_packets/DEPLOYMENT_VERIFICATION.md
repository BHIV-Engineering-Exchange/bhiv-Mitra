# MITRA Deployment Verification Guide

**Document Version:** 1.0.0  
**Date:** July 2025  
**Status:** Production Ready

---

## Quick Start

### 1. Docker Compose Deployment

```bash
# Clone the repository
git clone https://github.com/your-org/MITRA-main.git
cd MITRA-main

# Start all services
cd backend
docker-compose up -d

# Verify services
docker-compose ps
```

### 2. Verify Backend Health

```bash
# Basic health check
curl http://localhost:8000/health

# System health check
curl http://localhost:8000/health/system

# Root endpoint
curl http://localhost:8000/
```

### 3. Verify Frontend

```bash
# Navigate to frontend
cd frontend/frontend

# Install dependencies
npm install

# Start development server
npm start

# Open browser to http://localhost:3000
```

---

## Endpoint Verification

### Authentication Endpoints

```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "securepassword123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "securepassword123"}'

# Get User (with JWT token)
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <your_jwt_token>"
```

### Assistant Endpoint

```bash
# Chat message
curl -X POST http://localhost:8000/api/assistant \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <your_api_key>" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -d '{
    "input": {"message": "Hello, can you help me?"},
    "context": {"platform": "web", "preferred_language": "en"}
  }'
```

### Ecosystem Integration

```bash
# List products
curl http://localhost:8000/api/ecosystem/products \
  -H "X-API-Key: <your_api_key>"

# Get manifests
curl http://localhost:8000/api/ecosystem/manifests \
  -H "X-API-Key: <your_api_key>"

# Health check
curl http://localhost:8000/api/ecosystem/health \
  -H "X-API-Key: <your_api_key>"

# Runtime proof
curl -X POST http://localhost:8000/api/ecosystem/runtime-proof \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <your_api_key>" \
  -d '{"product": "UniGuru", "action": "health_check"}'

# Demonstrate integration
curl -X POST http://localhost:8000/api/ecosystem/demonstrate \
  -H "X-API-Key: <your_api_key>"
```

### Disaster Recovery Replay

```bash
# Generate DR proof
curl -X POST http://localhost:8000/api/replay/{trace_id}/dr-proof \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <your_api_key>" \
  -d '{}'

# Get DR proofs
curl http://localhost:8000/api/replay/dr-proofs \
  -H "X-API-Key: <your_api_key>"

# Get DR summary
curl http://localhost:8000/api/replay/dr-summary \
  -H "X-API-Key: <your_api_key>"
```

### Observability

```bash
# Prometheus metrics
curl http://localhost:8000/metrics

# Grafana dashboard
open http://localhost:3001
```

---

## Expected Responses

### Health Check Response

```json
{
  "status": "ok",
  "version": "3.0.0",
  "mongodb": "ok",
  "timestamp": "2025-07-15T10:30:00Z"
}
```

### System Health Response

```json
{
  "status": "healthy",
  "modules": {
    "database": "connected",
    "redis": "connected",
    "bucket": "active",
    "enforcement": "active",
    "orchestrator": "active"
  },
  "ecosystem": {
    "registered_products": 11,
    "active_adapters": 11
  }
}
```

### Ecosystem Products Response

```json
{
  "status": "ok",
  "products": [
    "UniGuru", "SETU", "Gurukul", "Samruddhi", "NamamiGange",
    "SVACS", "UCCIS", "NYAI", "Brahmanda", "Bucket", "TANTRA"
  ],
  "active_adapters": [],
  "timestamp": "2025-07-15T10:30:00Z"
}
```

### Runtime Proof Response

```json
{
  "status": "ok",
  "proof": {
    "product": "UniGuru",
    "action": "health_check",
    "status": "success",
    "trace_id": "abc123...",
    "timestamp": "2025-07-15T10:30:00Z",
    "latency_ms": 45.2,
    "integrity_hash": "sha256:..."
  },
  "timestamp": "2025-07-15T10:30:00Z"
}
```

### DR Proof Response

```json
{
  "status": "ok",
  "proof": {
    "proof_id": "abc123...",
    "trace_id": "def456...",
    "original_stages_count": 5,
    "replayed_successfully": true,
    "original_hash": "sha256:...",
    "replayed_hash": "sha256:...",
    "integrity_match": true,
    "timestamp": "2025-07-15T10:30:00Z",
    "recovery_time_ms": 125.5
  },
  "timestamp": "2025-07-15T10:30:00Z"
}
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| MongoDB connection failed | Check `MONGODB_URI` env var |
| API key authentication failed | Check `API_KEY` env var |
| JWT token expired | Re-authenticate to get new token |
| Port already in use | Change port in docker-compose.yml |

### Logs

```bash
# View backend logs
docker-compose logs -f mitra-core

# View MongoDB logs
docker-compose logs -f mongodb

# View Redis logs
docker-compose logs -f redis
```

### Reset

```bash
# Stop all services
docker-compose down

# Remove volumes
docker-compose down -v

# Restart
docker-compose up -d
```

---

## Production Checklist

- [ ] Environment variables configured
- [ ] MongoDB replica set initialized
- [ ] Redis configured for caching
- [ ] SSL/TLS certificates installed
- [ ] Monitoring dashboards configured
- [ ] Alerting rules configured
- [ ] Backup strategy implemented
- [ ] Load balancer configured
- [ ] DNS records configured
- [ ] Firewall rules configured

---

**Document Prepared By:** DevOps Team  
**Last Updated:** July 2025