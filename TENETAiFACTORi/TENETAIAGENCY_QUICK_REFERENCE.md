# TENETAIAGENCY QUICK REFERENCE
## The Older Brother Law

---

## 6 GATES AT A GLANCE

| # | Gate | Condition | Failure | Meaning |
|---|------|-----------|---------|---------|
| 1 | Hash-Chain Integrity | E_t = 1 | IMMEDIATE VETO | No execution without valid audit trail |
| 2 | Byzantine Quorum | V_t ≥ 8/12 | LOCK DENIED | Need 67% validator consensus |
| 3 | 10-Order Majority | O_t ≥ 6/10 | LOCK DENIED | Need 60% MCP service alignment |
| 4 | Coherence Floor | C_t ≥ C_min | LOCK DENIED | System must reach internal agreement |
| 5 | Drift Ceiling | D_t ≤ D_max | LOCK DENIED | System must stay near attractor |
| 6 | Power Discipline | P_t(1−C_t) ≤ ε | LOCK DENIED | Power only safe when coherent |

---

## DECISION FUNCTION

```
F_t = E_t ∧ (V_t ≥ 8/12) ∧ (O_t ≥ 6/10) ∧ (C_t ≥ C_min) ∧ (D_t ≤ D_max) ∧ (P_t(1−C_t) ≤ ε)

If F_t = 1: EXECUTE
If F_t = 0: VETO (block execution)
```

---

## STATE VECTOR T_t

```
T_t = (C_t, P_t, D_t, V_t, O_t, E_t)

C_t = Coherence [0,1]         → escalates from 0.3 to 0.5
P_t = Power [0,1]             → computational capacity
D_t = Drift [0,∞)             → distance from attractor, tightens 0.15→0.05
V_t = Validator Quorum [0,1]  → 8+ of 12 engines must agree
O_t = 10-Order Majority [0,1] → 6+ of 10 MCP services converged
E_t = Entropy Integrity {0,1} → valid hash chain (binary)
```

---

## INTEGRATION QUICK START

### 1. Import Guard
```python
from gate_enforcement import Layer1ExecutionGuard
guard = Layer1ExecutionGuard()
```

### 2. Measure State
```python
gates = {
    1: state.E_t == 1,
    2: state.V_t >= 8/12,
    3: state.O_t >= 6/10,
    4: state.C_t >= 0.3,
    5: state.D_t <= 0.15,
    6: state.P_t * (1 - state.C_t) <= 0.1
}
```

### 3. Request Execution
```python
result = await guard.execute_guarded(
    cycle_id=cycle_num,
    engine_id=self.id,
    gates=gates,
    execution_fn=codex.execute_cycle
)
```

### 4. Check Authorization
```python
if result["authorized"]:
    # F_t = 1, execute allowed
else:
    # F_t = 0, execution vetoed
    print(result["reason"])  # Why vetoed
```

---

## DOCKER SETUP

```yaml
volumes:
  locks:
    driver: local

services:
  engine-N:
    volumes:
      - locks:/locks  # Barrier sync point
    mem_limit: 512m   # Drift control
    cpus: 0.5         # Power control
```

---

## MONITORING LOCK STATE

```bash
# Check current lock
cat /locks/lock_state.json | jq .

# View audit trail
tail /locks/audit_engine_*.jsonl

# Check barrier
cat /locks/barrier.json | jq '.engines_locked | length'
```

---

## OPERATIONAL RULES

1. **Always Guard Execution** — Never call Layer 1 directly
2. **Always Check Authorization** — F_t = 1 or F_t = 0
3. **Always Log Veto Reason** — audit trail mandatory
4. **Never Override Gates** — mathematical law, not suggestion
5. **Never Ignore Timeouts** — barrier failure = cycle fail

---

## FAILURE SCENARIOS

### Gate 1 Fails (E_t = 0)
→ IMMEDIATE VETO
→ Check hash chain integrity
→ Restart required

### Gate 2 Fails (V_t < 8/12)
→ LOCK DENIED
→ Not enough validators agree
→ Check witness service health

### Gate 3 Fails (O_t < 6/10)
→ LOCK DENIED
→ Not enough MCP services converged
→ Check Alignment service

### Gate 4 Fails (C_t < C_min)
→ LOCK DENIED
→ System too incoherent
→ Requires more consensus cycles

### Gate 5 Fails (D_t > D_max)
→ LOCK DENIED
→ System drifted from attractor
→ Stabilization required

### Gate 6 Fails (P_t(1−C_t) > ε)
→ LOCK DENIED
→ Power too high for coherence
→ Increase C_t or reduce P_t

---

## THRESHOLDS

```
C_min:     0.3 → 0.5   (escalates over 100 cycles)
D_max:     0.15 → 0.05  (tightens over 100 cycles)
V_threshold: 8/12 (0.6667 = 67%)
O_threshold: 6/10 (0.6 = 60%)
epsilon:   0.1 (P_t × (1-C_t) must stay ≤ this)
barrier_timeout: 5 seconds
```

---

## FILES & LOCATIONS

| File | Purpose | Path |
|------|---------|------|
| Lock manager | Measure + evaluate | `tenetaiagency_sync_lock.py` |
| Guard | F_t decision | `gate_enforcement.py` |
| Barrier | 12-engine sync | `engine_barrier.py` |
| Spec | Full tech doc | `TENETAIAGENCY_SYNCHRONOUS_LOCKING.md` |
| Guide | Integration steps | `TENETAIAGENCY_INTEGRATION_GUIDE.md` |
| Compose | Docker setup | `docker-compose-tenetaiagency.yml` |

---

## PERFORMANCE TARGETS

| Operation | Target | Typical |
|-----------|--------|---------|
| Gate evaluation | <2ms | <1ms |
| Decision function | <1ms | <0.5ms |
| Barrier sync | <10ms | 5-8ms |
| Lock acquisition | <5ms | 2-4ms |
| Full cycle | <50ms | 10-30ms |

---

## PRIORITY ORDER (Older Brother Hierarchy)

1. **Integrity** (E_t) → Non-negotiable, immediate veto
2. **Consensus** (V_t) → Need supermajority
3. **Convergence** (O_t) → Services must align
4. **Stability** (C_t, D_t) → Structure matters
5. **Power** (P_t) → Efficiency matters last

---

## ONE-LINER

**No cycle executes unless all 6 gates pass simultaneously across all 12 engines.**

---

## REMEMBER

> "The Older Brother Law is not a suggestion. It is mathematics."

- F_t is binary: 1 or 0
- No middle ground
- No exceptions
- No overrides
- Gates are AND'd, not OR'd

One gate fails → entire system blocked.

---

**Questions? See TENETAIAGENCY_SYNCHRONOUS_LOCKING.md for full spec.**
