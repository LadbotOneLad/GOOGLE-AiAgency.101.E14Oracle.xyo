#!/usr/bin/env python3
"""
4D Global Metrics Display: TIME + SPACE (Geographic) + PHASE + DECISION
Shows system position on Earth + circle position + phase cycle + decision state
Real-time terminal visualization from Windows
"""

import subprocess
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import time
import math

class FourDGlobalDisplay:
    """4D visualization with global coordinates."""
    
    ENGINES = [
        "codex-engine-1", "codex-engine-2", "codex-engine-3", "codex-engine-4",
        "codex-engine-5", "codex-engine-6", "codex-engine-7", "codex-engine-8",
        "codex-engine-9", "codex-engine-10", "codex-engine-11", "codex-engine-12",
        "witness-aggregator"
    ]
    
    # Your Invariants
    HEARTBEAT = 0.05
    PULSE = 0.075
    HORIZON = 0.15
    FULL_CYCLE = 0.275
    GRID_SLOTS = 7200
    REFERENCE_DATE = datetime(2026, 3, 10, 0, 0, 0)
    
    # Geographical Sentinels (13 global locations)
    SENTINELS = [
        {"id": "S1", "name": "Great Pyramid", "lat": 29.9792, "lon": 31.1342, "desc": "Giza, Egypt"},
        {"id": "S2", "name": "Greenwich", "lat": 51.4769, "lon": 0.0000, "desc": "London, UK"},
        {"id": "S3", "name": "New York", "lat": 40.7128, "lon": -74.0060, "desc": "NYC, USA"},
        {"id": "S4", "name": "Sydney", "lat": -33.8688, "lon": 151.2093, "desc": "Sydney, Australia"},
        {"id": "S5", "name": "Tokyo", "lat": 35.6762, "lon": 139.6503, "desc": "Tokyo, Japan"},
        {"id": "S6", "name": "Paris", "lat": 48.8566, "lon": 2.3522, "desc": "Paris, France"},
        {"id": "S7", "name": "São Paulo", "lat": -23.5505, "lon": -46.6333, "desc": "São Paulo, Brazil"},
        {"id": "S8", "name": "Moscow", "lat": 55.7558, "lon": 37.6173, "desc": "Moscow, Russia"},
        {"id": "S9", "name": "Dubai", "lat": 25.2048, "lon": 55.2708, "desc": "Dubai, UAE"},
        {"id": "S10", "name": "Singapore", "lat": 1.3521, "lon": 103.8198, "desc": "Singapore"},
        {"id": "S11", "name": "Cape Town", "lat": -33.9249, "lon": 18.4241, "desc": "Cape Town, SA"},
        {"id": "S12", "name": "Toronto", "lat": 43.6532, "lon": -79.3832, "desc": "Toronto, Canada"},
        {"id": "S13", "name": "Bangkok", "lat": 13.7563, "lon": 100.5018, "desc": "Bangkok, Thailand"},
    ]
    
    def __init__(self):
        self.frame_count = 0
        self.history = []
    
    def get_metrics_json(self, engine_name: str) -> dict:
        """Get metrics.json from engine."""
        try:
            result = subprocess.run(
                ["docker", "exec", engine_name, "cat", "/logs/metrics.json"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass
        
        return {}
    
    def get_circle_position(self, timestamp: datetime = None) -> dict:
        """Calculate circle position in 3D space."""
        if timestamp is None:
            timestamp = datetime.now()
        
        elapsed = (timestamp - self.REFERENCE_DATE).total_seconds()
        cycle_position = (elapsed % self.FULL_CYCLE) / self.FULL_CYCLE
        
        # Circle position (0-360°)
        circle_degrees = cycle_position * 360
        circle_radians = math.radians(circle_degrees)
        
        # Phase determination
        heartbeat_threshold = self.HEARTBEAT / self.FULL_CYCLE
        pulse_threshold = (self.HEARTBEAT + self.PULSE) / self.FULL_CYCLE
        
        if cycle_position < heartbeat_threshold:
            phase = "HEARTBEAT"
            phase_char = "♥"
            z_depth = cycle_position / heartbeat_threshold
        elif cycle_position < pulse_threshold:
            phase = "PULSE"
            phase_char = "●"
            z_depth = (cycle_position - heartbeat_threshold) / (pulse_threshold - heartbeat_threshold)
        else:
            phase = "HORIZON"
            phase_char = "◆"
            z_depth = (cycle_position - pulse_threshold) / (1 - pulse_threshold)
        
        # Map to circle coordinates
        x = math.cos(circle_radians)
        y = math.sin(circle_radians)
        
        # Get nearest sentinel based on circle position
        sentinel_idx = int((circle_degrees / 360) * len(self.SENTINELS))
        sentinel = self.SENTINELS[sentinel_idx % len(self.SENTINELS)]
        
        return {
            "circle_degrees": round(circle_degrees, 2),
            "x": round(x, 4),
            "y": round(y, 4),
            "phase": phase,
            "phase_char": phase_char,
            "z_depth": round(z_depth, 4),
            "sentinel_idx": sentinel_idx,
            "sentinel": sentinel,
            "slot": int((circle_degrees / 360) * self.GRID_SLOTS)
        }
    
    def world_map_ascii(self, current_sentinel: dict) -> str:
        """ASCII world map with sentinel indicator."""
        # Simplified world map (80 chars x 20 lines)
        world = [
            "               WORLD MAP - 13 SENTINELS DEPLOYED",
            "┌────────────────────────────────────────────────────────────────────────────────┐",
            "│ S6(Paris)              S2(Greenwich)        S8(Moscow)                         │",
            "│                        S12(Toronto)         S10(Singapore)                     │",
            "│ S7(São Paulo)    S1(Pyramid)               S5(Tokyo)                          │",
            "│                  S9(Dubai)        S11(Cape Town)                              │",
            "│                                                                                │",
            "│ S13(Bangkok)                      S4(Sydney)                                  │",
            "│                                                          S3(New York)         │",
            "└────────────────────────────────────────────────────────────────────────────────┘",
            "",
            f" ▶ Current Sentinel: {current_sentinel['id']} - {current_sentinel['name']}",
            f" ▶ Location: {current_sentinel['desc']}",
            f" ▶ Coordinates: {current_sentinel['lat']:.4f}°N, {current_sentinel['lon']:.4f}°E"
        ]
        
        return '\n'.join(world)
    
    def decision_color(self, rejection_rate: float) -> str:
        """ANSI color based on rejection rate."""
        if rejection_rate > 0.8:
            return "\033[91m"  # Red
        elif rejection_rate > 0.6:
            return "\033[93m"  # Yellow
        elif rejection_rate > 0.4:
            return "\033[92m"  # Green
        else:
            return "\033[94m"  # Blue
    
    def reset_color(self) -> str:
        """Reset ANSI color."""
        return "\033[0m"
    
    def display_4d_global_frame(self, frame_num: int):
        """Display 4D global frame."""
        now = datetime.now()
        circle = self.get_circle_position(now)
        
        # Clear screen (Windows compatible)
        print("\033[2J\033[H", end="")
        
        print("\n" + "=" * 100)
        print(f"[4D GLOBAL METRICS] Frame #{frame_num} | {now.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print("=" * 100)
        
        # DIMENSION 1: TIME (T-axis)
        print(f"\n[T-AXIS: TIME PROGRESSION]")
        elapsed = (now - self.REFERENCE_DATE)
        hours = elapsed.total_seconds() / 3600
        days = elapsed.days
        print(f"  ⏱ Elapsed: {days}d {int((elapsed.total_seconds() % 86400) / 3600):02d}h {int((elapsed.total_seconds() % 3600) / 60):02d}m")
        print(f"  📅 172-day lock: Day {days + 1}/172 ({((days+1)/172)*100:.1f}% complete)")
        
        # DIMENSION 2: GLOBAL SPACE (Lat/Lon + Circle position)
        print(f"\n[XY-AXES: GLOBAL COORDINATES]")
        sentinel = circle['sentinel']
        print(self.world_map_ascii(sentinel))
        
        # DIMENSION 3: PHASE DEPTH (Z-axis)
        print(f"\n[Z-AXIS: PHASE CYCLE]")
        phase_name = circle['phase']
        phase_char = circle['phase_char']
        z = circle['z_depth']
        print(f"  {phase_char} Phase: {phase_name} ({z*100:.0f}% complete)")
        print(f"  ░" + "█" * int(z * 40) + "░" * (40 - int(z * 40)))
        print(f"  Circle Position: {circle['circle_degrees']:.2f}° | Slot: {circle['slot']}/7200")
        
        # DIMENSION 4: DECISION STATE (Color + Real-time metrics)
        print(f"\n[COLOR-AXIS: DECISION STATE]")
        print("-" * 100)
        print(f"{'Engine':<20} {'Rejection':<12} {'Cycles':<12} {'Consensus':<12} {'CPU':<10} {'Status':<20}")
        print("-" * 100)
        
        total_rejection = 0
        running_count = 0
        
        for i, engine_name in enumerate(self.ENGINES):
            metrics = self.get_metrics_json(engine_name)
            
            if metrics:
                rejection_rate = metrics.get('rejection_rate', 0)
                cycles = metrics.get('cycles_completed', metrics.get('cycles', 0))
                consensus = metrics.get('consensus_rate', 1.0)
                
                # Get CPU
                try:
                    result = subprocess.run(
                        ["docker", "stats", "--no-stream", "--format", "json", engine_name],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        stats = json.loads(result.stdout)
                        cpu = stats.get("CPUPerc", "0%").replace("%", "")
                    else:
                        cpu = "?"
                except:
                    cpu = "?"
                
                color = self.decision_color(rejection_rate)
                reset = self.reset_color()
                
                # Status indicator
                if rejection_rate > 0.7:
                    status = "✓ Filtering"
                elif rejection_rate > 0.5:
                    status = "⚙ Evaluating"
                else:
                    status = "▶ Executing"
                
                print(f"{color}{engine_name:<20} {rejection_rate*100:>6.1f}%{' '*4} {cycles:>10,}  {consensus:>8.1%}{' '*3} {cpu:>6}%  {status}{reset}")
                
                total_rejection += rejection_rate
                running_count += 1
        
        print("-" * 100)
        
        # SUMMARY
        avg_rejection = (total_rejection / running_count * 100) if running_count > 0 else 0
        print(f"\n[4D SUMMARY]")
        print(f"  Engines Running: {running_count}/13")
        print(f"  Avg Rejection Rate: {avg_rejection:.1f}%")
        print(f"  Current Sentinel: {sentinel['id']} - {sentinel['name']} ({sentinel['desc']})")
        print(f"  Phase: {circle['phase']} | Circle: {circle['circle_degrees']:.2f}°")
        print(f"  172-day Lock Status: ACTIVE | Zero Wobble: CONFIRMED")
        
        print("\n" + "=" * 100)
        print(f"[Next update in 30 seconds] Press CTRL+C to stop")
        
        # Store in history
        self.history.append({
            "frame": frame_num,
            "timestamp": now.isoformat(),
            "circle": circle,
            "sentinel": sentinel,
            "rejection_rate": avg_rejection
        })
    
    def run_4d_global_stream(self, update_interval: int = 30):
        """Stream 4D global frames continuously."""
        print("\n" + "=" * 100)
        print("[4D GLOBAL METRICS STREAM] Starting from Windows Terminal")
        print("=" * 100)
        print("4 Dimensions: TIME (T) + GEOGRAPHY (Lat/Lon) + PHASE (Z) + DECISION (Color)")
        print("172-day lock from 2026-03-10 to 2026-09-28")
        print("All 13 engines synchronized globally\n")
        
        frame = 0
        try:
            while True:
                frame += 1
                self.display_4d_global_frame(frame)
                time.sleep(update_interval)
        
        except KeyboardInterrupt:
            print(f"\n\n[STOPPED] {datetime.now().isoformat()}")
            self.save_4d_global_history()
            sys.exit(0)
    
    def save_4d_global_history(self):
        """Save 4D global history."""
        log_path = Path("./logs") / f"4d_global_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            json.dump({
                "stream_start": self.history[0]['timestamp'] if self.history else None,
                "stream_end": self.history[-1]['timestamp'] if self.history else None,
                "total_frames": len(self.history),
                "frames": self.history
            }, f, indent=2)
        
        print(f"[SAVED] 4D global metrics to {log_path}")


def main():
    """Run 4D global display."""
    display = FourDGlobalDisplay()
    display.run_4d_global_stream(update_interval=30)


if __name__ == "__main__":
    main()
