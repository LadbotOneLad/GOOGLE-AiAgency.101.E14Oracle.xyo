import json, requests
from pathlib import Path

URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.json"

def main():
    data = requests.get(URL, timeout=10).json()
    packet = {
        "source": "ecb-fx-reference",
        "rates": data,
        "byte_stream": list(json.dumps(data).encode("utf-8"))
    }
    Path("market_anchor_fx.json").write_text(json.dumps(packet, indent=2))
    print("FX anchor updated.")

if __name__ == "__main__":
    main()
