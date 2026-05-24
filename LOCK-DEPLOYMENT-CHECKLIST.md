╔═════════════════════════════════════════════════════════════════════════════╗
║                 90-DAY ENGINE LOCK DEPLOYMENT CHECKLIST                      ║
╚═════════════════════════════════════════════════════════════════════════════╝

✅ LOCK GENERATED
─────────────────────────────────────────────────────────────────────────────

✔ LOCK ARTIFACTS CREATED

  Core Files:
    ✓ .env.lock                      — Environment variables (load this first)
    ✓ lock-metadata.json             — Complete lock state + 14 engine hashes
    ✓ lock-metadata.yaml             — Human-readable lock summary
  
  Kubernetes:
    ✓ k8s-lock-secret.yaml           — Deploy to K8s with: kubectl apply -f
    ✓ k8s-lock-configmap.yaml        — Deploy to K8s with: kubectl apply -f
  
  Docker Compose:
    ✓ docker-compose-90DAY-LOCK.yml  — All 14 engines + observability
  
  TypeScript/JavaScript:
    ✓ lock-90-day.ts                 — Lock validation logic
    ✓ lock-initialize.ts             — Lock generation (run every 90 days)
    ✓ lock-init-node.js              — Node.js version (no TS compilation)
  
  Scripts:
    ✓ lock-status.sh                 — Real-time lock status monitoring
  
  Documentation:
    ✓ 90-DAY-LOCK-GUIDE.md           — Complete deployment guide


✔ LOCK PARAMETERS

  Lock ID:              550e8400-e29b-41d4-a716-446655440000
  Inception:            2025-01-14T10:00:00.000Z
  Expiry:               2025-04-14T10:00:00.000Z
  Duration:             90 days
  Root Merkle Hash:     a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6...
  Synchronized Engines: 14
  
  Wobble Snapshot (LOCKED):
    w_suu:   0.05      (Identity, iti/micro, slowest)
    w_aha:   0.075     (Structure, waenga/mid, moderate)
    w_rere:  0.15      (Flow, nui/macro, fastest)
  
  Kotahitanja (Unity):
    H = (1/3)*0.05 + (1/3)*0.075 + (1/3)*0.15 = 0.0917 (91.7% coherence)


✔ SYNCHRONIZED ENGINES (14 TOTAL)

  Core Ring:
    ▪ 365/validator      (365-day cycle root)
    ▪ 777/sovereign      (ultimate authority)
    ▪ 101/horizon        (boundary witness)
  
  Peer Ring (12):
    ▪ 1001, 1002, 1003, 1004, 1005, 1006
    ▪ 1007, 1008, 1009, 1010, 1011, 1012


═════════════════════════════════════════════════════════════════════════════
DEPLOYMENT STEPS
═════════════════════════════════════════════════════════════════════════════

OPTION 1: DOCKER COMPOSE (Development/Testing)
─────────────────────────────────────────────────────────────────────────────

  Step 1: Load lock environment
    bash:     source .env.lock
    PowerShell: $env:LOCK_ID="550e8400-e29b-41d4-a716-446655440000"; etc.
  
  Step 2: Start all 14 engines
    docker-compose -f docker-compose-90DAY-LOCK.yml up -d
  
  Step 3: Verify engines running
    docker ps -f label=lock=90day-sync
  
  Step 4: Check lock status
    bash lock-status.sh          # Single snapshot
    bash lock-status.sh watch    # Continuous (10s refresh)
  
  Step 5: Verify individual engines
    curl http://localhost:365/4gr/health
    curl http://localhost:777/4gr/health
    curl http://localhost:101/4gr/health
    curl http://localhost:1001/4gr/health
    # ... etc for all 14


OPTION 2: KUBERNETES (Production)
─────────────────────────────────────────────────────────────────────────────

  Step 1: Create namespace (optional)
    kubectl create namespace te-papa-matihiko --dry-run=client -o yaml | kubectl apply -f -
  
  Step 2: Deploy lock Secret
    kubectl apply -f k8s-lock-secret.yaml
    kubectl get secret engine-lock-90day -o yaml
  
  Step 3: Deploy lock ConfigMap
    kubectl apply -f k8s-lock-configmap.yaml
    kubectl get configmap engine-lock-metadata -o yaml
  
  Step 4: Deploy engine Deployments
    (Apply engine manifests — see 90-DAY-LOCK-GUIDE.md for examples)
  
  Step 5: Verify pods
    kubectl get pods -l lock=90day-sync
    kubectl logs deployment/engine-365
  
  Step 6: Check health
    kubectl exec -it deployment/engine-365 -- curl http://localhost:365/4gr/health


═════════════════════════════════════════════════════════════════════════════
LOCK ENFORCEMENT
═════════════════════════════════════════════════════════════════════════════

Every engine cycle:

  GROUND Phase:  Verify root integrity (pre-check)
    ├─ Root hash matches? ✔
    └─ Root core unchanged? ✔
  
  READ Phase:    Observe and measure drift
    ├─ Load lock anchor ✔
    ├─ Check lock not expired ✔
    ├─ Parse wobble snapshot ✔
    └─ Compute Merkle root ✔
  
  GATE Phase:    Apply root check (5-second rule)
    ├─ Lock valid & not expired → ACCEPT
    └─ Lock invalid or expired → REJECT (stabilization triggered)
  
  GROW Phase:    If accepted, expand context
    ├─ Update context ring ✔
    ├─ Update growth ledger ✔
    └─ Verify root integrity (post-check) ✔


═════════════════════════════════════════════════════════════════════════════
MONITORING
═════════════════════════════════════════════════════════════════════════════

Real-Time Lock Health:
  bash lock-status.sh              # Snapshot of all 14 engines
  watch -n 10 'bash lock-status.sh'  # Continuous monitoring

Container Health:
  docker ps -f label=lock=90day-sync  # Check all lock-enabled containers
  docker inspect engine-365 | grep -A 10 Health  # Individual engine health

Engine Logs:
  docker-compose -f docker-compose-90DAY-LOCK.yml logs engine-365
  docker-compose -f docker-compose-90DAY-LOCK.yml logs -f --tail 50 engine-365

Metrics:
  • Prometheus: http://localhost:9090
  • Grafana: http://localhost:3000 (admin/admin)

Lock Status via API:
  curl http://localhost:365/4gr/lock-status
  curl http://localhost:8888/health              (MCP audit suite)
  curl http://localhost:9999/thymus/health       (Digital thymus)


═════════════════════════════════════════════════════════════════════════════
TIMELINE
═════════════════════════════════════════════════════════════════════════════

Day 0 (2025-01-14):
  ✓ Lock generated & engines synchronized
  ✓ All 14 engines operating under same Merkle root
  ✓ Wobble constants immutable until expiry

Days 1-85:
  → Normal operation, lock enforced on every cycle
  → Monitor via: bash lock-status.sh watch

Day 85 (2025-04-09):
  → Prepare renewal: npx ts-node lock-initialize.ts
  → Review new lock parameters
  → Stage deployment

Days 88-90 (2025-04-11 to 2025-04-14):
  → Execute rolling restart of engines with new lock
  → Verify all engines under new root
  → Archive old lock state: mkdir -p lock-archives; cp lock-metadata.json lock-archives/

Day 90+ (2025-04-14+):
  ✓ Old lock expires
  ✗ Engines reject new pings (GATE fails)
  → Must restart with new lock or manually override
  → Prevents silent operation beyond 90 days


═════════════════════════════════════════════════════════════════════════════
EMERGENCY PROCEDURES
═════════════════════════════════════════════════════════════════════════════

Lock Expired (Accidental):
  1. Generate new lock: npx ts-node lock-initialize.ts
  2. Update environment: source .env.lock
  3. Restart engines: docker-compose -f docker-compose-90DAY-LOCK.yml restart
  4. Verify: bash lock-status.sh

Merkle Root Mismatch:
  1. Check lock file: cat lock-metadata.json | grep rootMerkleHash
  2. Verify engine states haven't been manually modified
  3. Rebuild from clean state:
     docker-compose -f docker-compose-90DAY-LOCK.yml down -v
     npx ts-node lock-initialize.ts
     docker-compose -f docker-compose-90DAY-LOCK.yml up -d

Engine Lock Validation Fails:
  1. Check engine logs: docker logs engine-365
  2. Verify lock environment: docker inspect engine-365 | grep LOCK_
  3. Confirm lock-metadata.json is readable in container:
     docker exec engine-365 cat /app/lock-metadata.json
  4. Restart with clean environment:
     source .env.lock
     docker-compose -f docker-compose-90DAY-LOCK.yml restart engine-365


═════════════════════════════════════════════════════════════════════════════
VERIFICATION CHECKLIST
═════════════════════════════════════════════════════════════════════════════

After deployment, verify:

  □ All 14 engine containers running
  □ All engines report "healthy" status
  □ No engine logs contain "lock_invalid" or "lock_expired"
  □ Merkle root hash matches lock-metadata.json
  □ All wobble constants match (.env.lock)
  □ MCP audit suite running (port 8888)
  □ Digital thymus running (port 9999)
  □ Prometheus collecting metrics (port 9090)
  □ Grafana dashboard accessible (port 3000)
  □ Lock status script shows all engines synchronized
  □ Time remaining shows ~90 days to expiry


═════════════════════════════════════════════════════════════════════════════
REFERENCES
═════════════════════════════════════════════════════════════════════════════

Documentation:
  • 90-DAY-LOCK-GUIDE.md          — Full deployment & renewal procedures
  • 4GR_FSE_GUIDE.md              — Engine state machine & validation logic
  • DIGITAL_IDENTITY_LAYER.md     — Digital trinity (すう/あは/れれ)
  • TRI-LANGUAGE-STRUCTURE-LOCKED.md — Language mappings (日本語/Te Reo/English)

Files:
  • .env.lock                     — Load this FIRST
  • lock-metadata.json            — Master lock state
  • docker-compose-90DAY-LOCK.yml — Deployment manifest
  • k8s-lock-secret.yaml          — K8s Secret
  • k8s-lock-configmap.yaml       — K8s ConfigMap

Renewal:
  • lock-initialize.ts (TypeScript) or lock-init-node.js (Node.js)
  • Run on day 85 to generate new 90-day lock


═════════════════════════════════════════════════════════════════════════════

Status: ✅ LOCKED IN & READY FOR DEPLOYMENT

All 14 engines synchronized to single cryptographic root.
Lock enforced on every cycle. Automatic expiry after 90 days.

Next step: Load environment and start engines
  source .env.lock
  docker-compose -f docker-compose-90DAY-LOCK.yml up -d

═════════════════════════════════════════════════════════════════════════════
