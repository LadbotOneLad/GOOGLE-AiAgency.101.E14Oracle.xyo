# Production deployment guide for Codex 6.65 at scale
# Supports 48-256 engines + multi-region distribution

## Prerequisites

- Kubernetes cluster (EKS/AKS/GKE): 3+ nodes, 4+ CPU, 16GB+ RAM per node
- kubectl configured
- Container registry access (ECR/ACR/GCR)

## Build & Push Image

```bash
# Build multi-architecture image
docker buildx build --platform linux/amd64,linux/arm64 -t codex665:latest .

# Push to registry
docker push <registry>/codex665:latest

# Update image in k8s-deployment.yaml
sed -i 's|codex665:latest|<registry>/codex665:latest|g' k8s-deployment.yaml
```

## Deploy to Kubernetes

```bash
# Create namespace + apply deployment
kubectl apply -f k8s-deployment.yaml

# Apply monitoring stack
kubectl apply -f k8s-monitoring.yaml

# Verify pods are running
kubectl get pods -n codex-6-65 -w

# Scale engines (optional)
kubectl scale deployment codex-engine -n codex-6-65 --replicas=100
```

## Access Dashboards

```bash
# Port-forward Grafana
kubectl port-forward -n codex-6-65 svc/grafana 3000:3000

# Port-forward Prometheus
kubectl port-forward -n codex-6-65 svc/prometheus 9090:9090

# Port-forward Witness Aggregator
kubectl port-forward -n codex-6-65 svc/witness-aggregator 9090:9090
```

## Multi-Region Deployment (AWS)

### Region 1: us-east-1
```bash
kubectl config use-context us-east-1-context
kubectl apply -f k8s-deployment.yaml --namespace=codex-6-65
kubectl apply -f k8s-monitoring.yaml --namespace=codex-6-65
```

### Region 2: eu-west-1
```bash
kubectl config use-context eu-west-1-context
kubectl apply -f k8s-deployment.yaml --namespace=codex-6-65
kubectl apply -f k8s-monitoring.yaml --namespace=codex-6-65
```

### Region 3: ap-southeast-1
```bash
kubectl config use-context ap-southeast-1-context
kubectl apply -f k8s-deployment.yaml --namespace=codex-6-65
kubectl apply -f k8s-monitoring.yaml --namespace=codex-6-65
```

## Monitoring & Logs

### Prometheus Queries
```
# Engine CPU utilization
rate(container_cpu_usage_seconds_total{pod=~"codex-engine.*"}[5m])

# Memory usage per pod
container_memory_usage_bytes{pod=~"codex-engine.*"}

# Decision rejection rate
increase(codex_decisions_rejected_total[5m])

# Witness consensus score
codex_witness_consensus_score
```

### View Live Logs
```bash
# Follow engine-1 logs
kubectl logs -f -n codex-6-65 -l app=codex-engine --tail=50

# Follow witness aggregator
kubectl logs -f -n codex-6-65 -l app=witness-aggregator --tail=50

# Stream all pod events
kubectl get events -n codex-6-65 -w
```

## Performance Tuning

### For High Throughput (>100M cycles/day)
```bash
kubectl patch deployment codex-engine -n codex-6-65 --type='json' -p='[
  {"op": "replace", "path": "/spec/template/spec/containers/0/env/2/value", "value": "0.0001"}
]'
```

### Increase Resource Limits
```bash
kubectl set resources deployment codex-engine -n codex-6-65 \
  --limits=cpu=4000m,memory=2Gi \
  --requests=cpu=1000m,memory=512Mi
```

## Persistent Logs & Audit

All logs are persisted to shared storage:
- `/logs/codex665_summary.json` — Engine metrics
- `/logs/cycles.log` — Cycle telemetry
- `/logs/witness_aggregation/` — XYO+BOM witness data
- `/logs/audit.log` — Three-ring consensus decisions

Export logs:
```bash
kubectl exec -it -n codex-6-65 pod/codex-engine-xxx -- cat /logs/metrics.json
```

## Cost Optimization

| Config | Nodes | Engines | Est. Cost/Month (AWS) |
|--------|-------|---------|----------------------|
| Development | 3 | 48 | $300 |
| Production | 10 | 128 | $1,200 |
| Enterprise | 30 | 256 | $4,000 |

## Disaster Recovery

### Backup Strategy
```bash
# Backup PVCs
kubectl exec -it -n codex-6-65 pod/codex-engine-xxx -- \
  tar czf /logs/backup.tar.gz /logs/*

# Restore
kubectl cp codex-6-65/codex-engine-xxx:/logs/backup.tar.gz ./backup.tar.gz
```

### High Availability
- 3 witness aggregator replicas (Pod Disruption Budget)
- 24+ engine replicas minimum (Pod Disruption Budget)
- Auto-scaling 48→256 based on CPU/memory
- Rolling updates with 5-pod disruption tolerance

## Cleanup

```bash
# Delete all resources
kubectl delete namespace codex-6-65

# Delete specific deployment
kubectl delete deployment codex-engine -n codex-6-65
```

---

**Expected Performance at Scale:**

| Metric | Single Container | 48 Engines | 256 Engines |
|--------|------------------|-----------|------------|
| Cycles/second | ~5.8K | ~280K | ~1.5M |
| Memory | 256MB | 12GB | 64GB |
| CPU | 1 core | 24 cores | 128 cores |
| Rejection Rate | 71% | 71% | 71% |
| Consensus | 100% | 100% | 100% |

