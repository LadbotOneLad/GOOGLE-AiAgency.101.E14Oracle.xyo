# Codex 6.65 Scaling Analysis & Cost Model

## Current Baseline (Your 3-Engine Docker Setup)

From your metrics:
- **engine-365-days**: 29.8M cycles, 71% rejection rate, 100% consensus
- **ultimate-engine**: 6.1M cycles, 61% rejection rate  
- **tenetaiagency-101**: 1.47B ticks, 100% rejection rate
- **Resource usage**: 517e50634afe (48% CPU, 86.6MB RAM)

**Aggregate throughput**: ~215K cycles/second across 3 engines

## Scaling to Production

### Tier 1: Small Cluster (48 engines)
```
Infrastructure:
  - 3 Kubernetes nodes (4 CPU, 16GB RAM each)
  - EBS/PD: 500GB shared storage
  
Throughput:
  - 2.76M cycles/second
  - 238B cycles/day
  - 71% rejection rate (consistent)
  
Costs (AWS):
  - Compute: 3x t3.2xlarge = $600/month
  - Storage: 500GB EBS = $50/month
  - Data transfer: ~$20/month
  - Total: $670/month
```

### Tier 2: Medium Cluster (128 engines)
```
Infrastructure:
  - 10 Kubernetes nodes (8 CPU, 32GB RAM each)
  - EBS/PD: 1TB shared storage
  - Network Load Balancer
  
Throughput:
  - 7.36M cycles/second
  - 635B cycles/day
  - 3 witness aggregator replicas
  
Costs (AWS):
  - Compute: 10x r5.2xlarge = $2,400/month
  - Storage: 1TB EBS = $100/month
  - Load Balancer: $20/month
  - Data transfer: $50/month
  - Total: $2,570/month
```

### Tier 3: Enterprise Cluster (256 engines)
```
Infrastructure:
  - 30 Kubernetes nodes (16 CPU, 64GB RAM each)
  - EBS/PD: 2TB shared storage
  - Multi-region failover (3 regions)
  - Dedicated monitoring cluster
  
Throughput:
  - 14.72M cycles/second
  - 1.27T cycles/day
  - Global witness consensus
  - 5 aggregator replicas per region
  
Costs (AWS, 3 regions):
  - Compute: 90 nodes = $7,200/month
  - Storage: 2TB/region = $600/month
  - Load Balancers: $60/month
  - Data transfer: Inter-region = $300/month
  - Monitoring: Datadog/New Relic = $400/month
  - Total: $8,560/month
```

## Performance Characteristics

### Memory Scaling
- Per engine: ~256MB (requests) → 1GB (limits)
- 48 engines: 12GB
- 128 engines: 32GB
- 256 engines: 64GB

### CPU Scaling
- Per engine: 0.5 CPU (requests) → 2 CPU (limits)
- 48 engines: 24 CPU cores
- 128 engines: 64 CPU cores
- 256 engines: 128 CPU cores

### Network I/O
- Per engine: ~5KB/sec (metrics + logs)
- 48 engines: 240KB/sec aggregate
- 128 engines: 640KB/sec aggregate
- 256 engines: 1.3MB/sec aggregate

## Geographic Distribution Options

### Option 1: Single Region (Recommended for <100 engines)
```
Region: us-east-1 (N. Virginia)
Engines: 48-100
Witness Aggregators: 2
Latency: 1-5ms intra-cluster
Failover: Pod-level only
```

### Option 2: Multi-Region Active-Active (100-256 engines)
```
Region 1: us-east-1 (128 engines)
  ├─ Sydney witness aggregator (XYO)
  └─ Melbourne witness aggregator (BOM)

Region 2: eu-west-1 (64 engines)
  └─ European witness aggregator

Region 3: ap-southeast-1 (64 engines)
  └─ Asian-Pacific witness aggregator

Consensus: Global (3-way agreement)
Failover: Automatic (minutes)
```

### Option 3: Edge + Cloud Hybrid (256+ engines)
```
Cloud (Kubernetes): 128 engines
Edge Nodes: 128 engines
  ├─ AWS Greengrass/Azure Stack
  └─ Local witness aggregation

Sync: 5-minute intervals
Fallback: Cloud-only mode if edge fails
```

## Horizontal Pod Autoscaling (HPA)

```yaml
Min Replicas: 48
Max Replicas: 256
Scale-up trigger: CPU > 70% (30 seconds)
Scale-down trigger: CPU < 30% (5 minutes)

Example:
- 10:00 AM: 48 engines, 62% CPU
- 10:05 AM: 96 engines, 68% CPU (scale up 48)
- 10:10 AM: 192 engines, 71% CPU (scale up 96)
- 02:00 PM: 64 engines, 45% CPU (scale down to 64)
```

## Witness Aggregation at Scale

### 48-engine aggregation
```
Witness generation: 2.76M cycles/sec
XYO location records: ~48K/hour
BOM weather records: ~48K/hour
Consensus evaluations: 576K/hour
Export format: JSONL (newline-delimited JSON)
Storage: 50GB/month
```

### 256-engine aggregation
```
Witness generation: 14.72M cycles/sec
XYO location records: ~256K/hour
BOM weather records: ~256K/hour
Consensus evaluations: 3.07M/hour
Storage: 250GB/month
Retention: 1 year (2.5TB)
```

## Observability & Alerting

### Key Metrics to Monitor
```
- Rejection rate (should stay ~71%)
- Consensus rate (should stay ~100%)
- P99 latency (target: <100ms)
- Pod restart rate (target: 0)
- PVC usage (alert at 80%)
- Network saturation (alert at 70%)
```

### Recommended Dashboards
1. **Engine Health** — CPU, memory, restarts per pod
2. **Consensus Metrics** — Rejection rate, alignment, witness scores
3. **Witness Aggregation** — XYO + BOM ingestion rate, consensus score
4. **Capacity** — Storage usage, HPA scaling decisions
5. **Cost** — Actual vs. budgeted spend

## Migration Path

### Phase 1: Container (Current)
```
3 Docker containers (engine-365, ultimate-engine, tenet-101)
Single machine
Total throughput: 215K cycles/sec
```

### Phase 2: Kubernetes (Recommended First)
```
Deploy k8s-deployment.yaml on existing EKS cluster
Scale to 48 engines
Total throughput: 2.76M cycles/sec
Cost: ~$700/month
```

### Phase 3: Multi-Region
```
Replicate to 2 regions (us-east-1, eu-west-1)
Scale to 128 engines total
Total throughput: 7.36M cycles/sec
Cost: ~$2,500/month
```

### Phase 4: Enterprise
```
3-region deployment (NA, EU, APAC)
Scale to 256 engines
Add edge compute nodes
Total throughput: 14.72M cycles/sec
Cost: ~$8,600/month
```

## Cost Optimization Tips

1. **Use spot instances** (60% savings)
   ```bash
   kubectl patch deployment codex-engine -n codex-6-65 \
     --type='json' -p='[{"op": "add", "path": "/spec/template/spec/nodeSelector/karpenter.sh~1capacity-type", "value": "spot"}]'
   ```

2. **Reserved instances** (30% savings for 1-year commitment)

3. **Schedule scaling** (reduce to 24 engines during off-hours)
   ```bash
   kubectl patch hpa codex-engine-hpa -n codex-6-65 \
     --type='json' -p='[{"op": "replace", "path": "/spec/minReplicas", "value": 24}]'
   ```

4. **Compress logs** (reduce storage 50%)
   ```bash
   ENABLE_LOG_COMPRESSION=true kubectl apply -f k8s-deployment.yaml
   ```

---

**Recommendation**: Start with Tier 2 (128 engines, 3 nodes) for production workload. Scale to Tier 3 after validating 30-day uptime and cost metrics.

