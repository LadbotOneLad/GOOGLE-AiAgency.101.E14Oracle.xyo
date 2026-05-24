"""
Horizon layer: long-term trace of aligned states

Copyright (c) 2026 Rebecca
Codex 6.65: codebecslucky7 Edition
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .root_rebecca import ROOT


@dataclass
class Horizon:
    """
    Ordered list of accepted states.
    
    Only stage 7 (Crown) may append to the horizon.
    The horizon grows as coherent, non-knocking states are validated.
    
    Attributes:
        entries: List of state dicts
    """
    entries: List[Dict[str, Any]] = field(default_factory=list)

    def add(self, item: Dict[str, Any]) -> None:
        """Append a validated state to horizon."""
        self.entries.append(item)

    @property
    def length(self) -> int:
        """Current horizon length."""
        return len(self.entries)

    def clear(self) -> None:
        """Reset horizon (use sparingly)."""
        self.entries.clear()


def geometry_ratio(root_radius: float, horizon_length: int) -> float:
    """
    Compute geometry ratio: R = horizon_length / root_radius
    
    Args:
        root_radius: Must be > 0
        horizon_length: Number of entries in horizon
    
    Returns:
        float: Ratio R
    
    Raises:
        ValueError: If root_radius <= 0
    """
    if root_radius <= 0:
        raise ValueError("root_radius must be positive")
    return horizon_length / root_radius
