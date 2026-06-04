# 90-DAY ENGINE SYNCHRONIZATION LOCK

## Overview

The 90-day lock synchronizes all 14 engines (365, 777, 101, 1001-1012) to a single cryptographic anchor point. All engines validate against this root on every cycle, ensuring:

- **Temporal alignment** — All engines operate in phase
- **Wobble invariants** — Constants locked across all systems
- **Merkle integrity** — Parent-child chain verified per cycle
- **Automatic expiry** — 90-day window enforced, renewal required after

## Key Components

### 1. Lock Files Generated

After initialization (`npx ts-node lock-initialize.ts`), the following files are created:

| File | Purpose |
|------|---------|
| `.env.lock` | Environment variables for docker-compose |
| `lock-metadata.json` | Complete lock state (Merkle tree, engine hashes) |
| `lock-metadata.yaml` | Human-readable lock summary |
| `k8s-lock-secret.yaml` | Kubernetes Secret for production |
| `k8s-lock-configmap.yaml` | Kubernetes ConfigMap for metadata |

### 2. Lock Anchor Structure

```yaml
lockId: "550e8400-e29b-41d4-a716-446655440000"
inceptionTimestampIso: "2025-01-14T10:00:00Z"
expiryTimestampIso: "2025-04-14T10:00:00Z"          # T₀ + 90 days
engineCount: 14
rootMerkleHash: "a1b2c3d4e5f6..."                  # Immutable root
wobbleSnapshot:
  w_suu: 0.05                                       # Identity (iti)
  w_aha: 0.075                                      # Structure (waenga)
  w_rere: 0.15                                      # Flow (nui)
lockPhrase: "UNIT-LOCKED:14engines:90days:2025-01-14"
```

## Deployment

### Quick Start

```bash
# 1. Initialize lock
npx ts-node lock-initialize.ts

# 2. Load lock environment
source .env.lock

# 3. Start all engines with lock enforcement
docker-compose -f docker-compose-90DAY-LOCK.yml up -d

# 4. Verify lock status
bash lock-status.sh

# 5. Monitor continuously
watch -n 10 'bash lock-status.sh'
```

### Environment Variables Injected

Every engine container receives these variables:

```bash
LOCK_ID=550e8400-e29b-41d4-a716-446655440000
LOCK_INCEPTION=2025-01-14T10:00:00Z
LOCK_EXPIRY=2025-04-14T10:00:00Z
LOCK_ROOT_HASH=a1b2c3d4e5f6...
LOCK_PHRASE=UNIT-LOCKED:14engines:90days:2025-01-14
WOBBLE_SUU=0.05
WOBBLE_AHA=0.075
WOBBLE_RERE=0.15
ENFORCE_LOCK=true
```

## Validation Flow

Each engine validates on every cycle:

```
CYCLE START
   ↓
[GROUND] Verify root integrity
   ↓
[READ] Check lock metadata
   ├─ Lock ID present?
   ├─ Lock not expired?
   ├─ Wobble constants match?
   └─ Root hash matches?
   ↓
[GATE] Root check (5-second rule)
   ├─ Lock valid → ACCEPT & proceed
   └─ Lock invalid → REJECT & stabilize
   ↓
[GROW] Expand context (if lock valid)
   ↓
CYCLE END + Root integrity re-verified
```

## Kubernetes Deployment

```bash
# 1. Apply lock Secret
kubectl apply -f k8s-lock-secret.yaml

# 2. Apply lock ConfigMap
kubectl apply -f k8s-lock-configmap.yaml

# 3. Deploy engines (example for engine-365)
cat << 'EOF' | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: engine-365
  labels:
    app: te-papa-matihiko
    engine: validator
    lock: 90day-sync
spec:
  replicas: 1
  selector:
    matchLabels:
      app: te-papa-matihiko
      engine: validator
  template:
    metadata:
      labels:
        app: te-papa-matihiko
        engine: validator
    spec:
      containers:
      - name: engine-365
        image: engine-4gr:latest
        ports:
        - containerPort: 365
        env:
        - name: ENGINE_ID
          value: "365"
        - name: LOCK_ID
          valueFrom:
            secretKeyRef:
              name: engine-lock-90day
              key: lock-id
        - name: LOCK_EXPIRY
          valueFrom:
            secretKeyRef:
              name: engine-lock-90day
              key: lock-expiry
        - name: WOBBLE_SUU
          valueFrom:
            secretKeyRef:
              name: engine-lock-90day
              key: wobble-suu
        volumeMounts:
        - name: lock-metadata
          mountPath: /app/lock-metadata.json
          subPath: lock-metadata.json
      volumes:
      - name: lock-metadata
        configMap:
          name: engine-lock-metadata
EOF

# 4. Verify deployment
kubectl get pods -l lock=90day-sync
kubectl logs -f deployment/engine-365
```

## Lock Status Monitoring

### Real-Time Status

```bash
bash lock-status.sh        # Single snapshot
bash lock-status.sh watch  # Continuous monitoring (10s refresh)
bash lock-status.sh json   # Raw JSON output
```

### Status Indicators

- 🟢 **healthy** — Engine running, lock validated
- 🟡 **warning** — Engine running, health checks pending
- 🔴 **critical** — Engine unhealthy or lock failed
- ⚪ **offline** — Engine not running

### API Health Checks

```bash
# Check individual engine lock status
curl http://localhost:365/4gr/lock-status
curl http://localhost:777/4gr/lock-status
curl http://localhost:101/4gr/lock-status

# Check MCP audit suite
curl http://localhost:8888/health

# Check thymus (zero-trust layer)
curl http://localhost:9999/thymus/health
```

## Lock Renewal (After 90 Days)

### Timeline

- **Day 0-85** — Lock active, normal operation
- **Day 85** — Start renewal process
- **Day 88-90** — Final renewal window
- **Day 90+** — Lock expires (engines reject all new pings until renewed)

### Renewal Procedure

```bash
# 1. On day 85, initialize new lock
npx ts-node lock-initialize.ts

# This generates:
#   - New .env.lock (with new LOCK_ID, fresh LOCK_EXPIRY)
#   - New lock-metadata.json
#   - New K8s Secret/ConfigMap

# 2. Update environment
source .env.lock

# 3. Perform rolling restart of engines
docker-compose -f docker-compose-90DAY-LOCK.yml up -d --force-recreate

# 4. Verify all engines healthy
bash lock-status.sh

# 5. Archive old lock
mkdir -p lock-archives/$(date +%Y-%m-%d)
cp lock-metadata.json lock-archives/$(date +%Y-%m-%d)/
```

### Zero-Downtime Renewal (K8s)

```bash
# 1. Create new Secret
kubectl apply -f k8s-lock-secret.yaml

# 2. Update ConfigMap
kubectl apply -f k8s-lock-configmap.yaml

# 3. Perform rolling update of all deployments
kubectl rollout restart deployment/engine-365 -n default
kubectl rollout restart deployment/engine-777 -n default
kubectl rollout restart deployment/engine-101 -n default
# ... repeat for 1001-1012

# 4. Monitor rollout
kubectl rollout status deployment/engine-365 -n default
```

## Troubleshooting

### Lock Status Returns "Not Found"

```bash
# Verify lock files exist
ls -la lock-metadata.json .env.lock

# Regenerate if missing
npx ts-node lock-initialize.ts
source .env.lock
docker-compose -f docker-compose-90DAY-LOCK.yml restart
```

### Engine Reports Lock Expired

```bash
# Check expiry time
jq '.anchor.expiryTimestampIso' lock-metadata.json

# If actually expired:
npx ts-node lock-initialize.ts
source .env.lock
docker-compose -f docker-compose-90DAY-LOCK.yml up -d --force-recreate

# If not actually expired (clock skew?):
docker exec engine-365 date  # Check container time
docker exec engine-365 hwclock  # Check hardware clock
```

### Merkle Root Hash Mismatch

```bash
# Verify hash in file vs. running engine
jq '.anchor.rootMerkleHash' lock-metadata.json
curl http://localhost:365/4gr/lock-status | jq '.rootMerkleHash'

# If mismatch, rebuild from clean state:
docker-compose -f docker-compose-90DAY-LOCK.yml down -v
npx ts-node lock-initialize.ts
source .env.lock
docker-compose -f docker-compose-90DAY-LOCK.yml up -d
```

## Architecture: Merkle Tree Validation

```
                        ROOT
                    (all 14 engines)
                         |
                    ┌────┴────┐
                    |         |
                  HASH1     HASH2
                   /  \     /  \
                  h1  h2   h3  h4
                  |   |    |   |
              e365 e777  e101 e1001
              (validator) (sovereign) (horizon) (peer-1)
                 ...
```

Every cycle:
1. Each engine computes its own state hash
2. All hashes propagated to MCP audit suite
3. Merkle tree recomputed and compared to locked root
4. Mismatch → all engines REJECT_PING and enter stabilization

## Wobble Constants (Locked for 90 Days)

| Constant | Value | Layer | Meaning |
|----------|-------|-------|---------|
| w_suu | 0.05 | Identity | Micro (iti), slowest, most stable |
| w_aha | 0.075 | Structure | Mid (waenga), moderate coherence |
| w_rere | 0.15 | Flow | Macro (nui), fastest, highest energy |

**Kotahitanja (Unity) Formula:**
```
H = (1/3)*w_suu + (1/3)*w_aha + (1/3)*w_rere
  = (1/3)*0.05 + (1/3)*0.075 + (1/3)*0.15
  = 0.0917 ≈ 91.7% coherence
```

These values are **immutable** for the 90-day lock window and enforced on every engine cycle.

## Documentation Files

- `lock-90-day.ts` — Lock types and validation functions
- `lock-initialize.ts` — Lock generation (run once per 90 days)
- `lock-status.sh` — Real-time lock status display
- `docker-compose-90DAY-LOCK.yml` — Full deployment with 14 engines
- `k8s-lock-secret.yaml` — Kubernetes Secret (generated)
- `k8s-lock-configmap.yaml` — Kubernetes ConfigMap (generated)

## References

- [4GR-FSE Guide](./4GR_FSE_GUIDE.md) — Engine state machine & validation
- [Digital Trinity Architecture](./DIGITAL_IDENTITY_LAYER.md) — Three strata
- [Kotahitanja Unity Principle](./TRI-LANGUAGE-STRUCTURE-LOCKED.md) — Coherence model
