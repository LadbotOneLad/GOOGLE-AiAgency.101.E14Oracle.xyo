# Codex 6.65: Witness Aggregator Service
# Collects and aggregates XYO + BOM witness data from all 12 engines

import os
import json
import time
from datetime import datetime
from pathlib import Path
from geocryphical_witness import GeocryphicalWitnessAggregator


def run_witness_aggregator():
    """Continuous witness aggregation service"""
    aggregator = GeocryphicalWitnessAggregator()
    log_dir = Path("/logs/witness_aggregation")
    log_dir.mkdir(parents=True, exist_ok=True)

    print("Starting Witness Aggregator Service...")
    print(f"Aggregation logs: {log_dir}")

    start_time = time.time()
    iteration = 0

    try:
        while True:
            iteration += 1

            # Simulate witness evaluations from distributed engines
            for engine_id in range(1, 13):
                phase = (iteration + engine_id) / 100.0 % 1.0
                coherence = 0.5 + (iteration % 10) * 0.05
                power = 0.6 + (iteration % 20) * 0.02

                # Geographic distribution (Australia)
                if engine_id <= 4:
                    lat, lon = -33.8688, 151.2093  # Sydney
                elif engine_id <= 8:
                    lat, lon = -37.8136, 144.9631  # Melbourne
                else:
                    lat, lon = -31.9505, 115.8605  # Perth

                witness = aggregator.evaluate_with_witness(
                    phase=phase,
                    coherence=coherence,
                    power=power,
                    latitude=lat,
                    longitude=lon,
                    location="Sydney" if engine_id <= 4 else ("Melbourne" if engine_id <= 8 else "Perth"),
                )

            # Export summary every 50 iterations
            if iteration % 50 == 0:
                summary = aggregator.get_witness_summary()
                summary_file = log_dir / f"witness_summary_{iteration}.json"

                with open(summary_file, "w") as f:
                    json.dump(
                        {
                            "timestamp": datetime.utcnow().isoformat(),
                            "iteration": iteration,
                            "runtime_seconds": time.time() - start_time,
                            "summary": summary,
                        },
                        f,
                        indent=2,
                    )

                print(
                    f"[{iteration:04d}] Witnesses: {summary['total_witnesses']} | "
                    f"Aligned: {summary['alignment_rate']:.1%} | "
                    f"Score: {summary['avg_consensus_score']:.3f}"
                )

            # Export all witnesses to JSONL periodically
            if iteration % 100 == 0:
                export_file = log_dir / f"witnesses_{int(start_time)}_{iteration}.jsonl"
                aggregator.export_witness_log(str(export_file))
                print(f"Exported {len(aggregator.witnesses)} witnesses to {export_file.name}")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nWitness Aggregator shutting down...")
        final_summary = aggregator.get_witness_summary()
        print(f"Final Summary: {json.dumps(final_summary, indent=2)}")
        aggregator.export_witness_log(str(log_dir / "witnesses_final.jsonl"))


if __name__ == "__main__":
    run_witness_aggregator()
