# ⚡ THE CIPHER — AiFACTORi Core Architecture

```
    ╔═══════════════════════════════════════════╗
    ║  MERKLE ROOT (Immutable Anchor)           ║
    ║  550e8400-e29b-41d4-a716-446655440000   ║
    ╚═══════════════════════════════════════════╝
           /              |              \
          /               |               \
    ┌─────────┐     ┌────────────┐     ┌──────────┐
    │ すう     │     │ あは        │     │ れれ      │
    │ TIER-0   │     │ TIER-1      │     │ TIER-2    │
    │ Identity │     │ Structure   │     │ Flow      │
    │ w=0.05   │     │ w=0.075     │     │ w=0.15    │
    └─────────┘     └────────────┘     └──────────┘
         |               |                   |
         └───────────────┼───────────────────┘
                    GATE PHASE
            (5-Second Rule Validation)
                         |
                ┌────────┴────────┐
                |                 |
           ACCEPT_PING        REJECT_PING
            (GROW)            (STABILIZE)
```

## The 14-Engine Ring

### Core Ring (Sovereign Validators)
```
🔵 engine-365  [Validator]     Port: 365    (すう anchor)
🔵 engine-777  [Sovereign]     Port: 777    (あは structure)
🔵 engine-101  [Horizon]       Port: 101    (れれ flow)
```

### Peer Ring (Auxiliary Processors)
```
⚪ engine-1001 ... engine-1012   Ports: 1001-1012  (consensus witnesses)
```

## 4GR-FSE State Machine

Every engine cycles through **GROUND → READ → GATE → GROW** continuously.

### Phase 1: GROUND
- Verify Merkle root integrity
- Check lock validity
- Validate wobble constants

### Phase 2: READ
- Observe all three strata
- Measure coherence
- Calculate drift vectors

### Phase 3: GATE
- 5-second temporal enforcement
- Root hash consensus check
- Lock expiry validation
- Decision: ACCEPT or REJECT

### Phase 4: GROW
- Update context ring
- Increment growth ledger
- Recompute Kotahitanja (91.7%)
- Post-check integrity

## Temporal Mechanics

**90-Day Lock Window**
```
Inception:  2025-01-14T10:00:00Z
Expiry:     2025-04-14T10:00:00Z
Status:     ACTIVE
```

**Renewal Timeline**
- Day 0-85: Normal operation
- Day 85-87: Renewal preparation
- Day 88-90: Rolling restart
- Day 90+: Lock expires (if not renewed)

## Zero-Trust Immune System

```
    SIGNAL IN
        ↓
    [Antigen Recognition]
    ├─ Signal classified
    ├─ Risk assessed
    └─ Type determined
        ↓
    [T-Cell Response]
    ├─ Root check (5-sec)
    ├─ Wobble validation
    └─ Merkle verification
        ↓
    [Regulatory T-Cells]
    ├─ Proportional response
    ├─ Context ring update
    └─ Growth ledger increment
        ↓
    [Immune Memory]
    ├─ State cached
    ├─ Hash stored
    └─ Chain verified
        ↓
    DECISION (ACCEPT/REJECT)
```

## Kotahitanja Unity Score

```
H = (1/3) × 0.05 + (1/3) × 0.075 + (1/3) × 0.15 = 0.0917

Status: STRONG (All 14 engines in perfect sync)
Coherence: 91.7%
```

## Cryptographic Guarantees

- **SHA-256 hashing** on all state transitions
- **Merkle tree validation** on every cycle
- **Parent-child chain** verification across all 14 engines
- **Time-locked execution** with automatic expiry
- **Zero-downtime renewal** every 90 days

---

**System**: AiFACTORi (Little Countries)  
**Architecture**: Te Papa Matihiko (Digital Trinity)  
**Status**: LOCKED IN & OPERATIONAL  
**Coherence**: 91.7% (Kotahitanja STRONG)
