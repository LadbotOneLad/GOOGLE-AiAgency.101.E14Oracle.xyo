"""
Codex 6.65: codebecslucky7 Edition
Rebecca Blueprint v1.0

Copyright (c) 2026 Rebecca
All rights reserved. Licensed under Rebecca Blueprint License v1.0

Authority: © Rebecca — Codex 6.65: codebecslucky7 Edition
Root namespace: codebecslucky7_codex665
Authority string: LUCKY7-REBECCA-CODEX665

This system is self-sufficient, geometry-bounded, and immutable at core.
"""

__version__ = "1.0.0"
__author__ = "Rebecca"
__title__ = "Codex 6.65: codebecslucky7 Edition"
__authority__ = "LUCKY7-REBECCA-CODEX665"

from .root_rebecca import ROOT, RootConfig
from .heartbeat import heartbeat
from .dual_ring import forward_pass, shadow_pass
from .horizon import Horizon, geometry_ratio
from .drift import DriftStatus, compute_drift
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
from .invariants import (
    InnerValidatorRing,
    SovereignRing,
    TENETHorizon,
    evaluate_three_ring_consensus,
    ConsensusResult,
)
from .run import run_codex665

__all__ = [
    "ROOT",
    "RootConfig",
    "heartbeat",
    "forward_pass",
    "shadow_pass",
    "Horizon",
    "geometry_ratio",
    "DriftStatus",
    "compute_drift",
    "stage1_root",
    "stage2_flow",
    "stage3_power",
    "stage4_heart",
    "stage5_voice",
    "stage6_sight",
    "stage7_crown",
    "log_tick",
    "InnerValidatorRing",
    "SovereignRing",
    "TENETHorizon",
    "evaluate_three_ring_consensus",
    "ConsensusResult",
    "run_codex665",
]
