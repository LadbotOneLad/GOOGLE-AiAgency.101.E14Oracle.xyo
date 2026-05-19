# -*- coding: utf-8 -*-
import json
from pathlib import Path
import subprocess

def run_engine(path):
    print(f"--- Running {path} ---")
    subprocess.run(["python", path], check=True)

def main():
    base = Path(__file__).parent

    atm = base / "Atmospheric" / "atmospheric_truth_main.py"
    if atm.exists():
        run_engine(str(atm))

    xyo = base / "XYO" / "wire_ytdlp_to_xyo.py"
    if xyo.exists():
        run_engine(str(xyo))

    market = base / "Market" / "market_anchor_multi.py"
    if market.exists():
        run_engine(str(market))

if __name__ == "__main__":
    main()
