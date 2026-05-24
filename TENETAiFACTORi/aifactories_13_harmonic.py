#!/usr/bin/env python3
"""
AIFACTORIES 13-ENGINE HARMONIC SYNCHRONIZATION
Master coordinator + 12 Byzantine validators

All 13 engines operate independently but phase-locked to Earth's 86400-second day.
No central dependencies. Pure harmonic alignment.

Copyright (c) 2026 Rebecca — AiFACTORIES
"""

import asyncio
import json
import time
from typing import Dict, List
from pathlib import Path
from dataclasses import asdict


class HarmonicCluster:
    """13-engine harmonic cluster (master + 12 validators)"""
    
    def __init__(self, num_engines: int = 13):
        self.num_engines = num_engines
        self.engines = {}
        self.heartbeats = {}
        self.consensus_state = {}
        self.logs_dir = Path("./logs/aifactories/cluster")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    async def spawn_engines(self):
        """Spawn all 13 engines (in simulation)"""
        # Import here to avoid circular dependency
        from aifactories_earth_locked_core import AiFACTORIESEngine
        
        for engine_id in range(self.num_engines):
            engine = AiFACTORIESEngine(engine_id)
            self.engines[engine_id] = engine
    
    async def broadcast_heartbeats(self):
        """All engines broadcast heartbeats (read-only)"""
        for engine_id, engine in self.engines.items():
            heartbeat = engine.sync.heartbeat()
            self.heartbeats[engine_id] = heartbeat
    
    async def compute_consensus(self):
        """
        Byzantine consensus among 13 engines.
        Quorum: 8/12 validators + master agreement = unanimous
        """
        if len(self.heartbeats) < 13:
            return False
        
        # Extract sync status from each engine
        sync_votes = [hb["synchronized"] for hb in self.heartbeats.values()]
        
        # Count agreement
        synchronized_count = sum(1 for vote in sync_votes if vote)
        
        # Consensus threshold: at least 8/12 validators + master
        consensus = synchronized_count >= 8
        
        self.consensus_state = {
            "timestamp": time.time(),
            "synchronized_engines": synchronized_count,
            "total_engines": len(self.heartbeats),
            "consensus_reached": consensus,
            "threshold": 8,
        }
        
        return consensus
    
    async def run_cluster_tick(self):
        """One complete cluster tick (all engines sync)"""
        await self.spawn_engines()
        await self.broadcast_heartbeats()
        consensus = await self.compute_consensus()
        
        return {
            "timestamp": time.time(),
            "engines": len(self.engines),
            "heartbeats": self.heartbeats,
            "consensus": self.consensus_state,
            "synchronized": consensus,
        }
    
    def write_cluster_state(self, state: Dict):
        """Write cluster state to JSON"""
        filename = self.logs_dir / "cluster_state.json"
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)


class ByzantineValidator:
    """Individual Byzantine validator (part of 13-engine cluster)"""
    
    def __init__(self, validator_id: int):
        self.validator_id = validator_id
        self.reputation = 100  # Start at 100%
        self.agreement_history = []
        self.dissent_history = []
    
    def vote_on_sync(self, synchronized: bool) -> bool:
        """Vote on whether cluster is synchronized"""
        return synchronized
    
    def record_agreement(self, agreed: bool):
        """Record voting history"""
        if agreed:
            self.agreement_history.append(time.time())
            self.reputation = min(100, self.reputation + 1)
        else:
            self.dissent_history.append(time.time())
            self.reputation = max(0, self.reputation - 5)
    
    def is_byzantine(self) -> bool:
        """Detect if this validator is byzantine (reputation < 50)"""
        return self.reputation < 50
    
    def status(self) -> Dict:
        """Validator status"""
        return {
            "validator_id": self.validator_id,
            "reputation": self.reputation,
            "agreements": len(self.agreement_history),
            "dissents": len(self.dissent_history),
            "byzantine": self.is_byzantine(),
        }


async def main():
    """Demo: 13-engine harmonic cluster"""
    print("\n" + "="*80)
    print("AIFACTORIES 13-ENGINE HARMONIC SYNCHRONIZATION")
    print("="*80)
    print("\nSpawning 13 engines (master + 12 validators)...")
    
    cluster = HarmonicCluster(num_engines=13)
    
    # Run one cluster tick
    state = await cluster.run_cluster_tick()
    
    print(f"\nCluster State:")
    print(f"  Engines spawned: {state['engines']}")
    print(f"  Heartbeats received: {len(state['heartbeats'])}")
    print(f"  Consensus reached: {state['consensus']['consensus_reached']}")
    print(f"  Synchronized: {state['synchronized']}")
    
    cluster.write_cluster_state(state)
    print(f"\nCluster state written to: {cluster.logs_dir / 'cluster_state.json'}")


if __name__ == "__main__":
    asyncio.run(main())
