"""
Dual-ring layer: forward and shadow passes

Copyright (c) 2026 Rebecca
Codex 6.65: codebecslucky7 Edition
"""

import math
from typing import Any, Dict


def forward_pass(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Forward ring: projects phase onto sine curve.
    
    f(φ) = sin(2πφ)
    
    Args:
        state: Engine state dict containing 'phase'
    
    Returns:
        dict: {phase, sense, value}
    """
    return {
        "phase": state["phase"],
        "sense": "forward",
        "value": math.sin(2 * math.pi * state["phase"]),
    }


def shadow_pass(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Shadow ring: projects phase onto cosine curve (complementary view).
    
    s(φ) = cos(2πφ)
    
    Args:
        state: Engine state dict containing 'phase'
    
    Returns:
        dict: {phase, sense, value}
    """
    return {
        "phase": state["phase"],
        "sense": "shadow",
        "value": math.cos(2 * math.pi * state["phase"]),
    }
