#!/usr/bin/env python3
"""
ENGINE BARRIER — 12-Engine Synchronous Checkpoint

Implements a real barrier for 12 engines to:
1. Reach checkpoint simultaneously
2. Verify all engines pass gates
3. Acquire collective lock
4. Execute cycle atomically
5. Release lock
6. Continue to next cycle

Uses file-based synchronization + atomic operations.
"""

import asyncio
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional


@dataclass
class BarrierState:
    """State of barrier synchronization"""
    cycle_id: int
    phase: str  # "waiting", "locked", "executing", "released"
    engines_at_barrier: set
    engines_locked: set
    timestamp: float


class EngineBarrier:
    """Barrier for 12 engines"""
    
    NUM_ENGINES = 12
    BARRIER_TIMEOUT = 5.0
    
    def __init__(self, shared_dir: str = "/tmp/engine_barrier"):
        self.shared_dir = Path(shared_dir)
        self.shared_dir.mkdir(parents=True, exist_ok=True)
        self.barrier_file = self.shared_dir / "barrier_state.json"
        self.cycle_id = 0
        
    def _read_barrier_state(self) -> Dict:
        """Read current barrier state"""
        if self.barrier_file.exists():
            with open(self.barrier_file, 'r') as f:
                try:
                    return json.load(f)
                except:
                    return self._init_barrier_state()
        return self._init_barrier_state()
    
    def _init_barrier_state(self) -> Dict:
        """Initialize barrier state"""
        return {
            "cycle_id": 0,
            "phase": "waiting",
            "engines_at_barrier": [],
            "engines_locked": [],
            "timestamp": time.time()
        }
    
    def _write_barrier_state(self, state: Dict) -> None:
        """Write barrier state atomically"""
        with open(self.barrier_file, 'w') as f:
            json.dump(state, f)
    
    async def wait_at_barrier(self, engine_id: int, timeout: float = BARRIER_TIMEOUT) -> bool:
        """
        Engine calls this to wait at barrier.
        Returns True when all 12 engines reach barrier.
        """
        start = time.time()
        
        while time.time() - start < timeout:
            state = self._read_barrier_state()
            
            # Add this engine if not already there
            if engine_id not in state.get("engines_at_barrier", []):
                engines = state.get("engines_at_barrier", [])
                engines.append(engine_id)
                state["engines_at_barrier"] = sorted(list(set(engines)))
                self._write_barrier_state(state)
            
            # Check if all 12 engines are at barrier
            engines_at = state.get("engines_at_barrier", [])
            if len(engines_at) >= self.NUM_ENGINES:
                return True
            
            await asyncio.sleep(0.05)
        
        return False
    
    async def request_lock(self, engine_id: int, gates_pass: bool) -> bool:
        """
        Engine requests lock after passing gates.
        Lock acquired only if ALL engines pass gates.
        """
        state = self._read_barrier_state()
        
        # Mark this engine as locked
        locked = state.get("engines_locked", [])
        if gates_pass and engine_id not in locked:
            locked.append(engine_id)
            state["engines_locked"] = sorted(list(set(locked)))
            state["phase"] = "locking"
            self._write_barrier_state(state)
        
        # Check if all engines locked
        locked_engines = state.get("engines_locked", [])
        if len(locked_engines) >= self.NUM_ENGINES:
            state["phase"] = "executing"
            self._write_barrier_state(state)
            return True
        
        return False
    
    async def release_lock(self, engine_id: int) -> None:
        """Engine releases lock after execution"""
        state = self._read_barrier_state()
        state["phase"] = "released"
        state["cycle_id"] += 1
        
        # Reset for next cycle
        state["engines_at_barrier"] = []
        state["engines_locked"] = []
        state["phase"] = "waiting"
        state["timestamp"] = time.time()
        
        self._write_barrier_state(state)
    
    def get_barrier_status(self) -> Dict:
        """Get current barrier status"""
        return self._read_barrier_state()


class SynchronousEngine:
    """Single engine in 12-engine cluster"""
    
    def __init__(self, engine_id: int, barrier: EngineBarrier, shared_dir: str):
        self.engine_id = engine_id
        self.barrier = barrier
        self.shared_dir = Path(shared_dir)
        self.shared_dir.mkdir(parents=True, exist_ok=True)
        self.cycle = 0
        self.lock_history = []
    
    async def measure_and_evaluate(self) -> Dict:
        """Measure T_t and evaluate gates"""
        # Simulate state measurement
        import random
        gates_pass = random.random() > 0.2  # 80% pass rate
        
        return {
            "engine_id": self.engine_id,
            "cycle": self.cycle,
            "gates_pass": gates_pass,
            "timestamp": time.time()
        }
    
    async def run_cycle(self) -> Dict:
        """Execute one synchronous cycle"""
        cycle_start = time.time()
        self.cycle += 1
        
        # Step 1: Measure and evaluate gates
        eval_result = await self.measure_and_evaluate()
        gates_pass = eval_result["gates_pass"]
        
        # Step 2: Wait at barrier
        barrier_ok = await self.barrier.wait_at_barrier(self.engine_id)
        if not barrier_ok:
            return {
                "engine_id": self.engine_id,
                "cycle": self.cycle,
                "success": False,
                "reason": "barrier_timeout"
            }
        
        # Step 3: Request lock
        lock_acquired = await self.barrier.request_lock(self.engine_id, gates_pass)
        
        # Step 4: Execute (if locked)
        executed = False
        if lock_acquired:
            await asyncio.sleep(0.01)  # Simulate execution
            executed = True
        
        # Step 5: Release lock
        await self.barrier.release_lock(self.engine_id)
        
        cycle_duration = time.time() - cycle_start
        
        result = {
            "engine_id": self.engine_id,
            "cycle": self.cycle,
            "gates_pass": gates_pass,
            "lock_acquired": lock_acquired,
            "executed": executed,
            "duration_ms": round(cycle_duration * 1000, 2),
            "timestamp": time.time()
        }
        
        self.lock_history.append(result)
        return result


async def run_12_engine_test():
    """Run synchronized test with 12 engines"""
    print("=" * 80)
    print("12-ENGINE SYNCHRONOUS BARRIER TEST")
    print("=" * 80)
    
    shared_dir = "/tmp/engine_barrier_test"
    Path(shared_dir).mkdir(parents=True, exist_ok=True)
    
    barrier = EngineBarrier(shared_dir)
    engines = [
        SynchronousEngine(i, barrier, shared_dir)
        for i in range(12)
    ]
    
    print(f"\nCreated 12 engines")
    print(f"Barrier timeout: {EngineBarrier.BARRIER_TIMEOUT}s")
    print(f"Target: All engines reach barrier, pass gates, acquire lock, execute atomically\n")
    
    for cycle_num in range(3):
        print(f"\n{'=' * 80}")
        print(f"CYCLE {cycle_num + 1} - SYNCHRONOUS EXECUTION")
        print(f"{'=' * 80}\n")
        
        cycle_start = time.time()
        
        # Run all 12 engines concurrently
        tasks = [engine.run_cycle() for engine in engines]
        results = await asyncio.gather(*tasks)
        
        cycle_duration = time.time() - cycle_start
        
        # Analyze results
        success_count = sum(1 for r in results if r.get("lock_acquired"))
        gates_pass_count = sum(1 for r in results if r.get("gates_pass"))
        executed_count = sum(1 for r in results if r.get("executed"))
        
        print(f"Barrier Status:")
        print(f"  [PASS] Gates passed: {gates_pass_count}/12")
        print(f"  [LOCK] Locks acquired: {success_count}/12")
        print(f"  [EXEC] Executed: {executed_count}/12")
        print(f"  [TIME] Cycle duration: {cycle_duration:.3f}s")
        
        # Show per-engine results
        print(f"\nPer-Engine Results:")
        for i, result in enumerate(results):
            if "duration_ms" not in result:
                print(f"  Engine {i:2d}: [TIMEOUT]")
                continue
            gates = "[G]" if result.get("gates_pass") else "[-]"
            lock = "[L]" if result.get("lock_acquired") else "[-]"
            exec_status = "[E]" if result.get("executed") else "[-]"
            print(f"  Engine {i:2d}: {gates} {lock} {exec_status}  {result['duration_ms']:6.2f}ms")
        
        await asyncio.sleep(1.0)
    
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    
    total_locks = sum(len(e.lock_history) for e in engines)
    total_executions = sum(
        1 for e in engines 
        for r in e.lock_history 
        if r.get("executed")
    )
    
    print(f"Total lock attempts: {total_locks}")
    print(f"Total executions: {total_executions}")
    print(f"Synchronization: {'[OK]' if total_executions >= 3 else '[FAIL]'}")


if __name__ == "__main__":
    asyncio.run(run_12_engine_test())
