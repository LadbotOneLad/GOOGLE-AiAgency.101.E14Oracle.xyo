#!/usr/bin/env python3
"""
4D Deep Metrics Display: Time + Space + Phase + Decision
Shows metrics progression across 4 dimensions simultaneously
Timestamp (T) + Circle Position (X,Y) + Phase Cycle (Z) + Decision State (Color)
"""

import subprocess
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import time
import math

class FourDMetricsDisplay:
    """4D visualization of deep metrics."""
    
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
    
    def __init__(self):
        self.history = []
        self.frame_count = 0
    
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
        """Calculate 3D circle position."""
        if timestamp is None:
            timestamp = datetime.now()
        
        elapsed = (timestamp - self.REFERENCE_DATE).total_seconds()
        cycle_position = (elapsed % self.FULL_CYCLE) / self.FULL_CYCLE
        
        # X,Y on circle (0-360°)
        circle_degrees = cycle_position * 360
        circle_radians = math.radians(circle_degrees)
        
        x = math.cos(circle_radians)
        y = math.sin(circle_radians)
        
        # Z = phase depth (0-1)
        heartbeat_threshold = self.HEARTBEAT / self.FULL_CYCLE
        pulse_threshold = (self.HEARTBEAT + self.PULSE) / self.FULL_CYCLE
        
        if cycle_position < heartbeat_threshold:
            z = cycle_position / heartbeat_threshold  # 0-1 in HEARTBEAT
            phase = "HEARTBEAT"
        elif cycle_position < pulse_threshold:
            z = (cycle_position - heartbeat_threshold) / (pulse_threshold - heartbeat_threshold)  # 0-1 in PULSE
            phase = "PULSE"
        else:
            z = (cycle_position - pulse_threshold) / (1 - pulse_threshold)  # 0-1 in HORIZON
            phase = "HORIZON"
        
        return {
            "circle_degrees": round(circle_degrees, 2),
            "x": round(x, 4),
            "y": round(y, 4),
            "z": round(z, 4),
            "phase": phase,
            "cycle_position": round(cycle_position, 6)
        }
    
    def ascii_circle(self, x: float, y: float) -> str:
        """Draw ASCII circle position."""
        # Map x,y (-1 to 1) to grid (0-20)
        grid_x = int((x + 1) * 10)
        grid_y = int((y + 1) * 10)
        grid_x = max(0, min(20, grid_x))
        grid_y = max(0, min(20, grid_y))
        
        grid = [['.' for _ in range(21)] for _ in range(21)]
        grid[grid_y][grid_x] = '*'
        
        return '\n'.join(''.join(row) for row in grid)
    
    def decision_color(self, rejection_rate: float) -> str:
        """Map rejection rate to ANSI color."""
        if rejection_rate > 0.8:
            return "\033[91m"  # Red (high rejection)
        elif rejection_rate > 0.6:
            return "\033[93m"  # Yellow (medium rejection)
        elif rejection_rate > 0.4:
            return "\033[92m"  # Green (balanced)
        else:
            return "\033[94m"  # Blue (low rejection)
    
    def reset_color(self) -> str:
        """Reset ANSI color."""
        return "\033[0m"
    
    def display_4d_frame(self, frame_num: int):
        """Display one 4D frame."""
        now = datetime.now()
        circle = self.get_circle_position(now)
        
        print(f"\n{'='*160}")
        print(f"[4D FRAME #{frame_num}] {now.isoformat()}")
        print(f"{'='*160}")
        
        # Dimension 1: TIME (T axis)
        print(f"\n[T-AXIS: TIME]")
        print(f"Timestamp: {now.isoformat()}")
        uptime_hours = (now - self.REFERENCE_DATE).total_seconds() / 3600
        print(f"Uptime: {uptime_hours:.2f} hours ({(now - self.REFERENCE_DATE).days} days)")
        
        # Dimension 2: SPACE (X,Y axes - circle position)
        print(f"\n[X,Y-AXES: CIRCLE SPACE]")
        print(f"Position: {circle['circle_degrees']}°")
        print(f"Coordinates: X={circle['x']:+.4f}, Y={circle['y']:+.4f}")
        print(f"\nCircle Visualization:")
        print(self.ascii_circle(circle['x'], circle['y']))
        
        # Dimension 3: PHASE (Z axis)
        print(f"\n[Z-AXIS: PHASE DEPTH]")
        print(f"Phase: {circle['phase']} (τ={self.HEARTBEAT if circle['phase']=='HEARTBEAT' else self.PULSE if circle['phase']=='PULSE' else self.HORIZON}s)")
        print(f"Depth: {circle['z']:.1%} through {circle['phase']}")
        depth_bar = "█" * int(circle['z'] * 50) + "░" * (50 - int(circle['z'] * 50))
        print(f"[{depth_bar}]")
        
        # Dimension 4: DECISION STATE (Color + Metrics)
        print(f"\n[COLOR-AXIS: DECISION STATE]")
        print("-" * 160)
        print(f"{'Engine':<25} {'Rejection%':<15} {'Cycles':<15} {'Consensus':<15} {'CPU%':<12} {'Memory':<20}")
        print("-" * 160)
        
        total_rejection = 0
        engine_count = 0
        
        for engine_name in self.ENGINES:
            metrics = self.get_metrics_json(engine_name)
            
            if metrics:
                rejection_rate = metrics.get('rejection_rate', 0)
                cycles = metrics.get('cycles_completed', metrics.get('cycles', 0))
                consensus = metrics.get('consensus_rate', 1.0)
                
                # Get docker stats
                try:
                    result = subprocess.run(
                        ["docker", "stats", "--no-stream", "--format", "json", engine_name],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        stats = json.loads(result.stdout)
                        cpu = stats.get("CPUPerc", "N/A").replace("%", "")
                        mem = stats.get("MemUsage", "N/A")
                    else:
                        cpu = "N/A"
                        mem = "N/A"
                except:
                    cpu = "N/A"
                    mem = "N/A"
                
                color = self.decision_color(rejection_rate)
                reset = self.reset_color()
                
                print(f"{color}{engine_name:<25} {rejection_rate*100:>6.1f}%{' '*7} {cycles:>12,}  {consensus:>6.1%}{' '*7} {cpu:>8}{' '*3} {mem:<20}{reset}")
                
                total_rejection += rejection_rate
                engine_count += 1
        
        print("-" * 160)
        avg_rejection = (total_rejection / engine_count * 100) if engine_count > 0 else 0
        print(f"\n[4D METRICS SUMMARY]")
        print(f"Average Rejection Rate: {avg_rejection:.1f}%")
        print(f"Total Engines: {engine_count}/13")
        print(f"Circle Position: {circle['circle_degrees']}° (slot {int((circle['circle_degrees']/360)*self.GRID_SLOTS)}/7200)")
        print(f"Phase: {circle['phase']}")
        
        # Store frame in history
        self.history.append({
            "frame": frame_num,
            "timestamp": now.isoformat(),
            "circle": circle,
            "rejection_rate": avg_rejection
        })
    
    def run_4d_stream(self, update_interval: int = 30, max_frames: int = None):
        """Stream 4D frames continuously."""
        print("\n" + "=" * 160)
        print("[4D DEEP METRICS STREAM]")
        print("=" * 160)
        print("4 Dimensions: TIME (T) + CIRCLE (X,Y) + PHASE (Z) + DECISION (Color)")
        print("Updates every " + str(update_interval) + "s (CTRL+C to stop)\n")
        
        frame = 0
        try:
            while max_frames is None or frame < max_frames:
                frame += 1
                self.display_4d_frame(frame)
                print(f"\n[Sleeping {update_interval}s until next frame...]")
                time.sleep(update_interval)
        
        except KeyboardInterrupt:
            print(f"\n\n[STOPPED] {datetime.now().isoformat()}")
            self.save_4d_history()
            sys.exit(0)
    
    def save_4d_history(self):
        """Save 4D history to file."""
        log_path = Path("./logs") / f"4d_metrics_stream_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            json.dump({
                "frames": self.history,
                "total_frames": len(self.history)
            }, f, indent=2)
        
        print(f"[SAVED] 4D history to {log_path}")


def main():
    """Run 4D metrics display."""
    display = FourDMetricsDisplay()
    display.run_4d_stream(update_interval=30)


if __name__ == "__main__":
    main()
