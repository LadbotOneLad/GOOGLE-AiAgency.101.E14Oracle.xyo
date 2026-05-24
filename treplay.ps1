# treplay: Time Replay with RHYTHM
# Sessions have breath, history has pulse, time has dance

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

$LogDir = "$env:USERPROFILE\.logs\terminal"

# RHYTHM
$TICK = 100    # Fast pulse
$BEAT = 500    # Normal heartbeat
$BREATH = 1500 # Slow breath

function Tick { Start-Sleep -Milliseconds $TICK }
function Pulse-Beat { Start-Sleep -Milliseconds $BEAT }
function Breathe-Pause { Start-Sleep -Milliseconds $BREATH }

function Show-Timeline {
    $SessionDate = (Get-Date).ToString("yyyy-MM-dd")
    $logFile = Join-Path $LogDir "$SessionDate.log"
    
    if (-not (Test-Path $logFile)) {
        Write-Host "No logs yet. Starting fresh." -ForegroundColor Yellow
        return
    }
    
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║            SESSION TIMELINE - $SessionDate              ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    
    $logs = Get-Content $logFile | ConvertFrom-Json -ErrorAction SilentlyContinue
    
    if ($null -eq $logs) {
        Write-Host "No commands logged yet."
        return
    }
    
    $count = 0
    $logs | ForEach-Object {
        $count++
        $emoji = if ($_.exitCode -eq 0) { "✅" } else { "❌" }
        
        Write-Host -NoNewline "$emoji "
        Tick
        Write-Host -NoNewline "["
        Tick
        Write-Host -NoNewline $_.timestamp -ForegroundColor Green
        Tick
        Write-Host -NoNewline "] "
        Tick
        Write-Host $_.command -ForegroundColor Cyan
        
        if ($count % 3 -eq 0) {
            Breathe-Pause
        } else {
            Pulse-Beat
        }
    }
    
    Write-Host ""
}

function Show-Help {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║            TREPLAY: Time Replay System                ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "COMMANDS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  treplay timeline        Show session history with rhythm" -ForegroundColor Cyan
    Write-Host "  treplay search '<text>' Find commands in logs" -ForegroundColor Cyan
    Write-Host ""
}

switch ($Command.ToLower()) {
    "timeline" { Show-Timeline }
    "help" { Show-Help }
    default { Show-Help }
}
