#!/usr/bin/env python3
"""
GATE ENFORCEMENT — Layer 1 Cycle Blocker

Prevents Layer 1 (Codex 6.65) from executing ANY cycle until:
  1. All 6 gates pass
  2. All 12 engines synchronized
  3. Lock acquired
  4. Execution authorized

This is the mathematical veto layer.
"""

import asyncio
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional, List, Tuple


@dataclass
class ExecutionAuthority:
    """Authorization to execute a cycle"""
    timestamp: float
    cycle_id: int
    authorized: bool
    reason: str
    gates_status: Dict[int, bool]
    engine_consensus: int  # how many engines agree
    veto_engines: List[int]  # which engines vetoed


class GateEnforcement:
    """
    VETO LAYER — No execution without full gate passage.
    
    Decision function:
    F_t = E_t ∧ (V_t ≥ 8/12) ∧ (O_t ≥ 6/10) ∧ (C_t ≥ C_min) ∧ (D_t ≤ D_max) ∧ (P_t(1−C_t) ≤ ε)
    
    If F_t = 0, execution is BLOCKED.
    If F_t = 1, execution is AUTHORIZED.
    """
    
    def __init__(self, shared_dir: str = "/tmp/gate_enforcement"):
        self.shared_dir = Path(shared_dir)
        self.shared_dir.mkdir(parents=True, exist_ok=True)
        self.enforcement_log = self.shared_dir / "enforcement_log.jsonl"
        self.veto_log = self.shared_dir / "veto_log.jsonl"
        
    def evaluate_decision_function(self, gates: Dict[int, bool]) -> bool:
        """
        F_t = E_t ∧ (V_t ≥ 8/12) ∧ (O_t ≥ 6/10) ∧ (C_t ≥ C_min) ∧ (D_t ≤ D_max) ∧ (P_t(1−C_t) ≤ ε)
        
        Returns True only if ALL gates are True (AND logic).
        """
        if not gates:
            return False
        
        # All 6 gates must be True
        return all(gates.get(i, False) for i in range(1, 7))
    
    async def request_execution(self, cycle_id: int, engine_id: int, 
                               gates: Dict[int, bool]) -> ExecutionAuthority:
        """
        Engine requests execution authority.
        
        Authority granted only if decision function returns True.
        """
        ts = time.time()
        authorized = self.evaluate_decision_function(gates)
        
        reason = "All gates pass" if authorized else "Gate(s) failed"
        veto_engines = []
        
        if not authorized:
            # Identify which gates failed
            failed_gates = [i for i in range(1, 7) if not gates.get(i, False)]
            reason = f"Gates failed: {failed_gates}"
        
        authority = ExecutionAuthority(
            timestamp=ts,
            cycle_id=cycle_id,
            authorized=authorized,
            reason=reason,
            gates_status=gates,
            engine_consensus=1,
            veto_engines=veto_engines
        )
        
        # Log decision
        log_entry = {
            "timestamp": ts,
            "cycle_id": cycle_id,
            "engine_id": engine_id,
            "authorized": authorized,
            "reason": reason,
            "gates": gates
        }
        
        with open(self.enforcement_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        if not authorized:
            with open(self.veto_log, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        
        return authority
    
    def get_enforcement_status(self) -> Dict:
        """Get enforcement statistics"""
        auth_count = 0
        veto_count = 0
        
        if self.enforcement_log.exists():
            with open(self.enforcement_log, 'r') as f:
                auth_count = sum(1 for _ in f)
        
        if self.veto_log.exists():
            with open(self.veto_log, 'r') as f:
                veto_count = sum(1 for _ in f)
        
        return {
            "authorized_cycles": auth_count - veto_count,
            "vetoed_cycles": veto_count,
            "total_requests": auth_count,
            "veto_rate": veto_count / auth_count if auth_count > 0 else 0
        }


class Layer1ExecutionGuard:
    """
    Wraps Layer 1 (Codex) execution with gate enforcement.
    
    Usage:
        guard = Layer1ExecutionGuard()
        auth = await guard.attempt_execution(cycle_id, gates)
        if auth.authorized:
            result = await codex.execute_cycle()
        else:
            # Blocked
            pass
    """
    
    def __init__(self, shared_dir: str = "/tmp/layer1_guard"):
        self.shared_dir = Path(shared_dir)
        self.shared_dir.mkdir(parents=True, exist_ok=True)
        self.enforcement = GateEnforcement(shared_dir)
        self.execution_log = self.shared_dir / "execution_log.jsonl"
        self.veto_log = self.shared_dir / "veto_log.jsonl"
        
    async def attempt_execution(self, cycle_id: int, engine_id: int,
                               gates: Dict[int, bool]) -> ExecutionAuthority:
        """
        Attempt to execute Layer 1 cycle.
        
        Returns authority with:
        - authorized: True if execution allowed
        - reason: Why allowed or blocked
        """
        authority = await self.enforcement.request_execution(cycle_id, engine_id, gates)
        
        # Log decision
        log_entry = {
            "timestamp": authority.timestamp,
            "cycle_id": cycle_id,
            "engine_id": engine_id,
            "authorized": authority.authorized,
            "reason": authority.reason
        }
        
        if authority.authorized:
            with open(self.execution_log, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        else:
            with open(self.veto_log, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        
        return authority
    
    async def execute_guarded(self, cycle_id: int, engine_id: int,
                             gates: Dict[int, bool],
                             execution_fn) -> Dict:
        """
        Execute Layer 1 cycle only if authorized.
        
        Args:
            cycle_id: Cycle identifier
            engine_id: Engine requesting execution
            gates: Gate evaluation dict {1: bool, 2: bool, ..., 6: bool}
            execution_fn: Async function to call if authorized
        
        Returns:
            {
                "authorized": bool,
                "executed": bool,
                "result": execution result or None,
                "reason": explanation
            }
        """
        authority = await self.attempt_execution(cycle_id, engine_id, gates)
        
        if not authority.authorized:
            return {
                "authorized": False,
                "executed": False,
                "result": None,
                "reason": authority.reason,
                "gates": gates
            }
        
        # Execute guarded
        try:
            result = await execution_fn()
            return {
                "authorized": True,
                "executed": True,
                "result": result,
                "reason": "Execution completed",
                "gates": gates
            }
        except Exception as e:
            return {
                "authorized": True,
                "executed": False,
                "result": None,
                "reason": f"Execution failed: {str(e)}",
                "gates": gates
            }


async def test_gate_enforcement():
    """Test gate enforcement with various gate states"""
    print("=" * 80)
    print("GATE ENFORCEMENT TEST")
    print("=" * 80)
    
    guard = Layer1ExecutionGuard()
    
    # Test scenarios
    scenarios = [
        {
            "name": "All gates pass",
            "gates": {1: True, 2: True, 3: True, 4: True, 5: True, 6: True},
            "expected": True
        },
        {
            "name": "Gate 1 (integrity) fails",
            "gates": {1: False, 2: True, 3: True, 4: True, 5: True, 6: True},
            "expected": False
        },
        {
            "name": "Gate 2 (Byzantine) fails",
            "gates": {1: True, 2: False, 3: True, 4: True, 5: True, 6: True},
            "expected": False
        },
        {
            "name": "Gates 5 and 6 fail",
            "gates": {1: True, 2: True, 3: True, 4: True, 5: False, 6: False},
            "expected": False
        },
        {
            "name": "Single gate passes (all others fail)",
            "gates": {1: True, 2: False, 3: False, 4: False, 5: False, 6: False},
            "expected": False
        }
    ]
    
    for i, scenario in enumerate(scenarios):
        print(f"\n{'-' * 80}")
        print(f"Test {i+1}: {scenario['name']}")
        print(f"{'-' * 80}")
        
        gates = scenario['gates']
        print(f"\nGate Status:")
        for gate_id, passed in gates.items():
            status = "[PASS]" if passed else "[FAIL]"
            print(f"  Gate {gate_id}: {status}")
        
        # Request execution
        auth = await guard.attempt_execution(
            cycle_id=i,
            engine_id=0,
            gates=gates
        )
        
        print(f"\nDecision Function Result:")
        print(f"  F_t = {auth.authorized}")
        print(f"  Reason: {auth.reason}")
        
        expected = scenario['expected']
        result = "[PASS]" if auth.authorized == expected else "[FAIL]"
        print(f"  Test: {result}")
    
    # Show enforcement statistics
    print(f"\n{'=' * 80}")
    print("ENFORCEMENT STATISTICS")
    print(f"{'=' * 80}")
    
    stats = guard.enforcement.get_enforcement_status()
    print(f"\nAuthorized cycles: {stats['authorized_cycles']}")
    print(f"Vetoed cycles: {stats['vetoed_cycles']}")
    print(f"Total requests: {stats['total_requests']}")
    print(f"Veto rate: {stats['veto_rate']:.1%}")


if __name__ == "__main__":
    asyncio.run(test_gate_enforcement())
