# Deployment Code Packet

**Subsystem:** Deployment  
**Date:** July 2025  
**Status:** Production Ready

---

## Entry Files

| File | Purpose |
|------|---------|
| `backend/Dockerfile` | Docker image build |
| `backend/docker-compose.yml` | Multi-service orchestration |
| `backend/deploy/kubernetes/` | K8s manifests |
| `backend/deploy/grafana/` | Grafana dashboards |
| `backend/deploy/prometheus/` | Prometheus config |

---

## Files Changed

### 1. `backend/Dockerfile` (UNCHANGED)

**Purpose:** Build Docker image for MITRA backend

**Key Features:**
- Multi-stage build for optimization
- Non-root user for security
- Health check included
- Environment variable support

**Integration Impact:**
- Consistent deployment across environments
- Security best practices
- Health monitoring built-in

### 2. `backend/docker-compose.yml` (UNCHANGED)

**Purpose:** Orchestrate all MITRA services

**Services:**
- `mitra-core` - Main FastAPI application
- `mongodb` - Primary database
- `redis` - Caching layer
- `prometheus` - Metrics scraping
- `grafana` - Dashboard visualization
- `otel-collector` - OpenTelemetry collector

**Integration Impact:**
- All services run together
- Consistent environment
- Easy scaling

### 3. `backend/deploy/kubernetes/` (UNCHANGED)

**Purpose:** Kubernetes deployment manifests

**Manifests:**
- `namespace.yml` - Namespace definition
- `deployment.yml` - Application deployment
- `service.yml` - Service definition
- `ingress.yml` - Ingress configuration
- `configmap.yml` - Configuration maps
- `secrets.yml` - Secrets management
- `network-policy.yml` - Network policies

**Integration Impact:**
- Production-ready Kubernetes deployment
- Scalable and resilient
- Secure by default

---

## Deployment Options

### Option 1: Docker Compose (Development)

```bash
cd backend
docker-compose up -d
```

### Option 2: Kubernetes (Production)

```bash
cd backend/deploy/kubernetes
kubectl apply -f namespace.yml
kubectl apply -f deployment.yml
kubectl apply -f service.yml
kubectl apply -f ingress.yml
```

### Option 3: Render (Cloud)

```bash
# Push to GitHub
git push origin main

# Deploy via Render dashboard
```

### Option 4: Vercel (Frontend)

```bash
cd frontend/frontend
vercel deploy
```

---

## Environment Variables

### Backend

| Variable | Description | Default |
|----------|-------------|---------|
| `ENV` | Environment | development |
| `MONGODB_URI` | MongoDB connection | mongodb://localhost:27017 |
| `API_KEY` | API authentication | localtest |
| `JWT_SECRET_KEY` | JWT signing | secret |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `GROQ_API_KEY` | Groq API key | - |

### Frontend

| Variable | Description | Default |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend URL | http://localhost:8000 |
| `REACT_APP_API_KEY` | API key | localtest |

---

## Monitoring Stack

### Prometheus

- **URL:** http://localhost:9090
- **Purpose:** Metrics scraping
- **Targets:** mitra-core, otel-collector

### Grafana

- **URL:** http://localhost:3001
- **Purpose:** Dashboard visualization
- **Dashboards:** MITRA Overview

### OpenTelemetry

- **Port:** 4317 (gRPC), 4318 (HTTP)
- **Purpose:** Distributed tracing
- **Exporter:** OTLP

---

## Scaling

### Horizontal Scaling

```yaml
# kubernetes/deployment.yml
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: mitra-core
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Auto-scaling

```yaml
# kubernetes/hpa.yml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mitra-core
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Security

### Network Policies

```yaml
# kubernetes/network-policy.yml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
spec:
  podSelector:
    matchLabels:
      app: mitra-core
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
```

### Secrets Management

```bash
# Create secrets
kubectl create secret generic mitra-secrets \
  --from-literal=MONGODB_URI=mongodb://... \
  --from-literal=API_KEY=... \
  --from-literal=JWT_SECRET_KEY=...
```

---

## Code Changes Summary

### Unchanged Files
- `backend/Dockerfile`
- `backend/docker-compose.yml`
- `backend/deploy/kubernetes/`
- `backend/deploy/grafana/`
- `backend/deploy/prometheus/`
- `backend/deploy/otel-collector/`

### New Files
- `review_packets/DEPLOYMENT_VERIFICATION.md`

---

## Testing

### Verify Deployment

```bash
# Health check
curl http://localhost:8000/health

# System health
curl http://localhost:8000/health/system

# Prometheus metrics
curl http://localhost:8000/metrics
```

### Load Testing

```bash
cd backend/deploy/loadtest
locust -f locustfile.py --host=http://localhost:8000
```

---

**Code Packet Prepared By:** DevOps Team  
**Last Updated:** July 2025