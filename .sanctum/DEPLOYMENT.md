# 🔮 THE SANCTUM — Deployment & Operations

## Dr. Strange Portal (Kubernetes)

```yaml
# Invoke the Sanctum with arcane incantations
kubectl apply -f k8s-lock-secret.yaml
kubectl apply -f k8s-lock-configmap.yaml
kubectl apply -f k8s-lock-deployment.yaml
```

## The Nexus (Docker Compose)

```bash
# Load the mystical lock
source .env.lock

# Open all portals simultaneously
docker-compose -f docker-compose-90DAY-LOCK.yml up -d

# Monitor the astral plane
bash lock-status.sh watch
```

## Port Manifest

| Engine | Port | Role | Reality Anchor |
|--------|------|------|---------|
| engine-365 | 365 | Validator | Identity (すう) |
| engine-777 | 777 | Sovereign | Structure (あは) |
| engine-101 | 101 | Horizon | Flow (れれ) |
| engine-1001 | 1001 | Peer | Consensus |
| engine-1002 | 1002 | Peer | Consensus |
| ... | ... | ... | ... |
| engine-1012 | 1012 | Peer | Consensus |
| mcp-audit | 8888 | Compliance | Audit Trail |
| thymus-core | 9999 | Immune | Zero-Trust |
| prometheus | 9090 | Metrics | Observatory |
| grafana | 3000 | Dashboard | Scrying Pool |

## The Ritual (Deployment Steps)

### Step 1: Invoke the Environment
```bash
source .env.lock
export LOCK_ID="550e8400-e29b-41d4-a716-446655440000"
export LOCK_EXPIRY="2025-04-14T10:00:00.000Z"
```

### Step 2: Summon the Engines
```bash
docker-compose -f docker-compose-90DAY-LOCK.yml up -d
```

### Step 3: Verify the Convergence
```bash
bash lock-status.sh watch
# Wait for all 14 engines to report HEALTHY
```

### Step 4: Establish the Merkle Consensus
```bash
# All 14 engines should report identical root hash
for i in {365,777,101} {1001..1012}; do
  curl http://localhost:$i/4gr/health | jq '.merkle_root'
done
```

## The Scrying Pool (Observability)

### Prometheus (Raw Signals)
```
http://localhost:9090
Query: 4gr_cycles_completed{engine_id="engine-365"}
```

### Grafana (Vision Board)
```
http://localhost:3000
Dashboard: AiFACTORi Fleet Status
User: admin
Pass: admin
```

### MCP Audit Suite (Compliance Records)
```
http://localhost:8888/health
http://localhost:8888/audit/trail
```

### Digital Thymus (Immune Scan)
```
http://localhost:9999/thymus/health
http://localhost:9999/thymus/validation_log
```

## Emergency Protocols

### The Reboot Incantation
```bash
# Full reset (use only in extremis)
docker-compose -f docker-compose-90DAY-LOCK.yml down -v
npx ts-node lock-initialize.ts
source .env.lock
docker-compose -f docker-compose-90DAY-LOCK.yml up -d
bash lock-status.sh watch
```

### Lock Renewal (Every 90 Days)
```bash
# On day 85, regenerate
npx ts-node lock-initialize.ts

# Load new seal
source .env.lock

# Rolling restart
docker-compose -f docker-compose-90DAY-LOCK.yml up -d --force-recreate

# Verify convergence
bash lock-status.sh watch
```

### Diagnose a Sick Engine
```bash
# Check individual health
docker logs engine-365 | tail -50
docker exec engine-365 cat /app/lock-metadata.json | jq '.'

# Restart if needed
docker restart engine-365

# Monitor recovery
bash lock-status.sh watch
```

## The Vault (Persistent State)

```
volumes:
  prometheus_data/      → Historical metrics
  grafana_data/         → Dashboard configurations
  audit_data/           → Compliance records
  thymus_data/          → Validation cache
  logs/                 → Engine telemetry
```

---

**Sanctum Status**: Ready for invocation  
**Portal Integrity**: 14/14 stable  
**Arcane Energy**: 91.7% coherent
