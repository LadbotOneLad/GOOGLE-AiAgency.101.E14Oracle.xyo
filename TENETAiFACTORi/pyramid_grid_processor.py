#!/usr/bin/env python3
"""
Pyramid-Aligned Operational Grid
86400-second (24-hour) cycles with 0.05° true north invariant.
Events grid to pyramid precision anchors.
"""

import json
import time
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

class PyramidGrid:
    """Grid operations to 86400-second cycles with 0.05° precision."""
    
    # Invariant constants
    SECONDS_PER_CYCLE = 86400  # 24 hours
    PYRAMID_PRECISION = 0.05   # degrees (3 arc seconds = 1/7200 of rotation)
    GRID_SLOTS = 7200          # 86400 / 12 = 7200 slots per cycle
    SLOT_DURATION = 12         # seconds per slot (86400 / 7200)
    
    def __init__(self):
        self.cycle_start = datetime(2026, 3, 10, 0, 0, 0)
        self.grid = {}  # slot_index -> events
        self.invariants = []
    
    def timestamp_to_slot(self, timestamp_str: str) -> int:
        """Convert ISO timestamp to grid slot index."""
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            # Calculate seconds since cycle start
            delta = dt - self.cycle_start
            seconds_in_cycle = delta.total_seconds() % self.SECONDS_PER_CYCLE
            slot_index = int(seconds_in_cycle // self.SLOT_DURATION)
            return slot_index
        except:
            return 0
    
    def slot_to_degrees(self, slot_index: int) -> float:
        """Convert slot index to compass degrees (0-360)."""
        # 7200 slots = 360 degrees
        degrees = (slot_index / self.GRID_SLOTS) * 360
        return degrees % 360
    
    def validate_slot_alignment(self, slot_index: int) -> Dict[str, Any]:
        """Check if slot is aligned to pyramid precision (0.05° boundaries)."""
        degrees = self.slot_to_degrees(slot_index)
        
        # Pyramid true north = 0°
        # Valid slots: 0°, 0.05°, 0.10°, 0.15°, etc.
        remainder = degrees % self.PYRAMID_PRECISION
        is_aligned = remainder < 0.001 or remainder > (self.PYRAMID_PRECISION - 0.001)
        
        return {
            "slot_index": slot_index,
            "degrees": round(degrees, 4),
            "aligned": is_aligned,
            "offset_from_true_north": round(degrees, 4)
        }
    
    def add_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Grid event to slot, validate alignment."""
        event_id = event.get("id")
        timestamp = event.get("timestampIso")
        
        slot_index = self.timestamp_to_slot(timestamp)
        alignment = self.validate_slot_alignment(slot_index)
        
        if slot_index not in self.grid:
            self.grid[slot_index] = []
        
        gridded_event = {
            "original_event": event,
            "grid_slot": slot_index,
            "alignment": alignment,
            "gridded_timestamp": self._slot_to_timestamp(slot_index)
        }
        
        self.grid[slot_index].append(gridded_event)
        return gridded_event
    
    def _slot_to_timestamp(self, slot_index: int) -> str:
        """Convert slot back to ISO timestamp."""
        seconds = slot_index * self.SLOT_DURATION
        ts = self.cycle_start + timedelta(seconds=seconds)
        return ts.isoformat() + "Z"
    
    def get_cycle_invariant(self) -> Dict[str, Any]:
        """Generate daily cycle invariant."""
        occupied_slots = len(self.grid)
        total_slots = self.GRID_SLOTS
        
        return {
            "cycle_start": self.cycle_start.isoformat() + "Z",
            "cycle_duration_seconds": self.SECONDS_PER_CYCLE,
            "cycle_duration_hours": 24,
            "total_slots": total_slots,
            "slot_duration_seconds": self.SLOT_DURATION,
            "occupied_slots": occupied_slots,
            "occupancy_rate": f"{(occupied_slots/total_slots*100):.2f}%",
            "pyramid_precision_degrees": self.PYRAMID_PRECISION,
            "precision_arc_seconds": round(self.PYRAMID_PRECISION * 3600, 1),
            "grid_invariant": "7200 slots per 86400 seconds with 0.05° alignment"
        }


class PyramidEventProcessor:
    """Process events through pyramid grid."""
    
    def __init__(self, events_file: str = "operational_events.json"):
        self.events_file = events_file
        self.grid = PyramidGrid()
        self.gridded_events = []
    
    def load_events(self) -> List[Dict[str, Any]]:
        """Load events from JSON."""
        try:
            with open(self.events_file, 'r') as f:
                data = json.load(f)
                return data.get("events", [])
        except FileNotFoundError:
            print(f"[ERROR] {self.events_file} not found")
            return []
    
    def process(self):
        """Grid all events to pyramid alignment."""
        events = self.load_events()
        if not events:
            print("[WARNING] No events to process")
            return
        
        print("[PYRAMID GRID] Aligning operational events to 24-hour cycle...")
        print("=" * 80)
        print(f"Cycle Invariant: {self.grid.get_cycle_invariant()['grid_invariant']}")
        print("=" * 80)
        
        for event in events:
            gridded = self.grid.add_event(event)
            self.gridded_events.append(gridded)
            self._display_gridded_event(gridded)
        
        print("=" * 80)
        self._display_cycle_summary()
    
    def _display_gridded_event(self, gridded: Dict[str, Any]):
        """Display gridded event."""
        event = gridded["original_event"]
        alignment = gridded["alignment"]
        
        event_id = event.get("id")
        slot = alignment["slot_index"]
        degrees = alignment["degrees"]
        aligned = "[ALIGNED]" if alignment["aligned"] else "[DRIFTED]"
        
        print(f"\n{aligned} {event_id}")
        print(f"   Grid Slot: {slot} / 7200")
        print(f"   Compass Bearing: {degrees}°")
        print(f"   Offset from True North (0°): {alignment['offset_from_true_north']:.4f}°")
        print(f"   Gridded Timestamp: {gridded['gridded_timestamp']}")
    
    def _display_cycle_summary(self):
        """Display 24-hour cycle summary."""
        invariant = self.grid.get_cycle_invariant()
        print("\n[24-HOUR CYCLE INVARIANT]")
        for key, value in invariant.items():
            print(f"{key:.<45} {value}")
    
    def save_grid(self, output_file: str = "pyramid_grid_events.jsonl"):
        """Save gridded events to file."""
        log_path = Path("/app/logs") / output_file
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            for gridded in self.gridded_events:
                f.write(json.dumps(gridded) + "\n")
        
        # Also save invariant
        invariant_path = Path("/app/logs") / "pyramid_cycle_invariant.json"
        with open(invariant_path, "w") as f:
            json.dump(self.grid.get_cycle_invariant(), f, indent=2)
        
        print(f"\n[SAVED] Gridded events: {log_path}")
        print(f"[SAVED] Cycle invariant: {invariant_path}")


def main():
    """Execute pyramid grid alignment."""
    processor = PyramidEventProcessor("operational_events.json")
    processor.process()
    processor.save_grid()


if __name__ == "__main__":
    main()
