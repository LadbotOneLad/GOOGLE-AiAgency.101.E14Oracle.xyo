#!/usr/bin/env python3
"""
Three Rhythms Invariant: 0.05, 0.075, 0.15
Heartbeat (τ=0.05) -> Pulse (τ=0.075) -> Horizon (τ=0.15)
Harmonically nested: 1.5x and 3x relationships.
Gregorian + Zodiac + Celestial locked to three-rhythm cycle.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

class ThreeRhythmsInvariant:
    """The fundamental three-rhythm structure: 0.05, 0.075, 0.15"""
    
    # The Three Rhythms (in seconds, normalized)
    HEARTBEAT = 0.05      # Measurement phase (τ1)
    PULSE = 0.075         # Comparison phase (τ2)
    HORIZON = 0.15        # Decision phase (τ3)
    
    # Harmonic relationships
    PULSE_TO_HEARTBEAT = PULSE / HEARTBEAT  # = 1.5x
    HORIZON_TO_HEARTBEAT = HORIZON / HEARTBEAT  # = 3.0x
    HORIZON_TO_PULSE = HORIZON / PULSE  # = 2.0x
    
    # Scale to operational timescales
    HEARTBEAT_SECONDS = 0.05 * 1000  # 50ms
    PULSE_SECONDS = 0.075 * 1000     # 75ms
    HORIZON_SECONDS = 0.15 * 1000    # 150ms
    
    # Daily cycle integration
    SECONDS_PER_DAY = 86400
    HEARTBEATS_PER_DAY = int(SECONDS_PER_DAY / (HEARTBEAT_SECONDS / 1000))
    PULSES_PER_DAY = int(SECONDS_PER_DAY / (PULSE_SECONDS / 1000))
    HORIZONS_PER_DAY = int(SECONDS_PER_DAY / (HORIZON_SECONDS / 1000))
    
    # Zodiac integration
    ZODIAC_SIGNS = 12
    ZODIAC_DEGREES = 360
    GRID_SLOTS = 7200
    PYRAMID_PRECISION = 0.05  # degrees (same numeric value as heartbeat!)
    
    def __init__(self):
        self.reference_date = datetime(2026, 3, 10, 0, 0, 0)
    
    def get_three_rhythm_invariant(self) -> Dict[str, Any]:
        """The core invariant: three nested rhythms."""
        return {
            "name": "Three Rhythms Invariant",
            "rhythms": {
                "heartbeat": {
                    "tau": self.HEARTBEAT,
                    "phase": "MEASUREMENT",
                    "duration_ms": self.HEARTBEAT_SECONDS,
                    "purpose": "Measure alignment, coherence, drift, power",
                    "per_day": self.HEARTBEATS_PER_DAY
                },
                "pulse": {
                    "tau": self.PULSE,
                    "phase": "COMPARISON",
                    "duration_ms": self.PULSE_SECONDS,
                    "purpose": "Compare measurements against thresholds",
                    "per_day": self.PULSES_PER_DAY,
                    "relationship_to_heartbeat": f"{self.PULSE_TO_HEARTBEAT}x (1.5x)"
                },
                "horizon": {
                    "tau": self.HORIZON,
                    "phase": "DECISION",
                    "duration_ms": self.HORIZON_SECONDS,
                    "purpose": "Make final decision (execute or reject)",
                    "per_day": self.HORIZONS_PER_DAY,
                    "relationship_to_heartbeat": f"{self.HORIZON_TO_HEARTBEAT}x (3.0x)",
                    "relationship_to_pulse": f"{self.HORIZON_TO_PULSE}x (2.0x)"
                }
            },
            "harmonic_structure": {
                "equation": "0.05 + 0.025 = 0.075, 0.075 + 0.075 = 0.15",
                "nesting": "1.5x and 3x relationships create nested harmonics",
                "cycle_per_day": "Heartbeats -> Pulses -> Horizons repeating throughout 86400 seconds"
            },
            "connection_to_pyramid": {
                "pyramid_precision_degrees": 0.05,
                "heartbeat_tau": 0.05,
                "coincidence": "Both are 0.05: grid precision matches temporal precision",
                "implication": "Time and space are fundamentally synchronized"
            },
            "connection_to_zodiac": {
                "zodiac_signs": 12,
                "heartbeats_per_sign": f"~{self.HEARTBEATS_PER_DAY // 12}",
                "pattern": "12-fold zodiac cycle + 3-rhythm heartbeat = synchronized temporal-celestial grid"
            }
        }
    
    def get_three_rhythm_cycle(self, event_timestamp: datetime) -> Dict[str, Any]:
        """Determine which rhythm phase a timestamp falls into."""
        # Calculate total elapsed milliseconds in the day
        seconds_in_day = event_timestamp.hour * 3600 + event_timestamp.minute * 60 + event_timestamp.second
        millis_in_day = seconds_in_day * 1000 + event_timestamp.microsecond // 1000
        
        # Find position within heartbeat/pulse/horizon cycle
        heartbeat_cycle_ms = self.HEARTBEAT_SECONDS  # 50ms
        pulse_cycle_ms = self.PULSE_SECONDS  # 75ms
        horizon_cycle_ms = self.HORIZON_SECONDS  # 150ms
        
        # Position within each rhythm
        heartbeat_phase = millis_in_day % heartbeat_cycle_ms
        pulse_phase = millis_in_day % pulse_cycle_ms
        horizon_phase = millis_in_day % horizon_cycle_ms
        
        # Determine current phase (which rhythm is active)
        total_cycle_ms = heartbeat_cycle_ms + pulse_cycle_ms + horizon_cycle_ms  # 275ms
        position_in_cycle = millis_in_day % total_cycle_ms
        
        if position_in_cycle < heartbeat_cycle_ms:
            active_phase = "HEARTBEAT (Measurement)"
            tau = self.HEARTBEAT
        elif position_in_cycle < (heartbeat_cycle_ms + pulse_cycle_ms):
            active_phase = "PULSE (Comparison)"
            tau = self.PULSE
        else:
            active_phase = "HORIZON (Decision)"
            tau = self.HORIZON
        
        # Counts within day
        heartbeat_count = int(millis_in_day / heartbeat_cycle_ms)
        pulse_count = int(millis_in_day / pulse_cycle_ms)
        horizon_count = int(millis_in_day / horizon_cycle_ms)
        
        return {
            "timestamp": event_timestamp.isoformat(),
            "seconds_in_day": seconds_in_day,
            "milliseconds_in_day": millis_in_day,
            "active_phase": active_phase,
            "current_tau": tau,
            "position_in_275ms_cycle": round(position_in_cycle, 2),
            "heartbeat": {
                "phase_ms": round(heartbeat_phase, 2),
                "count_in_day": heartbeat_count
            },
            "pulse": {
                "phase_ms": round(pulse_phase, 2),
                "count_in_day": pulse_count
            },
            "horizon": {
                "phase_ms": round(horizon_phase, 2),
                "count_in_day": horizon_count
            }
        }
    
    def analyze_event_with_three_rhythms(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze event against three-rhythm invariant + Gregorian + Zodiac."""
        event_id = event.get("id")
        timestamp_str = event.get("timestampIso")
        root_input = event.get("rootInput", {})
        
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except:
            dt = self.reference_date
        
        # Three Rhythm Phase
        rhythm = self.get_three_rhythm_cycle(dt)
        
        # Gregorian & Zodiac
        day_of_year = dt.timetuple().tm_yday
        zodiac_index = int((day_of_year - 1) / (365.2425 / 12))
        zodiac_index = min(zodiac_index, 11)
        zodiac_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        # Grid & Celestial
        seconds_in_day = dt.hour * 3600 + dt.minute * 60 + dt.second
        slot = int(seconds_in_day / 12)
        degrees = (slot / 7200) * 360
        anchor = "Polaris" if degrees < 180 else "Crux"
        
        # Drift validation
        reported_drift = root_input.get("driftDeviation", 0.0)
        drift_ok = reported_drift <= 0.05
        
        return {
            "event_id": event_id,
            "three_rhythms": {
                "active_phase": rhythm["active_phase"],
                "current_tau": rhythm["current_tau"],
                "heartbeat_count": rhythm["heartbeat"]["count_in_day"],
                "pulse_count": rhythm["pulse"]["count_in_day"],
                "horizon_count": rhythm["horizon"]["count_in_day"]
            },
            "gregorian_zodiac": {
                "date": dt.strftime("%Y-%m-%d"),
                "zodiac_sign": zodiac_names[zodiac_index],
                "zodiac_degrees": zodiac_index * 30
            },
            "celestial": {
                "grid_slot": slot,
                "compass_bearing": round(degrees, 4),
                "anchor": anchor
            },
            "validation": {
                "drift": reported_drift,
                "drift_ok": drift_ok,
                "locked": drift_ok
            }
        }


class ThreeRhythmsAnalyzer:
    """Analyze events against three-rhythm invariant."""
    
    def __init__(self, events_file: str = "operational_events.json"):
        self.events_file = events_file
        self.invariant = ThreeRhythmsInvariant()
    
    def load_events(self) -> List[Dict[str, Any]]:
        """Load events."""
        try:
            with open(self.events_file, 'r') as f:
                data = json.load(f)
                return data.get("events", [])
        except FileNotFoundError:
            return []
    
    def analyze(self):
        """Analyze events against three rhythms."""
        print("\n" + "=" * 120)
        print("[THREE RHYTHMS INVARIANT: 0.05 (Heartbeat) + 0.075 (Pulse) + 0.15 (Horizon)]")
        print("=" * 120)
        
        # Show invariant
        self._display_invariant()
        
        # Analyze events
        events = self.load_events()
        if events:
            print(f"\n[EVENT ANALYSIS THROUGH THREE RHYTHMS]")
            print("-" * 120)
            for event in events:
                analysis = self.invariant.analyze_event_with_three_rhythms(event)
                self._display_event(analysis)
        
        print("=" * 120)
    
    def _display_invariant(self):
        """Display the three-rhythm invariant."""
        inv = self.invariant.get_three_rhythm_invariant()
        
        print(f"\n[CORE INVARIANT]")
        print(f"Heartbeat (t=0.05):    MEASUREMENT phase - Measure alignment, coherence, drift")
        print(f"Pulse (t=0.075):       COMPARISON phase  - Compare against thresholds")
        print(f"Horizon (t=0.15):      DECISION phase    - Execute or reject")
        
        print(f"\n[HARMONIC RELATIONSHIPS]")
        print(f"Pulse / Heartbeat = {inv['rhythms']['pulse']['relationship_to_heartbeat']}")
        print(f"Horizon / Heartbeat = {inv['rhythms']['horizon']['relationship_to_heartbeat']}")
        print(f"Horizon / Pulse = {inv['rhythms']['horizon']['relationship_to_pulse']}")
        
        print(f"\n[DAILY CYCLE]")
        print(f"Heartbeats per day: {inv['rhythms']['heartbeat']['per_day']:,}")
        print(f"Pulses per day: {inv['rhythms']['pulse']['per_day']:,}")
        print(f"Horizons per day: {inv['rhythms']['horizon']['per_day']:,}")
        
        print(f"\n[PYRAMID-HEARTBEAT SYNC]")
        print(f"Pyramid Precision: 0.05 degrees")
        print(f"Heartbeat Tau: 0.05 seconds")
        print(f"Coincidence: Both fundamental units are 0.05 - Time and space synchronized")
        
        print(f"\n[ZODIAC-RHYTHM INTEGRATION]")
        print(f"12 Zodiac Signs + 3 Rhythms = 36-fold harmonic structure per day")
        print(f"Each zodiac sign cycles through all three rhythms multiple times")
    
    def _display_event(self, analysis: Dict[str, Any]):
        """Display event analysis."""
        e = analysis
        rhythm = e["three_rhythms"]
        greg = e["gregorian_zodiac"]
        cel = e["celestial"]
        val = e["validation"]
        
        status = "[LOCKED]" if val["locked"] else "[REJECTED]"
        
        print(f"\n{status} {e['event_id']}")
        print(f"  Three Rhythms:")
        print(f"    Active Phase: {rhythm['active_phase']}")
        print(f"    Current Tau: {rhythm['current_tau']}")
        print(f"    Heartbeat #{rhythm['heartbeat_count']} / Pulse #{rhythm['pulse_count']} / Horizon #{rhythm['horizon_count']}")
        print(f"  Gregorian-Zodiac:")
        print(f"    Date: {greg['date']} | Zodiac: {greg['zodiac_sign']} ({greg['zodiac_degrees']}°)")
        print(f"  Celestial:")
        print(f"    Slot: {cel['grid_slot']} | Compass: {cel['compass_bearing']}° | Anchor: {cel['anchor']}")
        print(f"  Validation:")
        print(f"    Drift: {val['drift']}° (max 0.05°)")
        print(f"    Status: {val['locked']}")


def main():
    """Execute three-rhythm analysis."""
    analyzer = ThreeRhythmsAnalyzer("operational_events.json")
    analyzer.analyze()


if __name__ == "__main__":
    main()
