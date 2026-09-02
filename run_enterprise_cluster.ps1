# ==============================================================================
# ENTERPRISE SOVEREIGN MOE MASTER ORCHESTRATOR
# ==============================================================================
param(
    [string]$Action = "run"
)

$RootDir = "C:\zsh-Robllama-copilot-ai"
$InferenceDir = "$RootDir\vendor\deepseek-v3-inference"

switch ($Action) {
    "run" {
        Write-Host "[MASTER] Launching Enterprise MoE Kuramoto-Newton Daemon..." -ForegroundColor Cyan
        python "$InferenceDir\enterprise_moe_daemon.py"
    }
    "status" {
        Write-Host "[MASTER] Checking Enterprise Repository Matrix..." -ForegroundColor Cyan
        cd $RootDir
        git status
        git branch --show-current
    }
    "logs" {
        $LogFile = "$RootDir\logs\enterprise_moe.log"
        if (Test-Path $LogFile) {
            Get-Content $LogFile -Tail 50 -Wait
        } else {
            Write-Host "[ERROR] Log file not found yet. Run the daemon first." -ForegroundColor Red
        }
    }
    default {
        Write-Host "Usage: .\run_enterprise_cluster.ps1 [-Action run|status|logs]" -ForegroundColor Yellow
    }
}
