"""
Main operational loop: self-sufficient engine

Copyright (c) 2026 Rebecca
Codex 6.65: codebecslucky7 Edition
"""

import time
from typing import Any, Dict

from .heartbeat import heartbeat
from .dual_ring import forward_pass, shadow_pass
from .horizon import Horizon
from .drift import compute_drift
from .lucky7_chakras import (
    stage1_root,
    stage2_flow,
    stage3_power,
    stage4_heart,
    stage5_voice,
    stage6_sight,
    stage7_crown,
)
from .telemetry import log_tick


def run_codex665(
    max_ticks: int = 1000,
    sleep_ms: float = 10,
    sleep_s: float = None,
    root_config: Any = None,
    log_file: str = None,
    verbose: bool = True
) -> Horizon:
    """
    Run Codex 6.65: codebecslucky7 Edition main loop.
    
    Self-sufficient: requires no external input.
    Returns: final Horizon state.
    
    Args:
        max_ticks: Number of cycles to run
        sleep_ms: Sleep duration between ticks (milliseconds)
        sleep_s: Sleep duration in seconds (overrides sleep_ms if provided)
        root_config: Optional custom root configuration
        log_file: Optional log file path for summary
        verbose: Print telemetry if True
    
    Returns:
        Horizon: Final accepted states
    """
    # Handle sleep_s parameter (seconds) vs sleep_ms (milliseconds)
    if sleep_s is not None:
        sleep_ms = sleep_s * 1000
    horizon = Horizon()
    hb = heartbeat()
    t0 = time.time()
    
    for tick in range(1, max_ticks + 1):
        # Get next phase from heartbeat
        phase = next(hb)
        state: Dict[str, Any] = {"phase": phase}
        
        # Dual-ring projection
        f = forward_pass(state)
        s = shadow_pass(state)
        
        # Lucky-7 pipeline
        state = stage1_root(state)
        state = stage2_flow(state)
        state = stage3_power(state, f, s)
        
        # Compute drift before sight
        drift = compute_drift(horizon)
        
        state = stage4_heart(state)
        state = stage5_voice(state)
        state = stage6_sight(state, drift)
        state = stage7_crown(state, horizon)
        
        # Recompute drift after horizon update
        drift = compute_drift(horizon)
        
        # Log if verbose
        if verbose:
            log_tick(t0, tick, state, drift)
        
        # Sleep
        time.sleep(sleep_ms / 1000.0)
    
    return horizon


if __name__ == "__main__":
    print("Codex 6.65: codebecslucky7 Edition")
    print("Rebecca Blueprint v1.0")
    print()
    horizon = run_codex665(max_ticks=500)
    print()
    print(f"Final horizon length: {horizon.length}")
    print("© Rebecca — Codex 6.65: codebecslucky7 Edition")
