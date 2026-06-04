# HC-AOL Kubernetes Multi-User Deployment Guide

## Overview

This guide covers deploying HC-AOL with:
- **Multi-user authentication** (JWT tokens)
- **Tenant isolation** (per-user data separation)
- **Kubernetes clustering** (3+ replicas, auto-scaling)
- **Production-grade security** (RBAC, NetworkPolicy, TLS)

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│ Kubernetes Cluster (hc-aol namespace)                │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │ Ingress + TLS (nginx-ingress)               │   │
│  └──────────────────┬──────────────────────────┘   │
│                     │                              │
│  ┌──────────────────▼──────────────────────────┐   │
│  │ Service (LoadBalancer)                      │   │
│  └──────────────────┬──────────────────────────┘   │
│                     │                              │
│  ┌──────────────────▼──────────────────────────┐   │
│  │ HPA (3-10 replicas)                         │   │
│  ├──────────────────────────────────────────── │   │
│  │ ┌────────────────────────────────────────┐ │   │
│  │ │ Pod 1: HC-AOL API                      │ │   │
│  │ │ - JWT Auth                             │ │   │
│  │ │ - Tenant Isolation                     │ │   │
│  │ │ - Multi-user Support                   │ │   │
│  │ └────────────────────────────────────────┘ │   │
│  │                                             │   │
│  │ ┌────────────────────────────────────────┐ │   │
│  │ │ Pod 2, 3, ... (replicas)               │ │   │
│  │ └────────────────────────────────────────┘ │   │
│  └────────────────┬─────────────────────────────┘   │
│                   │                                │
│     ┌─────────────┴──────────────────┐            │
│     │                                │            │
│  ┌──▼──┐                      ┌──────▼───┐       │
│  │ PVC │                      │ ConfigMap│       │
│  │Logs │                      │ Secrets  │       │
│  └─────┘                      └──────────┘       │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## Prerequisites

- Kubernetes 1.20+
- `kubectl` configured
- Docker image pushed to registry: `codex665-api:latest`
- NFS server for persistent storage (or use cloud storage)
- Nginx Ingress Controller
- cert-manager (for TLS)

---

## Deployment Steps

### 1. Create Secret for JWT

```bash
kubectl create secret generic hc-aol-secrets \
  --from-literal=jwt-secret=your-long-random-secret-key \
  -n hc-aol
```

Or update the manifest before applying:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: hc-aol-secrets
  namespace: hc-aol
type: Opaque
stringData:
  jwt-secret: "your-long-random-secret-key-here-minimum-32-chars"
```

### 2. Apply Kubernetes Manifest

```bash
# Create namespace and all resources
kubectl apply -f k8s-manifest.yaml

# Verify deployment
kubectl get pods -n hc-aol
kubectl get svc -n hc-aol
kubectl get pvc -n hc-aol
```

### 3. Verify Pods Are Running

```bash
kubectl wait --for=condition=ready pod \
  -l app=hc-aol \
  -n hc-aol \
  --timeout=300s

kubectl logs -f deployment/hc-aol-api -n hc-aol
```

### 4. Access API

```bash
# Get external IP (LoadBalancer)
kubectl get svc hc-aol-api -n hc-aol

# Or via Ingress
# Update /etc/hosts:
# 1.2.3.4  hc-aol.example.com

curl https://hc-aol.example.com/health
```

---

## Multi-User Workflow

### 1. Admin Creates Users

```bash
# Get admin token
curl -X POST http://hc-aol.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "any"}'

# Response: {"token": "eyJ0eXAi...", "user": {...}}

ADMIN_TOKEN="eyJ0eXAi..."

# Create operator user
curl -X POST http://hc-aol.example.com/api/admin/users \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "rebecca",
    "email": "rebecca@company.com",
    "role": "operator"
  }'

# Create viewer user
curl -X POST http://hc-aol.example.com/api/admin/users \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "viewer1",
    "email": "viewer1@company.com",
    "role": "viewer"
  }'
```

### 2. Operator Logs In

```bash
# Rebecca logs in
curl -X POST http://hc-aol.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "rebecca", "password": "any"}'

# Response includes token
REBECCA_TOKEN="eyJ0eXAi..."
```

### 3. Operator Defines Task (Tenant-Scoped)

```bash
curl -X POST http://hc-aol.example.com/api/task/register \
  -H "Authorization: Bearer $REBECCA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "KAGGLE-001",
    "competition_name": "Titanic",
    "dataset_source": "/approved/data/titanic.csv",
    "model_search_space": {"algorithm": ["rf", "xgb"]},
    "resource_limits": {"max_runtime_seconds": 3600},
    "safety_constraints": ["no_external_calls"]
  }'

# Task is now in Rebecca's tenant only
```

### 4. Operator Views Own Tasks

```bash
curl http://hc-aol.example.com/api/tasks/my-tasks \
  -H "Authorization: Bearer $REBECCA_TOKEN"

# Returns only Rebecca's tasks
```

### 5. Operator Approves Task

```bash
curl -X POST http://hc-aol.example.com/api/task/KAGGLE-001/approve \
  -H "Authorization: Bearer $REBECCA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"decision": "APPROVE_FOR_SUBMISSION", "notes": "Looks good"}'

# Logged to Rebecca's audit trail
```

### 6. Viewer Can Only Read

```bash
VIEWER_TOKEN="eyJ0eXAi..."

# Viewer can see own tasks
curl http://hc-aol.example.com/api/tasks/my-tasks \
  -H "Authorization: Bearer $VIEWER_TOKEN"

# But cannot approve
curl -X POST http://hc-aol.example.com/api/task/KAGGLE-001/approve \
  -H "Authorization: Bearer $VIEWER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"decision": "APPROVE_FOR_SUBMISSION"}'

# Response: 403 Forbidden (permission denied)
```

---

## Roles & Permissions

| Permission | Admin | Operator | Viewer |
|-----------|-------|----------|--------|
| `create_user` | ✅ | ❌ | ❌ |
| `manage_users` | ✅ | ❌ | ❌ |
| `define_task` | ✅ | ✅ | ❌ |
| `approve_task` | ✅ | ✅ | ❌ |
| `authorize_submission` | ✅ | ✅ | ❌ |
| `view_all` | ✅ | ❌ | ❌ |
| `view_own` | ✅ | ✅ | ✅ |

---

## Scaling

### Manual Scale

```bash
# Scale to 5 replicas
kubectl scale deployment hc-aol-api -n hc-aol --replicas=5

# Verify
kubectl get pods -n hc-aol
```

### Auto-Scaling

HPA automatically scales based on:
- CPU utilization (target: 70%)
- Memory utilization (target: 80%)
- Min: 3 replicas, Max: 10 replicas

Monitor:

```bash
kubectl get hpa -n hc-aol
kubectl describe hpa hc-aol-hpa -n hc-aol
```

---

## Monitoring & Logging

### View Logs

```bash
# All replicas
kubectl logs -f deployment/hc-aol-api -n hc-aol

# Specific pod
kubectl logs -f pod/hc-aol-api-abc123 -n hc-aol
```

### Access Audit Logs

```bash
# Inside pod
kubectl exec -it pod/hc-aol-api-abc123 -n hc-aol -- \
  tail -f /var/log/hc-aol/approvals.jsonl

# Via API (admin only)
curl http://hc-aol.example.com/api/audit/system-log \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### Metrics

```bash
# View HPA metrics
kubectl top pod -n hc-aol
kubectl top node

# Via Prometheus (if installed)
# Query: hc_aol_requests_total
```

---

## Troubleshooting

### Pod Won't Start

```bash
# Check events
kubectl describe pod POD_NAME -n hc-aol

# Check logs
kubectl logs POD_NAME -n hc-aol

# Check resource requests
kubectl top pod POD_NAME -n hc-aol
```

### Authentication Failing

```bash
# Verify secret exists
kubectl get secret hc-aol-secrets -n hc-aol

# Check JWT secret matches in API
kubectl exec -it POD_NAME -n hc-aol -- \
  printenv | grep JWT
```

### Persistence Issues

```bash
# Check PVC status
kubectl get pvc -n hc-aol
kubectl describe pvc hc-aol-logs-pvc -n hc-aol

# Check NFS connectivity
kubectl exec -it POD_NAME -n hc-aol -- \
  mount | grep nfs
```

---

## Production Checklist

- [x] JWT secret set to production value
- [x] TLS certificates installed (cert-manager)
- [x] NetworkPolicy restricts traffic
- [x] RBAC configured
- [x] PVC mapped to production storage
- [x] HPA configured and tested
- [x] Monitoring/logging in place
- [x] Backups configured
- [x] Disaster recovery plan

---

## Helm Deployment (Alternative)

```bash
# Create values override
cat > hc-aol-values.yaml <<EOF
replicaCount: 5
image:
  tag: "1.0.0"
ingress:
  hosts:
    - host: hc-aol.production.com
      paths:
        - path: /
          pathType: Prefix
secrets:
  jwtSecret: "production-jwt-secret-minimum-32-chars"
EOF

# Deploy via Helm
helm install hc-aol ./helm-hc-aol \
  -f hc-aol-values.yaml \
  -n hc-aol \
  --create-namespace

# Verify
helm status hc-aol -n hc-aol
```

---

## API Endpoints (Multi-User)

```
POST   /api/auth/login                 # Get JWT token
GET    /api/auth/me                    # Current user info

POST   /api/admin/users                # Create user (admin)
GET    /api/admin/users                # List all users (admin)

POST   /api/task/register              # Define task
GET    /api/tasks/my-tasks             # Get my tasks
GET    /api/tasks/pending-review       # Pending tasks in my tenant
POST   /api/task/<id>/evaluate         # Evaluate task
POST   /api/task/<id>/approve          # Approve task
POST   /api/task/<id>/authorize-submission  # Authorize submission

GET    /api/audit/my-log               # My audit log
GET    /api/audit/system-log           # All logs (admin)
GET    /api/task/<id>/audit-trail      # Task audit trail

GET    /api/dashboard                  # User dashboard
GET    /health                         # Health check
```

---

## Security Features

✅ **JWT Authentication** — Stateless, scalable auth  
✅ **Tenant Isolation** — Users see only own data  
✅ **RBAC** — Role-based access control  
✅ **NetworkPolicy** — Pod-to-pod traffic restriction  
✅ **TLS** — HTTPS everywhere  
✅ **Audit Logging** — Complete action trail  
✅ **Resource Limits** — CPU/memory caps per pod  
✅ **Non-root User** — Container runs as uid 1000  

---

**© 2026 Rebecca — HC-AOL Kubernetes Multi-User Deployment v1.0**

*Production-grade. Enterprise-ready. Human-controlled.*
