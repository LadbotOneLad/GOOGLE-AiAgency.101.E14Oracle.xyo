# -*- coding: utf-8 -*-
import json
import time
import urllib.request
from urllib.error import HTTPError
from pathlib import Path
from collections import Counter
from sympy import Matrix, symbols
from xyo_witness import xyo_witness

XYO_NODE3 = "466e84dfcbfbae8d50ad4276e8f2b5d37e8834a8"

SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

def fetch_market_bytes(symbol, retries=5):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"

    for attempt in range(retries):
        try:
            return urllib.request.urlopen(url).read(), url
        except HTTPError as e:
            if e.code == 429:
                time.sleep(1.5 + attempt)  # backoff
                continue
            raise
    raise RuntimeError(f"Failed to fetch {symbol} after retries")

def build_markov(byte_seq):
    transitions = Counter()
    counts = Counter()
    for a, b in zip(byte_seq, byte_seq[1:]):
        transitions[(a, b)] += 1
        counts[a] += 1
    states = sorted(set(byte_seq))
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    P = [[0]*n for _ in range(n)]
    for (a, b), c in transitions.items():
        i, j = idx[a], idx[b]
        P[i][j] = c / counts[a]
    return states, Matrix(P)

def stationary(P):
    n = P.shape[0]
    p = symbols('p0:'+str(n))
    vec = Matrix(p)
    eqs = list((vec.T * P - vec.T)[0, :]) + [sum(p) - 1]
    sol = Matrix(eqs).gauss_jordan_solve(Matrix([0]*n + [0]))[0]
    return [float(s.evalf()) for s in sol]

def score(dist):
    import math
    eps = 1e-12
    H = -sum(p*math.log(p+eps) for p in dist)
    maxH = math.log(len(dist)+eps)
    return float(H / (maxH+eps))

def main():
    out_dir = Path("output") / "market"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_witnesses = []

    for symbol in SYMBOLS:
        raw_bytes, source_url = fetch_market_bytes(symbol)
        byte_seq = list(raw_bytes)

        states, P = build_markov(byte_seq)
        dist = stationary(P)
        s = score(dist)

        metrics = {
            "symbol": symbol,
            "reality_score": s,
            "states_sampled": len(states),
            "bytes_observed": len(byte_seq),
            "source_url": source_url
        }

        pseudo_path = Path(f"MARKET_STREAM_{symbol}")

        witness = xyo_witness(
            engine="market-xyo-reality",
            source_path=pseudo_path,
            metrics=metrics,
            tags=["market", "xyo", "reality", "markov"]
        )

        all_witnesses.append(witness)

        time.sleep(1.2)  # prevent 429

    (out_dir / "market_witness_batch.json").write_text(json.dumps(all_witnesses, indent=2))
    print(json.dumps(all_witnesses, indent=2))

if __name__ == "__main__":
    main()
