# 4D TERMINAL SETUP GUIDE
# .15% SOLAR WAGYU — DIGITAL CUT Global Control Room

## What You Now Have

A **4D global terminal** architecture for controlling 14 synchronized engines:

```
DIMENSION 1: SPACE
  └─ Profiles, panes, profiles (6 tab profiles in Windows Terminal)

DIMENSION 2: TIME
  └─ Session logging, replay, timeline search (treplay system)

DIMENSION 3: TOPOLOGY
  └─ Engine registry, health checks, ASCII maps (gtop CLI)

DIMENSION 4: IDENTITY/INTENT
  └─ Task modes (dev, ops, audit, experiment)
```

---

## File Structure

```
.
├── topology.yaml              # Engine registry + modes (SPACE+TOPOLOGY)
├── gtop.ps1                   # Global topology CLI (TOPOLOGY+IDENTITY)
├── treplay.ps1                # Session logger + replay (TIME)
├── wt-profiles-4d.json        # WT tab profiles (SPACE)
├── cockpit-launch.ps1         # Multi-pane layout launcher (SPACE+TIME)
└── docker-compose-14engines.yml  # 14-engine deployment
```

---

## Quick Start

### 1. Add to PowerShell Profile

Add this to `$PROFILE` (edit with `notepad $PROFILE`):

```powershell
# 4D Terminal shortcuts
$4dDir = "C:\Users\Admin\OneDrive\Desktop\(   .  Y  .    )ENGINE"

function gtop { & "$4dDir\gtop.ps1" @args }
function treplay { & "$4dDir\treplay.ps1" @args }
function cockpit { & "$4dDir\cockpit-launch.ps1" @args }

function gstatus { gtop status }
function gmap { gtop map }
function glist { gtop list }
function ghealth { param($id) gtop health $id }

# Task modes
function mode-dev { $env:MODE = 'dev'; Write-Host '👤 Dev' -ForegroundColor Green }
function mode-ops { $env:MODE = 'ops'; Write-Host '🔧 Ops' -ForegroundColor Yellow }
function mode-audit { $env:MODE = 'audit'; Write-Host '🔍 Audit' -ForegroundColor Red }

# Engine jumps
function e365 { $env:ENGINE_ID = '365'; Write-Host '[Engine-365 Validator]' }
function e777 { $env:ENGINE_ID = '777'; Write-Host '[Engine-777 Sovereign]' }
function e101 { $env:ENGINE_ID = '101'; Write-Host '[Engine-101 Horizon]' }

function cdengine { Set-Location $4dDir }

# Initialize logging
if (-not (Test-Path "$env:USERPROFILE\.logs\terminal")) {
    & "$4dDir\treplay.ps1" init
}
```

Then run: `$PROFILE | notepad` to edit, save, and reload PowerShell.

### 2. Launch the Cockpit

```powershell
# Opens multi-pane WT layout
cockpit -Mode ops

# Or open individual tabs:
gtop status    # Health dashboard
gtop map       # Topology visualization
gtop list      # Engine list
```

### 3. Switch Modes

```powershell
mode-dev       # Development mode
mode-ops       # Operations mode
mode-audit     # Audit mode
```

### 4. Check Engine Health

```powershell
gtop status          # All engines
gtop health 365      # Specific engine
gtop list            # Full list
gtop map             # Visual topology
```

### 5. Search Session History

```powershell
treplay timeline           # All commands today
treplay search 'docker'    # Find docker commands
treplay replay --minutes 30 # Last 30 minutes
```

---

## What Each Tool Does

### **gtop** (Global Topology)

```
gtop list      → 14 engines + status
gtop status    → Quick health %
gtop health ID → Single engine health
gtop map       → ASCII topology visualization
gtop config    → Show YAML topology
gtop mode NAME → Switch task mode
```

**Example:**
```powershell
PS> gtop status

╔════════════════════════════════════════╗
║        GLOBAL ENGINE HEALTH           ║
╚════════════════════════════════════════╝

  Status: 14/14 healthy (100%)
  Lock ID: 550e8400-e29b-41d4-a716-446655440000
  Expiry: 2025-04-14T10:00:00.000Z
```

### **treplay** (Time Dimension)

Logs all your commands with timestamps, exit codes, duration.

```
treplay init              → Start logging
treplay timeline          → Show all commands
treplay search 'pattern'  → Find commands
treplay replay -Minutes 30 → Replay last 30 min
```

**Example:**
```powershell
PS> treplay timeline

✅ [2026-04-04 16:45:30] docker build -f Dockerfile.4gr -t 4gr-fse:test .
❌ [2026-04-04 16:46:15] npm run build
✅ [2026-04-04 16:47:01] docker compose -f docker-compose-14engines.yml up -d
```

### **cockpit-launch** (Multi-Pane Layout)

Opens Windows Terminal with 4-pane layout:

```
┌──────────────────────────────────┐
│ Health (gtop status) │ Map (gtop) │
├──────────────────────────────────┤
│                                  │
│    Command/Control (you type)    │
│                                  │
└──────────────────────────────────┘
```

---

## The 4 Dimensions in Action

### SPACE (Where are you?)
```powershell
PS [E365 validator][dev] C:\ENGINE>
   ├─ E365        = Engine ID
   ├─ validator   = Role
   ├─ dev         = Mode (task context)
   └─ ENGINE      = Directory
```

### TIME (When did you do it?)
```powershell
treplay timeline
  ✅ [2026-04-04 16:45:30] command 1
  ❌ [2026-04-04 16:46:15] command 2
  ✅ [2026-04-04 16:47:01] command 3
  ↑  timestamp   ↑ success/fail
```

### TOPOLOGY (What is the shape?)
```
                   Engine-365 (validator)
                        │
                  ┌─────┼─────┐
                  │     │     │
               777     101   ...
                │      │      │
            (peer cluster 1001-1012)
```

### IDENTITY/INTENT (Who and why?)
```
mode-dev       # Building, testing, iterating
mode-ops       # Managing health, restarting, scaling
mode-audit     # Verifying locks, immutable logs
mode-experiment # Running stress tests, pings
```

---

## Practical Workflows

### Workflow 1: Daily Health Check (Ops)

```powershell
mode-ops
gtop status      # See overall health
gtop list        # See all engines
gtop health 365  # Check validator
```

### Workflow 2: Development Build (Dev)

```powershell
mode-dev
cdengine
docker compose -f docker-compose-14engines.yml up -d
gtop status
```

### Workflow 3: Audit Verification (Audit)

```powershell
mode-audit
treplay timeline              # See what happened
gtop health 365               # Check validator integrity
cat lock-metadata.json        # Verify lock state
```

### Workflow 4: Stress Testing (Experiment)

```powershell
mode-experiment
gtop map                      # See topology
# Run stress test script
gtop status                   # Monitor health
treplay search 'stress'       # Find test commands
```

---

## Environment Variables Set by Mode

```
MODE=dev       → LOGLEVEL=debug
MODE=ops       → LOGLEVEL=info
MODE=audit     → LOGLEVEL=warn
MODE=experiment → LOGLEVEL=debug
```

Each mode can load different aliases and functions.

---

## Next Steps

1. ✅ Add to PowerShell profile
2. ✅ Run `gtop status` to verify
3. ✅ Try `gtop map` to see topology
4. ✅ Switch modes: `mode-ops`, `mode-audit`, etc.
5. ✅ Set up task dashboard (paned layout)
6. ⏳ Add Prometheus metrics to gtop
7. ⏳ Implement peer discovery between engines
8. ⏳ Test 90-day lock renewal

---

## Color + Glyph Legend

```
🔴 Core Ring      (Red)      - Validator, Sovereign, Horizon
🟡 Peer Ring      (Yellow)   - 1001-1012
🟢 Healthy        (Green)    - All systems nominal
🔴 Unhealthy      (Red)      - Issue detected
👤 Dev mode       (Cyan)     - Development context
🔧 Ops mode       (Yellow)   - Operations context
🔍 Audit mode     (Red)      - Audit context
🧪 Experiment     (Magenta)  - Experiment context
```

---

## Troubleshooting

**Q: gtop not found**
A: Add gtop to PowerShell profile path or call explicitly: `& "$4dDir\gtop.ps1" status`

**Q: Windows Terminal profiles not appearing**
A: Merge `wt-profiles-4d.json` into `$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json`

**Q: Logs not being created**
A: Run `treplay init` to create `$env:USERPROFILE\.logs\terminal`

**Q: Cockpit panes not splitting**
A: Windows Terminal may need a recent version. Manual pane splitting: Alt+Shift+D (down), Alt+Shift+Plus (right)

---

## Architecture Summary

You now have a **production-grade control room** for 14 engines with:

- **Space**: 6 WT profiles + multi-pane layouts
- **Time**: Session logging + replay system
- **Topology**: Registry of all 14 + health checks
- **Identity**: 4 task modes (dev/ops/audit/experiment)

Every prompt shows you **where** you are, **what** mode you're in, and **how healthy** the system is.

This is a 4D terminal.

---

**Created:** 2026-04-04  
**System:** .15% SOLAR WAGYU — DIGITAL CUT  
**Engines:** 14 synchronized, Merkle-locked  
**Status:** 🟢 OPERATIONAL
