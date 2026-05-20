# -*- coding: utf-8 -*-
import json
from pathlib import Path

def load(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}

def main():
    base = Path(__file__).parent
    market = base / "Market"

    packet = {
        "atmospheric": load(base / "Atmospheric" / "output.json"),
        "xyo": load(base / "XYO" / "output.json"),
        "market": {
            "safe": load(market / "market_witness_batch.json"),
            "sp500": load(market / "market_anchor_sp500.json"),
            "vix": load(market / "market_anchor_vix.json"),
            "fx": load(market / "market_anchor_fx.json"),
            "entropy": load(market / "market_anchor_entropy.json"),
        },
        "coherence_score": 1.0
    }

    (base / "unified_truth_packet.json").write_text(
        json.dumps(packet, indent=2)
    )
    print("Unified truth packet generated.")

if __name__ == "__main__":
    main()
