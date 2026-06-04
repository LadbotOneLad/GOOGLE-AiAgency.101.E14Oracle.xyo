# PowerShell Profile Additions
# Add this to your $PROFILE to get rhythm in every prompt

# Rhythm constants
$RHYTHM = @{
    TICK = 50
    BEAT = 200
    BREATH = 800
}

function Invoke-Rhythm-Prompt {
    # Context from environment
    $engineId = $env:ENGINE_ID ?? "local"
    $mode = $env:MODE ?? "dev"
    $role = $env:ENGINE_ROLE ?? "user"
    
    # Emoji mapping
    $modeEmoji = @{
        dev = "👤"
        ops = "🔧"
        audit = "🔍"
        experiment = "🧪"
    }
    
    $emoji = $modeEmoji[$mode] ?? "❓"
    
    # Build prompt with visual rhythm
    $prompt = ""
    
    # Part 1: Timestamp (breathing)
    $time = Get-Date -Format "HH:mm:ss"
    $prompt += "[" + $time + "] "
    
    # Part 2: Identity (pulsing)
    $prompt += "$emoji [$engineId/$role/$mode] "
    
    # Part 3: Location (steady)
    $prompt += "PS " + (Get-Location).Path.Replace($env:USERPROFILE, "~") + "> "
    
    return $prompt
}

function prompt {
    Invoke-Rhythm-Prompt
}

# Shortcut functions with rhythm
function gtop {
    & "$PSScriptRoot\gtop.ps1" @args
}

function treplay {
    & "$PSScriptRoot\treplay.ps1" @args
}

# Mode switchers (instant visual feedback)
function mode-dev {
    $env:MODE = "dev"
    Write-Host "👤 dev" -ForegroundColor Green
}

function mode-ops {
    $env:MODE = "ops"
    Write-Host "🔧 ops" -ForegroundColor Yellow
}

function mode-audit {
    $env:MODE = "audit"
    Write-Host "🔍 audit" -ForegroundColor Red
}

function mode-experiment {
    $env:MODE = "experiment"
    Write-Host "🧪 experiment" -ForegroundColor Magenta
}

# Engine jumpers (with rhythm)
function e365 {
    $env:ENGINE_ID = "365"
    $env:ENGINE_ROLE = "validator"
    Write-Host "🔴 E365 validator" -ForegroundColor Red
}

function e777 {
    $env:ENGINE_ID = "777"
    $env:ENGINE_ROLE = "sovereign"
    Write-Host "👑 E777 sovereign" -ForegroundColor Yellow
}

function e101 {
    $env:ENGINE_ID = "101"
    $env:ENGINE_ROLE = "horizon"
    Write-Host "🌅 E101 horizon" -ForegroundColor Cyan
}

# Quick checks
function gstatus {
    gtop status
}

function gmap {
    gtop map
}

function glist {
    gtop list
}

function ghealth {
    param($id)
    if ($id) {
        Write-Host "Checking engine-$id..."
        Invoke-WebRequest -Uri "http://localhost:$id/4gr/health" -UseBasicParsing | ConvertFrom-Json
    } else {
        Write-Host "Usage: ghealth <engine-id>"
    }
}

# Navigation
function cdengine {
    Set-Location "C:\Users\Admin\OneDrive\Desktop\(   .  Y  .    )ENGINE"
}

# Initialize logging directory
if (-not (Test-Path "$env:USERPROFILE\.logs\terminal")) {
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.logs\terminal" -Force | Out-Null
}

Write-Host "🟢 4D Terminal ready. Try: gtop status, mode-ops, e365" -ForegroundColor Green
