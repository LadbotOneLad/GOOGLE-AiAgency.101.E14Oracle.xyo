# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pathlib import Path
import json

app = FastAPI(title="Unified Truth Engine Dashboard")

BASE = Path(__file__).parent
MARKET = BASE / "Market"

def load(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}

@app.get("/market")
def market_state():
    return {
        "safe": load(MARKET / "market_witness_batch.json"),
        "sp500": load(MARKET / "market_anchor_sp500.json"),
        "vix": load(MARKET / "market_anchor_vix.json"),
        "fx": load(MARKET / "market_anchor_fx.json"),
        "entropy": load(MARKET / "market_anchor_entropy.json"),
    }

@app.get("/unified")
def unified_packet():
    return load(BASE / "unified_truth_packet.json")
