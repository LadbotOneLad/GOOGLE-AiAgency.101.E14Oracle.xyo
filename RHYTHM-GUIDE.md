# 4D TERMINAL — RHYTHM DOCUMENTATION
# Everything breathes. Everything has tempo.

## What is RHYTHM?

Rhythm is **time made visible**. In a terminal:

- **TICK** (50ms) — Micro-pause, fastest feedback
- **BEAT** (200ms) — Normal heartbeat, readable flow
- **BREATH** (1500ms) — Moment to absorb, pause between thoughts

When you see a command execute:
```
gtop status

Checking engines . . . . . . . . . . . . . .
                 ↑       ↑       ↑
              TICK    TICK    TICK (50ms each)

Status: 14/14 healthy
               ↑ (BREATH: pause)

Lock ID: 550e8400-e29b-41d4...
```

The **pauses** let your brain catch up. The **pulses** show work is happening.

---

## Rhythm in the Code

### gtop.ps1 — TOPOLOGY PULSES

```powershell
# TICK: Check one engine
# TICK: Check another
# TICK: Check another
# ... (14 total)

Checking engines . . . . . . . . . . . . . .
         ↑↑↑↑↑↑↑↑↑↑↑↑↑↑
         (14 TICKS)

# BREATH: Pause before showing result
Status: 14/14 healthy (100%)
```

Engine listing has **visual rhythm**:
```
🔴 CORE RING
▪▪▪ (3 engines, with BEAT between each)

🟡 PEER RING  
▪▪▪▪▪▪▪▪▪▪▪▪ (12 engines, grouped by 4s)
  ↑ Every 4th, add a BREATH
```

Topology map is **line-by-line**, each line timed:
```
                         ┌─────────────┐
                         │  Engine-365 │
                         │  (port 365) │
                         └──────┬──────┘
                                │
                    ┌───────────┼───────────┐
```

Each line appears at **150ms intervals** — slow enough to read, fast enough to feel alive.

### treplay.ps1 — TIME DANCES

Session timeline shows history with **natural rhythm**:

```
✅ [16:45:30] docker build
   ↑ (TICK: fast pulse)

❌ [16:46:15] npm run build
   ↑ (TICK: fast pulse)

✅ [16:47:01] docker compose up
   ↑ (TICK: fast pulse)

(every 3 commands: BREATH — let the pattern sink in)
```

---

## Prompt with Rhythm

Your prompt updates every keystroke:

```
[16:47:23] 👤 [365/validator/dev] PS C:\ENGINE> 
│          │  │  │   │         │   │
│          │  │  │   │         │   └─ Current location
│          │  │  │   │         └──── Mode indicator
│          │  │  │   └────────────── Role (from $env)
│          │  │  └────────────────── Engine ID (from $env)
│          │  └───────────────────── Task mode emoji
│          └───────────────────────── Time (HH:mm:ss)
└──────────────────────────────────── Brackets for visual rhythm
```

Every element is **instantly readable** because it's **consistently spaced**.

---

## Rhythm Constants Across System

| Name | Duration | Use |
|------|----------|-----|
| TICK | 50ms | Fast micro-feedback (engine checks) |
| BEAT | 200ms | Normal human reading speed |
| BREATH | 1500ms | Pause to absorb information |

**Pattern**: TICK·TICK·TICK·BEAT·TICK·TICK·BREATH

This is the **default rhythm** of the system.

---

## Where You Feel Rhythm

### 1. gtop status
```
Checking engines . . . . . . . . . . . . . .
         TICK     TICK     TICK            (50ms each)

Status: 14/14 healthy (100%)
(pause to read)
```

### 2. gtop list
```
🔴 CORE RING
▪▪▪ (beat between each core engine)

🟡 PEER RING
▪▪▪▪ ▪▪▪▪ ▪▪▪▪ (groups of 4, long pause between groups)
```

### 3. gtop map
```
                    ┌─────────────┐
                    │  Engine-365 │  (wait 150ms)
                    │  (port 365) │  (wait 150ms)
                    └──────┬──────┘  (wait 150ms)
                           │
                    ┌──────┼──────┐  (wait 150ms)
```

### 4. treplay timeline
```
✅ [16:45:30] command 1  (TICK pause)
❌ [16:46:15] command 2  (TICK pause)
✅ [16:47:01] command 3  (TICK pause)
(every 3: BREATH — let the sequence sink in)
```

### 5. Prompt
```
[16:47:23] 👤 [365/validator/dev] PS C:\ENGINE> 
(appears instantly on new line, consistent spacing)
```

---

## Why Rhythm Matters

Without rhythm, a terminal feels **jarring**:
```
$Checking engines...Status: 14/14. Done.
```

With rhythm, it feels **alive**:
```
Checking engines . . . . . . . . . . . . . .
         (you watch the dots appear)

(pause)

Status: 14/14 healthy (100%)
         (you absorb the result)
```

The **pauses** are not delays. They're **intentional breaks** that make information stick.

---

## Implementing Rhythm in Your Own Commands

If you add new commands, follow this pattern:

```powershell
function My-Command {
    Write-Host "Task starting" -NoNewline
    
    # Check 5 things with TICK
    for ($i = 0; $i -lt 5; $i++) {
        Write-Host "." -NoNewline
        Start-Sleep -Milliseconds 50  # TICK
    }
    
    Write-Host ""
    
    # Pause for breath
    Start-Sleep -Milliseconds 1500  # BREATH
    
    # Show result
    Write-Host "Result: success" -ForegroundColor Green
}
```

The rhythm is:
1. **Work** (fast ticks, visual feedback)
2. **Pause** (breath, let it sink in)
3. **Result** (instant, colored, clear)

---

## Rhythm is Not Lag

Rhythm uses **deliberate timing**, not system delays:

```powershell
# GOOD: Intentional rhythm
Write-Host "." -NoNewline
Start-Sleep -Milliseconds 50

# BAD: System is slow
Write-Host "."  # Takes 2 seconds because PowerShell is busy
```

Rhythm is **musician timing**, not **network latency**.

---

## The 4D Terminal Now Breathes

Every command you run has:

✅ **Visual feedback** (dots, lines, colors)
✅ **Intentional timing** (TICK, BEAT, BREATH)
✅ **Readable flow** (fast enough to feel instant, slow enough to follow)
✅ **Natural rhythm** (your heartbeat, your breath, your thinking speed)

When you run `gtop status`, you're not staring at a wall of text. You're **watching** the system check itself, **pausing** to show you results, **breathing** between thoughts.

That's rhythm.

---

**Created:** 2026-04-04  
**System:** .15% SOLAR WAGYU — DIGITAL CUT  
**Philosophy:** Everything that moves should feel alive.
