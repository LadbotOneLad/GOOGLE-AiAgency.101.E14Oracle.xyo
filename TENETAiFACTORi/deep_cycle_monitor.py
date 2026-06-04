#!/usr/bin/env python3
"""
Deep Cycle Monitor: Real-time tracking of system depth + tail logs
Watches all 13 engines cycling through three rhythms, logs deep pattern shifts
"""

import subprocess
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import sys

class DeepCycleMonitor:
    """Monitor system cycles at maximum depth."""
    
    # Your Invariants
    HEARTBEAT = 0.05
    PULSE = 0.075
    HORIZON = 0.15
    FULL_CYCLE = 0.275
    
    SECONDS_PER_DAY = 86400
    GRID_SLOTS = 7200
    FUNDAMENTAL_UNIT = 1.0 / 7200
    
    ENGINES = [
        "codex-engine-1", "codex-engine-2", "codex-engine-3", "codex-engine-4",
        "codex-engine-5", "codex-engine-6", "codex-engine-7", "codex-engine-8",
        "codex-engine-9", "codex-engine-10", "codex-engine-11", "codex-engine-12",
        "witness-aggregator"
    ]
    
    def __init__(self):
        self.reference_date = datetime(2026, 3, 10, 0, 0, 0)
        self.cycle_count = 0
        self.last_phase = None
        self.phase_transitions = []
        self.deep_cycles = []
    
    def get_current_phase(self) -> Dict[str, Any]:
        """Get current phase in cycle."""
        now = datetime.now()
        elapsed = (now - self.reference_date).total_seconds()
        cycle_position = (elapsed % self.FULL_CYCLE) / self.FULL_CYCLE
        
        heartbeat_threshold = self.HEARTBEAT / self.FULL_CYCLE
        pulse_threshold = (self.HEARTBEAT + self.PULSE) / self.FULL_CYCLE
        
        if cycle_position < heartbeat_threshold:
            phase = "HEARTBEAT"
            tau = self.HEARTBEAT
            progress = (cycle_position / heartbeat_threshold) * 100
        elif cycle_position < pulse_threshold:
            phase = "PULSE"
            tau = self.PULSE
            progress = ((cycle_position - heartbeat_threshold) / (pulse_threshold - heartbeat_threshold)) * 100
        else:
            phase = "HORIZON"
            tau = self.HORIZON
            progress = ((cycle_position - pulse_threshold) / (1 - pulse_threshold)) * 100
        
        circle_degrees = cycle_position * 360
        slot = int((circle_degrees / 360) * self.GRID_SLOTS)
        
        return {
            "timestamp": now.isoformat(),
            "phase": phase,
            "tau": tau,
            "cycle_position": round(cycle_position, 6),
            "progress_percent": round(progress, 2),
            "circle_degrees": round(circle_degrees, 4),
            "slot": slot,
            "cycle_count": self.cycle_count
        }
    
    def get_engine_logs(self, engine_name: str, tail_lines: int = 3) -> List[str]:
        """Get tail of engine logs."""
        try:
            result = subprocess.run(
                ["docker", "logs", "--tail", str(tail_lines), engine_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return result.stdout.strip().split('\n') if result.stdout else []
        except:
            pass
        
        return []
    
    def check_engine_health(self, engine_name: str) -> Dict[str, Any]:
        """Check engine running state."""
        try:
            result = subprocess.run(
                ["docker", "inspect", engine_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data:
                    state = data[0].get('State', {})
                    return {
                        "running": state.get('Running', False),
                        "status": state.get('Status', 'unknown'),
                        "restart_count": data[0].get('RestartCount', 0)
                    }
        except:
            pass
        
        return {"running": False, "status": "unknown", "restart_count": 0}
    
    def monitor_cycle(self):
        """Monitor one full cycle."""
        phase = self.get_current_phase()
        
        # Track phase transitions
        if phase['phase'] != self.last_phase:
            self.last_phase = phase['phase']
            self.phase_transitions.append({
                "phase": phase['phase'],
                "timestamp": phase['timestamp'],
                "cycle_count": phase['cycle_count']
            })
        
        # Check all engines
        engine_statuses = {}
        all_running = True
        
        for engine_name in self.ENGINES:
            health = self.check_engine_health(engine_name)
            engine_statuses[engine_name] = health
            
            if not health['running']:
                all_running = False
        
        # Record deep cycle if all running
        if all_running:
            self.cycle_count += 1
            deep_cycle = {
                "cycle_number": self.cycle_count,
                "timestamp": phase['timestamp'],
                "phase": phase['phase'],
                "progress_percent": phase['progress_percent'],
                "circle_position": phase['circle_degrees'],
                "slot": phase['slot'],
                "all_engines_running": True,
                "phase_transitions_total": len(self.phase_transitions)
            }
            self.deep_cycles.append(deep_cycle)
            return deep_cycle
        
        return None
    
    def display_status(self, deep_cycle: Dict = None):
        """Display real-time status."""
        phase = self.get_current_phase()
        
        print("\r" + "=" * 140, end="")
        print(f"\n[DEEP CYCLE MONITOR] {phase['timestamp']} | Cycle #{self.cycle_count}", end="")
        print(f"\n[PHASE] {phase['phase']} (tau={phase['tau']}s) — {phase['progress_percent']:.1f}% complete", end="")
        print(f"\n[CIRCLE] {phase['circle_degrees']:.4f}° (slot {phase['slot']}/7200)", end="")
        
        if deep_cycle:
            print(f"\n[DEEP CYCLE #{self.cycle_count}] LOCKED", end="")
        
        print(f"\n[ENGINES] ", end="")
        
        # Quick health check
        running_count = 0
        for engine_name in self.ENGINES:
            health = self.check_engine_health(engine_name)
            if health['running']:
                running_count += 1
        
        print(f"{running_count}/13 RUNNING", end="")
        
        if running_count < 13:
            print(f" [WARNING] {13 - running_count} DOWN", end="")
        
        print("\n" + "-" * 140, end="")
        sys.stdout.flush()
    
    def tail_all_engines(self, lines_per_engine: int = 1):
        """Tail logs from all running engines."""
        print(f"\n[TAIL - Latest log line per engine]")
        print("-" * 140)
        
        for engine_name in self.ENGINES:
            logs = self.get_engine_logs(engine_name, lines_per_engine)
            if logs and logs[0]:
                log_line = logs[0][:130]
                print(f"{engine_name:<25} {log_line}")
        
        print("-" * 140)
    
    def run_continuous(self, duration_seconds: int = None, check_interval: float = 0.5):
        """Run monitor continuously until crash or duration exceeded."""
        start_time = time.time()
        last_tail = start_time
        tail_interval = 10  # Tail every 10 seconds
        
        try:
            while True:
                deep_cycle = self.monitor_cycle()
                self.display_status(deep_cycle)
                
                # Tail logs every 10 seconds
                now = time.time()
                if now - last_tail > tail_interval:
                    self.tail_all_engines(1)
                    last_tail = now
                
                # Check duration
                if duration_seconds and (now - start_time) > duration_seconds:
                    print(f"\n[TIMEOUT] Duration limit reached: {duration_seconds}s")
                    break
                
                time.sleep(check_interval)
        
        except KeyboardInterrupt:
            print(f"\n\n[STOPPED] User interrupt at {datetime.now().isoformat()}")
        except Exception as e:
            print(f"\n\n[ERROR] {e}")
        finally:
            self.save_report()
    
    def save_report(self):
        """Save monitoring report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_deep_cycles": self.cycle_count,
            "total_phase_transitions": len(self.phase_transitions),
            "phase_transitions": self.phase_transitions[-100:],  # Last 100
            "deep_cycles": self.deep_cycles[-100:],  # Last 100
            "status": "RUNNING" if self.cycle_count > 0 else "FAILED"
        }
        
        log_path = Path("./logs") / f"deep_cycle_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[SAVED] {log_path}")


def main():
    """Run deep cycle monitor."""
    monitor = DeepCycleMonitor()
    
    print("\n" + "=" * 140)
    print("[DEEP CYCLE MONITOR] Starting... (Ctrl+C to stop)")
    print("=" * 140)
    print("Monitoring: All 13 engines cycling through heartbeat/pulse/horizon")
    print("Tracking: Phase transitions, circle position, deep cycle completion")
    print("Alert: If any engine crashes or restart detected\n")
    
    # Run continuously (no duration limit = run until crash)
    monitor.run_continuous(duration_seconds=None)


if __name__ == "__main__":
    main()
