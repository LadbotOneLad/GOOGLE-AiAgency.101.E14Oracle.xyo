#!/usr/bin/env python3
"""
Deep Metrics Monitor: Real-time engine metrics like engine-365-days
Pulls metrics.json, cycles.log, audit.log from all running engines
Shows uptime, cycles, decisions, rejection rate, validator health
"""

import subprocess
import json
import sys
from datetime import datetime
from pathlib import Path
import time

class DeepMetricsMonitor:
    """Monitor deep metrics from all containers."""
    
    ENGINES = [
        "codex-engine-1", "codex-engine-2", "codex-engine-3", "codex-engine-4",
        "codex-engine-5", "codex-engine-6", "codex-engine-7", "codex-engine-8",
        "codex-engine-9", "codex-engine-10", "codex-engine-11", "codex-engine-12",
        "witness-aggregator"
    ]
    
    def get_metrics_json(self, engine_name: str) -> Dict:
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
    
    def get_tail_log(self, engine_name: str, log_file: str, lines: int = 10) -> list:
        """Get tail of log file."""
        try:
            result = subprocess.run(
                ["docker", "exec", engine_name, "tail", "-" + str(lines), log_file],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return result.stdout.strip().split('\n') if result.stdout else []
        except:
            pass
        
        return []
    
    def get_container_stats(self, engine_name: str) -> Dict:
        """Get docker stats for engine."""
        try:
            result = subprocess.run(
                ["docker", "stats", "--no-stream", "--format", "json", engine_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return {
                    "cpu_percent": data.get("CPUPerc", "N/A"),
                    "memory_usage": data.get("MemUsage", "N/A"),
                    "memory_limit": data.get("MemLimit", "N/A")
                }
        except:
            pass
        
        return {}
    
    def display_engine_deep_output(self, engine_name: str):
        """Display engine deep output like the example."""
        print(f"\n# {engine_name} deep output")
        print(f"PS C:\\WINDOWS\\system32> docker exec {engine_name} cat /logs/metrics.json")
        
        metrics = self.get_metrics_json(engine_name)
        if metrics:
            print(json.dumps(metrics, indent=1))
        else:
            print("(no metrics)")
        
        # Tail cycles log
        print(f"PS C:\\WINDOWS\\system32> docker exec {engine_name} tail -20 /logs/cycles.log")
        cycles = self.get_tail_log(engine_name, "/logs/cycles.log", 20)
        for line in cycles:
            if line.strip():
                print(line)
        
        if not cycles or not cycles[0]:
            print("(no cycles log)")
        
        # Stats
        stats = self.get_container_stats(engine_name)
        if stats:
            print(f"PS C:\\WINDOWS\\system32> docker stats {engine_name}")
            print(f"CPU: {stats.get('cpu_percent', 'N/A')} | Memory: {stats.get('memory_usage', 'N/A')} / {stats.get('memory_limit', 'N/A')}")
    
    def run_continuous(self, update_interval: int = 30):
        """Run continuous monitoring."""
        print("\n" + "=" * 160)
        print(f"[DEEP METRICS MONITOR] {datetime.now().isoformat()}")
        print("=" * 160)
        print("Pulling metrics.json, cycles.log, docker stats from all engines")
        print("Updates every " + str(update_interval) + " seconds (CTRL+C to exit)\n")
        
        try:
            cycle_count = 0
            while True:
                cycle_count += 1
                print(f"\n\n{'='*160}")
                print(f"[UPDATE #{cycle_count}] {datetime.now().isoformat()}")
                print(f"{'='*160}")
                
                for engine_name in self.ENGINES:
                    self.display_engine_deep_output(engine_name)
                    print()
                
                print(f"\n[SLEEPING] {update_interval}s until next update...")
                time.sleep(update_interval)
        
        except KeyboardInterrupt:
            print(f"\n\n[STOPPED] {datetime.now().isoformat()}")
            sys.exit(0)


def main():
    """Run deep metrics monitor."""
    monitor = DeepMetricsMonitor()
    monitor.run_continuous(update_interval=30)


if __name__ == "__main__":
    main()
