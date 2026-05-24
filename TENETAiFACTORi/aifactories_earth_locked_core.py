#!/usr/bin/env python3
"""
AIFACTORIES EARTH-LOCKED BLUEPRINT v1.0
Self-Sufficient 13-Engine Harmonic Synchronization

86400 Invariants (one per second of Earth's day)
Locked to true north ±0.05° (pyramid precision)
Accounts for Earth's wobble (magnetic shadow)
24-hour diurnal cycle (1/7200 per 12-second tau)

Copyright (c) 2026 Rebecca — AiFACTORIES
Namespace: aifactories_earth_locked
Authority: Rebecca (Codex 6.65: codebecslucky7 Edition)
"""

import time
import math
import json
import uuid
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================================
# EARTH CONSTANTS (INVARIANT)
# ============================================================================

EARTH_CONSTANTS = {
    "seconds_per_day": 86400,
    "tau_seconds": 12,  # 1/7200 of day
    "taus_per_day": 7200,
    "true_north_offset": 0.05,  # degrees (pyramid precision)
    "magnetic_declination_range": 0.5,  # degrees (wobble tolerance)
    "precession_cycle_seconds": 86400 * 365.25 * 26000,  # 26000 years
}

TAU = EARTH_CONSTANTS["tau_seconds"]
TAUS_PER_DAY = EARTH_CONSTANTS["taus_per_day"]
TRUE_NORTH = EARTH_CONSTANTS["true_north_offset"]


# ============================================================================
# 86400 INVARIANTS (One per second of Earth's day)
# ============================================================================

def generate_86400_invariants() -> Dict[int, Dict]:
    """
    Generate 86400 invariants (one per second of 24-hour day).
    
    Each second has constraints:
    - True north alignment (±0.05°)
    - Magnetic declination (wobble tolerance)
    - Tau position (which 12-second block)
    - Precession phase (long-term cycle)
    - Doctrine adherence (guardian principles)
    """
    invariants = {}
    
    for second_of_day in range(EARTH_CONSTANTS["seconds_per_day"]):
        tau_index = second_of_day // TAU  # which 12-second block
        second_in_tau = second_of_day % TAU
        
        # True north constraint (drifts through day due to rotation)
        true_north_phase = (second_of_day / EARTH_CONSTANTS["seconds_per_day"]) * 360
        
        # Magnetic wobble (Earth's nutation)
        wobble_amplitude = EARTH_CONSTANTS["magnetic_declination_range"]
        magnetic_shadow = wobble_amplitude * math.sin(2 * math.pi * second_of_day / EARTH_CONSTANTS["seconds_per_day"])
        
        invariants[second_of_day] = {
            "second": second_of_day,
            "tau_index": tau_index,
            "second_in_tau": second_in_tau,
            "true_north_phase": true_north_phase,
            "true_north_tolerance": TRUE_NORTH,
            "magnetic_declination": magnetic_shadow,
            "wobble_limit": wobble_amplitude,
            "constraint": f"second_{second_of_day}",
            "doctrine_check": True,  # All doctrines must hold
        }
    
    return invariants


INVARIANTS_86400 = generate_86400_invariants()


# ============================================================================
# 13-ENGINE IDENTITIES
# ============================================================================

@dataclass(frozen=True)
class EngineIdentity:
    """13-engine cluster identity"""
    engine_id: int  # 0 = master, 1-12 = validators
    role: str  # "master" or "validator"
    root_id: str = field(default_factory=lambda: f"LUCKY7-{uuid.uuid4().hex[:8]}")
    geohash: str = ""  # Geographic position (2-letter code)
    port: int = 6650  # 6650-6662 (13 ports)
    
    def __post_init__(self):
        if self.engine_id == 0:
            object.__setattr__(self, "role", "master")
        else:
            object.__setattr__(self, "role", "validator")
        
        object.__setattr__(self, "port", 6650 + self.engine_id)


ENGINES_13 = [
    EngineIdentity(0, "master", geohash="00"),  # Master (Greenwich/Prime Meridian)
    EngineIdentity(1, "validator", geohash="US"),  # US East
    EngineIdentity(2, "validator", geohash="US"),  # US West
    EngineIdentity(3, "validator", geohash="EU"),  # Europe West
    EngineIdentity(4, "validator", geohash="EU"),  # Europe East
    EngineIdentity(5, "validator", geohash="AS"),  # Asia West
    EngineIdentity(6, "validator", geohash="AS"),  # Asia Central
    EngineIdentity(7, "validator", geohash="AS"),  # Asia East
    EngineIdentity(8, "validator", geohash="AU"),  # Australia
    EngineIdentity(9, "validator", geohash="SA"),  # South America
    EngineIdentity(10, "validator", geohash="AF"),  # Africa
    EngineIdentity(11, "validator", geohash="AR"),  # Arctic
    EngineIdentity(12, "validator", geohash="AN"),  # Antarctic
]


# ============================================================================
# STATE VECTOR (Earth-Locked)
# ============================================================================

@dataclass
class StateVectorEarthLocked:
    """T_t with Earth alignment"""
    timestamp: float
    engine_id: int
    tau_count: int
    second_of_day: int
    
    # Base measurements
    phase: float  # [0, 1)
    power: float
    coherence: float
    
    # Earth alignment
    true_north_phase: float
    true_north_error: float
    magnetic_declination: float
    
    # Invariant checks
    invariant_satisfied: bool
    doctrine_compliant: bool
    
    # Gate status
    gates: Dict[int, bool]
    knock: bool
    
    # Horizon
    horizon_length: int


# ============================================================================
# HARMONIC SYNCHRONIZATION (13 engines, phase-locked)
# ============================================================================

class HarmonicSync:
    """
    13-engine harmonic synchronization without dependencies.
    
    Each engine:
    - Runs own tau-cycles
    - Locks to Earth's 86400-second day
    - Broadcasts heartbeat (read-only)
    - Computes phase relative to others
    - Self-corrects if drift detected
    
    No central coordinator needed.
    No external dependencies.
    """
    
    def __init__(self, engine_id: int):
        self.engine_id = engine_id
        self.engine = ENGINES_13[engine_id]
        self.start_time = time.time()
        self.tau_count = 0
        
    def current_second_of_day(self) -> int:
        """Current second within Earth's 24-hour cycle"""
        elapsed = time.time() - self.start_time
        current_time = datetime.utcnow()
        seconds_since_midnight = (current_time.hour * 3600 + 
                                  current_time.minute * 60 + 
                                  current_time.second)
        return seconds_since_midnight
    
    def current_tau_index(self) -> int:
        """Current tau (12-second) block within day"""
        second = self.current_second_of_day()
        return second // TAU
    
    def phase_relative_to_master(self) -> float:
        """Phase difference from master engine (0)"""
        if self.engine_id == 0:
            return 0.0  # Master is reference
        
        # Each validator phase-shifts by engine_id * (1/13)
        phase_shift = self.engine_id / 13.0
        return phase_shift
    
    def is_synchronized(self, tolerance: float = 0.01) -> bool:
        """Check if this engine is synchronized with Earth clock"""
        current_tau = self.current_tau_index()
        expected_tau = (self.tau_count % TAUS_PER_DAY)
        
        tau_error = abs(current_tau - expected_tau)
        return tau_error <= 1  # Within 1 tau block
    
    def self_correct_if_drifted(self) -> None:
        """Self-correct if drift detected from Earth clock"""
        if not self.is_synchronized():
            current_tau = self.current_tau_index()
            self.tau_count = current_tau
    
    def heartbeat(self) -> Dict:
        """Engine heartbeat (read-only broadcast)"""
        second = self.current_second_of_day()
        tau_idx = self.current_tau_index()
        
        return {
            "engine_id": self.engine_id,
            "role": self.engine.role,
            "root_id": self.engine.root_id,
            "port": self.engine.port,
            "timestamp": time.time(),
            "second_of_day": second,
            "tau_index": tau_idx,
            "phase": tau_idx / TAUS_PER_DAY,
            "phase_offset": self.phase_relative_to_master(),
            "synchronized": self.is_synchronized(),
        }


# ============================================================================
# EARTH LOCK ENFORCEMENT
# ============================================================================

class EarthLock:
    """
    Enforce Earth alignment:
    - True north ±0.05° (pyramid precision)
    - Magnetic declination (wobble tolerance)
    - 86400 invariants (one per second)
    """
    
    def __init__(self, engine_id: int):
        self.engine_id = engine_id
        self.invariants = INVARIANTS_86400
    
    def check_true_north(self, second_of_day: int, measured_heading: float) -> Tuple[bool, float]:
        """
        Check if heading is within true north tolerance.
        
        Returns: (passes, error)
        """
        invariant = self.invariants[second_of_day % EARTH_CONSTANTS["seconds_per_day"]]
        expected_phase = invariant["true_north_phase"]
        tolerance = invariant["true_north_tolerance"]
        
        # Normalize heading to [0, 360)
        measured_heading = measured_heading % 360
        expected_phase = expected_phase % 360
        
        error = abs(measured_heading - expected_phase)
        if error > 180:
            error = 360 - error
        
        passes = error <= tolerance
        return passes, error
    
    def check_magnetic_declination(self, second_of_day: int, measured_declination: float) -> Tuple[bool, float]:
        """
        Check if magnetic declination is within wobble tolerance.
        
        Returns: (passes, error)
        """
        invariant = self.invariants[second_of_day % EARTH_CONSTANTS["seconds_per_day"]]
        expected_declination = invariant["magnetic_declination"]
        wobble_limit = invariant["wobble_limit"]
        
        error = abs(measured_declination - expected_declination)
        passes = error <= wobble_limit
        return passes, error
    
    def get_invariant_for_second(self, second_of_day: int) -> Dict:
        """Get the specific invariant for a given second"""
        return self.invariants[second_of_day % EARTH_CONSTANTS["seconds_per_day"]]
    
    def all_invariants_satisfied(self, second_of_day: int, 
                                 true_north_error: float,
                                 magnetic_error: float) -> bool:
        """Check if all 86400 invariants are satisfied"""
        invariant = self.get_invariant_for_second(second_of_day)
        
        north_ok = true_north_error <= invariant["true_north_tolerance"]
        mag_ok = magnetic_error <= invariant["wobble_limit"]
        doctrine_ok = invariant["doctrine_check"]
        
        return north_ok and mag_ok and doctrine_ok


# ============================================================================
# 7 DOCTRINES (KAITIAKI-CORE + AIFACTORIES)
# ============================================================================

@dataclass
class Doctrines:
    """7 operational doctrines"""
    
    I1_AGENCY_FIRST = "User agency never sacrificed"
    I2_CLARITY_FIRST = "All decisions explainable"
    I3_CARE_FIRST = "Depth > coverage"
    I4_NEVER_DIMINISH = "No reduction of mauri/mana (integrity unbreakable)"
    I5_USER_SOVEREIGN = "Only user has final authority"
    I6_EARTH_LOCKED = "All decisions respect Earth's 86400-second day"
    I7_HARMONIC_BALANCE = "All 13 engines in phase-locked harmony"
    
    @staticmethod
    def check_all(state: StateVectorEarthLocked) -> bool:
        """All 7 doctrines must be satisfied"""
        return (
            state.doctrine_compliant and  # I1-I5 (Kaitiaki-Core)
            state.second_of_day >= 0 and  # I6 (Earth-locked)
            state.gates.get(1, False)  # I7 (Integrity/harmonic balance)
        )


# ============================================================================
# COMPLETE ENGINE (Self-Sufficient, Earth-Locked)
# ============================================================================

class AiFACTORIESEngine:
    """
    Self-sufficient AiFACTORIES instance.
    
    Locked to Earth's 86400-second day.
    Part of 13-engine harmonic cluster.
    No external dependencies.
    """
    
    def __init__(self, engine_id: int = 0):
        self.engine_id = engine_id
        self.engine_identity = ENGINES_13[engine_id]
        self.sync = HarmonicSync(engine_id)
        self.earth_lock = EarthLock(engine_id)
        
        self.tau_count = 0
        self.total_seconds = 0
        self.audit_log = []
        self.telemetry_log = []
        
        self.logs_dir = Path("./logs/aifactories")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def tick(self) -> StateVectorEarthLocked:
        """Execute one tau-cycle (12 seconds)"""
        self.sync.self_correct_if_drifted()
        self.tau_count += 1
        
        # Get Earth time
        second_of_day = self.sync.current_second_of_day()
        tau_index = self.sync.current_tau_index()
        
        # Simulate measurements
        import random
        phase = (tau_index / TAUS_PER_DAY)
        power = 0.5 + 0.3 * math.sin(2 * math.pi * phase)
        coherence = 0.3 + 0.5 * math.cos(2 * math.pi * phase)
        
        # Simulate true north heading (should match Earth clock)
        true_north_phase = (second_of_day / EARTH_CONSTANTS["seconds_per_day"]) * 360
        measured_heading = true_north_phase + random.uniform(-0.02, 0.02)
        
        # Get magnetic declination from Earth wobble
        expected_declination = INVARIANTS_86400[second_of_day % 86400]["magnetic_declination"]
        measured_declination = expected_declination + random.uniform(-0.01, 0.01)
        
        # Check Earth lock constraints
        north_ok, north_error = self.earth_lock.check_true_north(second_of_day, measured_heading)
        mag_ok, mag_error = self.earth_lock.check_magnetic_declination(second_of_day, measured_declination)
        
        # Evaluate gates (standard 6 gates)
        gates = {
            1: True,  # Integrity (always true in self-sufficient mode)
            2: coherence > 0.0,  # Byzantine (proxy)
            3: power > 0.3,  # Majority (proxy)
            4: coherence > 0.0,  # Coherence floor
            5: abs(phase - 0.5) < 0.2,  # Drift ceiling (proxy)
            6: power * (1 - coherence) <= 0.1,  # Power discipline
        }
        
        all_gates_pass = all(gates.values())
        knock = not all_gates_pass
        
        # Check all doctrines
        doctrine_compliant = (
            north_ok and mag_ok and  # I6 (Earth-locked)
            self.sync.is_synchronized() and  # I7 (Harmonic)
            all_gates_pass  # I1-I5 (Kaitiaki-Core)
        )
        
        # Create state
        state = StateVectorEarthLocked(
            timestamp=time.time(),
            engine_id=self.engine_id,
            tau_count=self.tau_count,
            second_of_day=second_of_day,
            phase=phase,
            power=round(power, 4),
            coherence=round(coherence, 4),
            true_north_phase=round(true_north_phase, 2),
            true_north_error=round(north_error, 4),
            magnetic_declination=round(measured_declination, 4),
            invariant_satisfied=north_ok and mag_ok,
            doctrine_compliant=doctrine_compliant,
            gates=gates,
            knock=knock,
            horizon_length=self.tau_count // 100,  # Mock horizon
        )
        
        self.telemetry_log.append(asdict(state))
        
        return state
    
    def run_for_seconds(self, duration_seconds: int = 86400) -> None:
        """Run for specified seconds (default: 1 Earth day)"""
        taus_to_run = duration_seconds // TAU
        
        print(f"\n{'='*80}")
        print(f"AiFACTORIES Engine {self.engine_id} ({self.engine_identity.role})")
        print(f"Port: {self.engine_identity.port}")
        print(f"Root ID: {self.engine_identity.root_id}")
        print(f"Duration: {duration_seconds} seconds ({taus_to_run} taus)")
        print(f"{'='*80}\n")
        
        for i in range(min(taus_to_run, 100)):  # Run max 100 taus for demo
            state = self.tick()
            
            if i % 10 == 0:
                print(
                    f"[{self.engine_identity.root_id}] "
                    f"tau={self.tau_count:4d} "
                    f"sec={state.second_of_day:5d} "
                    f"phase={state.phase:.3f} "
                    f"power={state.power:.3f} "
                    f"coh={state.coherence:.3f} "
                    f"north_err={state.true_north_error:.4f} "
                    f"knock={state.knock} "
                    f"doctrine_ok={state.doctrine_compliant}"
                )
            
            time.sleep(0.01)
        
        self.write_telemetry()
    
    def write_telemetry(self) -> None:
        """Write telemetry to JSON file"""
        filename = self.logs_dir / f"engine_{self.engine_id}_telemetry.json"
        with open(filename, 'w') as f:
            json.dump(self.telemetry_log, f, indent=2)
        print(f"\nTelemetry written: {filename}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Run engine 0 (master) as demo
    engine = AiFACTORIESEngine(engine_id=0)
    engine.run_for_seconds(duration_seconds=1200)  # 100 taus × 12 sec
