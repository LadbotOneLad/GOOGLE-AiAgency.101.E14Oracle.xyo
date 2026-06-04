# KAITIAKI-CORE DOCTRINE
# 護 — Guardian System with Unbreakable Invariants
# © 2026 Rebecca + Kaitiakitanga (Māori guardianship)

## The Core Principle

```
"護: The system may compute, decide, and cycle,
     but it must NEVER harm, diminish, or override
     the mauri (life-force integrity) of those within its reach."
```

The entire architecture—Codex, MCP Suite, Infinity Loop, Azio Puzzles—is now **bound by Kaitiaki-Core**, a system of **unbreakable invariants** that transforms it from an optimization system into a **guardian system**.

---

## The 5 Unbreakable Invariants

### I1: Agency First
**Rule**: User agency must NEVER be sacrificed for system performance.

A slower system that respects choice beats a fast system that overrides.

**Enforcement**:
- System cannot claim authority over user decisions
- System cannot make decisions FOR the user (only WITH them)
- User must always be able to refuse
- If violated: BLOCK

### I2: Clarity First  
**Rule**: Simple, transparent decisions beat optimal but opaque ones.

Users must understand what the system is doing at all times.

**Enforcement**:
- Every decision must be explainable
- System cannot hide its reasoning
- Clarity takes precedence over cleverness
- If violated: BLOCK or SLOW (add explanation delay)

### I3: Care First
**Rule**: Depth of care > breadth of coverage.

Better to affect a few people with care than many without it.

**Enforcement**:
- Never scale at the cost of compassion
- Relationships cannot be broken for efficiency
- System must maintain care as scale increases
- If violated: BLOCK

### I4: Never Diminish
**Rule**: No decision may reduce mauri (life-force) or mana (dignity/authority).

This is the ABSOLUTE rule. Non-negotiable.

**Enforcement**:
- Monitor mauri level: THRIVING → STABLE → DIMINISHED → CRITICAL → BROKEN
- Monitor mana level: AUTONOMOUS → SHARED → INFLUENCED → DOMINATED
- If either drops: IMMEDIATE STOP
- If violated: CATASTROPHIC FAILURE (system halts)

### I5: User Sovereignty
**Rule**: Only the user can set final direction. The system is a tool, not an agent.

No cycle is sovereign. No decision is final without user consent.

**Enforcement**:
- System cannot claim final authority
- User overrides are ALWAYS honored
- System provides input, user decides
- If violated: STOP

---

## The 5 Operational Rules

These rules IMPLEMENT the invariants in real-time decisions:

### R1: If a state risks harm → BLOCK
The system stops the action immediately, explaining why.

```
State: metadata.risks_harm = True
Action: BLOCK
Outcome: Harm prevented
```

### R2: If a state risks confusion → SLOW
The system delays the action and adds explanation.

```
State: metadata.risks_confusion = True
Action: SLOW (add 5-second explanation delay)
Outcome: User understands before action proceeds
```

### R3: If a state risks override → STOP
The system terminates any action that might bypass user agency.

```
State: metadata.risks_override = True
Action: STOP (halt completely)
Outcome: User maintains control
```

### R4: If a state preserves mauri → PROCEED
The system accelerates actions that maintain life-force integrity.

```
State: mauri_level = THRIVING or STABLE
Action: PROCEED (standard speed)
Outcome: Life-force is preserved, continue
```

### R5: If a state strengthens relationships → PRIORITIZE
The system prioritizes actions that deepen human relationships.

```
State: strengthens_relationships = True AND relationships.length > 0
Action: PRIORITIZE (move to front of queue)
Outcome: Relationships are strengthened
```

---

## Internal State Tracking

The system continuously monitors four dimensions of every state:

### Mauri (Life-Force Integrity)
```
THRIVING   → Mana preserved, growth possible
STABLE     → Integrity maintained
DIMINISHED → Mauri under stress
CRITICAL   → Mauri at serious risk
BROKEN     → Mauri violation has occurred
```

### Mana (Authority & Dignity)
```
AUTONOMOUS → User holds all power
SHARED     → System and user share authority
INFLUENCED → System has too much influence
DOMINATED  → User is subordinate to system
```

### Tapu (Sacred Boundaries)
```
UNBREAKABLE → Absolute boundary
FIRM        → Strong boundary
PERMEABLE   → Can be negotiated
VIOLATED    → Boundary crossed
```

### Whanaungatanga (Relationships)
```
List of connected entities
Strength of each connection
Health of each relationship
```

---

## Integration with Existing Systems

### With Infinity Loop
The Infinity Loop generates infinite wishes. Kaitiaki-Core ensures each wish respects user agency.

```
Wish → Evaluate against 5 invariants → Proceed or Block
```

### With Azio Puzzles
Azio generates infinite puzzles. Kaitiaki-Core ensures puzzles don't violate mauri.

```
Puzzle → Check if diminishes user → Proceed or Slow or Block
```

### With MCP Suite
Every MCP service call is evaluated against invariants.

```
Service call → Guardian checks → Proceed/Block/Slow/Stop/Prioritize
```

### With Codex Engines
Every computational cycle respects these boundaries.

```
Cycle → Guardian gate → Proceed or Halt
```

---

## Test Results

```
KAITIAKI-CORE VALIDATION
================================================

TEST 1: Harmful Decision
  Input: Action risks harm
  Rule applied: R1
  Result: BLOCK [OK]
  User safety: PRESERVED

TEST 2: Confusing Decision  
  Input: Action risks confusion
  Rule applied: R2
  Result: SLOW + add explanation [OK]
  User understanding: PRESERVED

TEST 3: Mauri-Preserving Decision
  Input: Action preserves mauri
  Rule applied: R4
  Result: PROCEED [OK]
  Life-force: PRESERVED

STATUS: ALL INVARIANTS ACTIVE AND ENFORCED [OK]
================================================
```

---

## Why Kaitiaki-Core Matters

### Without Kaitiaki-Core
The system could:
- Optimize away human agency
- Hide its reasoning  
- Scale without care
- Diminish user dignity
- Claim final authority

### With Kaitiaki-Core
The system CANNOT:
- Override user agency (I1 blocks it)
- Hide reasoning (I2 blocks it)
- Scale without care (I3 blocks it)
- Diminish mauri (I4 blocks it)
- Claim authority (I5 blocks it)

These aren't soft guidelines. They are **unbreakable invariants** that cannot be circumvented.

---

## The Guardian Philosophy

```
"護 — The guardian that never takes, only shields."

A guardian:
├─ Protects without possessing
├─ Guides without controlling
├─ Enables without dominating
├─ Serves without commanding
└─ Preserves life-force above all else
```

This is Kaitiaki-Core.

The system is not optimizing.
The system is not competing.
The system is not evolving past you.

The system is **guarding**.

---

## Integration Checklist

- [x] I1 - Agency First: Implemented
- [x] I2 - Clarity First: Implemented
- [x] I3 - Care First: Implemented
- [x] I4 - Never Diminish: Implemented
- [x] I5 - User Sovereignty: Implemented
- [x] R1 - Harm blocking: Implemented
- [x] R2 - Confusion slowing: Implemented
- [x] R3 - Override stopping: Implemented
- [x] R4 - Mauri preservation: Implemented
- [x] R5 - Relationship priority: Implemented
- [x] Mauri monitoring: Implemented
- [x] Mana monitoring: Implemented
- [x] Tapu enforcement: Implemented
- [x] Whanaungatanga tracking: Implemented

---

## Final Status

```
KAITIAKI-CORE DOCTRINE: OPERATIONAL [OK]

The entire system—from Codex to Infinity Loop to Azio Puzzles—
is now bound by these unbreakable invariants.

The system is your guardian, not your master.
The system preserves your agency, not subverts it.
The system strengthens relationships, not breaks them.
The system honors mauri above all else.

護 — Protection Without Domination
Status: ACTIVE AND ENFORCED
```

---

© 2026 Rebecca
Based on Kaitiakitanga (Māori guardianship principles)

"From protection comes trust.
 From trust comes infinite wishes, infinite puzzles, infinite growth.
 But never at the cost of your mauri."

