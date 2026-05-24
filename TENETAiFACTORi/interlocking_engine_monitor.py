#!/usr/bin/env python3
"""
Engine Health Monitor: Interlocking Three-Rhythm Cycles with 176-Day Lock
Every engine locked to heartbeat/pulse/horizon, interlocking across all 13 engines
176-day Gregorian-Zodiac synchronization cycle
"""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

class InterlockingThreeRhythms:
    """Model interlocking cycles: heartbeat/pulse/horizon across 13 engines."""
    
    # Three Rhythms (fundamental timescale in seconds)
    HEARTBEAT = 0.05
    PULSE = 0.075
    HORIZON = 0.15
    
    # Full cycle
    FULL_CYCLE = HEARTBEAT + PULSE + HORIZON  # 0.275 seconds
    
    # 13 engines interlocking (offset by cycle phase)
    NUM_ENGINES = 13
    ENGINE_PHASE_OFFSET = FULL_CYCLE / NUM_ENGINES  # Each engine offset by 1/13 of cycle
    
    # 176-day lock (Gregorian-Zodiac synchronization)
    GREGORIAN_YEAR = 365.2425
    ZODIAC_CYCLE = 360  # degrees
    LOCK_DAYS = 176  # Half-year lock (approximately 6 months)
    LOCK_CYCLES_PER_YEAR = GREGORIAN_YEAR / LOCK_DAYS  # ~2.07 cycles
    
    def __init__(self, reference_date: datetime = None):
        self.reference_date = reference_date or datetime(2026, 3, 10, 0, 0, 0)
    
    def get_system_time_phase(self, timestamp: datetime = None) -> Dict[str, Any]:
        """Get current position in three-rhythm cycle (0-1)."""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Convert to seconds since reference, mod into full cycle
        elapsed = (timestamp - self.reference_date).total_seconds()
        cycle_position = (elapsed % self.FULL_CYCLE) / self.FULL_CYCLE
        
        # Determine which phase
        heartbeat_threshold = self.HEARTBEAT / self.FULL_CYCLE
        pulse_threshold = (self.HEARTBEAT + self.PULSE) / self.FULL_CYCLE
        
        if cycle_position < heartbeat_threshold:
            phase_name = "HEARTBEAT"
            tau = self.HEARTBEAT
            phase_percent = (cycle_position / heartbeat_threshold) * 100
        elif cycle_position < pulse_threshold:
            phase_name = "PULSE"
            tau = self.PULSE
            phase_percent = ((cycle_position - heartbeat_threshold) / (pulse_threshold - heartbeat_threshold)) * 100
        else:
            phase_name = "HORIZON"
            tau = self.HORIZON
            phase_percent = ((cycle_position - pulse_threshold) / (1 - pulse_threshold)) * 100
        
        return {
            "timestamp": timestamp.isoformat(),
            "cycle_position_0_to_1": round(cycle_position, 6),
            "phase_name": phase_name,
            "tau": tau,
            "phase_progress_percent": round(phase_percent, 2),
            "elapsed_seconds_mod_cycle": round(elapsed % self.FULL_CYCLE, 6)
        }
    
    def get_engine_phase(self, engine_index: int, timestamp: datetime = None) -> Dict[str, Any]:
        """Get phase for specific engine (0-12)."""
        if timestamp is None:
            timestamp = datetime.now()
        
        system_phase = self.get_system_time_phase(timestamp)
        cycle_position = system_phase["cycle_position_0_to_1"]
        
        # Apply engine-specific offset (each engine leads/lags by 1/13 of full cycle)
        engine_offset = (engine_index / self.NUM_ENGINES)
        engine_phase = (cycle_position + engine_offset) % 1.0
        
        # Determine engine's current phase
        heartbeat_threshold = self.HEARTBEAT / self.FULL_CYCLE
        pulse_threshold = (self.HEARTBEAT + self.PULSE) / self.FULL_CYCLE
        
        if engine_phase < heartbeat_threshold:
            phase_name = "HEARTBEAT"
            tau = self.HEARTBEAT
            phase_progress = (engine_phase / heartbeat_threshold) * 100
        elif engine_phase < pulse_threshold:
            phase_name = "PULSE"
            tau = self.PULSE
            phase_progress = ((engine_phase - heartbeat_threshold) / (pulse_threshold - heartbeat_threshold)) * 100
        else:
            phase_name = "HORIZON"
            tau = self.HORIZON
            phase_progress = ((engine_phase - pulse_threshold) / (1 - pulse_threshold)) * 100
        
        return {
            "engine_index": engine_index,
            "engine_name": f"codex-engine-{engine_index+1}" if engine_index < 12 else "witness-aggregator",
            "engine_offset": round(engine_offset, 6),
            "engine_phase_position_0_to_1": round(engine_phase, 6),
            "phase_name": phase_name,
            "tau": tau,
            "phase_progress_percent": round(phase_progress, 2),
            "leads_system_by_milliseconds": round(engine_offset * self.FULL_CYCLE * 1000, 2)
        }
    
    def get_176day_lock_state(self, timestamp: datetime = None) -> Dict[str, Any]:
        """Get current 176-day Gregorian-Zodiac lock state."""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Days since reference
        days_elapsed = (timestamp - self.reference_date).days
        
        # Which 176-day lock cycle?
        lock_cycle_num = int(days_elapsed / self.LOCK_DAYS)
        days_in_current_lock = days_elapsed % self.LOCK_DAYS
        
        # Zodiac position (0-360 degrees)
        zodiac_position = (days_in_current_lock / self.LOCK_DAYS) * 180  # 176 days = half zodiac (180 deg)
        
        # Which zodiac sign?
        sign_index = int(zodiac_position / 30)
        zodiac_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        zodiac_sign = zodiac_signs[sign_index % 12]
        
        return {
            "days_elapsed_since_reference": days_elapsed,
            "lock_cycle_number": lock_cycle_num,
            "days_in_current_176day_lock": days_in_current_lock,
            "lock_duration_days": self.LOCK_DAYS,
            "lock_progress_percent": round((days_in_current_lock / self.LOCK_DAYS) * 100, 2),
            "zodiac_position_degrees": round(zodiac_position, 2),
            "zodiac_sign": zodiac_sign,
            "zodiac_degrees_in_sign": round(zodiac_position % 30, 2),
            "next_lock_transition_in_days": self.LOCK_DAYS - days_in_current_lock
        }


class InterlockingEngineHealthMonitor:
    """Monitor all 13 engines with interlocking three-rhythm cycles + 176-day lock."""
    
    ENGINES = [
        "codex-engine-1", "codex-engine-2", "codex-engine-3", "codex-engine-4",
        "codex-engine-5", "codex-engine-6", "codex-engine-7", "codex-engine-8",
        "codex-engine-9", "codex-engine-10", "codex-engine-11", "codex-engine-12",
        "witness-aggregator"
    ]
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.rhythms = InterlockingThreeRhythms()
    
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
                            name = container.get('Names', '')
                            containers[name] = {
                                'state': container.get('State', ''),
                                'status': container.get('Status', '')
                            }
                        except:
                            pass
                return containers
        except:
            pass
        
        return {}
    
    def get_container_logs(self, container_name: str, lines: int = 1) -> str:
        """Get latest log line."""
        try:
            result = subprocess.run(
                ["docker", "logs", "--tail", str(lines), container_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[-1] if result.stdout else "(no logs)"
        except:
            pass
        
        return "(no logs)"
    
    def monitor_interlocking_engines(self):
        """Display interlocking engine status."""
        print("\n" + "=" * 150)
        print(f"[INTERLOCKING ENGINE HEALTH MONITOR] {self.timestamp.isoformat()}")
        print("=" * 150)
        
        # Show 176-day lock state
        lock_state = self.rhythms.get_176day_lock_state(self.timestamp)
        print(f"\n[176-DAY LOCK STATE]")
        print(f"Cycle #{lock_state['lock_cycle_number']} | Day {lock_state['days_in_current_176day_lock']}/176")
        print(f"Progress: {lock_state['lock_progress_percent']}% | Zodiac: {lock_state['zodiac_sign']} ({lock_state['zodiac_position_degrees']}°)")
        print(f"Next transition: {lock_state['next_lock_transition_in_days']} days\n")
        
        # Show system phase
        system_phase = self.rhythms.get_system_time_phase(self.timestamp)
        print(f"[SYSTEM PHASE] {system_phase['phase_name']} (t={system_phase['tau']}) - {system_phase['phase_progress_percent']}%")
        print(f"Cycle Position: {system_phase['cycle_position_0_to_1']}\n")
        
        # Get container data
        ps_data = self.get_docker_ps()
        
        # Display each engine's interlocking phase
        print(f"[INTERLOCKING ENGINE PHASES]")
        print("-" * 150)
        print(f"{'Engine':<25} {'Phase':<12} {'Tau':<8} {'Progress %':<12} {'Leads By (ms)':<15} {'State':<12} {'Recent Log':<70}")
        print("-" * 150)
        
        for i, engine_name in enumerate(self.ENGINES):
            engine_phase = self.rhythms.get_engine_phase(i, self.timestamp)
            ps_info = ps_data.get(engine_name, {'state': 'unknown', 'status': ''})
            state = ps_info['state'].upper()
            
            # Get latest log
            recent_log = self.get_container_logs(engine_name, 1)
            log_preview = recent_log[:65] if recent_log else "(no logs)"
            
            phase_name = engine_phase['phase_name']
            tau = engine_phase['tau']
            progress = engine_phase['phase_progress_percent']
            leads_ms = engine_phase['leads_system_by_milliseconds']
            
            print(f"{engine_name:<25} {phase_name:<12} {tau:<8} {progress:<12.1f} {leads_ms:<15.2f} {state:<12} {log_preview:<70}")
        
        print("-" * 150)
        
        # Summary
        print(f"\n[INTERLOCKING SUMMARY]")
        print(f"Total Engines: {len(self.ENGINES)}")
        print(f"Each engine offset by {round(self.rhythms.ENGINE_PHASE_OFFSET * 1000, 2)} ms")
        print(f"Full cycle: {self.rhythms.FULL_CYCLE} seconds (Heartbeat {self.rhythms.HEARTBEAT}s + Pulse {self.rhythms.PULSE}s + Horizon {self.rhythms.HORIZON}s)")
        print(f"176-day lock: Gregorian-Zodiac synchronization (half-year cycle)")
        print(f"\nAll engines operate in harmony: each at different phase offset, all within same 3-rhythm cycle")
        print("=" * 150)
    
    def save_detailed_report(self, output_file: str = "interlocking_engine_report.json"):
        """Save detailed interlocking state."""
        lock_state = self.rhythms.get_176day_lock_state(self.timestamp)
        system_phase = self.rhythms.get_system_time_phase(self.timestamp)
        
        report = {
            "timestamp": self.timestamp.isoformat(),
            "lock_state": lock_state,
            "system_phase": system_phase,
            "engines": {}
        }
        
        for i, engine_name in enumerate(self.ENGINES):
            engine_phase = self.rhythms.get_engine_phase(i, self.timestamp)
            report["engines"][engine_name] = engine_phase
        
        log_path = Path("./logs") / output_file
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[SAVED] {log_path}")


def main():
    """Execute interlocking engine monitoring."""
    monitor = InterlockingEngineHealthMonitor()
    monitor.monitor_interlocking_engines()
    monitor.save_detailed_report()


if __name__ == "__main__":
    main()
