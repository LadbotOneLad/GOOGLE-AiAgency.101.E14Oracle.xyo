import os, json, random
from pathlib import Path

def main():
    entropy = [random.randint(0, 255) for _ in range(256)]
    packet = {
        "source": "synthetic-entropy",
        "entropy": entropy,
        "byte_stream": entropy
    }
    Path("market_anchor_entropy.json").write_text(json.dumps(packet, indent=2))
    print("Synthetic entropy anchor updated.")

if __name__ == "__main__":
    main()
