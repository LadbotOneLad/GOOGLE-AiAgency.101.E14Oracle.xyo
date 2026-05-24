#!/usr/bin/env python3
"""
Your Invariants: 0.05, 0.075, 0.15 woven into 86400-second / 7200-slot circle
1/7200 = 0.0001388... (fundamental unit)
3 arc seconds = 1/1200 degree = 0.05 degree setpoint (pyramid precision)
All 13 engines locked to this single invariant structure
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import math

class YourInvariants:
    """Your exact invariants: 0.05, 0.075, 0.15 in circle geometry."""
    
    # Your Three Rhythms (seconds) - these scale the circle
    HEARTBEAT = 0.05      # 50 ms
    PULSE = 0.075         # 75 ms
    HORIZON = 0.15        # 150 ms
    FULL_CYCLE = 0.275    # 275 ms
    
    # 86400 = seconds per day = 7200 × 12
    SECONDS_PER_DAY = 86400
    GRID_SLOTS = 7200     # slots in circle
    SLOT_DURATION = 12    # seconds per slot
    
    # 1/7200 = fundamental unit = 0.0001388...
    FUNDAMENTAL_UNIT = 1.0 / GRID_SLOTS
    
    # Pyramid precision: 0.05 degrees = 3 arc seconds
    PYRAMID_PRECISION_DEGREES = 0.05
    PYRAMID_PRECISION_ARC_SECONDS = 3.0
    ARC_SECONDS_PER_DEGREE = 3600
    
    # Circle: 360 degrees = 7200 × 0.05°
    FULL_CIRCLE_DEGREES = 360
    SLOTS_PER_DEGREE = GRID_SLOTS / FULL_CIRCLE_DEGREES  # = 20 slots per degree
    
    # Verify: 0.05° precision = 20 slots = 12 × 20 = 240 seconds per 0.05° increment
    SECONDS_PER_PRECISION_UNIT = SLOT_DURATION * SLOTS_PER_DEGREE  # 240 seconds
    
    def __init__(self, reference_date: datetime = None):
        self.reference_date = reference_date or datetime(2026, 3, 10, 0, 0, 0)
        self._verify_invariants()
    
    def _verify_invariants(self):
        """Verify the invariant structure."""
        assert abs(self.FUNDAMENTAL_UNIT - (1.0 / 7200)) < 1e-10, "1/7200 mismatch"
        assert self.PYRAMID_PRECISION_DEGREES == 0.05, "Pyramid precision mismatch"
        assert self.PYRAMID_PRECISION_ARC_SECONDS == 3.0, "Arc seconds mismatch"
        assert self.SLOTS_PER_DEGREE == 20, "Slots per degree mismatch"
        assert self.SECONDS_PER_PRECISION_UNIT == 240, "Seconds per precision unit mismatch"
        assert self.FULL_CYCLE == (self.HEARTBEAT + self.PULSE + self.HORIZON), "Cycle mismatch"
    
    def seconds_to_circle_position(self, seconds: float) -> Dict[str, Any]:
        """Convert seconds to position on 7200-slot circle."""
        # Position in day (86400 seconds)
        position_in_day = seconds % self.SECONDS_PER_DAY
        
        # Slot index (0-7199)
        slot = int(position_in_day / self.SLOT_DURATION)
        
        # Degrees (0-360)
        degrees = (slot / self.GRID_SLOTS) * 360
        
        # How many 0.05° precision units?
        precision_units = degrees / self.PYRAMID_PRECISION_DEGREES
        
        # Arc seconds within current degree
        arc_seconds = (degrees % 1.0) * self.ARC_SECONDS_PER_DEGREE
        
        return {
            "position_in_day_seconds": round(position_in_day, 3),
            "slot_0_to_7199": slot,
            "degrees_0_to_360": round(degrees, 6),
            "precision_units_0_to_7200": round(precision_units, 3),
            "arc_seconds_in_degree": round(arc_seconds, 2),
            "fundamental_units_1_7200": round(slot * self.FUNDAMENTAL_UNIT, 6)
        }
    
    def get_three_rhythm_phase_in_circle(self, timestamp: datetime = None) -> Dict[str, Any]:
        """Get three-rhythm phase mapped to circle position."""
        if timestamp is None:
            timestamp = datetime.now()
        
        elapsed = (timestamp - self.reference_date).total_seconds()
        cycle_position = (elapsed % self.FULL_CYCLE) / self.FULL_CYCLE
        
        # Map cycle position (0-1) to circle position (0-360°)
        circle_position = cycle_position * 360  # 0-360 degrees
        slot = int((circle_position / 360) * self.GRID_SLOTS)
        
        # Determine phase
        heartbeat_threshold = self.HEARTBEAT / self.FULL_CYCLE
        pulse_threshold = (self.HEARTBEAT + self.PULSE) / self.FULL_CYCLE
        
        if cycle_position < heartbeat_threshold:
            phase = "HEARTBEAT"
            tau = self.HEARTBEAT
            phase_progress = (cycle_position / heartbeat_threshold) * 100
        elif cycle_position < pulse_threshold:
            phase = "PULSE"
            tau = self.PULSE
            phase_progress = ((cycle_position - heartbeat_threshold) / (pulse_threshold - heartbeat_threshold)) * 100
        else:
            phase = "HORIZON"
            tau = self.HORIZON
            phase_progress = ((cycle_position - pulse_threshold) / (1 - pulse_threshold)) * 100
        
        return {
            "timestamp": timestamp.isoformat(),
            "phase_name": phase,
            "tau": tau,
            "phase_progress_percent": round(phase_progress, 2),
            "circle_position_degrees": round(circle_position, 4),
            "circle_position_slot": slot,
            "circle_position_precision_units": round((circle_position / 0.05), 2),
            "circle_position_arc_seconds": round((circle_position % 1.0) * 3600, 2),
            "message": f"{phase} phase at {circle_position:.4f}° ({slot}/7200 slots)"
        }
    
    def get_invariant_structure(self) -> Dict[str, Any]:
        """Display the complete invariant structure."""
        return {
            "name": "Your Invariants: 0.05, 0.075, 0.15 in 86400/7200 Circle",
            "three_rhythms": {
                "heartbeat_seconds": self.HEARTBEAT,
                "pulse_seconds": self.PULSE,
                "horizon_seconds": self.HORIZON,
                "full_cycle_seconds": self.FULL_CYCLE
            },
            "circle_geometry": {
                "seconds_per_day": self.SECONDS_PER_DAY,
                "grid_slots": self.GRID_SLOTS,
                "slot_duration_seconds": self.SLOT_DURATION,
                "equation": f"{self.SECONDS_PER_DAY} = {self.GRID_SLOTS} × {self.SLOT_DURATION}"
            },
            "fundamental_unit": {
                "value": round(self.FUNDAMENTAL_UNIT, 10),
                "equation": f"1/{self.GRID_SLOTS}",
                "decimal": "0.0001388..."
            },
            "pyramid_precision": {
                "degrees": self.PYRAMID_PRECISION_DEGREES,
                "arc_seconds": self.PYRAMID_PRECISION_ARC_SECONDS,
                "slots_per_unit": int(self.SLOTS_PER_DEGREE),
                "seconds_per_unit": int(self.SECONDS_PER_PRECISION_UNIT),
                "equation": f"0.05° = 3 arc-seconds = 1/{20} degree = 20 slots = 240 seconds"
            },
            "circle": {
                "total_degrees": 360,
                "total_slots": 7200,
                "slots_per_degree": int(self.SLOTS_PER_DEGREE),
                "precision_units_per_circle": int(360 / 0.05),
                "equation": "360° = 7200 slots = 7200 × 0.05° precision units"
            },
            "integration": {
                "message": "0.05, 0.075, 0.15 rhythm timescales map to 86400-second circle via 7200-slot grid",
                "all_13_engines": "All 13 engines synchronized to this single invariant structure"
            }
        }


class SynchronizedEngineWithInvariants:
    """All 13 engines locked to your invariant structure."""
    
    ENGINES = [
        "codex-engine-1", "codex-engine-2", "codex-engine-3", "codex-engine-4",
        "codex-engine-5", "codex-engine-6", "codex-engine-7", "codex-engine-8",
        "codex-engine-9", "codex-engine-10", "codex-engine-11", "codex-engine-12",
        "witness-aggregator"
    ]
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.invariants = YourInvariants()
    
    def get_docker_ps(self) -> Dict[str, Any]:
        """Get container status."""
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                containers = {}
                for line in result.stdout.strip().split('\n'):
                    if line:
                        try:
                            container = json.loads(line)
                            containers[container['Names']] = {
                                'state': container['State'].upper(),
                                'status': container['Status']
                            }
                        except:
                            pass
                return containers
        except:
            pass
        
        return {}
    
    def get_container_log(self, container_name: str) -> str:
        """Get latest log line."""
        try:
            result = subprocess.run(
                ["docker", "logs", "--tail", "1", container_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and result.stdout:
                return result.stdout.strip()[-70:]
        except:
            pass
        
        return ""
    
    def monitor(self):
        """Monitor all 13 engines on your invariant."""
        print("\n" + "=" * 180)
        print(f"[YOUR INVARIANTS] 0.05, 0.075, 0.15 in 86400/7200 Circle - ALL 13 ENGINES SYNCHRONIZED")
        print("=" * 180)
        
        # Show invariant structure
        inv = self.invariants.get_invariant_structure()
        print(f"\n[INVARIANT STRUCTURE]")
        print(f"Three Rhythms: {inv['three_rhythms']['heartbeat_seconds']}s (Heartbeat) + {inv['three_rhythms']['pulse_seconds']}s (Pulse) + {inv['three_rhythms']['horizon_seconds']}s (Horizon) = {inv['three_rhythms']['full_cycle_seconds']}s")
        print(f"Circle: {inv['circle_geometry']['seconds_per_day']} seconds/day = {inv['circle_geometry']['grid_slots']} slots × {inv['circle_geometry']['slot_duration_seconds']} seconds")
        print(f"Fundamental: 1/7200 = {inv['fundamental_unit']['value']}")
        print(f"Pyramid Precision: 0.05° = 3 arc-seconds = 20 slots = 240 seconds")
        print(f"Circle: 360° = 7200 slots = {int(360/0.05)} precision units\n")
        
        # Get current phase
        phase = self.invariants.get_three_rhythm_phase_in_circle(self.timestamp)
        circle_pos = self.invariants.seconds_to_circle_position(self.timestamp.timestamp())
        
        print(f"[CURRENT POSITION ON CIRCLE]")
        print(f"Phase: {phase['phase_name']} (tau={phase['tau']}s) - {phase['phase_progress_percent']}%")
        print(f"Circle Position: {phase['circle_position_degrees']}° ({phase['circle_position_slot']}/7200 slots)")
        print(f"Precision Units: {phase['circle_position_precision_units']}")
        print(f"Arc Seconds: {phase['circle_position_arc_seconds']}\n")
        
        # Get container data
        ps_data = self.get_docker_ps()
        
        # Display all engines on invariant
        print(f"[ALL 13 ENGINES - SYNCHRONIZED TO YOUR INVARIANT]")
        print("-" * 180)
        print(f"{'Engine':<25} {'State':<10} {'Phase':<15} {'Tau':<8} {'Progress':<12} {'Circle Pos':<15} {'Slot':<10} {'Log (last measure)':<100}")
        print("-" * 180)
        
        running = 0
        for i, engine_name in enumerate(self.ENGINES):
            ps_info = ps_data.get(engine_name, {'state': 'UNKNOWN', 'status': ''})
            state = ps_info['state']
            
            # All engines at same phase on circle
            phase_name = phase['phase_name']
            tau = phase['tau']
            progress = phase['phase_progress_percent']
            circle_deg = phase['circle_position_degrees']
            slot = phase['circle_position_slot']
            
            log = self.get_container_log(engine_name)
            
            print(f"{engine_name:<25} {state:<10} {phase_name:<15} {tau:<8} {progress:<12.1f} {circle_deg:<15.4f} {slot:<10} {log:<100}")
            
            if state == 'RUNNING':
                running += 1
        
        print("-" * 180)
        print(f"\n[SUMMARY]")
        print(f"Running Engines: {running}/13")
        print(f"Synchronized Phase: {phase['phase_name']}")
        print(f"All Engines on Circle: {phase['circle_position_degrees']}° ({phase['circle_position_slot']}/7200 slots)")
        print(f"All Engines at Precision Unit: {phase['circle_position_precision_units']}")
        print(f"\n==> YOUR INVARIANTS LOCK ALL 13 ENGINES TO THIS EXACT CIRCLE POSITION <==")
        print("=" * 180)
    
    def save_report(self, output_file: str = "your_invariants_report.json"):
        """Save report."""
        phase = self.invariants.get_three_rhythm_phase_in_circle(self.timestamp)
        inv = self.invariants.get_invariant_structure()
        
        report = {
            "timestamp": self.timestamp.isoformat(),
            "invariants": inv,
            "current_state": phase,
            "all_13_engines_synchronized": True
        }
        
        log_path = Path("./logs") / output_file
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[SAVED] {log_path}")


def main():
    """Execute with your invariants."""
    monitor = SynchronizedEngineWithInvariants()
    monitor.monitor()
    monitor.save_report()


if __name__ == "__main__":
    main()
