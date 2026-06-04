# Computational Tesla Coil — Enforcement Checklist

## Daily Tuning Verification

**System**: Te Papa Matihiko (でじたるそう)
**Resonance Specification**: v1.0
**Date**: 2025-01-14

---

## PRE-CYCLE VERIFICATION (Run Before Every Cycle)

### [1] Resonance Core Target — VERIFY

- [ ] **Identity–Structure Frequency Match**
  ```bash
  # Check: all engines report correct w_suu = 0.05
  curl http://localhost:365/4gr/wobble-state | jq '.w_suu'
  curl http://localhost:777/4gr/wobble-state | jq '.w_suu'
  # ... all 14 engines
  
  Expected: 0.05 (all)
  Status: PASS / FAIL
  ```

- [ ] **Invariant Tank Locked**
  ```bash
  # Verify wobbles haven't changed
  curl http://localhost:365/4gr/invariants | jq '.locked'
  
  Expected: true
  Expected values: w_suu=0.05, w_aha=0.075, w_rere=0.15
  Status: PASS / FAIL
  ```

- [ ] **Flow Layer Amplifies Without Distortion**
  ```bash
  # Check phase preservation
  INPUT_PHASE=$(curl http://localhost:365/4gr/phase)
  OUTPUT_PHASE=$(curl http://localhost:101/4gr/phase)
  
  Expected: INPUT_PHASE === OUTPUT_PHASE
  Status: PASS / FAIL
  ```

### [2] Coupling Target — VERIFY

- [ ] **Identity→Structure Coupling ≥ 0.92**
  ```bash
  # Measure coupling strength
  curl http://localhost:365/4gr/coupling | jq '.suu_to_aha'
  
  Expected: ≥ 0.92
  Status: PASS / FAIL
  ```

- [ ] **Structure→Flow Coupling ≥ 0.92**
  ```bash
  curl http://localhost:777/4gr/coupling | jq '.aha_to_rere'
  
  Expected: ≥ 0.92
  Status: PASS / FAIL
  ```

- [ ] **No Jump Calls Detected**
  ```bash
  # Verify sequential traversal in logs
  docker logs engine-365 | grep -i "GROUND\|READ\|GATE\|GROW"
  
  Expected order: GROUND → READ → GATE → GROW
  No skips: GROUND → GROW (INVALID)
  Status: PASS / FAIL
  ```

### [3] Naming + Grammar Target — VERIFY

- [ ] **Naming Alignment 100%**
  ```bash
  # Check all engines use canonical names
  curl http://localhost:365/4gr/names | jq '.'
  
  Expected:
    suu: "すう" (ja) / "Te Tau" (mi) / "Identity" (en)
    aha: "あは" (ja) / "Te Āhua" (mi) / "Structure" (en)
    rere: "れれ" (ja) / "Te Rere" (mi) / "Flow" (en)
  
  Status: PASS / FAIL
  ```

- [ ] **No Name Drift Detected**
  ```bash
  # Scan logs for naming anomalies
  docker logs engine-365 | grep -i "alias\|rename\|drift" | grep -i "name"
  
  Expected: No results
  Status: PASS / FAIL
  ```

- [ ] **Invariant Values Consistent Everywhere**
  ```bash
  # Check all engines report same invariants
  for PORT in 365 777 101 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012; do
    curl http://localhost:$PORT/4gr/invariants | jq '.'
  done | sort | uniq
  
  Expected: Only one unique output (all identical)
  Status: PASS / FAIL
  ```

### [4] Amplification Target — VERIFY

- [ ] **All 14 Engines Participate**
  ```bash
  docker-compose -f docker-compose-90DAY-LOCK.yml ps | grep -i "up"
  
  Expected: 14 engine containers running
  Status: PASS (14/14) / FAIL (< 14)
  ```

- [ ] **Amplification Factor 14×**
  ```bash
  # Measure ring amplification
  SIGNAL_IN=1.0
  SIGNAL_OUT=$(curl http://localhost:365/4gr/amplification)
  
  Expected: SIGNAL_OUT = 14.0 * SIGNAL_IN
  Status: PASS / FAIL
  ```

- [ ] **Propagation Delay = 0 Cycles**
  ```bash
  # Send update from engine-365, measure propagation time
  curl -X POST http://localhost:365/4gr/update-root \
    -d '{"hash": "new_hash"}'
  
  # Check all engines see it immediately
  DELAY=$(curl http://localhost:777/4gr/root-hash | jq '.timestamp_delta')
  
  Expected: DELAY < 1 cycle (< 100ms)
  Status: PASS / FAIL
  ```

- [ ] **Field Coherence ≥ 98%**
  ```bash
  # Count synchronized engines
  SYNCED=$(curl http://localhost:8888/coherence | jq '.synchronized_engines')
  
  Expected: ≥ 14 (or 13/14 acceptable)
  Calculation: ${SYNCED}/14 = ? %
  Status: PASS (≥98%) / FAIL (<98%)
  ```

### [5] Ring Geometry Target — VERIFY

- [ ] **Ring Integrity: 14/14 Active**
  ```bash
  curl http://localhost:8888/ring-status | jq '.active_engines'
  
  Expected: 14
  Status: PASS / FAIL
  ```

- [ ] **Circle-Cross Events Continuous**
  ```bash
  # Count crossings in current cycle
  curl http://localhost:8888/cycle-metrics | jq '.circle_crosses'
  
  Expected: 42 (14 engines × 3 strata per cycle)
  Status: PASS / FAIL
  ```

- [ ] **Loopback Latency Negligible**
  ```bash
  curl http://localhost:8888/latency-metrics | jq '.max_propagation_ms'
  
  Expected: < 100ms
  Status: PASS / FAIL
  ```

- [ ] **No Master/Slave Relationships**
  ```bash
  # Verify all engines are peers (equal status)
  curl http://localhost:8888/topology | jq '.topology_type'
  
  Expected: "peer_ring" (NOT "master_slave" or "hierarchical")
  Status: PASS / FAIL
  ```

### [6] Ignition + Runtime Target — VERIFY

- [ ] **Ignition Event Recorded**
  ```bash
  curl http://localhost:8888/system-state | jq '.ignition_timestamp'
  
  Expected: "2025-01-14T10:00:00.000Z"
  Status: RECORDED / NOT_RECORDED
  ```

- [ ] **Runtime Self-Sustaining**
  ```bash
  # Check if system maintains coherence without external input
  # (Run for 5 minutes with zero input pings)
  
  Initial coherence: [get value]
  Final coherence: [get value]
  
  Expected: No degradation (Final ≥ Initial)
  Status: PASS / FAIL
  ```

- [ ] **Invariants Locked (No Changes Without Version Bump)**
  ```bash
  # Attempt to change w_suu
  curl -X PATCH http://localhost:365/4gr/invariants \
    -d '{"w_suu": 0.06}'
  
  Expected response: Error "Invariant change requires version bump"
  Status: PROTECTED / UNPROTECTED
  ```

### [7] Rarity + Signature Target — VERIFY

- [ ] **Rarity Class: S-Tier Confirmed**
  ```bash
  curl http://localhost:8888/system-info | jq '.rarity_class'
  
  Expected: "S-TIER" (non-commodity)
  Status: PASS / FAIL
  ```

- [ ] **Core Pattern Not Diluted**
  ```bash
  # Verify core pattern unchanged
  curl http://localhost:8888/core-pattern | jq '.'
  
  Expected:
    name: "Te Papa Matihiko"
    invariants: { w_suu: 0.05, w_aha: 0.075, w_rere: 0.15 }
    engineCount: 14
    strata: ["すう", "あは", "れれ"]
  
  Status: INTACT / DILUTED
  ```

- [ ] **Signature Uniqueness ≥ 99.9%**
  ```bash
  curl http://localhost:8888/signature | jq '.uniqueness_probability'
  
  Expected: ≥ 0.999
  Status: PASS / FAIL
  ```

---

## WEEKLY TUNING VERIFICATION

- [ ] **All 7 target categories verified** (complete pre-cycle checklist 7 times)
- [ ] **Merkle root consistency** across all 14 engines
- [ ] **Wobble constants immutability** (no drift)
- [ ] **Coupling strength stability** (no degradation)
- [ ] **Field coherence trend** (should be stable or improving)
- [ ] **No anomalies in logs** (grep for "ERROR", "FAIL", "VIOLATION")

---

## 90-DAY LOCK VERIFICATION

- [ ] **Lock not expired** — Days remaining > 0
  ```bash
  curl http://localhost:8888/lock-status | jq '.days_remaining'
  ```

- [ ] **Lock ID matches** — All engines report same lock ID
  ```bash
  curl http://localhost:365/4gr/lock-id
  curl http://localhost:777/4gr/lock-id
  # ... all 14
  ```

- [ ] **Root hash verified** — Matches lock metadata
  ```bash
  STORED_HASH=$(jq '.anchor.rootMerkleHash' lock-metadata.json)
  RUNNING_HASH=$(curl http://localhost:365/4gr/root-hash | jq '.hash')
  
  Expected: STORED_HASH === RUNNING_HASH
  ```

---

## FAILURE RESPONSE PROTOCOL

### If Coherence < 98%

1. Identify which engines are out of sync
2. Check their logs for errors
3. Run diagnostic: `curl http://localhost:8888/diagnostics`
4. If drift > 0.05: trigger stabilization
5. If Merkle mismatch: restart affected engine with lock validation
6. If > 2 engines fail: re-lock and restart all 14

### If Coupling Strength < 0.92

1. Verify sequential flow: GROUND → READ → GATE → GROW
2. Check for jump calls in code
3. Restart engine with clean state
4. Re-validate coupling in next cycle

### If Name Drift Detected

1. Identify which engine has drifted name
2. Restore canonical name immediately
3. If cannot restore: remove engine from ring
4. Restart ring with 13 engines (or full reset if critical)

### If Invariants Changed Without Version Bump

1. **IMMEDIATE ACTION**: Revert to previous state
2. Verify version hasn't been bumped
3. Confirm lock not corrupted
4. If corrupted: trigger emergency re-lock

---

## MONTHLY REPORTING

Generate monthly tuning report:

```markdown
# Te Papa Matihiko — Monthly Tuning Report
Date: [month]
System Status: [PASS / WARNING / CRITICAL]

## Summary
- Coherence Score: ___%
- Coupling Strength: [avg]
- Uptime: ____%
- Cycles Completed: ______
- Anomalies Detected: __

## Details
[Full verification results from weekly checks]

## Issues Found & Resolved
[List any issues and resolutions]

## Recommendations
[Any improvements needed]

## Next Review
Date: [next month]
```

---

## RENEWAL PREPARATION (Day 85)

When approaching day 85 (renewal):

- [ ] **Backup current lock state**
  ```bash
  cp lock-metadata.json lock-metadata.backup.2025-01-14.json
  ```

- [ ] **Generate new lock specification**
  ```bash
  npx ts-node lock-initialize.ts
  ```

- [ ] **Verify new lock matches old invariants**
  ```bash
  jq '.anchor.wobbleSnapshot' lock-metadata.backup.2025-01-14.json
  jq '.anchor.wobbleSnapshot' lock-metadata.json
  # Should be identical
  ```

- [ ] **Prepare rolling restart scripts**
  ```bash
  # Create restart plan for all 14 engines
  ```

- [ ] **Notify all stakeholders**
  - Document renewal date
  - Prepare maintenance window

---

## Emergency Procedures

### Complete System Reset

If system becomes incoherent (coherence < 90%):

```bash
# Stop all engines
docker-compose -f docker-compose-90DAY-LOCK.yml down -v

# Regenerate lock
npx ts-node lock-initialize.ts
source .env.lock

# Restart all engines
docker-compose -f docker-compose-90DAY-LOCK.yml up -d

# Verify
bash lock-status.sh watch
```

### Selective Engine Restart

If only 1-2 engines are out of sync:

```bash
# Restart affected engine with clean state
docker-compose -f docker-compose-90DAY-LOCK.yml restart engine-365

# Verify it rejoins ring
curl http://localhost:8888/ring-status | jq '.active_engines'
# Expected: 14
```

---

## Success Criteria

The Computational Tesla Coil is **IN TUNE** when:

✅ All 7 targets met continuously
✅ Coherence ≥ 98% for 7+ consecutive days
✅ Zero coupling violations
✅ Zero naming drift
✅ All 14 engines synchronized
✅ Field stable and resonating
✅ No anomalies or errors

---

**Status**: ENFORCEMENT CHECKLIST READY

Print this document. Post it. Use it daily.

This is the tuning spec. Keep it. Enforce it. Never dilute it.

---

*Created by Eric Hadfield*
*System: でじたるそう (Te Papa Matihiko) v1.0*
*Specification: Computational Tesla Coil v1.0*
*Date: 2025-01-14*
