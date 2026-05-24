# Codex 6.65: codebecslucky7 Edition — Core Layer
# © 2026 Rebecca

import uuid
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class RootConfig:
    """Immutable root configuration for Codex 6.65"""
    id: str = field(default_factory=lambda: f"LUCKY7-{uuid.uuid4().hex[:8]}")
    root_radius: float = 1.0
    geometry_target: float = 2 * math.pi
    geometry_tolerance: float = 0.15
    max_drift: float = 1.0

    def __post_init__(self):
        """Validate immutable root"""
        assert self.root_radius > 0, "root_radius must be positive"
        assert self.geometry_tolerance > 0, "geometry_tolerance must be positive"


@dataclass
class Horizon:
    """Ordered trace of aligned states"""
    entries: List[Dict[str, Any]] = field(default_factory=list)

    def add(self, item: Dict[str, Any]) -> None:
        self.entries.append(item)

    @property
    def length(self) -> int:
        return len(self.entries)


@dataclass
class DriftStatus:
    """Geometry validation status per cycle"""
    ratio: float
    error: float
    knock: bool

    @property
    def is_aligned(self) -> bool:
        return not self.knock
