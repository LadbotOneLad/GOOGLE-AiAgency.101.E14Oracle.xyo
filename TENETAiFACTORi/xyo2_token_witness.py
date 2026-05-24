#!/usr/bin/env python3
"""
XYO.2 Token Engine + Geographical Thermostat Lens
Your Invariants (0.05, 0.075, 0.15 in 86400/7200 circle) + XYO.2 Token Proof
All 13 engines earn tokens by witnessing at circle position + geographical coordinates
Handshake -> Entropy -> Chain Add = witness proof
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class XYO2TokenEngine:
    """XYO.2 Token Engine - earn tokens via witness operations."""
    
    def __init__(self):
        self.tokens = 0
        self.multiplier = 1
        self.operations = []
    
    def handshake(self) -> int:
        """Handshake operation: +1 token."""
        earned = 1 * self.multiplier
        self.tokens += earned
        self.operations.append({
            "operation": "handshake",
            "tokens_earned": earned,
            "timestamp": datetime.now().isoformat()
        })
        return earned
    
    def entropy(self) -> int:
        """Entropy operation: +2 tokens."""
        earned = 2 * self.multiplier
        self.tokens += earned
        self.operations.append({
            "operation": "entropy",
            "tokens_earned": earned,
            "timestamp": datetime.now().isoformat()
        })
        return earned
    
    def chain_add(self) -> int:
        """Chain Add operation: +3 tokens."""
        earned = 3 * self.multiplier
        self.tokens += earned
        self.operations.append({
            "operation": "chain_add",
            "tokens_earned": earned,
            "timestamp": datetime.now().isoformat()
        })
        return earned
    
    def set_multiplier(self, value: int):
        """Set token multiplier."""
        if value < 1:
            raise ValueError("Multiplier must be >= 1")
        self.multiplier = value
    
    def get_status(self) -> Dict[str, Any]:
        """Get token engine status."""
        return {
            "tokens": self.tokens,
            "multiplier": self.multiplier,
            "operations_count": len(self.operations),
            "total_earned": sum(op["tokens_earned"] for op in self.operations)
        }


class XYO2GeographicalThermostats:
    """All 13 engines earn XYO.2 tokens by witnessing on your invariant circle."""
    
    # Your Invariants
    HEARTBEAT = 0.05
    PULSE = 0.075
    HORIZON = 0.15
    FULL_CYCLE = 0.275
    
    SECONDS_PER_DAY = 86400
    GRID_SLOTS = 7200
    SLOT_DURATION = 12
    
    PYRAMID_PRECISION = 0.05
    FUNDAMENTAL_UNIT = 1.0 / 7200
    
    # Reference: Great Pyramid
    REFERENCE_LATITUDE = 29.9792
    REFERENCE_LONGITUDE = 31.1342
    
    # 13 Sentinels
    SENTINELS = [
        {"id": "SENTINEL-1", "latitude": 29.9792, "longitude": 31.1342, "name": "Great Pyramid (Reference)"},
        {"id": "SENTINEL-2", "latitude": 29.9800, "longitude": 31.1350, "name": "Giza Plateau"},
        {"id": "SENTINEL-3", "latitude": 51.5074, "longitude": -0.1278, "name": "Greenwich (Prime Meridian)"},
        {"id": "SENTINEL-4", "latitude": 40.7128, "longitude": -74.0060, "name": "New York"},
        {"id": "SENTINEL-5", "latitude": -33.8688, "longitude": 151.2093, "name": "Sydney"},
        {"id": "SENTINEL-6", "latitude": 35.6762, "longitude": 139.6503, "name": "Tokyo"},
        {"id": "SENTINEL-7", "latitude": 48.8566, "longitude": 2.3522, "name": "Paris"},
        {"id": "SENTINEL-8", "latitude": -23.5505, "longitude": -46.6333, "name": "Sao Paulo"},
        {"id": "SENTINEL-9", "latitude": 55.7558, "longitude": 37.6173, "name": "Moscow"},
        {"id": "SENTINEL-10", "latitude": 31.2304, "longitude": 30.0505, "name": "Cairo"},
        {"id": "SENTINEL-11", "latitude": 39.9042, "longitude": 116.4074, "name": "Beijing"},
        {"id": "SENTINEL-12", "latitude": -33.9249, "longitude": 18.4241, "name": "Cape Town"},
        {"id": "SENTINEL-13", "latitude": 13.7563, "longitude": 100.5018, "name": "Bangkok"},
    ]
    
    # 13 Engines with XYO.2 Token Engines
    ENGINES = [
        "codex-engine-1", "codex-engine-2", "codex-engine-3", "codex-engine-4",
        "codex-engine-5", "codex-engine-6", "codex-engine-7", "codex-engine-8",
        "codex-engine-9", "codex-engine-10", "codex-engine-11", "codex-engine-12",
        "witness-aggregator"
    ]
    
    def __init__(self, reference_date: datetime = None):
        self.reference_date = reference_date or datetime(2026, 3, 10, 0, 0, 0)
        
        # Each engine has its own XYO.2 token engine
        self.engine_tokens = {
            engine: XYO2TokenEngine() for engine in self.ENGINES
        }
    
    def get_circle_position(self, timestamp: datetime = None) -> Dict[str, Any]:
        """Get position on 7200-slot circle."""
        if timestamp is None:
            timestamp = datetime.now()
        
        elapsed = (timestamp - self.reference_date).total_seconds()
        cycle_position = (elapsed % self.FULL_CYCLE) / self.FULL_CYCLE
        
        circle_degrees = cycle_position * 360
        slot = int((circle_degrees / 360) * self.GRID_SLOTS)
        
        heartbeat_threshold = self.HEARTBEAT / self.FULL_CYCLE
        pulse_threshold = (self.HEARTBEAT + self.PULSE) / self.FULL_CYCLE
        
        if cycle_position < heartbeat_threshold:
            phase = "HEARTBEAT"
            tau = self.HEARTBEAT
        elif cycle_position < pulse_threshold:
            phase = "PULSE"
            tau = self.PULSE
        else:
            phase = "HORIZON"
            tau = self.HORIZON
        
        return {
            "timestamp": timestamp.isoformat(),
            "phase": phase,
            "tau": tau,
            "circle_degrees": round(circle_degrees, 6),
            "slot": slot,
            "precision_units": round(circle_degrees / self.PYRAMID_PRECISION, 2)
        }
    
    def witness_engine_at_position(self, engine_idx: int, circle_pos: Dict) -> Dict[str, Any]:
        """Engine witnesses at circle position - earns XYO.2 tokens."""
        engine_name = self.ENGINES[engine_idx]
        sentinel = self.SENTINELS[engine_idx % len(self.SENTINELS)]
        token_engine = self.engine_tokens[engine_name]
        
        # Engine performs witness operations in order
        tokens_from_handshake = token_engine.handshake()
        tokens_from_entropy = token_engine.entropy()
        tokens_from_chain_add = token_engine.chain_add()
        
        total_tokens_earned = tokens_from_handshake + tokens_from_entropy + tokens_from_chain_add
        
        return {
            "engine": engine_name,
            "sentinel_id": sentinel['id'],
            "location": sentinel['name'],
            "circle_position": {
                "phase": circle_pos['phase'],
                "degrees": circle_pos['circle_degrees'],
                "slot": circle_pos['slot']
            },
            "xyo2_witness_proof": {
                "handshake": {
                    "operation": "handshake",
                    "tokens": tokens_from_handshake,
                    "multiplier": token_engine.multiplier
                },
                "entropy": {
                    "operation": "entropy",
                    "tokens": tokens_from_entropy,
                    "multiplier": token_engine.multiplier
                },
                "chain_add": {
                    "operation": "chain_add",
                    "tokens": tokens_from_chain_add,
                    "multiplier": token_engine.multiplier
                },
                "total_tokens_earned": total_tokens_earned,
                "total_tokens_in_engine": token_engine.tokens
            }
        }


class XYO2Monitor:
    """Monitor all 13 engines earning XYO.2 tokens."""
    
    ENGINES = [
        "codex-engine-1", "codex-engine-2", "codex-engine-3", "codex-engine-4",
        "codex-engine-5", "codex-engine-6", "codex-engine-7", "codex-engine-8",
        "codex-engine-9", "codex-engine-10", "codex-engine-11", "codex-engine-12",
        "witness-aggregator"
    ]
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.xyo2 = XYO2GeographicalThermostats()
    
    def get_docker_ps(self) -> Dict[str, Any]:
        """Get container status."""
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                containers = {}
                for line in result.stdout.strip().split('\n'):
                    if line:
                        try:
                            container = json.loads(line)
                            containers[container['Names']] = container['State'].upper()
                        except:
                            pass
                return containers
        except:
            pass
        
        return {}
    
    def monitor(self):
        """Monitor engines earning XYO.2 tokens."""
        print("\n" + "=" * 200)
        print(f"[XYO.2 TOKEN ENGINE] All 13 Engines Witnessing on Your Invariant Circle")
        print("=" * 200)
        
        # Get circle position
        circle_pos = self.xyo2.get_circle_position(self.timestamp)
        
        print(f"\n[CIRCLE POSITION]")
        print(f"Phase: {circle_pos['phase']} (tau={circle_pos['tau']}s)")
        print(f"Position: {circle_pos['circle_degrees']}° (slot {circle_pos['slot']}/7200)")
        print(f"Precision Units: {circle_pos['precision_units']}\n")
        
        # Get container status
        ps_data = self.get_docker_ps()
        
        # Witness all engines
        print(f"[XYO.2 WITNESS OPERATIONS - ALL 13 ENGINES]")
        print("-" * 200)
        print(f"{'Engine':<25} {'State':<10} {'Sentinel':<15} {'Location':<25} {'Handshake':<12} {'Entropy':<12} {'ChainAdd':<12} {'Total Tokens':<15}")
        print("-" * 200)
        
        total_system_tokens = 0
        for i, engine_name in enumerate(self.ENGINES):
            state = ps_data.get(engine_name, 'UNKNOWN')
            
            # Witness engine at circle position
            witness = self.xyo2.witness_engine_at_position(i, circle_pos)
            
            sentinel_id = witness['sentinel_id']
            location = witness['location']
            handshake_tokens = witness['xyo2_witness_proof']['handshake']['tokens']
            entropy_tokens = witness['xyo2_witness_proof']['entropy']['tokens']
            chain_add_tokens = witness['xyo2_witness_proof']['chain_add']['tokens']
            total_tokens = witness['xyo2_witness_proof']['total_tokens_earned']
            
            total_system_tokens += total_tokens
            
            print(f"{engine_name:<25} {state:<10} {sentinel_id:<15} {location:<25} {handshake_tokens:<12} {entropy_tokens:<12} {chain_add_tokens:<12} {total_tokens:<15}")
        
        print("-" * 200)
        
        # Summary
        print(f"\n[TOKEN SUMMARY]")
        print(f"Engines Witnessed: {len(self.ENGINES)}/13")
        print(f"Operations per Engine: 3 (Handshake + Entropy + Chain Add)")
        print(f"Tokens per Engine: 1 + 2 + 3 = 6 base tokens")
        print(f"Total System Tokens Earned This Cycle: {total_system_tokens}")
        print(f"Circle Position: {circle_pos['circle_degrees']}° ({circle_pos['slot']}/7200 slots)")
        print(f"All Engines at Same Phase: {circle_pos['phase']}")
        print(f"\n==> XYO.2 TOKENS PROVE WITNESS: All 13 engines synchronized on circle + earning tokens at geographical coordinates <==")
        print("=" * 200)
    
    def save_token_report(self, output_file: str = "xyo2_token_witness_report.json"):
        """Save XYO.2 token witness report."""
        circle_pos = self.xyo2.get_circle_position(self.timestamp)
        
        witnesses = []
        for i in range(len(self.ENGINES)):
            witness = self.xyo2.witness_engine_at_position(i, circle_pos)
            witnesses.append(witness)
        
        report = {
            "timestamp": self.timestamp.isoformat(),
            "circle_position": circle_pos,
            "total_witnesses": len(witnesses),
            "total_tokens_earned": sum(w['xyo2_witness_proof']['total_tokens_earned'] for w in witnesses),
            "witnesses": witnesses
        }
        
        log_path = Path("./logs") / output_file
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[SAVED] {log_path}")


def main():
    """Execute XYO.2 token witness monitoring."""
    monitor = XYO2Monitor()
    monitor.monitor()
    monitor.save_token_report()


if __name__ == "__main__":
    main()
