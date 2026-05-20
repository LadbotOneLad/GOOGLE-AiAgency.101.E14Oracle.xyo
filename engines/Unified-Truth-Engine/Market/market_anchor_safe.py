# -*- coding: utf-8 -*-
import csv
import json
import requests
from pathlib import Path

# Public, safe, regulator-friendly GitHub CSV (NO Yahoo)
URL = "https://raw.githubusercontent.com/datasets/finance-vix/master/data/vix-daily.csv"

def fetch_public_market_data():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    lines = r.text.splitlines()
    reader = csv.DictReader(lines)
    return list(reader)[-5:]  # last 5 rows only

def convert_to_bytes(rows):
    text = json.dumps(rows)
    return list(text.encode("utf-8"))

def main():
    base = Path(__file__).parent
    rows = fetch_public_market_data()
    byte_stream = convert_to_bytes(rows)

    packet = {
        "source": "public-github-vix",
        "rows": rows,
        "byte_stream": byte_stream
    }

    (base / "market_witness_batch.json").write_text(
        json.dumps(packet, indent=2)
    )

    print("Safe market anchor updated.")

if __name__ == "__main__":
    main()
