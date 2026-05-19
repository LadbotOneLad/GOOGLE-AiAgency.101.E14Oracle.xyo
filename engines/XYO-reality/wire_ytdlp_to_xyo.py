# -*- coding: utf-8 -*-
import json
from pathlib import Path
from collections import Counter
from sympy import Matrix, symbols
from xyo_witness import xyo_witness

XYO_NODE3 = "466e84dfcbfbae8d50ad4276e8f2b5d37e8834a8"

def load_photons():
    meta_dir = Path("..\\yt-dlp\\runtime\\metadata")
    files = sorted(meta_dir.glob("*.info.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise RuntimeError("No yt-dlp metadata found")
    return files[0], list(files[0].read_bytes())

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
    source_file, photons = load_photons()
    states, P = build_markov(photons)
    dist = stationary(P)
    s = score(dist)

    out = {
        "xyo_node": XYO_NODE3,
        "states": states[:50],
        "stationary_distribution": dist[:50],
        "reality_score": s
    }

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)
    (out_dir / "reality_chain.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

    metrics = {
        "reality_score": s,
        "states_sampled": len(states),
        "bytes_observed": len(photons)
    }

    witness_packet = xyo_witness(
        engine="yt-dlp-xyo-reality",
        source_path=source_file,
        metrics=metrics,
        tags=["yt-dlp", "markov", "xyo", "reality"]
    )

    print("XYO WITNESS PACKET:")
    print(json.dumps(witness_packet, indent=2))

if __name__ == "__main__":
    main()
