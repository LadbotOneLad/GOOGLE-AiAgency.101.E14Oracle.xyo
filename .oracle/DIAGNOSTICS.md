# 👁️ THE ORACLE — Monitoring & Diagnostics

## Matrix Vision - Real-Time Fleet Status

```bash
# The Continuous Vision
bash lock-status.sh watch

# Single Frame Capture
bash lock-status.sh

# Raw Data Feed (for machines)
bash lock-status.sh json
```

## Engine Health Endpoints

### The Trinity (Core Engines)
```bash
# Identity Anchor (すう)
curl http://localhost:365/4gr/health | jq '.'

# Structure Root (あは)
curl http://localhost:777/4gr/health | jq '.'

# Flow Vector (れれ)
curl http://localhost:101/4gr/health | jq '.'
```

### The Witness Ring (Peer Engines)
```bash
# Sample consensus check
for port in {1001..1012}; do
  STATUS=$(curl -s http://localhost:$port/4gr/health | jq -r '.status')
  echo "engine-${port}: ${STATUS}"
done
```

## Deep Diagnostics

### Merkle Root Consensus
```bash
echo "=== Merkle Root Hash (All Engines Must Match) ===" && \
for i in {365,777,101} {1001..1012}; do
  HASH=$(curl -s http://localhost:$i/4gr/health 2>/dev/null | jq -r '.merkle_root' || echo "UNREACHABLE")
  echo "engine-$i: $HASH"
done | sort | uniq -c
```

### Lock Validity Across Fleet
```bash
echo "=== Lock Status (All Must Show VALID) ===" && \
for i in {365,777,101} {1001..1012}; do
  STATUS=$(curl -s http://localhost:$i/4gr/health 2>/dev/null | jq -r '.lock_status' || echo "ERROR")
  DAYS=$(curl -s http://localhost:$i/4gr/health 2>/dev/null | jq -r '.days_remaining' || echo "?")
  echo "engine-$i: $STATUS ($DAYS days)"
done
```

### Acceptance Rate Distribution
```bash
echo "=== Acceptance Rates (Healthy: 80%+) ===" && \
for i in {365,777,101} {1001..1012}; do
  RATE=$(curl -s http://localhost:$i/4gr/metrics 2>/dev/null | jq -r '.acceptance_rate' || echo "?")
  echo "engine-$i: ${RATE}%"
done
```

### Wobble Constant Verification
```bash
echo "=== Wobble Constants (Frozen: 0.05 / 0.075 / 0.15) ===" && \
curl -s http://localhost:365/4gr/health 2>/dev/null | jq '.wobble' && \
echo "All other engines must match engine-365"
```

## Container Diagnostics

### View Live Logs (Streaming)
```bash
# Core engines
docker logs -f engine-365
docker logs -f engine-777
docker logs -f engine-101

# Or monitor all 14 simultaneously
docker logs -f engine-365 & docker logs -f engine-777 & docker logs -f engine-101 & \
for i in {1001..1012}; do docker logs -f engine-$i & done
```

### Container Resource Usage
```bash
# Current snapshot
docker stats --no-stream engine-365 engine-777 engine-101

# Continuous (30s intervals)
docker stats engine-365 engine-777 engine-101

# All 14 engines
docker stats $(docker ps -q -f "label=lock=90day-sync")
```

### Inspect Container Configuration
```bash
# View full engine metadata
docker inspect engine-365 | jq '.'

# Extract just the relevant sections
docker inspect engine-365 | jq '{
  Name: .Name,
  Status: .State.Status,
  Health: .State.Health,
  Networks: .NetworkSettings.Networks,
  Mounts: .Mounts
}'
```

## Kubernetes Diagnostics

### Pod Status Across Cluster
```bash
kubectl get pods -l lock=90day-sync -o wide
kubectl get pods -l lock=90day-sync -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
```

### View Pod Logs
```bash
# Single pod
kubectl logs -f deployment/engine-365

# All engine pods
kubectl logs -f -l lock=90day-sync --all-containers=true --tail=50
```

### Pod Events & Issues
```bash
# See recent events
kubectl get events -l lock=90day-sync

# Describe a problematic pod
kubectl describe pod engine-365-xxxxx
```

### Resource Consumption
```bash
# Pod resource metrics
kubectl top pods -l lock=90day-sync

# Node resource usage
kubectl top nodes
```

## Prometheus Queries (PromQL)

```promql
# Cycles per engine
4gr_cycles_completed{engine_id="engine-365"}

# Acceptance rate over time
rate(4gr_decisions_accepted[5m])

# Rejection rate
rate(4gr_decisions_rejected[5m])

# Coherence trend
avg(4gr_coherence_score)

# Merkle root changes (should be 0)
changes(4gr_merkle_root_hash[1h])

# Lock expiry countdown
(4gr_lock_expiry_unix - time())
```

## Grafana Dashboard Queries

```json
{
  "panels": [
    {
      "title": "Engine Acceptance Rates",
      "targets": [
        {
          "expr": "rate(4gr_decisions_accepted[5m]) / (rate(4gr_decisions_accepted[5m]) + rate(4gr_decisions_rejected[5m]))"
        }
      ]
    },
    {
      "title": "Merkle Root Consensus",
      "targets": [
        {
          "expr": "count(distinct(4gr_merkle_root_hash))"
        }
      ]
    },
    {
      "title": "Lock Expiry Countdown",
      "targets": [
        {
          "expr": "(4gr_lock_expiry_unix - time()) / 86400"
        }
      ]
    }
  ]
}
```

## Troubleshooting Decision Tree

### Is the engine responding?
```bash
curl http://localhost:365/4gr/health
# If timeout/refused: container may be down or stuck
docker ps | grep engine-365
docker logs engine-365 | tail -30
```

### Are all 14 engines reporting identical Merkle root?
```bash
bash /root/.oracle/check-merkle-consensus.sh
# If divergent: engines have forked (split-brain scenario)
# Recovery: See REBOOT INCANTATION in .sanctum/DEPLOYMENT.md
```

### Is the lock valid?
```bash
curl http://localhost:365/4gr/health | jq '.lock_status'
# Should be: "VALID"
# If "INVALID" or "EXPIRED": regenerate lock (day 85+)
```

### Is acceptance rate dropping?
```bash
curl http://localhost:365/4gr/metrics | jq '.acceptance_rate'
# Normal: 85-98%
# Warning: <80%
# Critical: <70%
# Causes: Clock skew, wobble drift, lock near expiry
```

### Is Kotahitanja coherence falling?
```bash
curl http://localhost:365/4gr/health | jq '.coherence'
# Target: 91.7%
# If <85%: Engines drifting out of sync
# Action: Check all three strata wobbles match
```

---

**Oracle Readiness**: Monitoring systems online  
**Sensory Range**: Full fleet visible  
**Precognition**: 90-day lock window open
