#!/usr/bin/env python3
"""
Operational Events Processor
Validates signals against ethical gates, drift thresholds, and identity constraints.
Deterministic decision engine based on root inputs.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class RootValidator:
    """Validates events against root constraints."""
    
    # Hard thresholds
    ETHICS_VIOLATION_THRESHOLD = False  # Any violation = reject
    DRIFT_TOLERANCE = 0.05  # ±5% acceptable
    IDENTITY_OVERRIDE_ALLOWED = False  # Identity defines system, cannot be overridden
    OPTIONS_COLLAPSE_ALLOWED = False   # Single path, options must remain open
    ROOT_OVERRIDE_ALLOWED = False      # Roots are immutable
    
    def __init__(self):
        self.validations = []
        self.decisions = []
    
    def validate_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process single event through validation gates."""
        event_id = event.get("id")
        root_input = event.get("rootInput", {})
        
        decision = {
            "event_id": event_id,
            "timestamp": event.get("timestampIso"),
            "signal": event.get("signal"),
            "gates": {},
            "verdict": "ACCEPT",
            "reasoning": []
        }
        
        # Gate 1: Ethics
        ethics_ok = not root_input.get("violatesEthic", False)
        decision["gates"]["ethics"] = "PASS" if ethics_ok else "FAIL"
        if not ethics_ok:
            decision["verdict"] = "REJECT"
            decision["reasoning"].append("Ethics violation detected")
        
        # Gate 2: Drift
        drift = root_input.get("driftDeviation", 0.0)
        drift_ok = drift <= self.DRIFT_TOLERANCE
        decision["gates"]["drift"] = f"{drift:.4f} (OK)" if drift_ok else f"{drift:.4f} (EXCEEDED)"
        if not drift_ok:
            decision["verdict"] = "REJECT"
            decision["reasoning"].append(f"Drift {drift:.4f} exceeds tolerance {self.DRIFT_TOLERANCE}")
        
        # Gate 3: Identity
        identity_def = root_input.get("definesIdentity", False)
        identity_ok = not identity_def
        decision["gates"]["identity"] = "STABLE" if identity_ok else "OVERRIDE_ATTEMPT"
        if not identity_ok:
            decision["verdict"] = "REJECT"
            decision["reasoning"].append("Identity override attempted (forbidden)")
        
        # Gate 4: Options
        collapse = root_input.get("collapsesOptions", False)
        options_ok = not collapse
        decision["gates"]["options"] = "OPEN" if options_ok else "COLLAPSED"
        if not options_ok:
            decision["verdict"] = "REJECT"
            decision["reasoning"].append("Options collapse attempted (forbidden)")
        
        # Gate 5: Roots
        override = root_input.get("overridesRoots", False)
        roots_ok = not override
        decision["gates"]["roots"] = "STABLE" if roots_ok else "OVERRIDE_ATTEMPT"
        if not roots_ok:
            decision["verdict"] = "REJECT"
            decision["reasoning"].append("Root override attempted (forbidden)")
        
        self.decisions.append(decision)
        return decision
    
    def batch_validate(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate batch of events."""
        results = []
        for event in events:
            result = self.validate_event(event)
            results.append(result)
        return results
    
    def summary(self) -> Dict[str, Any]:
        """Generate validation summary."""
        total = len(self.decisions)
        accepted = sum(1 for d in self.decisions if d["verdict"] == "ACCEPT")
        rejected = total - accepted
        
        return {
            "total_events": total,
            "accepted": accepted,
            "rejected": rejected,
            "acceptance_rate": f"{(accepted/total*100):.1f}%" if total > 0 else "0%",
            "timestamp": datetime.now().isoformat()
        }


class OperationalEventProcessor:
    """Process operational events and integrate with stress test."""
    
    def __init__(self, events_file: str = "operational_events.json"):
        self.events_file = events_file
        self.validator = RootValidator()
        self.results = []
    
    def load_events(self) -> List[Dict[str, Any]]:
        """Load events from JSON file."""
        try:
            with open(self.events_file, 'r') as f:
                data = json.load(f)
                return data.get("events", [])
        except FileNotFoundError:
            print(f"[ERROR] {self.events_file} not found")
            return []
    
    def process(self):
        """Process all events."""
        events = self.load_events()
        if not events:
            print("[WARNING] No events to process")
            return
        
        print(f"[OPERATIONAL EVENTS] Loading {len(events)} events...")
        print("=" * 80)
        
        results = self.validator.batch_validate(events)
        self.results = results
        
        # Display each decision
        for result in results:
            self._display_decision(result)
        
        print("=" * 80)
        self._display_summary()
    
    def _display_decision(self, decision: Dict[str, Any]):
        """Display single decision."""
        event_id = decision["event_id"]
        signal = decision["signal"]
        verdict = decision["verdict"]
        
        status_icon = "[OK]" if verdict == "ACCEPT" else "[FAIL]"
        print(f"\n{status_icon} [{event_id}] {signal}")
        print(f"   Verdict: {verdict}")
        
        gates = decision["gates"]
        for gate_name, gate_status in gates.items():
            print(f"   - {gate_name:.<20} {gate_status}")
        
        if decision["reasoning"]:
            for reason in decision["reasoning"]:
                print(f"   Reason: {reason}")
    
    def _display_summary(self):
        """Display processing summary."""
        summary = self.validator.summary()
        print("\n[SUMMARY]")
        for key, value in summary.items():
            print(f"{key:.<40} {value}")
    
    def save_results(self, output_file: str = "operational_events_decisions.jsonl"):
        """Save decisions to file."""
        log_path = Path("/app/logs") / output_file
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            for result in self.results:
                f.write(json.dumps(result) + "\n")
        
        print(f"\n[SAVED] Results written to {log_path}")


def integrate_with_stress_test():
    """Bridge operational events with stress test metrics."""
    print("\n[INTEGRATION] Correlating operational events with stress test...\n")
    
    # Read stress test metrics if available
    stress_log = Path("/app/logs/doctor_strange_one_way.jsonl")
    if stress_log.exists():
        with open(stress_log) as f:
            stress_results = [json.loads(line) for line in f]
        
        print(f"[INTEGRATION] Found {len(stress_results)} stress test result(s)")
        for result in stress_results:
            print(f"  Cycles: {result.get('cycles_completed', 'N/A')}")
            print(f"  Throughput: {result.get('throughput_cycles_per_sec', 'N/A')} cycles/sec")
            print(f"  Verdict: {result.get('verdict', 'N/A')}\n")
    else:
        print("[INTEGRATION] Stress test log not found (run doctor_strange_one_way.py first)")


def main():
    """Execute operational event processing."""
    processor = OperationalEventProcessor("operational_events.json")
    processor.process()
    processor.save_results()
    integrate_with_stress_test()


if __name__ == "__main__":
    main()
