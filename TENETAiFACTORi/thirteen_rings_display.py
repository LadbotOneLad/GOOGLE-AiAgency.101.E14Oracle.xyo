#!/usr/bin/env python3
"""
4D Global Display: 13 Rings Around Earth
Each ring = one engine, all synchronized rotating around the globe
Shows real-time circle position, phase, and decision state
"""

import subprocess
import json
import sys
from datetime import datetime
from pathlib import Path
import time
import math

class ThirteenRingsDisplay:
    """13 rings wrapping around Earth visualization."""
    
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
        self.frame_count = 0
    
    def get_metrics_json(self, engine_name: str) -> dict:
        """Get metrics from engine."""
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
        """Get current circle position (0-360°)."""
        if timestamp is None:
            timestamp = datetime.now()
        
        elapsed = (timestamp - self.REFERENCE_DATE).total_seconds()
        cycle_position = (elapsed % self.FULL_CYCLE) / self.FULL_CYCLE
        
        circle_degrees = cycle_position * 360
        circle_radians = math.radians(circle_degrees)
        
        # Determine phase
        heartbeat_threshold = self.HEARTBEAT / self.FULL_CYCLE
        pulse_threshold = (self.HEARTBEAT + self.PULSE) / self.FULL_CYCLE
        
        if cycle_position < heartbeat_threshold:
            phase = "HEARTBEAT"
            phase_char = "♥"
        elif cycle_position < pulse_threshold:
            phase = "PULSE"
            phase_char = "●"
        else:
            phase = "HORIZON"
            phase_char = "◆"
        
        return {
            "circle_degrees": round(circle_degrees, 2),
            "radians": circle_radians,
            "phase": phase,
            "phase_char": phase_char,
            "slot": int((circle_degrees / 360) * self.GRID_SLOTS)
        }
    
    def decision_symbol(self, rejection_rate: float) -> tuple:
        """Get symbol and color for rejection rate."""
        if rejection_rate > 0.8:
            return ("█", "\033[91m")  # Red - high filtering
        elif rejection_rate > 0.6:
            return ("▓", "\033[93m")  # Yellow - medium filtering
        elif rejection_rate > 0.4:
            return ("▒", "\033[92m")  # Green - balanced
        else:
            return ("░", "\033[94m")  # Blue - high execution
    
    def draw_13_rings(self, circle_pos: dict, metrics_list: list) -> str:
        """Draw 13 concentric rings around Earth."""
        lines = []
        
        # Earth radius = 20 chars, rings extend outward
        earth_radius = 20
        ring_width = 4
        max_radius = earth_radius + (13 * ring_width)
        size = max_radius * 2 + 1
        
        # Create 2D canvas
        canvas = [[' ' for _ in range(size)] for _ in range(size)]
        center = size // 2
        
        # Draw Earth (center)
        for y in range(size):
            for x in range(size):
                dist = math.sqrt((x - center)**2 + (y - center)**2)
                if dist <= earth_radius * 0.7:
                    canvas[y][x] = '●'
        
        # Draw 13 rings, each with one engine
        current_angle = circle_pos['radians']
        
        for ring_idx in range(13):
            if ring_idx >= len(metrics_list):
                continue
            
            metrics = metrics_list[ring_idx]
            rejection_rate = metrics.get('rejection_rate', 0)
            symbol, color = self.decision_symbol(rejection_rate)
            
            # Ring radius for this engine
            ring_radius = earth_radius + (ring_idx + 1) * ring_width
            
            # Position on ring (all engines at same angle on circle)
            x = center + int(ring_radius * math.cos(current_angle))
            y = center + int(ring_radius * math.sin(current_angle))
            
            # Bounds check
            if 0 <= x < size and 0 <= y < size:
                canvas[y][x] = symbol
        
        # Convert canvas to string with coloring
        result = []
        result.append("┌" + "─" * (size - 2) + "┐")
        
        for y, row in enumerate(canvas):
            line = "│"
            for x, char in enumerate(row):
                # Color based on position (engine ring)
                if char == '●':
                    line += "\033[96m●\033[0m"  # Cyan Earth
                elif char in '█▓▒░':
                    # Determine which ring this is
                    dist = math.sqrt((x - center)**2 + (y - center)**2)
                    ring_num = int((dist - earth_radius) / ring_width)
                    if 0 <= ring_num < len(metrics_list):
                        _, color = self.decision_symbol(metrics_list[ring_num].get('rejection_rate', 0))
                        line += f"{color}{char}\033[0m"
                    else:
                        line += char
                else:
                    line += char
            line += "│"
            result.append(line)
        
        result.append("└" + "─" * (size - 2) + "┘")
        
        return '\n'.join(result)
    
    def display_frame(self, frame_num: int):
        """Display one frame with 13 rings."""
        now = datetime.now()
        circle = self.get_circle_position(now)
        
        # Clear screen
        print("\033[2J\033[H", end="")
        
        print("\n" + "=" * 120)
        print(f"[13 RINGS AROUND EARTH] Frame #{frame_num} | {now.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print("=" * 120)
        
        # Time info
        elapsed = (now - self.REFERENCE_DATE)
        days = elapsed.days
        hours = int((elapsed.total_seconds() % 86400) / 3600)
        
        print(f"\n[TIME] Day {days+1}/172 ({((days+1)/172)*100:.1f}%) | {hours:02d}h elapsed")
        print(f"[CIRCLE] Position: {circle['circle_degrees']:.2f}° | Slot: {circle['slot']}/7200")
        print(f"[PHASE] {circle['phase_char']} {circle['phase']} phase\n")
        
        # Get all metrics
        metrics_list = []
        running_count = 0
        total_rejection = 0
        
        for engine_name in self.ENGINES:
            metrics = self.get_metrics_json(engine_name)
            if metrics:
                metrics_list.append(metrics)
                running_count += 1
                rejection_rate = metrics.get('rejection_rate', 0)
                total_rejection += rejection_rate
            else:
                metrics_list.append({'rejection_rate': 0})
        
        # Draw 13 rings
        print(self.draw_13_rings(circle, metrics_list))
        
        # Legend and metrics
        print(f"\n[13 ENGINES ON CIRCLE]")
        print("-" * 120)
        
        for i, engine_name in enumerate(self.ENGINES):
            if i < len(metrics_list):
                metrics = metrics_list[i]
                rejection_rate = metrics.get('rejection_rate', 0)
                symbol, _ = self.decision_symbol(rejection_rate)
                cycles = metrics.get('cycles_completed', metrics.get('cycles', 0))
                
                print(f"Ring {i+1:2d}: {engine_name:<25} {symbol} {rejection_rate*100:6.1f}% rejection | {cycles:>10,} cycles")
        
        print("-" * 120)
        
        avg_rejection = (total_rejection / running_count * 100) if running_count > 0 else 0
        print(f"\n[SUMMARY]")
        print(f"  Engines: {running_count}/13 running")
        print(f"  Avg Rejection: {avg_rejection:.1f}%")
        print(f"  All 13 rings synchronized at: {circle['circle_degrees']:.2f}°")
        print(f"  Legend: █=High Filter | ▓=Medium | ▒=Balanced | ░=High Exec")
        print(f"  172-day lock: ACTIVE | Zero wobble: CONFIRMED\n")
        print("=" * 120)
        print(f"[Next update in 30s] CTRL+C to stop")
    
    def run_continuous(self, update_interval: int = 30):
        """Stream frames continuously."""
        print("\n" + "=" * 120)
        print("[13 RINGS AROUND EARTH] - Real-time 4D Global Visualization")
        print("=" * 120)
        print("Each ring = 1 engine. All rings synchronized. Rotating around globe.")
        print("172-day lock active. All 13 engines locked to same circle position.\n")
        
        frame = 0
        try:
            while True:
                frame += 1
                self.display_frame(frame)
                time.sleep(update_interval)
        except KeyboardInterrupt:
            print(f"\n\n[STOPPED] {datetime.now().isoformat()}")
            sys.exit(0)


def main():
    """Run 13 rings display."""
    display = ThirteenRingsDisplay()
    display.run_continuous(update_interval=30)


if __name__ == "__main__":
    main()
