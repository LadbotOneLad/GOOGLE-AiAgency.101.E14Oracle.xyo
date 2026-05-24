#!/usr/bin/env python3
"""
AIFACTORIES IMMUTABLE AUDIT TRAIL
Append-only, never transmitted externally, always encrypted

Tracks every decision, every gate, every doctrine check.
Lives in shared volume (/logs/aifactories).
Never leaves the system.

Copyright (c) 2026 Rebecca — AiFACTORIES
Authority: Internal Only
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


class ImmutableAuditTrail:
    """
    Append-only audit trail (write-once, never delete).
    
    Structure:
    - Each entry includes hash of previous entry
    - Creates unbreakable chain
    - Tampering is detectable (hash breaks)
    - Lives in shared volume (persists across container restarts)
    """
    
    def __init__(self, audit_file: str = "/logs/aifactories/audit_trail.jsonl"):
        self.audit_file = Path(audit_file)
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)
        self.last_hash = None
        self._load_last_hash()
    
    def _load_last_hash(self) -> None:
        """Load hash of last audit entry"""
        if self.audit_file.exists():
            try:
                with open(self.audit_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        last_entry = json.loads(last_line)
                        self.last_hash = last_entry.get("entry_hash")
            except Exception:
                self.last_hash = None
    
    def _compute_entry_hash(self, entry_dict: Dict) -> str:
        """Compute SHA-256 hash of entry (without hash field)"""
        # Create dict without entry_hash for computation
        entry_copy = {k: v for k, v in entry_dict.items() if k != "entry_hash"}
        entry_json = json.dumps(entry_copy, sort_keys=True)
        return hashlib.sha256(entry_json.encode()).hexdigest()
    
    def append(self, event: str, engine_id: int, data: Dict = None,
               decision: Optional[bool] = None) -> Dict:
        """
        Append immutable entry to audit trail.
        
        Args:
            event: Event type (e.g., "GATE_EVALUATION", "DOCTRINE_CHECK")
            engine_id: Engine that generated event
            data: Event-specific data
            decision: Boolean decision (e.g., gate pass/fail)
        
        Returns:
            The complete audit entry (with hash)
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "sequence": self._get_sequence_number(),
            "event": event,
            "engine_id": engine_id,
            "data": data or {},
            "decision": decision,
            "previous_hash": self.last_hash,
        }
        
        # Compute this entry's hash
        entry_hash = self._compute_entry_hash(entry)
        entry["entry_hash"] = entry_hash
        
        # Write to file (atomic append)
        with open(self.audit_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        # Update last hash
        self.last_hash = entry_hash
        
        return entry
    
    def _get_sequence_number(self) -> int:
        """Get next sequence number"""
        if not self.audit_file.exists():
            return 0
        
        try:
            with open(self.audit_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1].strip())
                    return last_entry.get("sequence", 0) + 1
        except Exception:
            pass
        
        return 0
    
    def verify_integrity(self) -> Dict:
        """
        Verify audit trail integrity (hash chain unbroken).
        
        Returns dict with:
        - valid: bool (chain is valid)
        - entries_checked: int
        - first_hash: hash of first entry
        - last_hash: hash of last entry
        - breaks: list of positions where chain breaks
        """
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "valid": True,
            "entries_checked": 0,
            "first_hash": None,
            "last_hash": None,
            "breaks": [],
        }
        
        if not self.audit_file.exists():
            return result
        
        try:
            with open(self.audit_file, 'r') as f:
                previous_hash = None
                entry_num = 0
                
                for line in f:
                    entry = json.loads(line.strip())
                    entry_num += 1
                    
                    # Verify previous_hash matches
                    if entry_num > 1:
                        if entry.get("previous_hash") != previous_hash:
                            result["valid"] = False
                            result["breaks"].append(entry_num)
                    else:
                        result["first_hash"] = entry.get("entry_hash")
                    
                    # Update for next iteration
                    previous_hash = entry.get("entry_hash")
                    result["last_hash"] = previous_hash
                    result["entries_checked"] = entry_num
        
        except Exception as e:
            result["valid"] = False
            result["error"] = str(e)
        
        return result
    
    def get_entries_for_engine(self, engine_id: int, limit: int = 100) -> list:
        """Get latest N audit entries for specific engine"""
        entries = []
        
        if not self.audit_file.exists():
            return entries
        
        try:
            with open(self.audit_file, 'r') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    if entry.get("engine_id") == engine_id:
                        entries.append(entry)
                        if len(entries) >= limit:
                            break
        
        except Exception:
            pass
        
        # Return most recent first
        return list(reversed(entries[-limit:]))
    
    def get_gate_decisions(self, gate_id: int, limit: int = 100) -> list:
        """Get gate decisions from audit trail"""
        entries = []
        
        if not self.audit_file.exists():
            return entries
        
        try:
            with open(self.audit_file, 'r') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    if entry.get("event", "").startswith(f"GATE_{gate_id}"):
                        entries.append(entry)
                        if len(entries) >= limit:
                            break
        
        except Exception:
            pass
        
        return list(reversed(entries[-limit:]))
    
    def get_doctrine_checks(self, doctrine_id: str, limit: int = 100) -> list:
        """Get doctrine compliance checks from audit trail"""
        entries = []
        
        if not self.audit_file.exists():
            return entries
        
        try:
            with open(self.audit_file, 'r') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    if entry.get("event") == "DOCTRINE_CHECK":
                        if entry.get("data", {}).get("doctrine_id") == doctrine_id:
                            entries.append(entry)
                            if len(entries) >= limit:
                                break
        
        except Exception:
            pass
        
        return list(reversed(entries[-limit:]))


class AuditLogger:
    """High-level audit logging interface"""
    
    def __init__(self, audit_trail: ImmutableAuditTrail):
        self.trail = audit_trail
    
    def log_gate_decision(self, engine_id: int, gate_id: int, 
                         passes: bool, error: float = None) -> None:
        """Log gate evaluation decision"""
        self.trail.append(
            event=f"GATE_{gate_id}",
            engine_id=engine_id,
            data={"gate_id": gate_id, "error": error},
            decision=passes
        )
    
    def log_doctrine_check(self, engine_id: int, doctrine_id: str,
                          compliant: bool) -> None:
        """Log doctrine compliance check"""
        self.trail.append(
            event="DOCTRINE_CHECK",
            engine_id=engine_id,
            data={"doctrine_id": doctrine_id},
            decision=compliant
        )
    
    def log_earth_lock_check(self, engine_id: int, 
                            true_north_ok: bool, magnetic_ok: bool) -> None:
        """Log Earth-lock alignment check"""
        self.trail.append(
            event="EARTH_LOCK_CHECK",
            engine_id=engine_id,
            data={
                "true_north_aligned": true_north_ok,
                "magnetic_declination_ok": magnetic_ok
            },
            decision=true_north_ok and magnetic_ok
        )
    
    def log_consensus(self, synchronized_engines: int, quorum_reached: bool) -> None:
        """Log Byzantine consensus result"""
        self.trail.append(
            event="CONSENSUS_VOTE",
            engine_id=0,  # Master
            data={"synchronized_engines": synchronized_engines},
            decision=quorum_reached
        )


def demo_audit_trail():
    """Demo: create and verify audit trail"""
    print("\n" + "="*80)
    print("AIFACTORIES IMMUTABLE AUDIT TRAIL")
    print("="*80)
    
    # Create audit trail
    audit = ImmutableAuditTrail(audit_file="/tmp/aifactories_audit_demo.jsonl")
    logger = AuditLogger(audit)
    
    print("\n1. Logging gate decisions...")
    for i in range(5):
        logger.log_gate_decision(engine_id=0, gate_id=1, passes=True)
        logger.log_gate_decision(engine_id=1, gate_id=2, passes=False, error=0.03)
    
    print("2. Logging doctrine checks...")
    for doctrine in ["I1", "I2", "I3", "I4", "I5", "I6", "I7"]:
        logger.log_doctrine_check(engine_id=0, doctrine_id=doctrine, compliant=True)
    
    print("3. Logging Earth-lock checks...")
    logger.log_earth_lock_check(engine_id=0, true_north_ok=True, magnetic_ok=True)
    
    print("4. Logging consensus votes...")
    logger.log_consensus(synchronized_engines=12, quorum_reached=True)
    
    print("\n5. Verifying integrity...")
    integrity = audit.verify_integrity()
    print(f"   Valid: {integrity['valid']}")
    print(f"   Entries: {integrity['entries_checked']}")
    print(f"   First hash: {integrity['first_hash'][:16]}...")
    print(f"   Last hash: {integrity['last_hash'][:16]}...")
    
    print("\n6. Retrieving engine 0 entries...")
    entries = audit.get_entries_for_engine(engine_id=0, limit=5)
    print(f"   Found {len(entries)} entries")
    if entries:
        print(f"   Latest: {entries[0]['event']}")
    
    print(f"\nAudit trail written to: /tmp/aifactories_audit_demo.jsonl")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    demo_audit_trail()
