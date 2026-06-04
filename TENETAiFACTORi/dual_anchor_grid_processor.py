#!/usr/bin/env python3
"""
Dual-Anchor Pyramid Grid: North Star + Southern Cross
Locks operational events to celestial references with Earth wobble tolerance.
Polaris (North Star) = True North (0°)
Crux (Southern Cross) = True South (180°)
"""

import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

class CelestialAnchors:
    """Model North Star (Polaris) and Southern Cross (Crux) as immutable references."""
    
    # Celestial Reference Points
    POLARIS_TRUE_NORTH = 0.0  # degrees (North Star)
    CRUX_TRUE_SOUTH = 180.0   # degrees (Southern Cross)
    POLARIS_DECLINATION = 89.264  # degrees (Polaris current declination)
    CRUX_DECLINATION = -62.87  # degrees (Southern Cross average declination)
    
    # Pyramid precision
    PYRAMID_PRECISION = 0.05  # degrees (1/7200 of rotation)
    
    # Earth wobble components (degrees)
    NUTATION_AMPLITUDE = 9.2 / 3600
    PRECESSION_RATE = 50.3 / 3600
    CHANDLER_WOBBLE_AMPLITUDE = 0.5 / 3600
    CHANDLER_WOBBLE_PERIOD = 433  # days
    
    # Precession: Polaris won't always be the north star
    # Currently closest (~0.47° away), cycle ~25920 years
    POLARIS_PRECESSION_DRIFT = 0.01 / 25920  # degrees/day
    
    def __init__(self, reference_date: datetime = None):
        self.reference_date = reference_date or datetime(2026, 3, 10, 0, 0, 0)
    
    def get_polaris_position(self, timestamp: datetime) -> Dict[str, float]:
        """Get Polaris (North Star) position accounting for precession and nutation."""
        if timestamp.tzinfo is not None:
            timestamp = timestamp.replace(tzinfo=None)
        
        days_since_ref = (timestamp - self.reference_date).days
        
        # Polaris slowly drifts due to precession
        polaris_drift = self.POLARIS_PRECESSION_DRIFT * days_since_ref
        
        # Nutation oscillation
        nutation_phase = (days_since_ref / 6793) * 2 * math.pi
        nutation = self.NUTATION_AMPLITUDE * math.sin(nutation_phase)
        
        # Chandler wobble
        chandler_phase = (days_since_ref / self.CHANDLER_WOBBLE_PERIOD) * 2 * math.pi
        chandler = self.CHANDLER_WOBBLE_AMPLITUDE * math.sin(chandler_phase)
        
        polaris_position = self.POLARIS_TRUE_NORTH + polaris_drift + nutation + chandler
        
        return {
            "reference_star": "Polaris (North Star)",
            "declination_degrees": self.POLARIS_DECLINATION,
            "base_position": self.POLARIS_TRUE_NORTH,
            "polaris_drift_degrees": round(polaris_drift, 8),
            "nutation_degrees": round(nutation, 6),
            "chandler_wobble_degrees": round(chandler, 6),
            "current_position_degrees": round(polaris_position, 6),
            "tolerance_band_min": round(polaris_position - abs(nutation + chandler), 6),
            "tolerance_band_max": round(polaris_position + abs(nutation + chandler), 6)
        }
    
    def get_crux_position(self, timestamp: datetime) -> Dict[str, float]:
        """Get Southern Cross (Crux) position accounting for precession and nutation."""
        if timestamp.tzinfo is not None:
            timestamp = timestamp.replace(tzinfo=None)
        
        days_since_ref = (timestamp - self.reference_date).days
        
        # Southern Cross drifts oppositely due to precession (180° offset)
        crux_drift = -self.POLARIS_PRECESSION_DRIFT * days_since_ref
        
        # Nutation oscillation
        nutation_phase = (days_since_ref / 6793) * 2 * math.pi
        nutation = self.NUTATION_AMPLITUDE * math.sin(nutation_phase)
        
        # Chandler wobble
        chandler_phase = (days_since_ref / self.CHANDLER_WOBBLE_PERIOD) * 2 * math.pi
        chandler = self.CHANDLER_WOBBLE_AMPLITUDE * math.sin(chandler_phase)
        
        crux_position = self.CRUX_TRUE_SOUTH + crux_drift + nutation + chandler
        
        return {
            "reference_star": "Crux (Southern Cross)",
            "declination_degrees": self.CRUX_DECLINATION,
            "base_position": self.CRUX_TRUE_SOUTH,
            "crux_drift_degrees": round(crux_drift, 8),
            "nutation_degrees": round(nutation, 6),
            "chandler_wobble_degrees": round(chandler, 6),
            "current_position_degrees": round(crux_position % 360, 6),
            "tolerance_band_min": round(crux_position - abs(nutation + chandler), 6),
            "tolerance_band_max": round(crux_position + abs(nutation + chandler), 6)
        }
    
    def is_aligned_to_north(self, measured_degrees: float, timestamp: datetime) -> Dict[str, bool]:
        """Check alignment to North Star anchor."""
        polaris = self.get_polaris_position(timestamp)
        min_bound = polaris["tolerance_band_min"]
        max_bound = polaris["tolerance_band_max"]
        
        aligned = min_bound <= measured_degrees <= max_bound
        distance = abs(measured_degrees - polaris["current_position_degrees"])
        
        return {
            "anchor": "Polaris",
            "aligned": aligned,
            "distance_degrees": round(distance, 6),
            "reference_position": polaris["current_position_degrees"],
            "tolerance_band": [min_bound, max_bound]
        }
    
    def is_aligned_to_south(self, measured_degrees: float, timestamp: datetime) -> Dict[str, bool]:
        """Check alignment to Southern Cross anchor."""
        crux = self.get_crux_position(timestamp)
        min_bound = crux["tolerance_band_min"]
        max_bound = crux["tolerance_band_max"]
        
        # Handle 360° wraparound
        measured_normalized = measured_degrees % 360
        crux_normalized = crux["current_position_degrees"] % 360
        
        aligned = min_bound <= measured_normalized <= max_bound or \
                 min_bound <= measured_normalized + 360 <= max_bound or \
                 min_bound - 360 <= measured_normalized <= max_bound - 360
        
        distance = abs(measured_normalized - crux_normalized)
        if distance > 180:
            distance = 360 - distance
        
        return {
            "anchor": "Crux",
            "aligned": aligned,
            "distance_degrees": round(distance, 6),
            "reference_position": crux_normalized,
            "tolerance_band": [min_bound, max_bound]
        }


class DualAnchorGrid:
    """Grid operations using North Star and Southern Cross as dual anchors."""
    
    SECONDS_PER_CYCLE = 86400
    GRID_SLOTS = 7200
    SLOT_DURATION = 12
    
    def __init__(self):
        self.cycle_start = datetime(2026, 3, 10, 0, 0, 0)
        self.anchors = CelestialAnchors(self.cycle_start)
        self.gridded_events = []
    
    def timestamp_to_slot(self, timestamp_str: str) -> int:
        """Convert ISO timestamp to grid slot."""
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            delta = dt - self.cycle_start
            seconds_in_cycle = delta.total_seconds() % self.SECONDS_PER_CYCLE
            slot_index = int(seconds_in_cycle // self.SLOT_DURATION)
            return slot_index
        except:
            return 0
    
    def slot_to_degrees(self, slot_index: int) -> float:
        """Convert slot to compass bearing (0-360)."""
        degrees = (slot_index / self.GRID_SLOTS) * 360
        return degrees % 360
    
    def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Grid event and validate against both North Star and Southern Cross."""
        event_id = event.get("id")
        timestamp_str = event.get("timestampIso")
        root_input = event.get("rootInput", {})
        
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except:
            dt = self.cycle_start
        
        # Grid positioning
        slot_index = self.timestamp_to_slot(timestamp_str)
        measured_degrees = self.slot_to_degrees(slot_index)
        
        # Get celestial anchor positions
        polaris = self.anchors.get_polaris_position(dt)
        crux = self.anchors.get_crux_position(dt)
        
        # Check alignment to both anchors
        north_alignment = self.anchors.is_aligned_to_north(measured_degrees, dt)
        south_alignment = self.anchors.is_aligned_to_south(measured_degrees, dt)
        
        # Verify drift
        reported_drift = root_input.get("driftDeviation", 0.0)
        max_allowed_drift = 0.05  # pyramid precision
        drift_acceptable = reported_drift <= max_allowed_drift
        
        # Verdict: aligned to at least one anchor + acceptable drift
        aligned_to_anchor = north_alignment["aligned"] or south_alignment["aligned"]
        verdict = "ACCEPT" if (aligned_to_anchor and drift_acceptable) else "REJECT"
        
        gridded = {
            "event_id": event_id,
            "original_event": event,
            "grid": {
                "slot": slot_index,
                "total_slots": self.GRID_SLOTS,
                "compass_bearing_degrees": round(measured_degrees, 4)
            },
            "celestial_anchors": {
                "polaris": polaris,
                "crux": crux
            },
            "alignment": {
                "north_star": north_alignment,
                "southern_cross": south_alignment,
                "primary_anchor": "Polaris" if north_alignment["aligned"] else "Crux" if south_alignment["aligned"] else "None"
            },
            "validation": {
                "reported_drift": reported_drift,
                "max_allowed_drift": max_allowed_drift,
                "drift_acceptable": drift_acceptable,
                "aligned_to_anchor": aligned_to_anchor,
                "verdict": verdict
            }
        }
        
        self.gridded_events.append(gridded)
        return gridded


class DualAnchorProcessor:
    """Process events through dual-anchor celestial grid."""
    
    def __init__(self, events_file: str = "operational_events.json"):
        self.events_file = events_file
        self.grid = DualAnchorGrid()
    
    def load_events(self) -> List[Dict[str, Any]]:
        """Load events."""
        try:
            with open(self.events_file, 'r') as f:
                data = json.load(f)
                return data.get("events", [])
        except FileNotFoundError:
            print(f"[ERROR] {self.events_file} not found")
            return []
    
    def process(self):
        """Process all events."""
        events = self.load_events()
        if not events:
            print("[WARNING] No events")
            return
        
        print("[DUAL-ANCHOR GRID] Locking events to North Star + Southern Cross...")
        print("=" * 100)
        
        for event in events:
            gridded = self.grid.process_event(event)
            self._display_event(gridded)
        
        print("=" * 100)
        self._display_summary()
    
    def _display_event(self, gridded: Dict[str, Any]):
        """Display gridded event."""
        event_id = gridded["event_id"]
        grid_info = gridded["grid"]
        alignment = gridded["alignment"]
        validation = gridded["validation"]
        
        verdict_str = "[LOCKED]" if validation["verdict"] == "ACCEPT" else "[REJECTED]"
        primary = alignment["primary_anchor"]
        
        print(f"\n{verdict_str} {event_id} (Anchor: {primary})")
        print(f"  Grid Slot: {grid_info['slot']} / {grid_info['total_slots']}")
        print(f"  Compass Bearing: {grid_info['compass_bearing_degrees']}°")
        
        north = alignment["north_star"]
        south = alignment["southern_cross"]
        
        print(f"  Polaris (North Star):")
        print(f"    Reference Position: {north['reference_position']}°")
        print(f"    Distance: {north['distance_degrees']:.6f}°")
        print(f"    Aligned: {north['aligned']}")
        
        print(f"  Crux (Southern Cross):")
        print(f"    Reference Position: {south['reference_position']}°")
        print(f"    Distance: {south['distance_degrees']:.6f}°")
        print(f"    Aligned: {south['aligned']}")
        
        print(f"  Drift: {validation['reported_drift']:.4f}° (max allowed: {validation['max_allowed_drift']:.4f}°)")
        print(f"  Verdict: {validation['verdict']}")
    
    def _display_summary(self):
        """Display summary."""
        print("\n[DUAL-ANCHOR CELESTIAL GRID]")
        print(f"North Anchor: Polaris (North Star) at 0.0°")
        print(f"South Anchor: Crux (Southern Cross) at 180.0°")
        print(f"Precision: 0.05° (Pyramid standard)")
        print(f"Cycle: 86400 seconds (24 hours), 7200 slots")
        print(f"Tolerance: Earth wobble (nutation + precession + Chandler)")
        
        accepted = sum(1 for e in self.grid.gridded_events if e["validation"]["verdict"] == "ACCEPT")
        total = len(self.grid.gridded_events)
        
        north_anchored = sum(1 for e in self.grid.gridded_events if e["alignment"]["north_star"]["aligned"])
        south_anchored = sum(1 for e in self.grid.gridded_events if e["alignment"]["southern_cross"]["aligned"])
        
        print(f"\nResults: {accepted}/{total} events locked")
        print(f"  Anchored to North Star: {north_anchored}")
        print(f"  Anchored to Southern Cross: {south_anchored}")
    
    def save_results(self):
        """Save gridded events."""
        log_path = Path("./logs") / "dual_anchor_events.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            for gridded in self.grid.gridded_events:
                f.write(json.dumps(gridded) + "\n")
        
        print(f"\n[SAVED] {log_path}")


def main():
    """Execute dual-anchor grid processor."""
    processor = DualAnchorProcessor("operational_events.json")
    processor.process()
    processor.save_results()


if __name__ == "__main__":
    main()
