# K8-MU-ORCH: Kubernetes Multi-User Orchestration
# .15% SOLAR WAGYU — DIGITAL CUT (K8S Edition)

## Overview

**K8-MU-ORCH** is a production-grade Kubernetes cluster hosting:

- **14 synchronized engines** (365, 777, 101, 1001-1012)
- **3-10 pod replicas** (HPA auto-scaling)
- **JWT + RBAC** multi-user identity (Admin/Operator/Viewer)
- **90-day lock** enforced across all pods
- **Rhythm-aware rollouts** (TICK/BEAT/BREATH deployment timing)
- **Zero-trust networking** (NetworkPolicy)
- **TLS + Ingress** for external access

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Kubernetes Cluster (k8-mu-orch namespace)               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────┐    │
│  │ Ingress (TLS) + LoadBalancer                  │    │
│  └──────────────────┬──────────────────────────┘    │
│                     │                               │
│  ┌──────────────────▼──────────────────────────┐    │
│  │ HPA (3-10 replicas)                         │    │
│  ├──────────────────────────────────────────── │    │
│  │                                             │    │
│  │ Pod 1: 14 Engines Synchronized              │    │
│  │   ├─ Engine-365 (validator)                 │    │
│  │   ├─ Engine-777 (sovereign)                 │    │
│  │   ├─ Engine-101 (horizon)                   │    │
│  │   └─ Engines 1001-1012 (peer ring)          │    │
│  │   ├─ JWT Auth                               │    │
│  │   ├─ Lock: 550e8400-e29b...                 │    │
│  │   └─ Kotahitanja: 0.0917                    │    │
│  │                                             │    │
│  │ Pod 2, 3, ... (replicas, same engines)     │    │
│  │                                             │    │
│  └────────────────┬─────────────────────────────┘    │
│                   │                                  │
│     ┌─────────────┴──────────────────┐              │
│     │                                │              │
│  ┌──▼──┐                      ┌──────▼───┐        │
│  │ PVC │                      │ConfigMap │        │
│  │State│                      │ Secrets  │        │
│  │Logs │                      │ Lock     │        │
│  └─────┘                      └──────────┘        │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## Prerequisites

```bash
# Kubernetes 1.20+
kubectl version

# kubectl configured with proper context
kubectl config current-context

# NFS server (for PV)
# Or use cloud storage (AWS EBS, GCP PD, etc.)

# Nginx Ingress Controller
kubectl get ns ingress-nginx

# Prometheus (optional, for metrics)
```

---

## Deployment

### 1. Apply Manifest

```bash
# Create namespace + all resources
kubectl apply -f k8s-mu-orch-manifest.yaml

# Verify
kubectl get pods -n k8-mu-orch
kubectl get svc -n k8-mu-orch
kubectl get statefulset -n k8-mu-orch
```

### 2. Verify Pods Running

```bash
# Wait for all pods
kubectl wait --for=condition=ready pod \
  -l app=te-papa-matihiko \
  -n k8-mu-orch \
  --timeout=300s

# Check status
kubectl get pods -n k8-mu-orch -l app=te-papa-matihiko
```

### 3. Test Engine Health

```bash
# Port-forward to a pod
kubectl port-forward \
  pod/k8-mu-orch-engines-0 \
  8000:365 \
  -n k8-mu-orch

# In another terminal
curl http://localhost:8000/4gr/health
```

### 4. Update Secrets (Production)

```bash
# Update JWT secret
kubectl patch secret k8-mu-orch-secrets \
  -n k8-mu-orch \
  --type=json \
  -p='[{"op":"replace","path":"/data/jwt-secret","value":"'$(echo -n 'your-production-jwt-secret' | base64)'"}]'

# Verify
kubectl get secret k8-mu-orch-secrets -n k8-mu-orch -o yaml
```

---

## Using gtop k8

Add to PowerShell profile:

```powershell
function gtop-k8 { & "C:\path\to\gtop-k8.ps1" @args }
```

Then:

```powershell
# Check pod health
gtop-k8 status

# View topology
gtop-k8 map

# Rolling deployment
gtop-k8 rollout 4gr-fse:v1.1

# Scale manually
gtop-k8 scale 5

# View logs
gtop-k8 logs k8-mu-orch-engines-0

# Check lock status
gtop-k8 lock

# RBAC users
gtop-k8 users
```

---

## Multi-User Workflow

### Admin Creates Users

```bash
# Create operator role binding
kubectl create rolebinding operator-binding \
  --clusterrole=k8-mu-orch-operator \
  --user=rebecca@company.com \
  -n k8-mu-orch

# Create viewer role binding
kubectl create rolebinding viewer-binding \
  --clusterrole=k8-mu-orch-viewer \
  --user=viewer1@company.com \
  -n k8-mu-orch
```

### Operator Scales Cluster

```bash
# Only operators can scale
gtop-k8 scale 7

# Only admins can do rollouts
gtop-k8 rollout 4gr-fse:v1.1
```

### Viewer Monitors Only

```bash
# View status (read-only)
gtop-k8 status
gtop-k8 logs k8-mu-orch-engines-0

# Cannot scale or deploy
gtop-k8 scale 5  # Error: forbidden
```

---

## Scaling

### Auto (HPA)

```bash
# HPA automatically scales 3-10 based on:
# - CPU: 70% target
# - Memory: 80% target

kubectl get hpa -n k8-mu-orch
kubectl describe hpa k8-mu-orch-hpa -n k8-mu-orch
```

### Manual (Operator)

```bash
# Operator scales manually
gtop-k8 scale 5

# Or via kubectl
kubectl scale statefulset k8-mu-orch-engines \
  --replicas=5 \
  -n k8-mu-orch
```

---

## Lock Synchronization

All pods share the same lock metadata:

```yaml
# ConfigMap: engine-lock-metadata
lockId: 550e8400-e29b-41d4-a716-446655440000
inceptionTimestampIso: 2025-01-14T10:00:00.000Z
expiryTimestampIso: 2025-04-14T10:00:00.000Z
kotahitanja-value: 0.0917
```

Each pod mounts this ConfigMap read-only, ensuring:
- **All engines** use the same Merkle root
- **Lock expires** simultaneously across cluster
- **Renewal** is coordinated (not individual)

---

## Rollout with Rhythm

Deployments use rhythm-aware timing:

```bash
gtop-k8 rollout 4gr-fse:v1.1

# Output:
# ROLLING DEPLOYMENT: 4gr-fse:v1.1
# Setting image to: 4gr-fse:v1.1...
# Rollout in progress (TICK/BEAT/BREATH timing)
# . . . . . (50ms per TICK)
# Waiting for pods...       (1500ms BREATH)
# Pod 0: updated, ready
# Pod 1: updating...
# Pod 2: updating...
```

**RollingUpdate strategy:**
- maxSurge: 1 (one extra pod during rollout)
- maxUnavailable: 0 (no downtime)
- Timing: 150ms per pod (RHYTHM pace)

---

## Monitoring

### Pod Health

```bash
# All pods
kubectl get pods -n k8-mu-orch -l app=te-papa-matihiko

# Specific pod
kubectl describe pod k8-mu-orch-engines-0 -n k8-mu-orch

# Events
kubectl get events -n k8-mu-orch
```

### Metrics

```bash
# CPU/Memory per pod
kubectl top pods -n k8-mu-orch

# Node usage
kubectl top nodes

# HPA metrics
kubectl get hpa k8-mu-orch-hpa -n k8-mu-orch --watch
```

### Logs

```bash
# All replicas
kubectl logs -f deployment/k8-mu-orch-engines -n k8-mu-orch

# Specific pod
kubectl logs -f pod/k8-mu-orch-engines-0 -n k8-mu-orch

# Watch all logs
kubectl logs -f -l app=te-papa-matihiko -n k8-mu-orch
```

---

## Troubleshooting

### Pod Won't Start

```bash
# Check events
kubectl describe pod k8-mu-orch-engines-0 -n k8-mu-orch

# Check logs
kubectl logs k8-mu-orch-engines-0 -n k8-mu-orch

# Check resource requests
kubectl top pod k8-mu-orch-engines-0 -n k8-mu-orch
```

### Lock Sync Failing

```bash
# Verify ConfigMap exists
kubectl get configmap engine-lock-metadata -n k8-mu-orch

# Verify pods can read it
kubectl exec -it k8-mu-orch-engines-0 -n k8-mu-orch -- \
  cat /app/config/lock-metadata.json
```

### Ingress Not Working

```bash
# Verify Ingress created
kubectl get ingress -n k8-mu-orch

# Check TLS certificate
kubectl describe cert k8-mu-orch-tls -n k8-mu-orch

# Test via port-forward
kubectl port-forward svc/k8-mu-orch-api 8000:365 -n k8-mu-orch
curl http://localhost:8000/4gr/health
```

---

## Production Checklist

- [ ] Update JWT secret in Secret manifest
- [ ] Update NFS server path
- [ ] Verify Ingress DNS resolves
- [ ] Test TLS certificate (cert-manager)
- [ ] Configure NetworkPolicy (zero-trust)
- [ ] Set resource limits appropriate for workload
- [ ] Enable monitoring (Prometheus/Grafana)
- [ ] Configure backups (PVC snapshots)
- [ ] Test RBAC users can/cannot do expected operations
- [ ] Document runbooks for ops team

---

## API Endpoints

```
# Engine health (any pod)
GET  http://k8-mu-orch.example.com/4gr/health
GET  http://k8-mu-orch.example.com/4gr/status
GET  http://k8-mu-orch.example.com/4gr/traces

# Engine control (secured by JWT)
POST http://k8-mu-orch.example.com/4gr/initialize
POST http://k8-mu-orch.example.com/4gr/cycle
POST http://k8-mu-orch.example.com/4gr/ping

# Metrics
GET  http://k8-mu-orch.example.com/metrics
```

---

## RBAC Roles

| Permission | Admin | Operator | Viewer |
|-----------|-------|----------|--------|
| Pod status | ✅ | ✅ | ✅ |
| Pod logs | ✅ | ✅ | ✅ |
| Scale (HPA) | ✅ | ✅ | ❌ |
| Rollout | ✅ | ❌ | ❌ |
| Edit ConfigMap | ✅ | ❌ | ❌ |
| Delete pods | ✅ | ❌ | ❌ |

---

## Commands Reference

```bash
# Deployment
kubectl apply -f k8s-mu-orch-manifest.yaml
kubectl delete -f k8s-mu-orch-manifest.yaml

# Status
kubectl get pods -n k8-mu-orch
kubectl get svc -n k8-mu-orch
kubectl get statefulset -n k8-mu-orch
kubectl get hpa -n k8-mu-orch

# Logs
kubectl logs -f pod/k8-mu-orch-engines-0 -n k8-mu-orch
kubectl logs -f -l app=te-papa-matihiko -n k8-mu-orch

# Scaling
kubectl scale statefulset k8-mu-orch-engines --replicas=5 -n k8-mu-orch

# Rolling update
kubectl set image statefulset/k8-mu-orch-engines \
  k8-mu-orch-engines=4gr-fse:v1.1 \
  -n k8-mu-orch --record

# Port-forward
kubectl port-forward svc/k8-mu-orch-api 8000:365 -n k8-mu-orch

# Execute in pod
kubectl exec -it k8-mu-orch-engines-0 -n k8-mu-orch -- /bin/sh
```

---

**© 2026 .15% SOLAR WAGYU — DIGITAL CUT**  
**K8-MU-ORCH: Production-grade Kubernetes orchestration with rhythm.**
