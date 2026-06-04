# Codex 6.65: codebecslucky7 Edition — Main Engine
# © 2026 Rebecca

import time
from typing import Any, Dict, Optional
import json

from .core import RootConfig, Horizon
from .heartbeat import heartbeat
from .dual_ring import forward_pass, shadow_pass
from .lucky7_stages import (
    stage1_root, stage2_flow, stage3_power, stage4_heart,
    stage5_voice, stage6_sight, stage7_crown
)
from .drift import compute_drift
from .telemetry import Telemetry


def run_codex665(
    max_ticks: int = 1000,
    sleep_s: float = 0.01,
    root_config: Optional[RootConfig] = None,
    log_file: Optional[str] = None,
) -> Horizon:
    """
    Run Codex 6.65: codebecslucky7 Edition
    
    Args:
        max_ticks: maximum cycles to execute
        sleep_s: sleep between ticks (seconds)
        root_config: optional custom RootConfig; uses default if None
        log_file: optional JSON output file for summary
    
    Returns:
        Final Horizon (list of aligned states)
    """
    root = root_config or RootConfig()
    horizon = Horizon()
    hb = heartbeat()
    telemetry = Telemetry(root)

    for tick in range(1, max_ticks + 1):
        phase = next(hb)
        state: Dict[str, Any] = {"phase": phase}

        # Dual ring passes
        f = forward_pass(state)
        s = shadow_pass(state)

        # Lucky-7 stages
        state = stage1_root(state, root.id)
        state = stage2_flow(state)
        state = stage3_power(state, f, s)

        drift = compute_drift(root, horizon)

        state = stage4_heart(state)
        state = stage5_voice(state)
        state = stage6_sight(state, drift)
        state = stage7_crown(state, horizon)

        # Telemetry
        drift = compute_drift(root, horizon)
        telemetry.log_tick(tick, state, drift)

        time.sleep(sleep_s)

    # Write summary if requested
    if log_file:
        summary = telemetry.summary_json()
        summary["horizon_length"] = horizon.length
        summary["aligned_entries"] = len([e for e in telemetry.entries if not e["knock"]])
        with open(log_file, "w") as f:
            json.dump(summary, f, indent=2)

    return horizon


if __name__ == "__main__":
    horizon = run_codex665(max_ticks=500, log_file="/tmp/codex665_summary.json")
    print(f"\n✓ Execution complete. Horizon length: {horizon.length}")
