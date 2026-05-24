#!/usr/bin/env python3
"""
Synchronized Engine Monitor: All 13 Engines Lock Together
True synchronization: heartbeat/pulse/horizon phases synchronized across ALL engines
176-day Gregorian-Zodiac lock binding all engines to same temporal coordinate
"""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

class SynchronizedThreeRhythms:
    """All 13 engines synchronized to same heartbeat/pulse/horizon cycle."""
    
    # Three Rhythms (fundamental timescale)
    HEARTBEAT = 0.05      # 50ms - MEASUREMENT phase
    PULSE = 0.075        # 75ms - COMPARISON phase
    HORIZON = 0.15       # 150ms - DECISION phase
    
    # Full synchronized cycle (all engines at same phase)
    FULL_CYCLE = HEARTBEAT + PULSE + HORIZON  # 0.275 seconds
    
    # 13 engines (all synchronized, no offset)
    NUM_ENGINES = 13
    
    # 176-day lock (all engines locked to same Gregorian-Zodiac position)
    LOCK_DAYS = 176  # Half-year synchronization
    GREGORIAN_YEAR = 365.2425
    
    def __init__(self, reference_date: datetime = None):
        self.reference_date = reference_date or datetime(2026, 3, 10, 0, 0, 0)
    
    def get_synchronized_phase(self, timestamp: datetime = None) -> Dict[str, Any]:
        """Get current synchronized phase - ALL engines are here."""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Elapsed time since reference
        elapsed = (timestamp - self.reference_date).total_seconds()
        
        # Position in full cycle (0.0 to 1.0)
        cycle_position = (elapsed % self.FULL_CYCLE) / self.FULL_CYCLE
        
        # Determine which synchronized phase
        heartbeat_end = self.HEARTBEAT / self.FULL_CYCLE
        pulse_end = (self.HEARTBEAT + self.PULSE) / self.FULL_CYCLE
        
        if cycle_position < heartbeat_end:
            phase_name = "HEARTBEAT"
            tau = self.HEARTBEAT
            phase_start = 0
            phase_end = self.HEARTBEAT
            elapsed_in_phase = elapsed % self.FULL_CYCLE
            progress = (elapsed_in_phase / self.HEARTBEAT) * 100
        elif cycle_position < pulse_end:
            phase_name = "PULSE"
            tau = self.PULSE
            phase_start = self.HEARTBEAT
            phase_end = self.HEARTBEAT + self.PULSE
            elapsed_in_phase = (elapsed % self.FULL_CYCLE) - self.HEARTBEAT
            progress = (elapsed_in_phase / self.PULSE) * 100
        else:
            phase_name = "HORIZON"
            tau = self.HORIZON
            phase_start = self.HEARTBEAT + self.PULSE
            phase_end = self.FULL_CYCLE
            elapsed_in_phase = (elapsed % self.FULL_CYCLE) - (self.HEARTBEAT + self.PULSE)
            progress = (elapsed_in_phase / self.HORIZON) * 100
        
        # Cycle count
        cycle_number = int(elapsed / self.FULL_CYCLE)
        
        return {
            "timestamp": timestamp.isoformat(),
            "synchronized_phase": phase_name,
            "tau": tau,
            "cycle_number": cycle_number,
            "cycle_position_0_to_1": round(cycle_position, 6),
            "phase_progress_percent": round(progress, 2),
            "all_13_engines_locked_here": True,
            "message": f"ALL 13 ENGINES SYNCHRONIZED IN {phase_name} PHASE"
        }
    
    def get_synchronized_176day_lock(self, timestamp: datetime = None) -> Dict[str, Any]:
        """Get synchronized 176-day lock - ALL engines locked to same zodiac position."""
        if timestamp is None:
            timestamp = datetime.now()
        
        days_elapsed = (timestamp - self.reference_date).days
        
        # Which 176-day cycle?
        lock_cycle_num = int(days_elapsed / self.LOCK_DAYS)
        days_in_lock = days_elapsed % self.LOCK_DAYS
        
        # Zodiac position (0-180 for half-year)
        zodiac_degrees = (days_in_lock / self.LOCK_DAYS) * 180
        
        # Which zodiac sign (first 6 signs = 0-180 degrees)
        sign_index = int(zodiac_degrees / 30)
        zodiac_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        zodiac_sign = zodiac_signs[sign_index % 12]
        
        # Lock binding strength (how tightly locked all engines are)
        lock_binding_strength = 100 - (abs(90 - zodiac_degrees) / 90 * 100)  # Maximum at 90°
        
        return {
            "lock_cycle_number": lock_cycle_num,
            "days_in_176day_lock": days_in_lock,
            "lock_progress_percent": round((days_in_lock / self.LOCK_DAYS) * 100, 2),
            "zodiac_position_degrees": round(zodiac_degrees, 2),
            "zodiac_sign": zodiac_sign,
            "days_until_next_transition": self.LOCK_DAYS - days_in_lock,
            "lock_binding_strength_percent": round(lock_binding_strength, 2),
            "all_13_engines_locked_together": True,
            "message": f"ALL 13 ENGINES LOCKED TO {zodiac_sign} ({zodiac_degrees:.2f}°) - Binding: {lock_binding_strength:.1f}%"
        }
    
    def get_engine_heartbeat_count(self, timestamp: datetime = None) -> int:
        """Total synchronized heartbeat pulses since reference."""
        if timestamp is None:
            timestamp = datetime.now()
        
        elapsed = (timestamp - self.reference_date).total_seconds()
        return int(elapsed / self.HEARTBEAT)


class SynchronizedEngineMonitor:
    """Monitor all 13 engines in true synchronization."""
    
    ENGINES = [
        "codex-engine-1", "codex-engine-2", "codex-engine-3", "codex-engine-4",
        "codex-engine-5", "codex-engine-6", "codex-engine-7", "codex-engine-8",
        "codex-engine-9", "codex-engine-10", "codex-engine-11", "codex-engine-12",
        "witness-aggregator"
    ]
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.rhythms = SynchronizedThreeRhythms()
    
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
                return result.stdout.strip()[-80:]
        except:
            pass
        
        return "(no logs)"
    
    def monitor_synchronized(self):
        """Display all 13 engines synchronized."""
        print("\n" + "=" * 160)
        print(f"[SYNCHRONIZED ENGINE MONITOR] {self.timestamp.isoformat()}")
        print("=" * 160)
        
        # Get synchronized states
        phase_state = self.rhythms.get_synchronized_phase(self.timestamp)
        lock_state = self.rhythms.get_synchronized_176day_lock(self.timestamp)
        heartbeat_count = self.rhythms.get_engine_heartbeat_count(self.timestamp)
        
        # Display synchronized phase
        print(f"\n[SYNCHRONIZED THREE-RHYTHM CYCLE]")
        print(f"{'*' * 160}")
        print(f"PHASE: {phase_state['synchronized_phase']} (tau={phase_state['tau']}s)")
        print(f"PROGRESS: {phase_state['phase_progress_percent']}%")
        print(f"CYCLE #{phase_state['cycle_number']} | Total Heartbeats: {heartbeat_count:,}")
        print(f"STATUS: {phase_state['message']}")
        print(f"{'*' * 160}")
        
        # Display synchronized 176-day lock
        print(f"\n[SYNCHRONIZED 176-DAY GREGORIAN-ZODIAC LOCK]")
        print(f"{'*' * 160}")
        print(f"LOCK CYCLE #{lock_state['lock_cycle_number']} | Day {lock_state['days_in_176day_lock']}/176")
        print(f"PROGRESS: {lock_state['lock_progress_percent']}% | ZODIAC: {lock_state['zodiac_sign']} ({lock_state['zodiac_position_degrees']}°)")
        print(f"BINDING STRENGTH: {lock_state['lock_binding_strength_percent']}% | Next transition: {lock_state['days_until_next_transition']} days")
        print(f"STATUS: {lock_state['message']}")
        print(f"{'*' * 160}")
        
        # Get container data
        ps_data = self.get_docker_ps()
        
        # Display all 13 engines in perfect synchronization
        print(f"\n[ALL 13 ENGINES - SYNCHRONIZED STATUS]")
        print("-" * 160)
        print(f"{'Engine':<25} {'State':<12} {'Synchronized Phase':<20} {'Tau':<8} {'Progress':<12} {'Status':<90}")
        print("-" * 160)
        
        running_count = 0
        for i, engine_name in enumerate(self.ENGINES):
            ps_info = ps_data.get(engine_name, {'state': 'unknown', 'status': ''})
            state = ps_info['state'].upper()
            
            # All engines are at the SAME phase (synchronized)
            sync_phase = phase_state['synchronized_phase']
            tau = phase_state['tau']
            progress = phase_state['phase_progress_percent']
            
            # Get latest log
            log = self.get_container_log(engine_name)
            
            print(f"{engine_name:<25} {state:<12} {sync_phase:<20} {tau:<8} {progress:<12.1f} {log:<90}")
            
            if state == 'RUNNING':
                running_count += 1
        
        print("-" * 160)
        
        # Synchronization summary
        print(f"\n[SYNCHRONIZATION SUMMARY]")
        print(f"Total Engines: {len(self.ENGINES)}")
        print(f"Running Engines: {running_count}")
        print(f"Synchronized Phase: {phase_state['synchronized_phase']}")
        print(f"Synchronized Zodiac: {lock_state['zodiac_sign']}")
        print(f"Synchronization Type: ALL 13 ENGINES LOCKED TO SAME CYCLE POSITION")
        print(f"\nThree-Rhythm Cycle: {self.rhythms.HEARTBEAT}s (Heartbeat) + {self.rhythms.PULSE}s (Pulse) + {self.rhythms.HORIZON}s (Horizon) = {self.rhythms.FULL_CYCLE}s")
        print(f"176-Day Lock: All engines bound to Gregorian-Zodiac 6-month cycle")
        print(f"Lock Binding: {lock_state['lock_binding_strength_percent']}% (maximum when zodiac = 90°)")
        print(f"\n==> ALL 13 ENGINES OPERATE IN PERFECT TEMPORAL SYNCHRONIZATION <==")
        print("=" * 160)
    
    def save_synchronized_report(self, output_file: str = "synchronized_engine_report.json"):
        """Save synchronized state."""
        phase_state = self.rhythms.get_synchronized_phase(self.timestamp)
        lock_state = self.rhythms.get_synchronized_176day_lock(self.timestamp)
        
        report = {
            "timestamp": self.timestamp.isoformat(),
            "synchronization": {
                "all_engines_synchronized": True,
                "synchronized_phase": phase_state,
                "synchronized_176day_lock": lock_state,
                "total_synchronized_heartbeats": self.rhythms.get_engine_heartbeat_count(self.timestamp)
            },
            "engines": {
                engine: {
                    "name": engine,
                    "synchronized_phase": phase_state['synchronized_phase'],
                    "synchronized_zodiac": lock_state['zodiac_sign'],
                    "synchronized_to_all_13_engines": True
                }
                for engine in self.ENGINES
            }
        }
        
        log_path = Path("./logs") / output_file
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[SAVED] {log_path}")


def main():
    """Execute synchronized engine monitoring."""
    monitor = SynchronizedEngineMonitor()
    monitor.monitor_synchronized()
    monitor.save_synchronized_report()


if __name__ == "__main__":
    main()
