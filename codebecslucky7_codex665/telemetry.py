"""
Telemetry layer: real-time operational logging

Copyright (c) 2026 Rebecca
Codex 6.65: codebecslucky7 Edition
"""

import time
from typing import Any, Dict

from .drift import DriftStatus
from .root_rebecca import ROOT


def log_tick(
    t0: float,
    tick: int,
    state: Dict[str, Any],
    drift: DriftStatus
) -> None:
    """
    Log a single tick with operational metrics.
    
    Args:
        t0: Start time (from time.time())
        tick: Tick counter
        state: Current state dict
        drift: DriftStatus object
    
    Output format:
        [ROOT_ID] tick=##### rpm=#### phase=0.### power=0.### 
                  geom=0.### err=0.### knock=True/False
    """
    elapsed = time.time() - t0
    rpm = tick / elapsed * 60 if elapsed > 0 else 0
    
    print(
        f"[{ROOT.id}] "
        f"tick={tick:05d} "
        f"rpm={rpm:8.1f} "
        f"phase={state['phase']:.3f} "
        f"power={state['power']:.3f} "
        f"geom={drift.ratio:.3f} "
        f"err={drift.error:.3f} "
        f"knock={drift.knock}"
    )
