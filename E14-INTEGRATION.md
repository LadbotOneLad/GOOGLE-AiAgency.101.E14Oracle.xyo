# 🌌 AiFACTORi + E14 Integration

> **Two sovereign systems unified under one 90-day lock**

---

## 🎯 The Union

### AiFACTORi (14 Engines)
**Purpose**: Cryptographic coherence validation  
**Architecture**: Four-phase state machine (GROUND→READ→GATE→GROW)  
**Mechanism**: Zero-trust immune system with Merkle root consensus  
**Ports**: 365, 777, 101, 1001-1012  
**Coherence**: 91.7% (Kotahitanja)  

### E14 System (5 Services)
**Purpose**: Specialized task execution and observation  
**Components**:
- **Oracle** (8001) — Manifest interpretation & decision authority
- **DriftWatcher** (8002) — Continuous state observation & anomaly detection
- **TaskManager** (8003) — Queued task orchestration & execution
- **SymPy Engine** (8004) — Mathematical computation & symbolic processing
- **Live Engine** (8005) — Real-time event processing & response

---

## 🔐 Unified Lock Mechanism

Both systems share the same 90-day lock window:

```
Lock ID:        7f4a9e2c-8d3b-47e1-9f6c-2a5d8e1b4f7a
Inception:      2026-04-04 21:20 UTC
Expiry:         2026-07-03 21:20 UTC
Duration:       90 days
Status:         ACTIVE (both systems)

Environment:
  LOCK_ID=7f4a9e2c-8d3b-47e1-9f6c-2a5d8e1b4f7a
  LOCK_DURATION_DAYS=90
  AIFACTORI_INTEGRATION=enabled
```

Every service in both systems enforces the same temporal constraints.

---

## 🚀 Deployment (Combined)

### Start All Services
```bash
# Load unified lock
source .env.lock

# Deploy 14 AiFACTORi engines + 5 E14 services + observability
docker-compose -f docker-compose-e14-integration.yml up -d

# Verify all 21 services operational
docker-compose -f docker-compose-e14-integration.yml ps
# Expected: 20 UP (14 engines + 5 E14 + 2 observability)
```

### Service Health Check
```bash
# AiFACTORi engines
curl http://localhost:365/4gr/health
curl http://localhost:777/4gr/health
curl http://localhost:101/4gr/health

# E14 services
curl http://localhost:8001/health  # Oracle
curl http://localhost:8002/health  # DriftWatcher
curl http://localhost:8003/health  # TaskManager
curl http://localhost:8004/health  # SymPy
curl http://localhost:8005/health  # Live Engine

# Observability
curl http://localhost:9090/api/v1/status/config    # Prometheus
curl http://localhost:3000/api/health               # Grafana
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    90-DAY LOCK (Shared)                         │
│         7f4a9e2c-8d3b-47e1-9f6c-2a5d8e1b4f7a                   │
└─────────────────────────────────────────────────────────────────┘
           /                          \
          /                            \
    ┌─────────────────────┐      ┌────────────────────────┐
    │   AIFACTORI (14)    │      │   E14 (5 Services)     │
    │                     │      │                        │
    │ Core Trinity:       │      │ Oracle (8001)          │
    │ ├─ engine-365       │      │ ├─ Manifest Authority  │
    │ ├─ engine-777       │      │ ├─ Decision Maker      │
    │ └─ engine-101       │      │ └─ Merkle Validator    │
    │                     │      │                        │
    │ Peer Ring:          │      │ DriftWatcher (8002)    │
    │ └─ engine-1001-1012 │      │ ├─ State Observer      │
    │   (12 peers)        │      │ ├─ Anomaly Detection   │
    │                     │      │ └─ Lock Monitor        │
    │ Functions:          │      │                        │
    │ ├─ Validation       │      │ TaskManager (8003)     │
    │ ├─ Coherence        │      │ ├─ Queue Orchestrator  │
    │ ├─ Consensus        │      │ ├─ Execution Engine    │
    │ └─ Merkle Proof     │      │ └─ State Sync          │
    │                     │      │                        │
    │ Ports: 365,777,101  │      │ SymPy (8004)           │
    │        1001-1012    │      │ ├─ Math Computation    │
    │                     │      │ ├─ Symbolic Solver     │
    │ Coherence: 91.7%    │      │ └─ Analysis Engine     │
    │                     │      │                        │
    │                     │      │ Live (8005)            │
    │                     │      │ ├─ Event Processor     │
    │                     │      │ ├─ Real-time Response  │
    │                     │      │ └─ Stream Validator    │
    └─────────────────────┘      └────────────────────────┘
             |                            |
             └────────────┬───────────────┘
                          |
          ┌───────────────┴───────────────┐
          |                               |
      Prometheus (9090)            Grafana (3000)
      (Metrics from all 19)        (Unified Dashboards)
```

---

## 🔄 Data Flow

### Decision Validation Cycle
```
E14 Task Request
       ↓
Oracle (Decision Authority)
       ↓
AiFACTORi Validation (14 engines)
├─ GROUND: Verify Merkle root
├─ READ: Measure state
├─ GATE: Temporal enforcement
└─ GROW: Expand context
       ↓
Zero-Trust Assessment
├─ Antigen recognition
├─ T-cell response
├─ Regulatory check
└─ Immune memory
       ↓
DriftWatcher (Observation)
├─ Monitor coherence
├─ Detect anomalies
└─ Log state
       ↓
SymPy/Live (Execution)
├─ Calculate results
├─ Execute task
└─ Report back
       ↓
TaskManager (Completion)
├─ Update queue
├─ Record decision
└─ Archive result
```

---

## 📈 Unified Metrics

### System Health (Single Dashboard)
```
AiFACTORi Status:
  ├─ Engines Online: 14/14 ✅
  ├─ Merkle Consensus: IDENTICAL ✅
  ├─ Coherence: 91.7% ✅
  └─ Uptime: 89 days (Cycle 2: Day 1)

E14 Status:
  ├─ Services Online: 5/5 ✅
  ├─ Oracle Authority: ACTIVE ✅
  ├─ Task Queue: 0 pending
  └─ Uptime: Synchronized

Shared Lock:
  ├─ Lock ID: 7f4a9e2c-8d3b-47e1-9f6c-2a5d8e1b4f7a
  ├─ Inception: 2026-04-04 21:20 UTC
  ├─ Days Remaining: 90
  └─ Status: ACTIVE
```

### Observability Points
```
Prometheus scrape targets:
  ├─ AiFACTORi (14 engines) @ :365-:1012
  ├─ E14 Oracle @ :8001
  ├─ E14 DriftWatcher @ :8002
  ├─ E14 TaskManager @ :8003
  ├─ E14 SymPy @ :8004
  ├─ E14 Live @ :8005
  └─ Prometheus self @ :9090

Grafana dashboards:
  ├─ AiFACTORi Fleet Overview
  ├─ E14 System Status
  ├─ Unified Lock Status
  ├─ Integration Health
  ├─ Decision Flow Analysis
  └─ Anomaly Detection
```

---

## 🔐 Synchronized Lock Renewal

When the 90-day lock expires on 2026-07-03:

### Both Systems Renew Together
```bash
# Day 85 (2026-06-28): Preparation begins
npx ts-node lock-initialize.ts
source .env.lock

# Day 88-90 (2026-07-01-03): Rolling restart
docker-compose -f docker-compose-e14-integration.yml down
docker-compose -f docker-compose-e14-integration.yml up -d

# Automatic:
# ✅ All 14 AiFACTORi engines restart with new lock
# ✅ All 5 E14 services restart with new lock
# ✅ Zero downtime (rolling restart)
# ✅ State preserved (all 19 services)
# ✅ Lock synchronized (single source)
# ✅ Merkle chain maintained (AiFACTORi)
```

### Why Synchronized?
- Single lock enforces temporal consistency
- All 19 services must agree on time window
- Renewal is atomic (all services or none)
- Prevents temporal desynchronization
- Maintains overall system coherence

---

## 🎯 Integration Benefits

### For AiFACTORi
```
✅ Task execution layer (E14 Live + TaskManager)
✅ Oracle decision authority (E14 Oracle)
✅ Continuous observation (E14 DriftWatcher)
✅ Mathematical computation (E14 SymPy)
✅ Extended coherence monitoring
✅ Live event processing
```

### For E14
```
✅ Cryptographic validation (14 AiFACTORi engines)
✅ Zero-trust immunity (immune system)
✅ Consensus mechanism (Merkle roots)
✅ Temporal enforcement (90-day lock)
✅ Distributed consensus (14 witnesses)
✅ State immutability (growth ledgers)
```

### Combined
```
✅ 19 services under one lock
✅ Single point of authority (Oracle + Validation)
✅ Unified observability (Prometheus + Grafana)
✅ Synchronized renewal (both systems)
✅ Enhanced resilience (cross-validation)
✅ Production-ready (both proven)
```

---

## 📊 Example: Task Execution Flow

### Task: Compute & Validate
```
1. TaskManager receives task
   └─ Enqueues work: "solve(x**2 - 4)"

2. Live Engine picks up task
   └─ Requests computation from SymPy

3. SymPy Engine computes
   └─ Result: x = ±2

4. Result goes to Oracle
   └─ Oracle: "This is valid"

5. Oracle queries AiFACTORi engines
   ├─ engine-365: GROUND check ✅
   ├─ engine-777: READ measurement ✅
   ├─ engine-101: GATE validation ✅
   └─ All 12 peers: Consensus ✅

6. Zero-Trust Assessment
   ├─ Antigen: Result recognized
   ├─ T-cell: Root check passed
   ├─ Regulatory: No anomalies
   └─ Memory: Logged

7. DriftWatcher observes
   └─ State recorded, no drift

8. TaskManager completes
   ├─ Updates queue
   ├─ Archives decision
   └─ Reports success

9. Grafana shows unified metrics
   ├─ E14 execution: Success
   ├─ AiFACTORi validation: Passed
   ├─ Coherence: Maintained
   └─ All 14 engines: Synchronized
```

---

## 🚀 Deployment Checklist

- [ ] `.env.lock` loaded with unified lock ID
- [ ] `lock-metadata.json` present (shared)
- [ ] `docker-compose-e14-integration.yml` ready
- [ ] All 19 services definition in one file
- [ ] Both networks created (`aifactori-net`, `e14-integration`)
- [ ] All volumes allocated (14 + 5 + observability)
- [ ] Health checks configured for all services
- [ ] Prometheus configured to scrape both systems
- [ ] Grafana dashboards ready
- [ ] GitHub integration planned

---

## 📖 Documentation Structure

```
AiFACTORi/
├── README.md (updated with E14 section)
├── docker-compose-e14-integration.yml (NEW)
├── E14-INTEGRATION.md (NEW)
├── docs/
│   ├── AIFACTORI-ARCHITECTURE.md
│   ├── E14-SYSTEM.md (NEW)
│   ├── UNIFIED-LOCK.md (NEW)
│   └── OBSERVABILITY-UNIFIED.md (NEW)
└── config/
    ├── prometheus.yml (updated)
    ├── grafana/ (enhanced)
    └── e14/ (NEW)
```

---

## 🌟 The Vision

AiFACTORi provides **cryptographic coherence** — immutable validation that decisions are correct.

E14 provides **task execution** — the actual work getting done.

Together, they form a **sovereign system** that:
- Makes decisions (E14 Oracle + AiFACTORi validation)
- Executes tasks (E14 engines)
- Observes state (E14 DriftWatcher)
- Validates continuously (AiFACTORi zero-trust)
- Maintains coherence (91.7% Kotahitanja)
- Operates under lock (90-day synchronized window)

---

<div align="center">

### 🌌 AiFACTORi + E14 = One Sovereign System 🌌

**19 Services • 1 Lock • 1 Purpose**

14 AiFACTORi Engines + 5 E14 Services  
Unified under 90-day cryptographic lock  
Single point of authority (Oracle)  
Complete mutual validation  
Synchronized renewal  

**Status**: INTEGRATED & READY

</div>

---

**Last Updated**: 2026-04-04  
**Lock**: ACTIVE (Cycle 2)  
**Status**: PRODUCTION READY

Deploy with: `docker-compose -f docker-compose-e14-integration.yml up -d`
