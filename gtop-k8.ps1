# gtop k8: Kubernetes Multi-User Orchestration CLI
# K8-MU-ORCH commands for .15% SOLAR WAGYU — DIGITAL CUT
# 
# Usage: gtop k8 <command> [args]
#   gtop k8 status          — Pod health across cluster
#   gtop k8 map             — K8s topology (nodes + pods)
#   gtop k8 rollout <image> — Rolling deployment with rhythm
#   gtop k8 scale <replicas> — HPA manual scale
#   gtop k8 logs <pod>      — Tail pod logs
#   gtop k8 lock            — Show lock status
#   gtop k8 users           — List RBAC users

param(
    [Parameter(Position=0)]
    [string]$SubCommand = "help",
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

# Constants
$NAMESPACE = "k8-mu-orch"
$STATEFULSET = "k8-mu-orch-engines"
$HEARTBEAT = 1000

function Cmd-K8-Status {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "  K8S CLUSTER STATUS" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    
    # Get pod status
    Write-Host "PODS (StatefulSet: $STATEFULSET)" -ForegroundColor Cyan
    $pods = kubectl get pods -n $NAMESPACE -l app=te-papa-matihiko -o json | ConvertFrom-Json
    
    $running = 0
    $total = $pods.items.Count
    
    foreach($pod in $pods.items) {
        $name = $pod.metadata.name
        $status = $pod.status.phase
        $emoji = if ($status -eq "Running") { "🟢" } else { "🔴" }
        Write-Host "  $emoji $name : $status"
        if ($status -eq "Running") { $running++ }
        Start-Sleep -Milliseconds 200
    }
    
    Write-Host ""
    Write-Host "  Status: $running/$total pods running" -ForegroundColor Green
    Write-Host ""
    
    # HPA status
    Write-Host "HPA SCALING" -ForegroundColor Yellow
    $hpa = kubectl get hpa -n $NAMESPACE -o json | ConvertFrom-Json
    foreach($h in $hpa.items) {
        $name = $h.metadata.name
        $replicas = $h.status.currentReplicas ?? "N/A"
        $desired = $h.status.desiredReplicas ?? "N/A"
        Write-Host "  $name : $replicas/$desired replicas"
    }
    
    Write-Host ""
}

function Cmd-K8-Map {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "  K8S TOPOLOGY MAP" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Get nodes
    Write-Host "NODES" -ForegroundColor Yellow
    $nodes = kubectl get nodes -o json | ConvertFrom-Json
    foreach($node in $nodes.items) {
        $name = $node.metadata.name
        $status = $node.status.conditions[-1].status
        $emoji = if ($status -eq "True") { "🟢" } else { "🔴" }
        Write-Host "  $emoji $name"
        Start-Sleep -Milliseconds 150
    }
    
    Write-Host ""
    Write-Host "STATEFULSET: $STATEFULSET" -ForegroundColor Green
    Write-Host "  Replicas: 3-10 (HPA)"
    Write-Host "  Lock: 550e8400-e29b-41d4..."
    Write-Host "  Engines: 365, 777, 101, 1001-1012"
    Write-Host ""
    
    Write-Host "  Pod Distribution:" -ForegroundColor Cyan
    $pods = kubectl get pods -n $NAMESPACE -l app=te-papa-matihiko -o json | ConvertFrom-Json
    foreach($pod in $pods.items) {
        $podName = $pod.metadata.name
        $nodeName = $pod.spec.nodeName ?? "unscheduled"
        Write-Host "    $podName -> $nodeName"
        Start-Sleep -Milliseconds 100
    }
    
    Write-Host ""
}

function Cmd-K8-Rollout {
    param([string]$Image)
    
    if (-not $Image) {
        Write-Host "Usage: gtop k8 rollout <image-tag>"
        Write-Host "Example: gtop k8 rollout 4gr-fse:v1.0"
        return
    }
    
    Write-Host ""
    Write-Host "ROLLING DEPLOYMENT: $Image" -ForegroundColor Yellow
    Write-Host ""
    
    # Update image
    Write-Host "Setting image to: $Image" -NoNewline
    Start-Sleep -Milliseconds 500
    Write-Host "." -NoNewline
    Start-Sleep -Milliseconds 500
    Write-Host "." -NoNewline
    Start-Sleep -Milliseconds 500
    Write-Host ""
    
    kubectl set image statefulset/$STATEFULSET -n $NAMESPACE `
      "k8-mu-orch-engines=$Image" --record
    
    Write-Host ""
    Write-Host "Rollout in progress (TICK/BEAT/BREATH timing)" -ForegroundColor Green
    Write-Host ""
    
    # Watch rollout with rhythm
    for ($i = 0; $i -lt 5; $i++) {
        Write-Host -NoNewline "."
        Start-Sleep -Milliseconds 50
    }
    Write-Host ""
    Write-Host "Waiting for pods..." -NoNewline
    Start-Sleep -Milliseconds 1500
    Write-Host ""
    Write-Host ""
    
    # Show status
    kubectl rollout status statefulset/$STATEFULSET -n $NAMESPACE --timeout=5m
}

function Cmd-K8-Scale {
    param([int]$Replicas)
    
    if (-not $Replicas -or $Replicas -lt 1 -or $Replicas -gt 10) {
        Write-Host "Usage: gtop k8 scale <replicas> (1-10)"
        return
    }
    
    Write-Host ""
    Write-Host "SCALING to $Replicas replicas" -ForegroundColor Yellow
    kubectl scale statefulset $STATEFULSET -n $NAMESPACE --replicas=$Replicas
    Write-Host ""
    Write-Host "Scaling..." -ForegroundColor Green
    Start-Sleep -Milliseconds 2000
    Cmd-K8-Status
}

function Cmd-K8-Logs {
    param([string]$Pod)
    
    if (-not $Pod) {
        Write-Host "Usage: gtop k8 logs <pod-name>"
        Write-Host "Pods:"
        kubectl get pods -n $NAMESPACE -l app=te-papa-matihiko -o jsonpath='{.items[*].metadata.name}' | ForEach-Object { Write-Host "  $_" }
        return
    }
    
    kubectl logs -f $Pod -n $NAMESPACE
}

function Cmd-K8-Lock {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Magenta
    Write-Host "  LOCK STATUS (K8S)" -ForegroundColor Magenta
    Write-Host "================================" -ForegroundColor Magenta
    Write-Host ""
    
    $cm = kubectl get configmap engine-lock-metadata -n $NAMESPACE -o json | ConvertFrom-Json
    
    Write-Host "Lock Phrase: " -NoNewline
    Write-Host $cm.data.'lock-phrase' -ForegroundColor Green
    
    Write-Host "Engine Count: " -NoNewline
    Write-Host $cm.data.'engine-count' -ForegroundColor Green
    
    Write-Host "Kotahitanja: " -NoNewline
    Write-Host $cm.data.'kotahitanja-value' -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Synchronized Engines:" -ForegroundColor Cyan
    Write-Host "  " + ($cm.data.'engine-ports' -replace ',', ', ') -ForegroundColor Green
    Write-Host ""
}

function Cmd-K8-Users {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Yellow
    Write-Host "  RBAC USERS (K8S)" -ForegroundColor Yellow
    Write-Host "================================" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "ROLES:" -ForegroundColor Cyan
    Write-Host "  k8-mu-orch-admin   — Full access (create/delete)"
    Write-Host "  k8-mu-orch-operator — Read + scale"
    Write-Host "  k8-mu-orch-viewer   — Read-only"
    Write-Host ""
    
    Write-Host "SERVICE ACCOUNTS:" -ForegroundColor Cyan
    $sas = kubectl get serviceaccounts -n $NAMESPACE -o json | ConvertFrom-Json
    foreach($sa in $sas.items) {
        Write-Host "  $($sa.metadata.name)"
    }
    
    Write-Host ""
}

function Cmd-K8-Help {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║  GTOP K8: Kubernetes Orchestration    ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "COMMANDS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  gtop k8 status           Pod health + HPA status" -ForegroundColor Cyan
    Write-Host "  gtop k8 map              K8s topology (nodes + pods)" -ForegroundColor Cyan
    Write-Host "  gtop k8 rollout <image>  Rolling deployment" -ForegroundColor Cyan
    Write-Host "  gtop k8 scale <replicas> Manual HPA scale (1-10)" -ForegroundColor Cyan
    Write-Host "  gtop k8 logs <pod>       Tail pod logs" -ForegroundColor Cyan
    Write-Host "  gtop k8 lock             Lock status" -ForegroundColor Cyan
    Write-Host "  gtop k8 users            RBAC users + roles" -ForegroundColor Cyan
    Write-Host ""
}

function Cmd-K8-Coherence {
    # Invoke coherence validator
    $coherencePath = Join-Path (Split-Path $PSScriptRoot) "k8-mu-orch-coherence.ps1"
    if (Test-Path $coherencePath) {
        & $coherencePath -Verbose
    } else {
        Write-Host "Coherence validator not found at $coherencePath" -ForegroundColor Red
    }
}

# Router
switch ($SubCommand.ToLower()) {
    "status" { Cmd-K8-Status }
    "map" { Cmd-K8-Map }
    "rollout" { Cmd-K8-Rollout $Args[0] }
    "scale" { Cmd-K8-Scale ([int]$Args[0]) }
    "logs" { Cmd-K8-Logs $Args[0] }
    "lock" { Cmd-K8-Lock }
    "users" { Cmd-K8-Users }
    "coherence" { Cmd-K8-Coherence }
    "help" { Cmd-K8-Help }
    default {
        Write-Host "Unknown: $SubCommand" -ForegroundColor Red
        Cmd-K8-Help
    }
}
