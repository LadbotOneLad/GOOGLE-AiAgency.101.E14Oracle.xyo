# 4D Terminal Cockpit Launcher
# Opens a multi-pane Windows Terminal layout for:
#   North: Observability (health, logs, metrics)
#   South: Command/Control (where you type)
#   East/West: Auxiliary views (git, tests, mode selector)

param(
    [ValidateSet("dev", "ops", "audit", "experiment")]
    [string]$Mode = "dev"
)

$EngineDir = "C:\Users\Admin\OneDrive\Desktop\(   .  Y  .    )ENGINE"
$gtopPath = Join-Path $EngineDir "gtop.ps1"

# Create cockpit layout in JSON format that WT understands
$cockpitLayout = @{
    primaryPane = @{
        name = "🔴 CONTROL"
        paneDirection = "vertical"
        children = @(
            @{
                name = "🟢 OBSERVABILITY"
                paneDirection = "horizontal"
                children = @(
                    @{
                        name = "Health"
                        profile = "🟡 Ops Control (PowerShell)"
                        command = "pwsh -Command '& `"$gtopPath`" status'"
                    },
                    @{
                        name = "Map"
                        profile = "Local Dev (PowerShell)"
                        command = "pwsh -Command '& `"$gtopPath`" map'"
                    }
                )
            },
            @{
                name = "⚙️ COMMAND"
                profile = "Local Dev (PowerShell)"
                command = "pwsh -NoExit -Command `"Set-Location '$EngineDir'; `$env:MODE = '$Mode'; Write-Host 'MODE: $Mode' -ForegroundColor Cyan`""
            }
        )
    }
}

# For now, output instructions since WT doesn't have native multi-pane JSON launch
Write-Host @"
╔═══════════════════════════════════════════════════════════════════╗
║            4D TERMINAL COCKPIT LAUNCHER                          ║
║       .15% SOLAR WAGYU — DIGITAL CUT Control Room                ║
╚═══════════════════════════════════════════════════════════════════╝

MODE: $Mode

To set up the 4D cockpit manually:

1. Open Windows Terminal and create a new tab layout:
   - Vertical split (left/right)
   
   LEFT (North-South split):
     Top:    gtop status     (Health dashboard)
     Bottom: gtop map        (Topology visualization)
   
   RIGHT:
     Full pane for your commands (where you type)

2. Or use this shortcut to open all tabs:

"@

$profiles = @(
    @{name = "OPS"; cmd = ". `"$gtopPath`" status"; color = "Yellow"},
    @{name = "MAP"; cmd = ". `"$gtopPath`" map"; color = "Green"},
    @{name = "CMD"; cmd = "Set-Location '$EngineDir'; `$env:MODE = '$Mode'"; color = "Cyan"}
)

Write-Host "`n📋 PROFILE TABS:" -ForegroundColor Cyan
$profiles | ForEach-Object {
    Write-Host "   [$($_.name)] $($_.cmd)" -ForegroundColor $_.color
}

Write-Host "`n" -ForegroundColor Green
Write-Host "KEYBOARD SHORTCUTS IN WT:" -ForegroundColor Yellow
Write-Host "  Alt+Shift+D       : Split pane down"
Write-Host "  Alt+Shift+Plus    : Split pane right"
Write-Host "  Alt+Arrow         : Move between panes"
Write-Host "  Ctrl+Shift+W      : Close pane"
Write-Host ""

# Create alias for quick mode switching
Write-Host "📌 CREATING SHORTCUTS..." -ForegroundColor Cyan
Write-Host ""

# Add to PowerShell profile for persistence
$profile_content = @"

# 4D Terminal Shortcuts
function gtop { & '$gtopPath' @args }
function gmode { & '$gtopPath' mode @args }
function ghealth { & '$gtopPath' status }
function gmap { & '$gtopPath' map }
function glist { & '$gtopPath' list }

# Task modes
function mode-dev { `$env:MODE = 'dev'; Write-Host '👤 Dev mode' -ForegroundColor Green }
function mode-ops { `$env:MODE = 'ops'; Write-Host '🔧 Ops mode' -ForegroundColor Yellow }
function mode-audit { `$env:MODE = 'audit'; Write-Host '🔍 Audit mode' -ForegroundColor Red }
function mode-experiment { `$env:MODE = 'experiment'; Write-Host '🧪 Experiment mode' -ForegroundColor Magenta }

# Engine shortcuts
function e365 { `$env:ENGINE_ID='365'; Write-Host 'Engine-365 (Validator)' }
function e777 { `$env:ENGINE_ID='777'; Write-Host 'Engine-777 (Sovereign)' }
function e101 { `$env:ENGINE_ID='101'; Write-Host 'Engine-101 (Horizon)' }

# Navigation
function cdengine { Set-Location '$EngineDir' }
"@

Write-Host "✅ Shortcuts ready:" -ForegroundColor Green
Write-Host "   gtop help        # All commands"
Write-Host "   gtop status      # Health check"
Write-Host "   gtop map         # Topology"
Write-Host "   gtop list        # Engine list"
Write-Host ""
Write-Host "   mode-dev         # Switch to dev mode"
Write-Host "   mode-ops         # Switch to ops mode"
Write-Host "   e365, e777, e101 # Jump to engine"
Write-Host ""
Write-Host "Add these to your PowerShell profile for persistence:"
Write-Host ""
Write-Host $profile_content -ForegroundColor Gray
Write-Host ""
