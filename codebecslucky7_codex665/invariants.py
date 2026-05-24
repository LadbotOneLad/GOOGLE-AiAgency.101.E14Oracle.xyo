# Codex 6.65: codebecslucky7 Edition — Invariant Validators
# © 2026 Rebecca
# Three-ring decision lattice with temperature-anchored dynamics

import math
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class RingMetrics:
    """Temperature-anchored ring metrics"""
    temperature: float
    target_rejection_rate: float
    accepted_count: int
    rejected_count: int
    total_processed: int

    @property
    def actual_rejection_rate(self) -> float:
        if self.total_processed == 0:
            return 0.0
        return self.rejected_count / self.total_processed

    @property
    def drift_from_target(self) -> float:
        return abs(self.actual_rejection_rate - self.target_rejection_rate)

    @property
    def is_aligned(self) -> bool:
        return self.drift_from_target < 0.05  # 5% tolerance


@dataclass
class RingDecision:
    """Decision from a single ring"""
    ring_name: str
    temperature: float
    decision: str  # "ACCEPT" | "REJECT"
    reason: str
    metrics: RingMetrics


class InnerValidatorRing:
    """T=0.05, ~71% rejection rate, high-frequency membrane"""

    def __init__(self):
        self.temperature = 0.05
        self.target_rejection_rate = 0.71
        self.metrics = RingMetrics(
            temperature=0.05,
            target_rejection_rate=0.71,
            accepted_count=0,
            rejected_count=0,
            total_processed=0,
        )

    def evaluate(self, state: dict, coherence: float, power: float) -> RingDecision:
        """Inner ring: filter for coherence and stability"""
        # High temperature = strict filtering
        threshold = 1.0 - self.temperature
        passes_coherence = coherence > threshold

        # Adjust based on power stability
        if power < 0.3:
            passes_coherence = False

        decision = "ACCEPT" if passes_coherence else "REJECT"
        reason = f"coherence={coherence:.3f}, threshold={threshold:.3f}, power={power:.3f}"

        if decision == "ACCEPT":
            self.metrics.accepted_count += 1
        else:
            self.metrics.rejected_count += 1
        self.metrics.total_processed += 1

        return RingDecision(
            ring_name="INNER_VALIDATOR",
            temperature=self.temperature,
            decision=decision,
            reason=reason,
            metrics=self.metrics,
        )


class SovereignRing:
    """T=0.075, ~60% rejection rate, policy enforcement"""

    def __init__(self):
        self.temperature = 0.075
        self.target_rejection_rate = 0.60
        self.metrics = RingMetrics(
            temperature=0.075,
            target_rejection_rate=0.60,
            accepted_count=0,
            rejected_count=0,
            total_processed=0,
        )

    def evaluate(self, state: dict, inner_decision: RingDecision) -> RingDecision:
        """Sovereign ring: enforce structural policy"""
        # Only processes accepted inner candidates
        if inner_decision.decision == "REJECT":
            decision = "REJECT"
            reason = "Failed inner validator ring"
        else:
            # Policy check: geometry alignment, horizon growth
            geometry_ratio = state.get("geom_ratio", float("inf"))
            target_2pi = 2 * math.pi

            error = abs(geometry_ratio - target_2pi)
            tolerance = 0.15

            # Stricter: policy accepts only well-aligned states
            passes_policy = error < tolerance

            decision = "ACCEPT" if passes_policy else "REJECT"
            reason = f"policy_check: geom_error={error:.3f}, tolerance={tolerance}"

        if decision == "ACCEPT":
            self.metrics.accepted_count += 1
        else:
            self.metrics.rejected_count += 1
        self.metrics.total_processed += 1

        return RingDecision(
            ring_name="SOVEREIGN_RING",
            temperature=self.temperature,
            decision=decision,
            reason=reason,
            metrics=self.metrics,
        )


class TENETHorizon:
    """T=∞, 100% rejection of boundary violations"""

    def __init__(self, max_drift: float = 1.0, max_time_seconds: float = 86400.0):
        self.temperature = float("inf")
        self.target_rejection_rate = 1.0  # Hard boundary
        self.max_drift = max_drift
        self.max_time_seconds = max_time_seconds
        self.metrics = RingMetrics(
            temperature=float("inf"),
            target_rejection_rate=1.0,
            accepted_count=0,
            rejected_count=0,
            total_processed=0,
        )

    def evaluate(
        self,
        state: dict,
        sovereign_decision: RingDecision,
        elapsed_seconds: float,
    ) -> RingDecision:
        """TENET: hard boundaries on drift, time, resources"""
        if sovereign_decision.decision == "REJECT":
            decision = "REJECT"
            reason = "Failed sovereign ring"
        else:
            # Hard boundaries
            violations = []

            # Drift check
            drift = state.get("geom_error", 0.0)
            if drift > self.max_drift:
                violations.append(f"drift_exceeded={drift:.3f}")

            # Time check
            if elapsed_seconds > self.max_time_seconds:
                violations.append(f"time_exceeded={elapsed_seconds:.1f}s")

            # Coherence check (sanity)
            coherence = state.get("coherence", 0.0)
            if coherence < -1.5:  # Physically impossible
                violations.append(f"coherence_violated={coherence:.3f}")

            decision = "REJECT" if violations else "ACCEPT"
            reason = f"TENET_boundaries: {', '.join(violations) if violations else 'all_clear'}"

        if decision == "ACCEPT":
            self.metrics.accepted_count += 1
        else:
            self.metrics.rejected_count += 1
        self.metrics.total_processed += 1

        return RingDecision(
            ring_name="TENET_HORIZON",
            temperature=self.temperature,
            decision=decision,
            reason=reason,
            metrics=self.metrics,
        )


@dataclass
class ConsensusResult:
    """Three-ring consensus output"""
    inner_decision: RingDecision
    sovereign_decision: RingDecision
    tenet_decision: RingDecision
    final_decision: str  # "ACCEPT" | "REJECT"
    aligned: bool
    coherence_score: float
    human_review_required: bool


def evaluate_three_ring_consensus(
    state: dict,
    coherence: float,
    power: float,
    elapsed_seconds: float,
    inner: InnerValidatorRing,
    sovereign: SovereignRing,
    tenet: TENETHorizon,
) -> ConsensusResult:
    """Run three-ring consensus: inner → sovereign → TENET"""

    # Ring 1: Inner validator
    inner_decision = inner.evaluate(state, coherence, power)

    # Ring 2: Sovereign policy
    sovereign_decision = sovereign.evaluate(state, inner_decision)

    # Ring 3: TENET hard boundaries
    tenet_decision = tenet.evaluate(state, sovereign_decision, elapsed_seconds)

    # Consensus: all three must accept
    final_decision = "ACCEPT" if tenet_decision.decision == "ACCEPT" else "REJECT"

    # Alignment: actual rejection rates match targets
    inner_aligned = inner.metrics.is_aligned
    sovereign_aligned = sovereign.metrics.is_aligned
    tenet_aligned = True  # TENET has no target, only absolutes

    all_aligned = inner_aligned and sovereign_aligned and tenet_aligned

    # Human review if:
    # - Decision boundary (borderline coherence)
    # - Ring disagreement (rare)
    # - High-stakes (accepted after high rejection)
    human_review_needed = (
        abs(coherence - 0.0) < 0.1  # Borderline
        or (inner_decision.decision != sovereign_decision.decision)  # Disagreement
        or (final_decision == "ACCEPT" and sovereign.metrics.actual_rejection_rate > 0.65)
    )

    return ConsensusResult(
        inner_decision=inner_decision,
        sovereign_decision=sovereign_decision,
        tenet_decision=tenet_decision,
        final_decision=final_decision,
        aligned=all_aligned,
        coherence_score=coherence,
        human_review_required=human_review_needed,
    )
