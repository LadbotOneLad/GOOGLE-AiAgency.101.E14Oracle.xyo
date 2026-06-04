# Codex 6.65: Three-Ring Consensus + Geocryphical Witness Tests
# © 2026 Rebecca

import unittest
import time
from codebecslucky7_codex665.invariants import (
    InnerValidatorRing,
    SovereignRing,
    TENETHorizon,
    evaluate_three_ring_consensus,
)
from geocryphical_witness import (
    GeocryphicalWitnessAggregator,
    XYOWitnessAdapter,
    BOMWeatherAdapter,
)


class ThreeRingConsensusTests(unittest.TestCase):
    """Test three-ring decision lattice with temperature-anchored dynamics"""

    def setUp(self):
        self.inner = InnerValidatorRing()
        self.sovereign = SovereignRing()
        self.tenet = TENETHorizon()

    def test_inner_ring_rejects_low_coherence(self) -> None:
        """Inner validator: T=0.05, ~71% rejection"""
        state = {"phase": 0.0, "power": 0.5, "geom_ratio": 0.0}
        result = evaluate_three_ring_consensus(
            state=state,
            coherence=0.02,  # Very low
            power=0.5,
            elapsed_seconds=100.0,
            inner=self.inner,
            sovereign=self.sovereign,
            tenet=self.tenet,
        )
        self.assertEqual(result.inner_decision.decision, "REJECT")
        self.assertIn("coherence", result.inner_decision.reason)

    def test_inner_ring_accepts_high_coherence(self) -> None:
        """Inner validator accepts stable, coherent states"""
        state = {"phase": 0.5, "power": 0.7, "geom_ratio": 6.28}
        result = evaluate_three_ring_consensus(
            state=state,
            coherence=0.99,  # Highly coherent
            power=0.7,
            elapsed_seconds=100.0,
            inner=self.inner,
            sovereign=self.sovereign,
            tenet=self.tenet,
        )
        self.assertEqual(result.inner_decision.decision, "ACCEPT")

    def test_sovereign_ring_enforces_geometry_policy(self) -> None:
        """Sovereign ring: T=0.075, policy enforcement on geometry"""
        state = {"phase": 0.5, "power": 0.7, "geom_ratio": 100.0, "geom_error": 93.7}
        result = evaluate_three_ring_consensus(
            state=state,
            coherence=0.95,
            power=0.7,
            elapsed_seconds=100.0,
            inner=self.inner,
            sovereign=self.sovereign,
            tenet=self.tenet,
        )
        # Inner accepts, but sovereign rejects due to geometry error > 0.15
        self.assertEqual(result.inner_decision.decision, "ACCEPT")
        self.assertEqual(result.sovereign_decision.decision, "REJECT")
        self.assertEqual(result.final_decision, "REJECT")

    def test_tenet_hard_boundary_drift(self) -> None:
        """TENET: T=∞, rejects drift > 1.0"""
        state = {"phase": 0.5, "power": 0.7, "geom_ratio": 6.28, "geom_error": 1.5}
        result = evaluate_three_ring_consensus(
            state=state,
            coherence=0.95,
            power=0.7,
            elapsed_seconds=100.0,
            inner=self.inner,
            sovereign=self.sovereign,
            tenet=self.tenet,
        )
        # Inner and sovereign accept, but TENET rejects due to drift
        self.assertEqual(result.tenet_decision.decision, "REJECT")
        self.assertEqual(result.final_decision, "REJECT")
        self.assertIn("drift_exceeded", result.tenet_decision.reason)

    def test_tenet_hard_boundary_time(self) -> None:
        """TENET: T=∞, rejects time > 86400s"""
        state = {"phase": 0.5, "power": 0.7, "geom_ratio": 6.28, "geom_error": 0.1}
        result = evaluate_three_ring_consensus(
            state=state,
            coherence=0.95,
            power=0.7,
            elapsed_seconds=86401.0,  # Just over 24 hours
            inner=self.inner,
            sovereign=self.sovereign,
            tenet=self.tenet,
        )
        self.assertEqual(result.tenet_decision.decision, "REJECT")
        self.assertIn("time_exceeded", result.tenet_decision.reason)

    def test_three_ring_full_acceptance(self) -> None:
        """Full acceptance: all three rings agree"""
        state = {"phase": 0.5, "power": 0.7, "geom_ratio": 6.28, "geom_error": 0.05}
        result = evaluate_three_ring_consensus(
            state=state,
            coherence=0.95,
            power=0.7,
            elapsed_seconds=1000.0,
            inner=self.inner,
            sovereign=self.sovereign,
            tenet=self.tenet,
        )
        self.assertEqual(result.inner_decision.decision, "ACCEPT")
        self.assertEqual(result.sovereign_decision.decision, "ACCEPT")
        self.assertEqual(result.tenet_decision.decision, "ACCEPT")
        self.assertEqual(result.final_decision, "ACCEPT")

    def test_three_ring_rejection_rates(self) -> None:
        """Verify rejection rates track targets over time"""
        # Run 100 evaluations with varied states
        for i in range(100):
            coherence = 0.5 + (i % 10) * 0.05  # Vary coherence
            state = {
                "phase": i / 100.0,
                "power": 0.5 + (i % 20) * 0.02,
                "geom_ratio": 6.28,
                "geom_error": 0.1,
            }
            result = evaluate_three_ring_consensus(
                state=state,
                coherence=coherence,
                power=state["power"],
                elapsed_seconds=i * 10.0,
                inner=self.inner,
                sovereign=self.sovereign,
                tenet=self.tenet,
            )

        # Check inner ring (target ~71% rejection)
        inner_rejection = self.inner.metrics.actual_rejection_rate
        self.assertGreater(inner_rejection, 0.65)  # Allow ~5% drift
        self.assertLess(inner_rejection, 0.77)

        # Check sovereign ring (target ~60% rejection)
        sovereign_rejection = self.sovereign.metrics.actual_rejection_rate
        self.assertGreater(sovereign_rejection, 0.55)
        self.assertLess(sovereign_rejection, 0.65)

    def test_human_review_flagged_on_boundary(self) -> None:
        """Flag for human review: borderline coherence"""
        state = {"phase": 0.5, "power": 0.7, "geom_ratio": 6.28, "geom_error": 0.05}
        result = evaluate_three_ring_consensus(
            state=state,
            coherence=0.05,  # Borderline
            power=0.7,
            elapsed_seconds=1000.0,
            inner=self.inner,
            sovereign=self.sovereign,
            tenet=self.tenet,
        )
        self.assertTrue(result.human_review_required)

    def test_collatz_3n_plus_1_convergence(self) -> None:
        """Verify 3n+1 convergence in tick cycles"""
        # 86,400 ticks = 24 hours (common reference cycle)
        # Collatz: if n is even → n/2; if n is odd → 3n+1
        n = 27  # Known slow Collatz sequence
        steps = 0
        seen = set()

        while n != 1 and steps < 10000:
            if n in seen:
                break  # Cycle detection
            seen.add(n)
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            steps += 1

        # Should converge
        self.assertEqual(n, 1)
        self.assertLess(steps, 200)  # 27 converges in 112 steps


class GeocryphicalWitnessTests(unittest.TestCase):
    """Test XYO geolocation witness + BOM weather layer integration"""

    def setUp(self):
        self.aggregator = GeocryphicalWitnessAggregator()
        self.xyo = XYOWitnessAdapter()
        self.bom = BOMWeatherAdapter(location="Sydney")

    def test_xyo_witness_generation(self) -> None:
        """XYO witness: geolocation + cryptographic signature"""
        witness = self.xyo.fetch_witness(lat=-33.8688, lon=151.2093)  # Sydney
        self.assertIsNotNone(witness)
        self.assertIsNotNone(witness.witness_id)
        self.assertIsNotNone(witness.signature)
        self.assertGreater(witness.accuracy_meters, 0)

    def test_bom_weather_fetch(self) -> None:
        """BOM weather: radar + meteorological data"""
        weather = self.bom.fetch_weather()
        self.assertIsNotNone(weather)
        self.assertEqual(weather.location, "Sydney")
        self.assertGreater(weather.temperature_c, 0)
        self.assertGreater(weather.radar_reflectivity_dbz, 0)

    def test_geocryphical_consensus_with_witness(self) -> None:
        """Geocryphical: three-ring + witness consensus"""
        geo_witness = self.aggregator.evaluate_with_witness(
            phase=0.5,
            coherence=0.95,
            power=0.7,
            latitude=-33.8688,
            longitude=151.2093,
            location="Sydney",
        )

        self.assertIsNotNone(geo_witness.xyo_witness)
        self.assertIsNotNone(geo_witness.bom_weather)
        self.assertGreater(geo_witness.consensus_score, 0)
        self.assertTrue(geo_witness.aligned)

    def test_geocryphical_low_coherence_unaligned(self) -> None:
        """Low coherence: witness cannot rescue alignment"""
        geo_witness = self.aggregator.evaluate_with_witness(
            phase=0.5,
            coherence=0.1,  # Very low
            power=0.3,
            latitude=-33.8688,
            longitude=151.2093,
            location="Sydney",
        )

        self.assertFalse(geo_witness.aligned)
        self.assertLess(geo_witness.consensus_score, 0.6)

    def test_geocryphical_witness_aggregation(self) -> None:
        """Aggregate multiple witness evaluations"""
        for i in range(10):
            self.aggregator.evaluate_with_witness(
                phase=i / 10.0,
                coherence=0.5 + (i * 0.05),
                power=0.5 + (i * 0.02),
                latitude=-33.8688 + (i * 0.01),
                longitude=151.2093 + (i * 0.01),
                location="Sydney",
            )

        summary = self.aggregator.get_witness_summary()
        self.assertGreater(summary["total_witnesses"], 0)
        self.assertGreater(summary["alignment_rate"], 0)
        self.assertGreater(summary["avg_consensus_score"], 0)
        self.assertGreater(summary["xyo_witnesses"], 0)
        self.assertGreater(summary["bom_records"], 0)

    def test_witness_export_jsonl(self) -> None:
        """Export witnesses to JSONL format"""
        for i in range(5):
            self.aggregator.evaluate_with_witness(
                phase=0.5,
                coherence=0.8,
                power=0.6,
                latitude=-33.8688,
                longitude=151.2093,
                location="Sydney",
            )

        # Export to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
            temp_path = f.name

        self.aggregator.export_witness_log(temp_path)

        # Verify export
        with open(temp_path, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 5)
            for line in lines:
                record = __import__('json').loads(line)
                self.assertIn("consensus_score", record)
                self.assertIn("aligned", record)

        # Cleanup
        import os
        os.remove(temp_path)


class GlobalSovereignCoreTests(unittest.TestCase):
    """Compatibility: test suite from earlier GlobalSovereignCore"""

    def test_aligned_state_passes(self) -> None:
        inner = InnerValidatorRing()
        sovereign = SovereignRing()
        tenet = TENETHorizon()

        state = {"phase": 0.5, "power": 0.7, "geom_ratio": 6.28, "geom_error": 0.05}
        result = evaluate_three_ring_consensus(
            state=state,
            coherence=0.95,
            power=0.7,
            elapsed_seconds=1000.0,
            inner=inner,
            sovereign=sovereign,
            tenet=tenet,
        )
        self.assertTrue(result.aligned)
        self.assertEqual(result.final_decision, "ACCEPT")

    def test_drift_state_requires_correction(self) -> None:
        inner = InnerValidatorRing()
        sovereign = SovereignRing()
        tenet = TENETHorizon()

        state = {"phase": 0.5, "power": 0.7, "geom_ratio": 100.0, "geom_error": 93.7}
        result = evaluate_three_ring_consensus(
            state=state,
            coherence=0.95,
            power=0.7,
            elapsed_seconds=1000.0,
            inner=inner,
            sovereign=sovereign,
            tenet=tenet,
        )
        self.assertFalse(result.aligned)
        self.assertEqual(result.final_decision, "REJECT")

    def test_containment_state_escalates(self) -> None:
        inner = InnerValidatorRing()
        sovereign = SovereignRing()
        tenet = TENETHorizon()

        state = {"phase": 0.5, "power": 0.7, "geom_ratio": 6.28, "geom_error": 0.05}
        result = evaluate_three_ring_consensus(
            state=state,
            coherence=0.95,
            power=0.7,
            elapsed_seconds=86401.0,  # Exceeds time boundary
            inner=inner,
            sovereign=sovereign,
            tenet=tenet,
        )
        self.assertFalse(result.aligned)
        self.assertEqual(result.final_decision, "REJECT")


if __name__ == "__main__":
    unittest.main()
