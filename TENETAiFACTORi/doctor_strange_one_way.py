#!/usr/bin/env python3
"""
Doctor Strange Stress Test: The One Way
Single deterministic path. No alternatives. Pure mathematical exhaustion.
Forces the engine to compute the only possible outcome.
"""

import json
import time
import math
import hashlib
from datetime import datetime
from pathlib import Path

class TheOneWay:
    """Deterministic single-path mathematical exhaustion."""
    
    def __init__(self, max_iterations: int = 100_000):
        self.max_iterations = max_iterations
        self.start_time = None
        self.cycles = 0
        self.checksum = 0
        self.path_depth = 0
        self.cpu_pressure = 0.0
        
    def _hard_math(self, x: float) -> float:
        """Lean, hard mathematical operations. No shortcuts."""
        # Single deterministic path
        result = x
        
        # Nested matrix-like operations (forcing CPU cache misses)
        for _ in range(100):
            result = math.sin(result) * math.cos(result)
            result = math.sqrt(abs(result) + 1e-10)
            result = math.exp(math.sin(result))
            result = math.log(abs(result) + 1e-10)
        
        return result
    
    def _quantum_collapse(self, position: float) -> int:
        """
        Like Doctor Strange's spell: infinite possibilities collapse to ONE.
        Calculate the only valid outcome through exhaustive enumeration.
        """
        valid_paths = 0
        best_outcome = 0
        
        # Exhaustive deterministic search (no branching, linear exploration)
        for i in range(1, 1000):
            # Test every possible outcome
            test_value = position * (i / 1000.0)
            
            # Hard computation (forces CPU work)
            hash_val = int(hashlib.md5(
                str(test_value).encode()
            ).hexdigest(), 16)
            
            # Only one path satisfies the condition
            if hash_val % 1000 == (i % 1000):
                valid_paths += 1
                best_outcome = hash_val
        
        return best_outcome
    
    def _pressure_gauge(self) -> float:
        """Measure CPU pressure (cycles per second)."""
        if self.start_time is None:
            return 0.0
        
        elapsed = time.perf_counter() - self.start_time
        if elapsed < 0.01:
            return 0.0
        
        return self.cycles / elapsed
    
    def run(self):
        """Execute The One Way: deterministic exhaustion."""
        self.start_time = time.perf_counter()
        
        position = 1.0  # Starting position
        
        print(f"[DOCTOR STRANGE] Initiating The One Way...")
        print(f"[DOCTOR STRANGE] Max iterations: {self.max_iterations:,}")
        print(f"[DOCTOR STRANGE] Computing the ONLY outcome...\n")
        
        checkpoint_interval = max(1, self.max_iterations // 10)
        
        try:
            while self.cycles < self.max_iterations:
                # Single deterministic path (no branching)
                position = self._hard_math(position)
                outcome = self._quantum_collapse(position)
                
                # Update checksum (proof of work)
                self.checksum ^= outcome
                self.path_depth += 1
                self.cycles += 1
                self.cpu_pressure = self._pressure_gauge()
                
                # Checkpoint logging
                if self.cycles % checkpoint_interval == 0:
                    progress = (self.cycles / self.max_iterations) * 100
                    print(f"[{progress:5.1f}%] Cycles: {self.cycles:,} | "
                          f"CPU: {self.cpu_pressure:,.0f} cycles/sec | "
                          f"Checksum: {self.checksum:016x}")
        
        except KeyboardInterrupt:
            print("\n[DOCTOR STRANGE] Spell interrupted. Computing final outcome...")
        
        return self._finalize()
    
    def _finalize(self) -> dict:
        """Compute final metrics."""
        elapsed = time.perf_counter() - self.start_time
        
        return {
            "timestamp": datetime.now().isoformat(),
            "cycles_completed": self.cycles,
            "elapsed_seconds": round(elapsed, 3),
            "throughput_cycles_per_sec": round(self.cycles / max(elapsed, 0.001), 0),
            "path_depth": self.path_depth,
            "final_checksum": f"{self.checksum:016x}",
            "cpu_pressure_max": round(self.cpu_pressure, 0),
            "verdict": "ONLY ONE WAY" if self.cycles == self.max_iterations else "INTERRUPTED"
        }


class InfinityStone:
    """Time Stone + Space Stone: Measure and enforce determinism."""
    
    def __init__(self):
        self.measurements = []
    
    def measure(self, result: dict):
        """Log the outcome."""
        self.measurements.append(result)
        
        # Write immutable record
        log_path = Path("/app/logs") / "doctor_strange_one_way.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "a") as f:
            f.write(json.dumps(result) + "\n")
        
        return result
    
    def report(self, result: dict):
        """Display the final outcome."""
        print("\n" + "=" * 80)
        print("[INFINITY STONE] THE OUTCOME IS WRITTEN")
        print("=" * 80)
        
        for key, value in result.items():
            print(f"{key:.<40} {value}")
        
        print("=" * 80)
        print("[DOCTOR STRANGE] There was only one way.\n")


def main():
    """The One Way: Execute."""
    stone = InfinityStone()
    spell = TheOneWay(max_iterations=100_000)
    
    result = spell.run()
    stone.measure(result)
    stone.report(result)


if __name__ == "__main__":
    main()
