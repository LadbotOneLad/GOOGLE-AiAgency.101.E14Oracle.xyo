"""
Drift layer: geometry monitoring and knock detection

Copyright (c) 2026 Rebecca
Codex 6.65: codebecslucky7 Edition
"""

from dataclasses import dataclass

from .root_rebecca import ROOT
from .horizon import Horizon, geometry_ratio


@dataclass
class DriftStatus:
    """
    Geometry and drift monitoring.
    
    Attributes:
        ratio: Current geometry ratio R = horizon_length / root_radius
        error: Distance from target (2π): |R - 2π|
        knock: True if error > tolerance (knock condition detected)
    """
    ratio: float
    error: float
    knock: bool


def compute_drift(horizon: Horizon) -> DriftStatus:
    """
    Compute drift status for current horizon.
    
    Knock condition: error > geometry_tolerance
    
    Args:
        horizon: Horizon instance
    
    Returns:
        DriftStatus with ratio, error, and knock flag
    """
    r = geometry_ratio(ROOT.root_radius, horizon.length)
    err = abs(r - ROOT.geometry_target)
    knock = err > ROOT.geometry_tolerance
    return DriftStatus(ratio=r, error=err, knock=knock)
