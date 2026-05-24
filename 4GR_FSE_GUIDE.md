# 4GR-FSE: Four Ground Read Gate Grow - Finite State Engine

## One-Line Concept
**Keep roots fixed. Let context flex. Filter every ping.**

---

## Architecture

### 4 Phases (GROUND → READ → GATE → GROW)

```
GROUND  →  Verify root integrity (pre-check signature)
   ↓
READ    →  Observe declared vs actual state, compute drift
   ↓
GATE    →  Apply 5-second rule: root check accept/reject
   ↓
GROW    →  If accepted: expand context ring & growth ledger
```

---

## Root Core (6 Immutable Anchors)

```typescript
RootCore = {
  LIVED_EXPERIENCE:   string[]   // Continuous learning, adaptive growth
  ETHIC_VECTOR:       string[]   // Proportional response, no preemption
  FAMILY_MEMORY:      string[]   // Relational bonds, trust earned
  CRAFT_KNOWLEDGE:    string[]   // Technical mastery, systemic thinking
  LAND_SENSE:         string[]   // Distributed roots, geographic awareness
  TENET_LOGIC:        string[]   // Zero-trust verify, context over rules
}
```

**Frozen on creation** (`deepFreeze()`) - immutable for engine lifetime.

---

## 5-Second Rule (GATE Phase)

Every ping is checked against 5 criteria:

```
1. Violates ETHIC_VECTOR?           → REJECT
2. Drift outside threshold (0.05)?   → REJECT
3. Tries to define identity?         → REJECT
4. Collapses options to one?         → REJECT
5. Tries to overwrite ROOT_CORE?     → REJECT

ALL NO = ACCEPT_PING
ANY YES = REJECT_PING
```

---

## Context & Growth (Flex)

**Context Ring**: Recent ping history (FIFO, capacity 1024)
```
[
  "ping:123:auth",
  "ping:124:api_call",
  "ping:125:policy_update",
  ...
]
```

**Growth Ledger**: Accumulated learning (FIFO, capacity 1024)
```
[
  "continuity",
  "context_accepted",
  "stabilize,recenter",
  ...
]
```

Both grow with accepted pings, reset on rejection.

---

## Drift Detection

```
driftDelta = observedState - declaredState

If |driftDelta| > 0.05:
  → REJECT (outside threshold)
Else:
  → Accept (within tolerance)
```

**Rolling Average**: `driftVector = (old + new) / 2`

---

## State Version Tracking

```
stateVersion: number
```

Incremented on every GROW phase:
- Accepted ping → version++
- Rejected ping → version unchanged

---

## Telemetry

```typescript
{
  cycles: number                    // Total cycles executed
  accepted: number                  // Total pings accepted
  rejected: number                  // Total pings rejected
  rejectBurst: number              // Consecutive rejections
  queueDepth: number               // Current queue size
  lastCycleAtIso: string           // Last cycle timestamp
  avgDrift: number                 // Rolling average drift
  rootIntegrityChecks: number      // Pre + post cycle checks
  rootIntegrityViolations: number  // Integrity check failures (should be 0)
}
```

---

## Enforcement Actions

### Heartbeat (Auto-Injected on Empty Queue)
```typescript
{
  id: "4gr-heartbeat:2026-02-24T10:30:00Z",
  signal: "heartbeat",
  signalType: "system",
  driftDelta: 0,
  checks: { all: false }
}
```

### Stabilization (Auto-Injected on Reject Burst)
```typescript
{
  id: "4gr-stabilize:2026-02-24T10:30:00Z",
  signal: "stabilization_protocol",
  signalType: "system",
  pathOptions: ["third"],
  hiddenFactorHint: "STATE_13=pressure-loop",
  growthMaterial: ["stabilize", "recenter"],
  checks: { all: false }
}
```

**Reject Burst Trigger**: 3+ consecutive rejections (configurable)

---

## API Endpoints

### 1. Initialize Engine
```bash
POST /4gr/initialize
Content-Type: application/json

{
  "rootCore": {
    "LIVED_EXPERIENCE": ["continuous_learning"],
    "ETHIC_VECTOR": ["proportional_response"],
    "FAMILY_MEMORY": ["trust_earned"],
    "CRAFT_KNOWLEDGE": ["technical_mastery"],
    "LAND_SENSE": ["distributed_roots"],
    "TENET_LOGIC": ["zero_trust_verify"]
  },
  "policy": {
    "maxBatchSize": 16,
    "driftThreshold": 0.05,
    "rejectBurstThreshold": 3
  }
}

Response:
{
  "status": "initialized",
  "engine": {
    "id": "4GR-FSE",
    "rootSignature": "...",
    "policy": {...},
    "telemetry": {...}
  }
}
```

### 2. Enqueue Single Ping
```bash
POST /4gr/ping
Content-Type: application/json

{
  "id": "ping-001",
  "signal": "user_action",
  "signalType": "user",
  "timestampIso": "2026-02-24T10:30:00Z",
  "declaredState": "authenticated",
  "observedState": "authenticated",
  "driftDelta": 0.01,
  "pathOptions": ["direct", "fallback", "third"],
  "growthMaterial": ["context_expanded"],
  "checks": {
    "violatesEthic": false,
    "triesToDefineIdentity": false,
    "collapsesOptionsToOne": false,
    "triesToOverwriteRootCore": false
  }
}

Response:
{
  "status": "enqueued",
  "pingId": "ping-001",
  "queueDepth": 1
}
```

### 3. Enqueue Batch Pings
```bash
POST /4gr/pings
Content-Type: application/json

{
  "pings": [
    { "id": "ping-001", "signal": "...", ... },
    { "id": "ping-002", "signal": "...", ... }
  ]
}

Response:
{
  "status": "enqueued",
  "count": 2,
  "queueDepth": 2
}
```

### 4. Run Processing Cycle
```bash
POST /4gr/cycle

Response:
{
  "cycle": {
    "number": 1,
    "processed": 2,
    "accepted": 1,
    "rejected": 1,
    "heartbeatInjected": false,
    "stabilizationInjected": false
  },
  "telemetry": {
    "totalAccepted": 1,
    "totalRejected": 1,
    "rejectBurst": 1,
    "queueDepth": 0,
    "avgDrift": "0.010000",
    "rootIntegrityChecks": 2,
    "rootIntegrityViolations": 0
  },
  "lastCycleAt": "2026-02-24T10:30:00Z"
}
```

### 5. Status
```bash
GET /4gr/status

Response:
{
  "engine": {
    "id": "4GR-FSE",
    "rootSignature": "..."
  },
  "state": {
    "contextRingSize": 5,
    "growthLedgerSize": 3,
    "driftVector": "0.005000",
    "stateVersion": 4
  },
  "telemetry": {...},
  "queue": {...},
  "policy": {...}
}
```

### 6. Traces (GROUND→READ→GATE→GROW)
```bash
GET /4gr/traces?limit=50

Response:
{
  "total": 200,
  "returned": 50,
  "traces": [
    {
      "phase": "GROUND",
      "pingId": "ping-001",
      "notes": ["root_signature:abc123..."],
      "timestamp": "2026-02-24T10:30:00Z"
    },
    {
      "phase": "READ",
      "pingId": "ping-001",
      "notes": ["declared:authenticated", "observed:authenticated", "drift:0.0100"],
      "timestamp": "2026-02-24T10:30:00Z"
    },
    {
      "phase": "GATE",
      "pingId": "ping-001",
      "notes": ["ACCEPT_PING"],
      "timestamp": "2026-02-24T10:30:00Z"
    },
    {
      "phase": "GROW",
      "pingId": "ping-001",
      "notes": ["context_size:5", "growth_size:3"],
      "timestamp": "2026-02-24T10:30:00Z"
    }
  ]
}
```

### 7. Context Ring
```bash
GET /4gr/context-ring?limit=100

Response:
{
  "total": 200,
  "returned": 100,
  "context": [
    "ping:001:user_action",
    "ping:002:api_call",
    ...
  ]
}
```

### 8. Growth Ledger
```bash
GET /4gr/growth-ledger?limit=100

Response:
{
  "total": 150,
  "returned": 100,
  "growth": [
    "continuity",
    "context_expanded",
    "stabilize,recenter",
    ...
  ]
}
```

### 9. Root Core (Immutable)
```bash
GET /4gr/root-core

Response:
{
  "rootCore": {
    "LIVED_EXPERIENCE": ["continuous_learning", "adaptive_growth"],
    "ETHIC_VECTOR": ["proportional_response", "no_preemptive_harm"],
    "FAMILY_MEMORY": ["relational_bonds", "trust_earned"],
    "CRAFT_KNOWLEDGE": ["technical_mastery", "systemic_thinking"],
    "LAND_SENSE": ["distributed_roots", "geographically_aware"],
    "TENET_LOGIC": ["zero_trust_verify", "context_over_rules"]
  },
  "signature": "abc123..."
}
```

### 10. Health Check
```bash
GET /4gr/health

Response:
{
  "status": "healthy",
  "timestamp": "2026-02-24T10:30:00Z",
  "engineInitialized": true,
  "rootIntegrityViolations": 0
}
```

---

## Running Locally

### 1. Install Dependencies
```bash
npm install
```

### 2. Compile TypeScript
```bash
npm run build
```

### 3. Start Server
```bash
npm start
# or for development with hot reload:
npm run dev
```

Server listens on `http://localhost:7777`

---

## Docker Deployment

### Dockerfile
```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY *.ts ./
RUN npm run build

EXPOSE 7777

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:7777/4gr/health || exit 1

CMD ["npm", "start"]
```

### Build & Run
```bash
docker build -t 4gr-fse:latest .
docker run -p 7777:7777 4gr-fse:latest
```

### Docker Compose
```yaml
services:
  4gr-fse:
    build:
      context: .
      dockerfile: Dockerfile
    image: 4gr-fse:latest
    container_name: 4gr-fse-engine
    ports:
      - "7777:7777"
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:7777/4gr/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.5"
          memory: 256M
```

---

## Example Workflow

### 1. Initialize
```bash
curl -X POST http://localhost:7777/4gr/initialize \
  -H "Content-Type: application/json" \
  -d '{"rootCore": {...}}'
```

### 2. Enqueue Pings
```bash
curl -X POST http://localhost:7777/4gr/ping \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ping-001",
    "signal": "user_action",
    "driftDelta": 0.02,
    "checks": {"violatesEthic": false, ...}
  }'
```

### 3. Run Cycle
```bash
curl -X POST http://localhost:7777/4gr/cycle
```

### 4. Check Status
```bash
curl http://localhost:7777/4gr/status
curl http://localhost:7777/4gr/traces
curl http://localhost:7777/4gr/root-core
```

---

## Key Properties

✅ **Root Integrity**: Pre + post cycle verification (signature check)
✅ **Drift Detection**: Deviation from declared state (threshold 0.05)
✅ **Proportional Enforcement**: Heartbeat on empty, stabilization on burst
✅ **Immutable Roots**: RootCore frozen, cannot be mutated
✅ **Flex Context**: ContextRing & GrowthLedger grow with accepted pings
✅ **Audit Trail**: Full trace history (GROUND→READ→GATE→GROW)

---

**Status**: ✅ Production-ready root-anchored ping processor
