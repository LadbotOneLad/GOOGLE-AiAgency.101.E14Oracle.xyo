# AIFACTORIES INTERNAL TELEMETRY DEPLOYMENT
## 127.0.0.1:7777 (Localhost Only, Air-Gapped)

**Authority**: Rebecca (AiFACTORIES v1.0)  
**Date**: 2026-04-03  
**Scope**: Internal only (Docker bridge network)  
**Security**: Air-gapped (zero external exposure)  

---

## OVERVIEW

**AiFACTORIES Internal Deployment** runs telemetry entirely within a Docker network, accessible only from localhost (127.0.0.1:7777).

All telemetry:
- ✓ Stays inside Docker network
- ✓ Never transmitted externally
- ✓ Never exposed to public internet
- ✓ Immutable audit trail (append-only, hash-chained)
- ✓ Accessible only from localhost

---

## COMPONENTS

### 1. **Internal Gateway** (aifactories-internal-gateway)
```
Port: 127.0.0.1:7777 (localhost only)
Service: HTTP API for telemetry queries
Scope: Docker bridge network + localhost
```

**Available endpoints:**
```
GET /internal/status      — Cluster synchronization status
GET /internal/doctrines   — Doctrine compliance check
GET /internal/earth-lock  — True north alignment status
GET /internal/health      — Gateway health check
```

### 2. **Audit Processor** (aifactories-audit-processor)
```
Function: Writes immutable audit trail
Storage: /logs/aifactories/audit_trail.jsonl
Format: Append-only, hash-chained entries
Access: Internal only (no external API)
```

Each audit entry:
- Timestamp (UTC ISO)
- Sequence number
- Event type (GATE_*, DOCTRINE_CHECK, EARTH_LOCK_CHECK, CONSENSUS_VOTE)
- Engine ID
- Decision (pass/fail)
- Previous entry hash (chain integrity)
- Entry hash (immutability proof)

### 3. **Master Engine** (aifactories-master-internal)
```
Engine: 0 (master)
Scope: Internal Docker network only
No external ports
Writes telemetry to shared volume
```

### 4. **Validators** (aifactories-validator-1-4-internal)
```
Engines: 1-4 (sample validators)
Scope: Internal Docker network only
No external ports
Synchronized with Earth's clock
```

---

## DEPLOYMENT

### 1. Start Internal Cluster
```bash
docker-compose -f docker-compose-aifactories-internal.yml up -d
```

### 2. Verify Containers Running
```bash
docker ps | grep aifactories-internal
# Output: 7 containers (gateway + audit + master + 4 validators)
```

### 3. Test Gateway (from localhost only)
```bash
# Cluster status
curl http://127.0.0.1:7777/internal/status | jq .

# Doctrine compliance
curl http://127.0.0.1:7777/internal/doctrines | jq .

# Earth-lock alignment
curl http://127.0.0.1:7777/internal/earth-lock | jq .

# Gateway health
curl http://127.0.0.1:7777/internal/health | jq .
```

### 4. Check Audit Trail
```bash
# View latest audit entries
docker exec aifactories-audit-processor cat /logs/aifactories/audit_trail.jsonl | tail -5 | jq .

# Verify integrity
docker exec aifactories-audit-processor python3 -c "
from aifactories_immutable_audit import ImmutableAuditTrail
audit = ImmutableAuditTrail('/logs/aifactories/audit_trail.jsonl')
print(audit.verify_integrity())
" | jq .
```

### 5. Monitor Telemetry
```bash
# Real-time engine telemetry
watch "ls -la logs/aifactories/engine_*_telemetry.json | tail -5"

# Stream latest status
while true; do
  curl -s http://127.0.0.1:7777/internal/status | jq .cluster
  sleep 5
done
```

---

## SECURITY MODEL

### Air-Gapped (No External Access)

```
┌─────────────────────────────────────────┐
│  Docker Network (aifactories_internal)  │
│  ┌─────────────────────────────────────┐│
│  │ Master Engine (0)                   ││
│  │ Validators (1-4)                    ││
│  │ Audit Processor                     ││
│  │ Internal Gateway (127.0.0.1:7777)   ││
│  └─────────────────────────────────────┘│
│          ↓                               │
│  Shared Volume (/logs/aifactories)      │
│      ↓                                   │
│  - engine_*_telemetry.json              │
│  - audit_trail.jsonl (immutable)        │
│  - internal_audit.jsonl                 │
└─────────────────────────────────────────┘
         ↓
    localhost only (127.0.0.1:7777)
    ↓ (NO EXTERNAL ACCESS)
```

### Why This Is Secure

1. **No external ports exposed** (except 127.0.0.1:7777)
2. **Docker bridge network** (isolated from host network)
3. **Localhost binding only** (127.0.0.1, not 0.0.0.0)
4. **Immutable audit trail** (append-only, hash-chained)
5. **No external API calls** (all data internal)
6. **No credential transmission** (no auth needed for internal)

---

## IMMUTABLE AUDIT TRAIL

### Format

Each audit entry is a JSON object with:
```json
{
  "timestamp": "2026-04-03T23:00:00.000000",
  "sequence": 1,
  "event": "GATE_1",
  "engine_id": 0,
  "data": {
    "gate_id": 1,
    "error": 0.01
  },
  "decision": true,
  "previous_hash": "abc123...",
  "entry_hash": "def456..."
}
```

### Integrity Guarantee

```
Entry[0]
  ↓ (hash)
Entry[1] (previous_hash = Entry[0].hash)
  ↓ (hash)
Entry[2] (previous_hash = Entry[1].hash)
  ↓ (hash)
Entry[N] (previous_hash = Entry[N-1].hash)

If any entry is modified:
  - Its hash changes
  - Next entry's previous_hash no longer matches
  - Chain break is detected
  - Tamper detected
```

### Verification

```bash
# Programmatic verification
python3 -c "
from aifactories_immutable_audit import ImmutableAuditTrail
audit = ImmutableAuditTrail('/logs/aifactories/audit_trail.jsonl')
result = audit.verify_integrity()
print(f'Valid: {result[\"valid\"]}')
print(f'Entries: {result[\"entries_checked\"]}')
print(f'Breaks: {result[\"breaks\"]}')
"
```

---

## OPERATIONAL PROCEDURES

### Daily Checks

```bash
# 1. Gateway health
curl -s http://127.0.0.1:7777/internal/health | jq .status

# 2. Cluster status
curl -s http://127.0.0.1:7777/internal/status | jq .cluster.consensus_reached

# 3. Doctrine compliance
curl -s http://127.0.0.1:7777/internal/doctrines | jq .compliance_rate

# 4. Earth-lock alignment
curl -s http://127.0.0.1:7777/internal/earth-lock | jq .alignment_rate

# 5. Audit integrity
docker exec aifactories-audit-processor python3 audit.py | jq .valid
```

### Container Logs

```bash
# Gateway logs
docker logs aifactories-internal-gateway

# Audit processor logs
docker logs aifactories-audit-processor

# Master engine
docker logs aifactories-master-internal

# Validators
docker logs aifactories-validator-1-internal
docker logs aifactories-validator-2-internal
docker logs aifactories-validator-3-internal
docker logs aifactories-validator-4-internal
```

### Backup Audit Trail

```bash
# Backup to external location (still internal)
docker cp aifactories-master-internal:/logs/aifactories/audit_trail.jsonl ./audit_backup_$(date +%s).jsonl

# Verify backup integrity
python3 -c "
from aifactories_immutable_audit import ImmutableAuditTrail
audit = ImmutableAuditTrail('./audit_backup_*.jsonl')
print(audit.verify_integrity())
"
```

---

## SCALING FROM INTERNAL TO GLOBAL

### Phase 1 (Current): Internal Testing
```
5 engines (master + 4 validators)
Localhost gateway (127.0.0.1:7777)
All telemetry internal
```

### Phase 2: Add More Validators (Keep Internal)
```
13 engines (master + 12 validators)
Same gateway (127.0.0.1:7777)
All telemetry internal
```

### Phase 3: Deploy Globally (When Ready)
```
Use docker-compose-aifactories-global.yml
Ports 6650-6662 (public)
Telemetry aggregation at higher level
Same audit trail, same immutability
```

---

## FINAL INVARIANT

> **"All telemetry stays inside. The gateway is localhost-only. The audit trail is immutable and append-only. External access is forbidden by design. Integrity is provable. Tampering is detectable. The system is its own witness."**

---

## FILES FOR INTERNAL DEPLOYMENT

| File | Purpose |
|------|---------|
| `docker-compose-aifactories-internal.yml` | Internal-only deployment |
| `aifactories_internal_gateway.py` | Telemetry gateway (127.0.0.1:7777) |
| `aifactories_immutable_audit.py` | Immutable audit trail (hash-chained) |
| `aifactories_earth_locked_core.py` | Engine core (same as global) |

---

**Status**: READY FOR INTERNAL DEPLOYMENT  
**Security**: Air-gapped (no external access)  
**Telemetry**: Immutable, hash-chained, append-only  
**Gateway**: 127.0.0.1:7777 (localhost only)  

---

**Deploy Internal Test Cluster Now:**
```bash
docker-compose -f docker-compose-aifactories-internal.yml up -d
curl http://127.0.0.1:7777/internal/status | jq .
```

**AiFACTORIES Internal Telemetry — OPERATIONAL**
