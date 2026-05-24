#!/usr/bin/env python3
"""
Real-time tail: Follow all 13 engines with live log streaming
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

ENGINES = [
    "codex-engine-1", "codex-engine-2", "codex-engine-3", "codex-engine-4",
    "codex-engine-5", "codex-engine-6", "codex-engine-7", "codex-engine-8",
    "codex-engine-9", "codex-engine-10", "codex-engine-11", "codex-engine-12",
    "witness-aggregator"
]

def tail_engine(engine_name: str, lines: int = 50):
    """Get tail of engine logs."""
    try:
        result = subprocess.run(
            ["docker", "logs", "--tail", str(lines), engine_name],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return result.stdout.strip().split('\n') if result.stdout else []
    except Exception as e:
        return [f"ERROR: {e}"]
    
    return []

def main():
    """Stream tails from all engines."""
    print("\n" + "=" * 160)
    print(f"[LIVE TAIL] All 13 Engines — {datetime.now().isoformat()}")
    print("=" * 160)
    print("Each engine shows last 50 lines. CTRL+C to exit.\n")
    
    try:
        while True:
            print("\n" + "=" * 160)
            print(f"[UPDATE] {datetime.now().isoformat()}")
            print("=" * 160)
            
            for engine_name in ENGINES:
                print(f"\n[{engine_name}]")
                print("-" * 160)
                
                logs = tail_engine(engine_name, 50)
                if logs:
                    for log_line in logs[-10:]:  # Last 10 lines
                        if log_line.strip():
                            print(f"  {log_line[:155]}")
                else:
                    print("  (no logs)")
            
            print("\n" + "=" * 160)
            print("Sleeping 5 seconds... (CTRL+C to stop)")
            import time
            time.sleep(5)
    
    except KeyboardInterrupt:
        print(f"\n\n[STOPPED] {datetime.now().isoformat()}")
        sys.exit(0)

if __name__ == "__main__":
    main()
