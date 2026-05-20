import csv, json, requests
from pathlib import Path

URL = "https://raw.githubusercontent.com/datasets/finance-vix/master/data/vix-daily.csv"

def main():
    r = requests.get(URL, timeout=10)
    rows = list(csv.DictReader(r.text.splitlines()))[-10:]
    packet = {
        "source": "public-vix",
        "rows": rows,
        "byte_stream": list(json.dumps(rows).encode("utf-8"))
    }
    Path("market_anchor_vix.json").write_text(json.dumps(packet, indent=2))
    print("VIX anchor updated.")

if __name__ == "__main__":
    main()
