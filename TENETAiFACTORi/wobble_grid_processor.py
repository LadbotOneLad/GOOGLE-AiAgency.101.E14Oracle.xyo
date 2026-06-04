#!/usr/bin/env python3
"""
Pyramid Grid with Earth's Axial Wobble Tolerance
86400-second cycles with true north setpoint locked to Earth's natural motion.
"""

import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

class EarthWobble:
    """Model Earth's axial wobble as tolerance band around true north (0°)."""
    
    TRUE_NORTH_SETPOINT = 0.0
    PYRAMID_PRECISION = 0.05  # degrees
    
    # Wobble components (degrees)
    NUTATION_AMPLITUDE = 9.2 / 3600
    PRECESSION_RATE = 50.3 / 3600
    CHANDLER_WOBBLE_AMPLITUDE = 0.5 / 3600
    CHANDLER_WOBBLE_PERIOD = 433  # days
    
    def __init__(self, reference_date: datetime = None):
        self.reference_date = reference_date or datetime(2026, 3, 10, 0, 0, 0)
    
    def get_wobble_at_time(self, timestamp: datetime) -> Dict[str, float]:
        """Calculate total wobble at given time."""
        if timestamp.tzinfo is not None:
            timestamp = timestamp.replace(tzinfo=None)
        
        days_since_ref = (timestamp - self.reference_date).days
        
        # Nutation: 18.6-year cycle
        nutation_phase = (days_since_ref / 6793) * 2 * math.pi
        nutation = self.NUTATION_AMPLITUDE * math.sin(nutation_phase)
        
        # Precession: slow drift
        precession = (self.PRECESSION_RATE / 365.25) * days_since_ref
        
        # Chandler wobble: 433-day oscillation
        chandler_phase = (days_since_ref / self.CHANDLER_WOBBLE_PERIOD) * 2 * math.pi
        chandler = self.CHANDLER_WOBBLE_AMPLITUDE * math.sin(chandler_phase)
        
        total_wobble = nutation + precession + chandler
        
        return {
            "timestamp": timestamp.isoformat() + "Z",
            "days_since_reference": days_since_ref,
            "nutation_degrees": round(nutation, 6),
            "precession_degrees": round(precession, 6),
            "chandler_wobble_degrees": round(chandler, 6),
            "total_wobble_degrees": round(total_wobble, 6),
            "tolerance_band_min": round(self.TRUE_NORTH_SETPOINT - abs(total_wobble), 6),
            "tolerance_band_max": round(self.TRUE_NORTH_SETPOINT + abs(total_wobble), 6)
        }


class PyramidGridWobble:
    """Grid operations to 86400-second cycles with wobble tolerance."""
    
    SECONDS_PER_CYCLE = 86400
    GRID_SLOTS = 7200
    SLOT_DURATION = 12
    
    def __init__(self):
        self.cycle_start = datetime(2026, 3, 10, 0, 0, 0)
        self.wobble = EarthWobble(self.cycle_start)
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
        """Convert slot to compass bearing."""
        degrees = (slot_index / self.GRID_SLOTS) * 360
        return degrees % 360
    
    def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Grid event and validate against wobble tolerance."""
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
        
        # Get wobble at this time
        wobble = self.wobble.get_wobble_at_time(dt)
        
        # Check if within wobble band
        min_bound = wobble["tolerance_band_min"]
        max_bound = wobble["tolerance_band_max"]
        within_band = min_bound <= measured_degrees <= max_bound
        
        # Verify drift against wobble (allow up to pyramid precision as minimum)
        reported_drift = root_input.get("driftDeviation", 0.0)
        wobble_magnitude = abs(wobble["total_wobble_degrees"])
        max_allowed_drift = max(wobble_magnitude, 0.05)
        drift_acceptable = reported_drift <= max_allowed_drift
        
        # Verdict: both conditions must pass
        verdict = "ACCEPT" if (within_band and drift_acceptable) else "REJECT"
        
        gridded = {
            "event_id": event_id,
            "original_event": event,
            "grid": {
                "slot": slot_index,
                "total_slots": self.GRID_SLOTS,
                "compass_bearing_degrees": round(measured_degrees, 4)
            },
            "wobble": wobble,
            "validation": {
                "within_wobble_band": within_band,
                "reported_drift": reported_drift,
                "wobble_magnitude": round(wobble_magnitude, 6),
                "max_allowed_drift": round(max_allowed_drift, 6),
                "drift_acceptable": drift_acceptable,
                "verdict": verdict
            }
        }
        
        self.gridded_events.append(gridded)
        return gridded


class WobbleAwareProcessor:
    """Process events through wobble-aware grid."""
    
    def __init__(self, events_file: str = "operational_events.json"):
        self.events_file = events_file
        self.grid = PyramidGridWobble()
    
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
        
        print("[WOBBLE-AWARE GRID] Locking events to true north with Earth wobble tolerance...")
        print("=" * 90)
        
        for event in events:
            gridded = self.grid.process_event(event)
            self._display_event(gridded)
        
        print("=" * 90)
        self._display_summary()
    
    def _display_event(self, gridded: Dict[str, Any]):
        """Display gridded event."""
        event_id = gridded["event_id"]
        grid_info = gridded["grid"]
        wobble = gridded["wobble"]
        validation = gridded["validation"]
        
        verdict_str = "[LOCKED]" if validation["verdict"] == "ACCEPT" else "[REJECTED]"
        
        print(f"\n{verdict_str} {event_id}")
        print(f"  Grid Slot: {grid_info['slot']} / {grid_info['total_slots']}")
        print(f"  Compass Bearing: {grid_info['compass_bearing_degrees']}°")
        print(f"  Earth Wobble Components:")
        print(f"    Nutation:     {wobble['nutation_degrees']:.6f}°")
        print(f"    Precession:   {wobble['precession_degrees']:.6f}°")
        print(f"    Chandler:     {wobble['chandler_wobble_degrees']:.6f}°")
        print(f"    Total Wobble: {wobble['total_wobble_degrees']:.6f}°")
        print(f"  Tolerance Band: [{wobble['tolerance_band_min']:.6f}° to {wobble['tolerance_band_max']:.6f}°]")
        print(f"  Reported Drift: {validation['reported_drift']:.4f}°")
        print(f"  Max Allowed Drift: {validation['max_allowed_drift']:.6f}°")
        print(f"  Drift Acceptable: {validation['drift_acceptable']}")
        print(f"  Verdict: {validation['verdict']}")
    
    def _display_summary(self):
        """Display summary."""
        print("\n[24-HOUR CYCLE INVARIANT]")
        print(f"True North Setpoint: 0.0°")
        print(f"Pyramid Precision: 0.05°")
        print(f"Tolerance: Earth's natural wobble (nutation + precession + Chandler)")
        print(f"Cycle Duration: 86400 seconds (24 hours)")
        print(f"Grid Slots: 7200 (each 12 seconds)")
        
        accepted = sum(1 for e in self.grid.gridded_events if e["validation"]["verdict"] == "ACCEPT")
        total = len(self.grid.gridded_events)
        print(f"\nResults: {accepted}/{total} events locked within wobble tolerance")
    
    def save_results(self):
        """Save gridded events."""
        log_path = Path("./logs") / "wobble_locked_events.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            for gridded in self.grid.gridded_events:
                f.write(json.dumps(gridded) + "\n")
        
        print(f"\n[SAVED] {log_path}")


def main():
    """Execute wobble-aware grid processor."""
    processor = WobbleAwareProcessor("operational_events.json")
    processor.process()
    processor.save_results()


if __name__ == "__main__":
    main()
