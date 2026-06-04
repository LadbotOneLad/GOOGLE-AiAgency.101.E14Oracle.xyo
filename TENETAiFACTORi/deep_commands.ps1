#!/usr/bin/env pwsh
# Deep Metrics Live Commands
# Run these in PowerShell to see real-time deep output

Write-Host "`n=== DEEP METRICS COMMANDS ===" -ForegroundColor Cyan
Write-Host "Run these in PowerShell to monitor all engines:`n" -ForegroundColor White

Write-Host "# 1. Engine-365-days style output (Python - continuous)" -ForegroundColor Green
Write-Host "python3 deep_metrics_monitor.py`n" -ForegroundColor Yellow

Write-Host "# 2. Quick snapshot of all engine metrics" -ForegroundColor Green
Write-Host "docker ps | Select-String 'codex|witness' | ForEach-Object { `$engine = `$_ -split ' ' | Where-Object {`$_} | Select-Object -First 1; docker exec `$engine cat /logs/metrics.json 2>nul | ConvertFrom-Json | Select-Object timestamp, uptime_days, cycles_completed, rejection_rate }" -ForegroundColor Yellow

Write-Host "`n# 3. Real-time stats for all engines" -ForegroundColor Green
Write-Host "docker stats --no-stream engine-365-days ultimate-engine tenetaiagency-101" -ForegroundColor Yellow

Write-Host "`n# 4. Live tail all 13 engines (updates every 5s)" -ForegroundColor Green
Write-Host "while (`$true) { Clear-Host; Write-Host '[LIVE TAIL]' (Get-Date); docker ps -q | ForEach-Object { Write-Host `"Container: `$_`"; docker logs --tail 5 `$_ } | Select-Object -Last 100; Start-Sleep -Seconds 5 }" -ForegroundColor Yellow

Write-Host "`n# 5. Watch rejection rate across all engines" -ForegroundColor Green
Write-Host "while (`$true) { Write-Host `"`n[REJECTION RATES] `$(Get-Date)`"; docker ps -q | ForEach-Object { `$m = docker exec `$_ cat /logs/metrics.json 2>nul | ConvertFrom-Json; Write-Host `"`$_: `$(`$m.rejection_rate * 100)%`" } | Sort-Object; Start-Sleep -Seconds 10 }" -ForegroundColor Yellow

Write-Host "`n# 6. Monitor for crashes (exits non-zero)" -ForegroundColor Green
Write-Host "while (`$true) { docker ps -a | Select-String 'Exited|Unhealthy' | Write-Host -ForegroundColor Red; Start-Sleep -Seconds 5 }" -ForegroundColor Yellow

Write-Host "`n=== RUN ONE OF THESE NOW ===" -ForegroundColor Cyan
