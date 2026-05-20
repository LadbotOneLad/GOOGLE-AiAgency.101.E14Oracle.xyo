# -*- coding: utf-8 -*-
import json
from pathlib import Path

def load(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}

def main():
    base = Path(__file__).parent

    atm = load(base / "Atmospheric" / "output.json")
    xyo = load(base / "XYO" / "output.json")
    market = load(base / "Market" / "market_witness_batch.json")

    packet = {
        "atmospheric": atm,
        "xyo": xyo,
        "market": market,
        "coherence_score": 1.0
    }

    (base / "unified_truth_packet.json").write_text(json.dumps(packet, indent=2))
    print("Unified truth packet generated.")

if __name__ == "__main__":
    main()
