"""
Heartbeat layer: phase generation

Copyright (c) 2026 Rebecca
Codex 6.65: codebecslucky7 Edition
"""

from typing import Generator


def heartbeat(step: float = 0.01) -> Generator[float, None, None]:
    """
    Generates cyclic phase values [0, 1).
    
    The heartbeat is self-sufficient: it needs no external input.
    It drives the entire engine loop via phase.
    
    Args:
        step: Phase increment per beat (default 0.01)
    
    Yields:
        float: Phase value in range [0, 1)
    
    Example:
        >>> hb = heartbeat()
        >>> next(hb)  # 0.0
        >>> next(hb)  # 0.01
    """
    phase = 0.0
    while True:
        yield phase
        phase = (phase + step) % 1.0
