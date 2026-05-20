import json, requests
from pathlib import Path

URL = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.json"

def main():
    data = requests.get(URL, timeout=10).json()
    packet = {
        "source": "public-sp500-metadata",
        "count": len(data),
        "byte_stream": list(json.dumps(data).encode("utf-8"))
    }
    Path("market_anchor_sp500.json").write_text(json.dumps(packet, indent=2))
    print("SP500 metadata anchor updated.")

if __name__ == "__main__":
    main()
