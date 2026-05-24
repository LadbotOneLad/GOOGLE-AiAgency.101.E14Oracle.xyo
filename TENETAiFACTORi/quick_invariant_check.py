#!/usr/bin/env python3
"""Quick invariant lock check."""

import subprocess
import re

engines = [f"codex-engine-{i}" for i in range(1, 13)] + ["codex-ultimate"]

print("\nLOCKING INVARIANT CHECK")
print("=" * 70)
print("\nCore Invariants (must be identical across all engines):")
print("  root_radius      = 1.0")
print("  geometry_target  = 2*pi = 6.283")
print("  tolerance        = 0.15")
print("=" * 70)

phases = []
geom_ratios = []
geom_errors = []
knock_states = []

for engine in engines:
    try:
        # Get last log line
        result = subprocess.run(
            ["docker", "logs", engine, "--tail", "1"],
            capture_output=True,
            text=True,
            timeout=2
        )
        
        if result.returncode != 0 or not result.stdout.strip():
            continue
        
        line = result.stdout.strip()
        
        # Extract values
        phase = float(re.search(r'phase=([\d.]+)', line).group(1))
        geom = float(re.search(r'geom=([\d.]+)', line).group(1))
        err = float(re.search(r'err=([\d.]+)', line).group(1))
        knock = 'True' in line and 'knock=True' in line
        
        phases.append(phase)
        geom_ratios.append(geom)
        geom_errors.append(err)
        knock_states.append(knock)
        
        knock_str = "KNOCK" if knock else "OK"
        print(f"{engine:20s} | phase={phase:.3f} geom={geom:.3f} err={err:.3f} [{knock_str}]")
    
    except Exception as e:
        print(f"{engine:20s} | ERROR: {str(e)[:40]}")

print("\n" + "=" * 70)
print("INVARIANT LOCK STATUS")
print("=" * 70)

if phases:
    phase_var = max(phases) - min(phases)
    geom_var = max(geom_errors) - min(geom_errors)
    knock_uniform = len(set(knock_states)) == 1
    
    print(f"\nPhase variance:     {phase_var:.4f} (target: < 0.01)")
    print(f"  Status: {'PASS' if phase_var < 0.01 else 'FAIL'}")
    
    print(f"\nGeom error range:   {min(geom_errors):.3f} - {max(geom_errors):.3f} (limit: 0.15)")
    print(f"  Status: {'PASS' if max(geom_errors) <= 0.15 else 'FAIL'}")
    
    print(f"\nKnock uniformity:   {sum(knock_states)}/{len(knock_states)} knocked")
    print(f"  Status: {'PASS' if knock_uniform else 'FAIL'}")
    
    all_pass = (phase_var < 0.01) and (max(geom_errors) <= 0.15) and knock_uniform
    
    print("\n" + "=" * 70)
    if all_pass:
        print("RESULT: ALL INVARIANTS LOCKED")
    else:
        print("RESULT: SOME INVARIANTS DRIFTED")
    print("=" * 70 + "\n")

