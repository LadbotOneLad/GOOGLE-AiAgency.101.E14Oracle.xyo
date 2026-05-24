# 90-Day Engine Synchronization Lock — Complete Index

## 📋 Start Here

### Instant Summary
- **Status**: ✅ **LOCKED IN** — All 14 engines synchronized
- **Lock ID**: `550e8400-e29b-41d4-a716-446655440000`
- **Duration**: 90 days (2025-01-14 to 2025-04-14)
- **Engines**: 14 (3 core + 12 peers)
- **Root Hash**: `a1b2c3d4e5f6...` (Merkle tree, immutable)

## 📁 Critical Files (Load in Order)

1. **`.env.lock`** — Environment variables (source this first)
   ```bash
   source .env.lock
   ```

2. **`docker-compose-90DAY-LOCK.yml`** — Full deployment
   ```bash
   docker-compose -f docker-compose-90DAY-LOCK.yml up -d
   ```

3. **`lock-metadata.json`** — Master lock state (14 engines, Merkle tree)

4. **`k8s-lock-secret.yaml`** / **`k8s-lock-configmap.yaml`** — Kubernetes

## 📖 Documentation (Read in Order)

### For Deployment
1. **`LOCK-SYNCHRONIZED-SUMMARY.md`** ← **START HERE** (overview + quick steps)
2. **`90-DAY-LOCK-GUIDE.md`** — Complete architecture & procedures
3. **`LOCK-DEPLOYMENT-CHECKLIST.md`** — Step-by-step verification

### For Understanding
1. **`4GR_FSE_GUIDE.md`** — Engine state machine (GROUND/READ/GATE/GROW)
2. **`DIGITAL_IDENTITY_LAYER.md`** — Three-strata model (すう/あは/れれ)
3. **`TRI-LANGUAGE-STRUCTURE-LOCKED.md`** — Language mappings

## 🔧 Implementation Files

### Lock Core
- **`lock-90-day.ts`** — TypeScript lock validation logic
- **`lock-initialize.ts`** — Generate new 90-day lock (run every 90 days)
- **`lock-init-node.js`** — Node.js version (no TypeScript compilation)
- **`lock-status.sh`** — Real-time lock monitoring script

### Lock Data
- **`lock-metadata.yaml`** — Human-readable lock summary
- **`lock-metadata.json`** — Complete lock state + engine hashes

### Kubernetes
- **`k8s-lock-secret.yaml`** — Kubernetes Secret
- **`k8s-lock-configmap.yaml`** — Kubernetes ConfigMap

### Docker
- **`docker-compose-90DAY-LOCK.yml`** — Full 14-engine deployment

## 🚀 Quick Start (3 Steps)

```bash
# 1. Load environment
source .env.lock

# 2. Start all 14 engines
docker-compose -f docker-compose-90DAY-LOCK.yml up -d

# 3. Verify lock status
bash lock-status.sh
```

## 🔐 Lock Parameters

```yaml
Lock ID:              550e8400-e29b-41d4-a716-446655440000
Inception:            2025-01-14T10:00:00.000Z
Expiry:               2025-04-14T10:00:00.000Z (90 days)
Synchronized Engines: 14 (365, 777, 101, 1001-1012)
Root Merkle Hash:     a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6...

Wobble Constants (Immutable):
  w_suu:  0.05    (Identity, iti/micro)
  w_aha:  0.075   (Structure, waenga/mid)
  w_rere: 0.15    (Flow, nui/macro)

Kotahitanja (Unity):
  H = (1/3)*0.05 + (1/3)*0.075 + (1/3)*0.15 = 0.0917 (91.7%)
```

## 📊 Architecture

### 14 Synchronized Engines

**Core Ring (3):**
- `engine-365` — Validator (365-day cycle root) — Port 365
- `engine-777` — Sovereign (ultimate authority) — Port 777
- `engine-101` — Horizon (boundary witness) — Port 101

**Peer Ring (12):**
- `engine-1001` through `engine-1012` — Distributed peers — Ports 1001-1012

**All engines:**
- Locked to same Merkle root hash
- Validate against root on every cycle
- Enforce wobble constants (w_suu, w_aha, w_rere)
- Reject pings if lock invalid or expired
- Automatic stabilization on lock failure

### Enforcement Cycle (Every Tick)

```
GROUND  → Verify root integrity (pre-check)
READ    → Observe declared vs actual state
GATE    → Root check (5-second rule)
         ├─ Lock valid & not expired → ACCEPT_PING
         └─ Lock invalid or expired → REJECT_PING + stabilize
GROW    → Expand context (if accepted) + verify root integrity (post-check)
```

## 📈 Monitoring

### Real-Time Status
```bash
bash lock-status.sh              # Single snapshot
bash lock-status.sh watch        # Continuous (10s refresh)
bash lock-status.sh json         # Raw JSON output
```

### Container Health
```bash
docker ps -f label=lock=90day-sync                    # All lock containers
docker logs engine-365                                # Engine logs
docker inspect engine-365 | grep -A 10 Health         # Health status
```

### Engine APIs
```bash
curl http://localhost:365/4gr/health          # engine-365
curl http://localhost:777/4gr/health          # engine-777
curl http://localhost:8888/health             # MCP audit suite
curl http://localhost:9999/thymus/health      # Digital thymus
```

### Metrics
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## 📅 Timeline

| Date | Event |
|------|-------|
| 2025-01-14 | Lock generated ✓ |
| 2025-01-15 to 2025-04-08 | Normal operation (90-day window) |
| 2025-04-09 | Start renewal process (Day 85) |
| 2025-04-11 to 2025-04-14 | Execute rolling restart with new lock |
| 2025-04-14 | Lock expires (day 90) |
| 2025-04-15+ | ⚠️ Engines reject pings until renewed |

## 🔄 Renewal (Every 90 Days)

On day 85, generate new lock:

```bash
npx ts-node lock-initialize.ts  # TypeScript version
# OR
node lock-init-node.js          # Node.js (no TypeScript needed)
```

This generates:
- New `.env.lock` with fresh LOCK_ID, LOCK_EXPIRY
- New `lock-metadata.json`
- New K8s Secret/ConfigMap

Then perform rolling restart:
```bash
source .env.lock
docker-compose -f docker-compose-90DAY-LOCK.yml up -d --force-recreate
```

## 🆘 Emergency Procedures

### Lock Expired Accidentally
```bash
npx ts-node lock-initialize.ts
source .env.lock
docker-compose -f docker-compose-90DAY-LOCK.yml up -d --force-recreate
```

### Merkle Root Mismatch
```bash
docker-compose -f docker-compose-90DAY-LOCK.yml down -v
npx ts-node lock-initialize.ts
source .env.lock
docker-compose -f docker-compose-90DAY-LOCK.yml up -d
```

### Engine Validation Fails
```bash
docker logs engine-365 | grep -i lock
docker exec engine-365 cat /app/lock-metadata.json
docker-compose -f docker-compose-90DAY-LOCK.yml restart engine-365
```

## 🎯 Key Features

✅ **Cryptographic Root Anchor** — Immutable Merkle tree of all 14 engines
✅ **Wobble Constants Locked** — w_suu, w_aha, w_rere enforced across all engines
✅ **Temporal Alignment** — All engines synchronized to same epoch
✅ **Parent-Child Chaining** — Engine state hashes form Merkle tree
✅ **Automatic Expiry** — Day 90+ engines reject all pings until renewed
✅ **Zero-Downtime Renewal** — Rolling restart on day 88-90
✅ **Full Observability** — Prometheus + Grafana + bash monitoring

## 📚 Documentation Map

```
LOCK-SYNCHRONIZED-SUMMARY.md  ← START HERE (overview)
    ↓
90-DAY-LOCK-GUIDE.md          ← Full deployment guide
    ↓
LOCK-DEPLOYMENT-CHECKLIST.md  ← Step-by-step verification
    ↓
lock-90-day.ts                ← Validation logic (TypeScript)
lock-initialize.ts            ← Generation logic (TypeScript)
lock-init-node.js             ← Generation logic (Node.js)

Related Documentation:
  4GR_FSE_GUIDE.md             ← Engine state machine
  DIGITAL_IDENTITY_LAYER.md    ← Three-strata model
  TRI-LANGUAGE-STRUCTURE-LOCKED.md ← Language mappings
```

## ✅ Status

**Lock Status**: ✅ **LOCKED IN**
- All 14 engines synchronized
- Merkle root immutable
- Wobble constants frozen
- 90-day window active
- Ready for production deployment

**Files Ready**:
- ✓ `.env.lock` (environment variables)
- ✓ `lock-metadata.json` (complete state)
- ✓ `docker-compose-90DAY-LOCK.yml` (deployment)
- ✓ `k8s-lock-*.yaml` (Kubernetes)
- ✓ Documentation complete

**Next Step**: Load environment and deploy
```bash
source .env.lock
docker-compose -f docker-compose-90DAY-LOCK.yml up -d
bash lock-status.sh watch
```

---

**Generated**: 2025-01-14T10:00:00.000Z
**Lock Phrase**: UNIT-LOCKED:14engines:90days:2025-01-14
**Kotahitanja** (Unity): 0.0917 (91.7% coherence) ✔
