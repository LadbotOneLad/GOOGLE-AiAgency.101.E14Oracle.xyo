# -*- coding: utf-8 -*-
import subprocess
import sys
from pathlib import Path

ANCHORS = [
    "market_anchor_safe.py",
    "market_anchor_sp500.py",
    "market_anchor_vix.py",
    "market_anchor_fx.py",
    "market_anchor_entropy.py",
]

def main():
    base = Path(__file__).parent
    for script in ANCHORS:
        path = base / script
        if path.exists():
            print(f"Running {script}...")
            subprocess.run([sys.executable, str(path)], check=True)
        else:
            print(f"Skipping missing {script}")
    print("All anchors updated.")

if __name__ == "__main__":
    main()
