#!/usr/bin/env python3
"""
Lean Stress Test Entrypoint
Runs Doctor Strange One Way + System Metrics in parallel
"""

import subprocess
import json
import time
import psutil
from pathlib import Path
from datetime import datetime

def monitor_system():
    """Monitor CPU, memory, disk during stress test."""
    log_path = Path("/app/logs") / "system_metrics.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("[MONITOR] Starting system metrics...")
    
    try:
        while True:
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_mb": psutil.virtual_memory().used / 1024 / 1024,
                "memory_percent": psutil.virtual_memory().percent,
            }
            
            with open(log_path, "a") as f:
                f.write(json.dumps(metrics) + "\n")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("[MONITOR] Stopped.")

def run_stress_test():
    """Execute The One Way stress test."""
    print("[STRESS TEST] Starting Doctor Strange One Way...\n")
    subprocess.run(["python3", "doctor_strange_one_way.py"], check=False)

def main():
    """Run both in sequence (or adapt for async if needed)."""
    run_stress_test()
    print("\n[STRESS TEST] Complete. Check logs/doctor_strange_one_way.jsonl")

if __name__ == "__main__":
    main()
