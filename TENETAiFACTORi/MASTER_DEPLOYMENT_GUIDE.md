# MASTER DEPLOYMENT GUIDE
# Codex 6.65: HC-AOL Complete System
# © 2026 Rebecca

## Quick Navigation

- **Want to start NOW?** → Jump to [Fast Start](#fast-start)
- **Need local development?** → [Local Setup](#local-setup)
- **Docker deployment?** → [Docker Deployment](#docker-deployment)
- **Kubernetes?** → [Kubernetes Deployment](#kubernetes-deployment)
- **Multi-user needed?** → [Multi-User Setup](#multi-user-setup)
- **Integration with Kaggle?** → [Integration](#integration-with-kagglearicrowd)

---

## System Overview

**What you have:**
- Codex 6.65 computational engine
- Three-ring consensus framework (Validator/Sovereign/TENET)
- HC-AOL human-controlled orchestration
- Multi-user authentication (JWT)
- Kubernetes deployment (3-10 replicas)
- Enterprise monitoring & audit

**What it does:**
- Humans define AI competition tasks
- System evaluates via three rings
- Humans approve/reject decisions
- Humans authorize submissions
- Complete audit trail maintained

**Key guarantee:** No autonomous actions. Ever.

---

## Fast Start (5 minutes)

### Option A: Python Direct

```bash
# Install dependencies
pip install -r requirements-multiuser.txt

# Start API
python hc_aol_multiuser_api.py

# In another terminal: test
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "any"}'

# Response: {"token": "eyJ0eXAi...", "user": {...}}
```

### Option B: Docker

```bash
# Build
docker build -t codex665-api:latest .
docker build -f Dockerfile.api -t codex665-api:latest .

# Run
docker compose up -d

# Test
curl http://localhost:8000/health
```

### Option C: Kubernetes

```bash
# Create secret
kubectl create secret generic hc-aol-secrets \
  --from-literal=jwt-secret=dev-secret-key \
  -n hc-aol

# Deploy
kubectl apply -f k8s-manifest.yaml

# Check
kubectl get pods -n hc-aol
```

---

## Local Setup

### Prerequisites

```bash
python 3.10+
pip
git
```

### Installation

```bash
# Clone/download repository
git clone https://github.com/yourname/codex665.git
cd codex665

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-multiuser.txt

# Run example
python hc_aol_implementation.py

# See complete workflow with human approvals
```

### Testing

```bash
# Run test suite
python -m pytest test_three_ring_consensus.py -v

# Output: 13 passed
```

---

## Docker Deployment

### Build Images

```bash
# Build engine container
docker build -t codex665:latest .

# Build API container
docker build -f Dockerfile.api -t codex665-api:latest .

# Verify
docker images | grep codex665
```

### Single Container

```bash
docker run -p 8000:8000 \
  -e JWT_SECRET=dev-secret \
  -v ./logs:/logs \
  codex665-api:latest
```

### Docker Compose

```bash
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f hc_aol_api

# Stop
docker compose down
```

### Multi-User Docker

```bash
# Build multi-user variant
docker build -f Dockerfile.api -t codex665-api:multiuser .

# Run with compose
docker compose -f docker-compose.human-controlled.yml up -d

# Access API
curl http://localhost:8000/api/health
```

---

## Kubernetes Deployment

### Prerequisites

```bash
kubectl 1.20+
Kubernetes cluster (local, cloud, or on-prem)
```

### One-Command Deploy

```bash
# 1. Create namespace and secret
kubectl create namespace hc-aol
kubectl create secret generic hc-aol-secrets \
  --from-literal=jwt-secret=your-production-secret-key \
  -n hc-aol

# 2. Apply manifests
kubectl apply -f k8s-manifest.yaml

# 3. Wait for pods
kubectl wait --for=condition=ready pod \
  -l app=hc-aol \
  -n hc-aol \
  --timeout=300s

# 4. Get external IP
kubectl get svc hc-aol-api -n hc-aol

# 5. Test
curl http://EXTERNAL_IP/api/health
```

### Helm Deploy

```bash
# Create custom values
cat > hc-aol-prod-values.yaml <<EOF
replicaCount: 5
image:
  tag: "1.0.0"
ingress:
  enabled: true
  hosts:
    - host: hc-aol.production.com
EOF

# Install
helm install hc-aol ./helm-hc-aol \
  -f hc-aol-prod-values.yaml \
  -n hc-aol \
  --create-namespace

# Verify
helm status hc-aol -n hc-aol
```

### Scale

```bash
# Manual scale
kubectl scale deployment hc-aol-api -n hc-aol --replicas=10

# Auto-scaling (HPA) already enabled
kubectl get hpa -n hc-aol
```

---

## Multi-User Setup

### Create Admin User (Already Done)

```bash
# Admin user created automatically:
# Username: admin
# Role: admin
```

### Create Operator User

```bash
# Get admin token
ADMIN_TOKEN=$(curl -s -X POST http://hc-aol.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"any"}' | jq -r '.token')

# Create operator
curl -X POST http://hc-aol.example.com/api/admin/users \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "rebecca",
    "email": "rebecca@company.com",
    "role": "operator"
  }'
```

### Create Viewer User

```bash
curl -X POST http://hc-aol.example.com/api/admin/users \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "viewer1",
    "email": "viewer1@company.com",
    "role": "viewer"
  }'
```

### User Logs In

```bash
# Rebecca logs in
REBECCA_TOKEN=$(curl -s -X POST http://hc-aol.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"rebecca","password":"any"}' | jq -r '.token')

echo $REBECCA_TOKEN
```

---

## Complete Workflow

### 1. Human Defines Task

```bash
curl -X POST http://hc-aol.example.com/api/task/register \
  -H "Authorization: Bearer $REBECCA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "KAGGLE-TITANIC-001",
    "competition_name": "Kaggle Titanic Survival",
    "dataset_source": "/approved/data/titanic.csv",
    "model_search_space": {
      "algorithm": ["logistic_regression", "random_forest", "xgboost"],
      "max_depth": [3, 5, 7, 10]
    },
    "resource_limits": {
      "max_runtime_seconds": 3600,
      "max_memory_mb": 2048
    },
    "safety_constraints": ["no_external_calls", "local_files_only"]
  }'
```

### 2. System Evaluates

```bash
curl -X POST http://hc-aol.example.com/api/task/KAGGLE-TITANIC-001/evaluate \
  -H "Authorization: Bearer $REBECCA_TOKEN"

# Output: Validator: ACCEPT | Sovereign: ACCEPT | TENET: ACCEPT | Final: ACCEPT
```

### 3. Human Reviews

```bash
curl http://hc-aol.example.com/api/tasks/pending-review \
  -H "Authorization: Bearer $REBECCA_TOKEN"

# Shows: [{ task_id, evaluation, requires_review }]
```

### 4. Human Approves

```bash
curl -X POST http://hc-aol.example.com/api/task/KAGGLE-TITANIC-001/approve \
  -H "Authorization: Bearer $REBECCA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "APPROVE_FOR_SUBMISSION",
    "notes": "Task looks good. All constraints are strict."
  }'
```

### 5. System Runs (with approved parameters)

```bash
# System evaluates model options:
# - Tests: logistic_regression, random_forest, xgboost
# - Finds best: XGBoost with max_depth=7
# - Predicted score: 0.82
# - Resource usage: 450s CPU, 512MB RAM
```

### 6. Human Authorizes Submission

```bash
curl -X POST http://hc-aol.example.com/api/task/KAGGLE-TITANIC-001/authorize-submission \
  -H "Authorization: Bearer $REBECCA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "solution_summary": "XGBoost with max_depth=7, learning_rate=0.05",
    "model_parameters": {"algorithm": "xgboost", "max_depth": 7, "learning_rate": 0.05},
    "predicted_score": 0.82,
    "resource_usage": {"runtime_seconds": 450, "memory_mb": 512}
  }'
```

### 7. View Audit Trail

```bash
curl http://hc-aol.example.com/api/task/KAGGLE-TITANIC-001/audit-trail \
  -H "Authorization: Bearer $REBECCA_TOKEN"

# Output: Complete trace of all decisions and approvals
```

---

## Integration with Kaggle/AIcrowd

### Implement Adapter

```python
# challenge_adapter.py (scaffold provided)

from challenge_adapter import KaggleAdapter

adapter = KaggleAdapter(api_key="your-kaggle-api-key")

# Fetch competition
competition = adapter.fetch_challenges()[0]

# Format as HC-AOL task
task = HumanTaskDefinition(
    task_id=competition["id"],
    competition_name=competition["name"],
    dataset_source=competition["data_path"],
    model_search_space={"param": [1, 2, 3]},  # Your ranges
    resource_limits={"max_runtime_seconds": 3600},
    safety_constraints=["no_external_calls"],
    human_operator="Rebecca",
    created_at=datetime.utcnow().isoformat(),
)

# Register with HC-AOL
orchestrator.register_human_task_definition(task)

# Evaluate
orchestrator.evaluate_human_task(task["id"])

# Human reviews in dashboard
# Human approves in API
# Human authorizes submission
```

---

## Monitoring

### Check Status

```bash
# Kubernetes
kubectl get pods -n hc-aol
kubectl top pod -n hc-aol

# Docker
docker compose ps
docker compose logs hc_aol_api

# Direct
curl http://localhost:8000/api/health
```

### View Audit Logs

```bash
# User's own audit
curl http://hc-aol.example.com/api/audit/my-log \
  -H "Authorization: Bearer $TOKEN"

# System audit (admin only)
curl http://hc-aol.example.com/api/audit/system-log \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Raw files
cat logs/hc-aol/approvals.jsonl
cat logs/hc-aol/authorizations.jsonl
```

### Dashboard

```bash
curl http://hc-aol.example.com/api/dashboard \
  -H "Authorization: Bearer $TOKEN"
```

---

## Troubleshooting

### "Connection refused"

```bash
# Check if service is running
docker compose ps
kubectl get pods -n hc-aol

# Check port
lsof -i :8000
ss -tlnp | grep 8000
```

### "Invalid token"

```bash
# Get new token
curl -X POST http://hc-aol.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"any"}'
```

### "Permission denied"

```bash
# Check user role
curl http://hc-aol.example.com/api/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Check permissions for user role
# Admin: all permissions
# Operator: define_task, approve, authorize, view_own
# Viewer: view_own only
```

### Kubernetes pod not starting

```bash
kubectl describe pod POD_NAME -n hc-aol
kubectl logs POD_NAME -n hc-aol
```

---

## File Reference

### Core Engine
- `codebecslucky7_codex665/` — Computation engine
- `hc_aol_specification.py` — HC-AOL spec
- `hc_aol_implementation.py` — Implementation
- `hc_aol_multiuser.py` — Multi-user auth

### APIs
- `hc_aol_multiuser_api.py` — Main multi-user API
- `hc_aol_api.py` — Single-user API

### Deployment
- `Dockerfile` — Engine container
- `docker-compose.yml` — Compose orchestration
- `k8s-manifest.yaml` — Kubernetes manifests
- `HELM_CHART_REFERENCE.md` — Helm templates

### Documentation
- `HC-AOL_SPECIFICATION.md` — Full spec
- `K8S_MULTIUSER_GUIDE.md` — K8s guide
- `README_HC_AOL.md` — Overview
- `INDEX.md` — Navigation

### Testing
- `test_three_ring_consensus.py` — Test suite

---

## Production Checklist

Before going live:

- [ ] JWT secret set to strong production value
- [ ] TLS certificates installed (cert-manager)
- [ ] NetworkPolicy restricts traffic
- [ ] RBAC configured
- [ ] PVC mapped to production storage
- [ ] HPA tested and working
- [ ] Monitoring/logging configured
- [ ] Backups tested
- [ ] Disaster recovery plan documented
- [ ] Team trained on workflow

---

## Support & Documentation

| Need | File |
|------|------|
| Full specification | `HC-AOL_SPECIFICATION.md` |
| Quick reference | `HC-AOL_QUICK_REFERENCE.md` |
| K8s guide | `K8S_MULTIUSER_GUIDE.md` |
| Deployment guide | `DEPLOYMENT.md` |
| Examples | `hc_aol_implementation.py` |
| Tests | `test_three_ring_consensus.py` |
| Navigation | `INDEX.md` |

---

## Contact & Attribution

**System**: Codex 6.65: HC-AOL Complete System  
**Author**: Rebecca  
**License**: Proprietary (© 2026 Rebecca)  
**Version**: 1.0.0  
**Status**: Production-Ready  

---

**Ready to Deploy. Choose Your Path Above.**
