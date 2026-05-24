"""
Root layer: immutable foundation

Copyright (c) 2026 Rebecca
Codex 6.65: codebecslucky7 Edition
"""

import math
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RootConfig:
    """
    Immutable root configuration.
    
    Attributes:
        id: Unique LUCKY7 root identifier
        root_radius: Fixed at 1.0 for geometry calculations
        geometry_target: Target geometry ratio (2π ≈ 6.283)
        geometry_tolerance: Knock threshold (default 0.15)
        max_drift: Maximum allowed distance from attractor
    """
    id: str = field(default_factory=lambda: f"LUCKY7-REBECCA-{uuid.uuid4().hex[:8]}")
    root_radius: float = 1.0
    geometry_target: float = 2 * math.pi
    geometry_tolerance: float = 0.15
    max_drift: float = 1.0

    def __post_init__(self):
        """Validate root parameters"""
        if self.root_radius <= 0:
            raise ValueError("root_radius must be positive")
        if self.geometry_tolerance < 0:
            raise ValueError("geometry_tolerance must be non-negative")


# Singleton root instance
ROOT = RootConfig()
