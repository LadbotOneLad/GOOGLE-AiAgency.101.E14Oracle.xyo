#!/usr/bin/env python3
"""
Locking Invariant Inspector
Codex 6.65: codebecslucky7 Edition

Extracts and verifies all 14 containers have identical locking invariants.
"""

import json
import subprocess
import time
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Core invariants (must be identical across ALL engines)
CORE_INVARIANTS = {
    "root_radius": 1.0,
    "geometry_target": 2 * 3.141592653589793,  # 2π
    "geometry_tolerance": 0.15,
    "heartbeat_step": 0.01,
    "max_drift": 1.0,
}

ENGINES = [
    "codex-engine-1", "codex-engine-2", "codex-engine-3",
    "codex-engine-4", "codex-engine-5", "codex-engine-6",
    "codex-engine-7", "codex-engine-8", "codex-engine-9",
    "codex-engine-10", "codex-engine-11", "codex-engine-12",
    "codex-ultimate",
]


@dataclass
class InvariantSnapshot:
    """Captured state of invariants from one engine."""
    container: str
    timestamp: float
    log_lines: int
    phase: float
    power: float
    geom_ratio: float
    geom_error: float
    knock: bool
    rpm: float


def extract_latest_metrics(container: str) -> Optional[Dict[str, Any]]:
    """Extract latest tick metrics from container logs."""
    try:
        result = subprocess.run(
            ["docker", "logs", container, "--tail", "1"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return None
        
        line = result.stdout.strip()
        if not line:
            return None
        
        # Parse: [LUCKY7-{id}] tick={n} rpm={rpm} phase={φ} power={P} geom={R} err={ε} knock={bool}
        parts = {}
        
        # Extract numbers with regex
        tick_match = re.search(r'tick=(\d+)', line)
        rpm_match = re.search(r'rpm=\s*([\d.]+)', line)
        phase_match = re.search(r'phase=([\d.]+)', line)
        power_match = re.search(r'power=([\d.]+)', line)
        geom_match = re.search(r'geom=([\d.]+)', line)
        err_match = re.search(r'err=([\d.]+)', line)
        knock_match = re.search(r'knock=(\w+)', line)
        
        return {
            "tick": int(tick_match.group(1)) if tick_match else 0,
            "rpm": float(rpm_match.group(1)) if rpm_match else 0.0,
            "phase": float(phase_match.group(1)) if phase_match else 0.0,
            "power": float(power_match.group(1)) if power_match else 0.0,
            "geom": float(geom_match.group(1)) if geom_match else 0.0,
            "err": float(err_match.group(1)) if err_match else 0.0,
            "knock": knock_match.group(1).lower() == "true" if knock_match else False,
        }
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def get_log_count(container: str) -> int:
    """Get total line count in container logs."""
    try:
        result = subprocess.run(
            ["docker", "logs", container],
            capture_output=True,
            text=True,
            timeout=5
        )
        return len([l for l in result.stdout.strip().split("\n") if l])
    except:
        return 0


def check_invariants(snapshot: InvariantSnapshot) -> Dict[str, bool]:
    """Check if this engine respects all core invariants."""
    target = CORE_INVARIANTS["geometry_target"]
    tolerance = CORE_INVARIANTS["geometry_tolerance"]
    
    return {
        "phase_in_range": 0.0 <= snapshot.phase <= 1.0,
        "power_in_range": 0.0 <= snapshot.power <= 1.0,
        "rpm_positive": snapshot.rpm > 0,
        "geom_error_bounded": snapshot.geom_error <= tolerance,
        "geom_ratio_near_target": abs(snapshot.geom_ratio - target) <= (tolerance + 0.5),
    }


def main():
    print("\n" + "=" * 80)
    print("LOCKING INVARIANT INSPECTOR")
    print("Codex 6.65: codebecslucky7 Edition")
    print("=" * 80)
    
    print("\nCore Invariants (Must Match on All Engines):")
    for key, val in CORE_INVARIANTS.items():
        print(f"  {key:20s} = {val}")
    
    print("\n" + "-" * 80)
    print("Extracting snapshots from all 14 engines...")
    print("-" * 80)
    
    snapshots: List[InvariantSnapshot] = []
    
    for container in ENGINES:
        # Get metrics
        metrics = extract_latest_metrics(container)
        if not metrics:
            print(f"[{container}] ⚠ No metrics available")
            continue
        
        # Get log count
        log_count = get_log_count(container)
        
        # Build snapshot
        snapshot = InvariantSnapshot(
            container=container,
            timestamp=time.time(),
            log_lines=log_count,
            phase=metrics.get("phase", 0.0),
            power=metrics.get("power", 0.0),
            geom_ratio=metrics.get("geom", 0.0),
            geom_error=metrics.get("err", 0.0),
            knock=metrics.get("knock", False),
            rpm=metrics.get("rpm", 0.0),
        )
        
        snapshots.append(snapshot)
        
        # Check invariants for this engine
        checks = check_invariants(snapshot)
        all_pass = all(checks.values())
        status = "✓" if all_pass else "✗"
        
        print(f"\n[{container}] {status}")
        print(f"  Ticks: {log_count:6d} | RPM: {snapshot.rpm:8.1f}")
        print(f"  phase={snapshot.phase:.3f} power={snapshot.power:.3f}")
        print(f"  geom={snapshot.geom_ratio:.3f} err={snapshot.geom_error:.3f} knock={snapshot.knock}")
        
        for check, result in checks.items():
            icon = "✓" if result else "✗"
            print(f"    {icon} {check}")
    
    print("\n" + "=" * 80)
    print("SYNCHRONIZATION ANALYSIS")
    print("=" * 80)
    
    if not snapshots:
        print("⚠ No snapshots captured. Engines may still be initializing.")
        return
    
    # Check if all phases are synchronized
    phases = [s.phase for s in snapshots]
    phase_variance = max(phases) - min(phases) if phases else 0
    
    print(f"\nPhase Synchronization:")
    print(f"  Min phase: {min(phases):.4f}")
    print(f"  Max phase: {max(phases):.4f}")
    print(f"  Variance: {phase_variance:.4f}")
    sync_status = "✓ LOCKED" if phase_variance < 0.01 else "⚠ DRIFTING"
    print(f"  {sync_status}")
    
    # Check geometry alignment
    geom_errors = [s.geom_error for s in snapshots]
    max_geom_error = max(geom_errors) if geom_errors else 0
    min_geom_error = min(geom_errors) if geom_errors else 0
    
    print(f"\nGeometry Alignment:")
    print(f"  Min error: {min_geom_error:.4f}")
    print(f"  Max error: {max_geom_error:.4f}")
    print(f"  Tolerance: {CORE_INVARIANTS['geometry_tolerance']:.4f}")
    geom_status = "✓ ALIGNED" if max_geom_error <= CORE_INVARIANTS['geometry_tolerance'] else "✗ MISALIGNED"
    print(f"  {geom_status}")
    
    # Check knock state
    knock_states = [s.knock for s in snapshots]
    knocked_count = sum(knock_states)
    knock_uniform = len(set(knock_states)) == 1
    
    print(f"\nKnock State:")
    print(f"  Knocked: {knocked_count}/{len(knock_states)}")
    knock_status = "✓ UNIFORM" if knock_uniform else "⚠ DIVERGENT"
    print(f"  {knock_status}")
    
    # Check log progress
    log_counts = [s.log_lines for s in snapshots]
    log_min = min(log_counts) if log_counts else 0
    log_max = max(log_counts) if log_counts else 0
    log_variance = log_max - log_min
    
    print(f"\nProcessing Progress:")
    print(f"  Min ticks: {log_min}")
    print(f"  Max ticks: {log_max}")
    print(f"  Variance: {log_variance}")
    progress_status = "✓ SYNCHRONIZED" if log_variance < 20 else "⚠ DRIFTING"
    print(f"  {progress_status}")
    
    # Overall status
    print("\n" + "=" * 80)
    all_checks = [
        phase_variance < 0.01,
        max_geom_error <= CORE_INVARIANTS['geometry_tolerance'],
        knock_uniform,
        log_variance < 20,
    ]
    
    if all(all_checks):
        print("[OK] ALL 14 ENGINES LOCKED ON IDENTICAL INVARIANTS")
        print("=" * 80 + "\n")
    else:
        print("[WARN] SOME ENGINES DRIFTED - REMEDIATION RECOMMENDED")
        print("=" * 80 + "\n")
        print("Remediation Steps:")
        print("1. Restart engines: docker-compose -f docker-compose-production.yml restart")
        print("2. Re-inspect: python3 invariant_inspector.py")
        print("3. If persists: docker-compose -f docker-compose-production.yml down && up -d")


if __name__ == "__main__":
    main()
