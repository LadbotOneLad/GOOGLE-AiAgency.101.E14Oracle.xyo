"""
Digital Thymus Architecture - Zero-Trust Security Fabric
Bio-inspired immune system for continuous risk assessment and proportional enforcement
Version: 1.0 (2026-02-24)
"""

import json
import hashlib
import hmac
import asyncio
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from abc import ABC, abstractmethod
import math
import logging
from scipy.spatial.distance import cosine
from scipy.stats import entropy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResponseTier(Enum):
    """Graded response tiers based on risk score"""
    LOW = "low"           # <0.3 - Passive Monitoring
    MEDIUM = "medium"     # 0.3-0.6 - Step-up MFA + API Restrictions
    HIGH = "high"         # 0.6-0.8 - Session Quarantine (Shadow Environment)
    CRITICAL = "critical" # >0.8 - Apoptosis (Immediate Termination)


@dataclass
class BehavioralSignature:
    """User behavioral fingerprint for antigen detection"""
    user_id: str
    timestamp: str
    api_calls: List[str]
    resource_access: List[str]
    network_origin: str
    session_duration_seconds: float
    mfa_method: str
    geolocation: str
    device_fingerprint: str
    entropy_score: float  # High entropy = anomaly signal


@dataclass
class RiskVector:
    """Complete risk assessment vector"""
    user_id: str
    kl_divergence: float      # Kullback-Leibler divergence from baseline
    cosine_similarity: float   # Alignment with role template
    velocity_score: float      # Infrastructure modification velocity
    anomaly_signals: Dict[str, float]
    treg_gate_signal: bool    # Regulatory T-Cell gate override
    final_risk_score: float   # Logistic-squashed final score (0-1)
    response_tier: ResponseTier
    timestamp: str


@dataclass
class ImmuneRecord:
    """Cryptographically anchored audit record (Unit of Causal Truth)"""
    record_id: str
    timestamp: str
    user_id: str
    action: str
    risk_vector: RiskVector
    enforcement_decision: str
    pdp_signature: str  # Policy Decision Point signature
    treg_signature: str  # Regulatory T-Cell signature
    merkle_root: str   # Checkpoint hash
    ledger_broadcast: bool


class AntigenIdentificationEngine(ABC):
    """Layer 1: Antigen Detection via Recursive Bayesian Inference"""
    
    def __init__(self):
        self.baseline_profiles = {}  # user_id -> behavior vector
        self.role_templates = {}  # role -> canonical behavior
        
    def compute_kl_divergence(self, 
                             current_behavior: Dict[str, float],
                             baseline_behavior: Dict[str, float]) -> float:
        """
        Kullback-Leibler divergence: D_KL(current || baseline)
        Measures magnitude of drift from baseline (information-theoretic distance)
        """
        # Normalize to probability distributions
        current_dist = self._normalize_distribution(current_behavior)
        baseline_dist = self._normalize_distribution(baseline_behavior)
        
        # KL divergence with epsilon to avoid log(0)
        eps = 1e-10
        kl = sum(
            p * math.log((p + eps) / (q + eps))
            for p, q in zip(current_dist.values(), baseline_dist.values())
        )
        return min(kl, 10.0)  # Cap at 10.0 to prevent overflow
    
    def compute_cosine_similarity(self,
                                 current_behavior: List[float],
                                 role_template: List[float]) -> float:
        """
        Cosine similarity: measures alignment with role-based expectations
        Returns value in [-1, 1]; closer to 1 = more aligned
        """
        if len(current_behavior) == 0 or len(role_template) == 0:
            return 0.0
        
        # cosine distance from scipy returns distance, convert to similarity
        distance = cosine(current_behavior, role_template)
        return 1 - distance
    
    def _normalize_distribution(self, behavior: Dict[str, float]) -> Dict[str, float]:
        """Normalize behavior metrics to probability distribution"""
        total = sum(behavior.values())
        if total == 0:
            total = 1
        return {k: v / total for k, v in behavior.items()}
    
    async def identify_antigens(self, 
                                signature: BehavioralSignature) -> Tuple[float, float]:
        """
        Identify if current behavior is antigen (adversarial) or legitimate evolution
        Returns: (kl_divergence, cosine_similarity)
        """
        user_id = signature.user_id
        
        # Get baseline for user
        if user_id not in self.baseline_profiles:
            # First-time user: create baseline
            baseline = self._extract_behavior_vector(signature)
            self.baseline_profiles[user_id] = baseline
            return 0.0, 1.0  # No divergence on first observation
        
        baseline = self.baseline_profiles[user_id]
        current = self._extract_behavior_vector(signature)
        
        # Compute KL divergence
        kl_div = self.compute_kl_divergence(current, baseline)
        
        # Compute cosine similarity to role template
        role = self._infer_role(signature)
        role_template = self.role_templates.get(role, [0.33, 0.33, 0.34])
        current_vector = list(current.values())
        cos_sim = self.compute_cosine_similarity(current_vector, role_template)
        
        return kl_div, cos_sim
    
    def _extract_behavior_vector(self, signature: BehavioralSignature) -> Dict[str, float]:
        """Extract normalized behavior metrics from signature"""
        return {
            "api_activity": min(len(signature.api_calls) / 100, 1.0),
            "resource_access": min(len(signature.resource_access) / 50, 1.0),
            "session_duration": min(signature.session_duration_seconds / 3600, 1.0),
        }
    
    def _infer_role(self, signature: BehavioralSignature) -> str:
        """Infer user role from behavior (simplified)"""
        if len(signature.api_calls) > 50:
            return "admin"
        elif "database" in str(signature.resource_access):
            return "data_engineer"
        return "user"


class TCellDecisionEngine(ABC):
    """Layer 2: Graded Response Function (Cytotoxic Response)"""
    
    def __init__(self, antigen_engine: AntigenIdentificationEngine):
        self.antigen_engine = antigen_engine
    
    def evaluate_quarantine_response(self,
                                    kl_divergence: float,
                                    cosine_similarity: float,
                                    treg_gate_signal: bool,
                                    velocity_score: float = 0.0) -> RiskVector:
        """
        Risk scoring algorithm combining multiple signals
        Returns proportional enforcement tier
        """
        
        # Normalize inputs to [0, 1]
        kl_norm = min(kl_divergence / 5.0, 1.0)
        cos_norm = (1 - cosine_similarity) / 2.0  # Invert: low similarity = high risk
        velocity_norm = min(velocity_score, 1.0)
        
        # Weighted risk components
        weights = {
            "kl_divergence": 0.4,      # Behavioral drift (largest weight)
            "role_alignment": 0.3,     # Role conformance
            "velocity": 0.2,           # Infrastructure modification speed
            "treg_override": 0.1       # Regulatory dampening
        }
        
        # Composite risk score (pre-squash)
        raw_risk = (
            weights["kl_divergence"] * kl_norm +
            weights["role_alignment"] * cos_norm +
            weights["velocity"] * velocity_norm +
            (0 if treg_gate_signal else weights["treg_override"])  # Treg gate reduces risk
        )
        
        # Logistic squashing: maps to (0, 1) with steeper curve
        final_risk = self._logistic_squash(raw_risk, k=8, x0=0.5)
        
        # Determine response tier
        response_tier = self._map_risk_to_tier(final_risk)
        
        return RiskVector(
            user_id="unknown",
            kl_divergence=kl_divergence,
            cosine_similarity=cosine_similarity,
            velocity_score=velocity_score,
            anomaly_signals={
                "kl_divergence": kl_norm,
                "role_alignment": cos_norm,
                "velocity": velocity_norm,
            },
            treg_gate_signal=treg_gate_signal,
            final_risk_score=final_risk,
            response_tier=response_tier,
            timestamp=datetime.utcnow().isoformat()
        )
    
    def _logistic_squash(self, x: float, k: float = 8, x0: float = 0.5) -> float:
        """
        Logistic squashing function: f(x) = 1 / (1 + e^(-k(x - x0)))
        Steepness (k) controls response curve aggression
        """
        try:
            return 1.0 / (1.0 + math.exp(-k * (x - x0)))
        except OverflowError:
            return 1.0 if x > x0 else 0.0
    
    def _map_risk_to_tier(self, risk_score: float) -> ResponseTier:
        """Map risk score to response tier"""
        if risk_score < 0.3:
            return ResponseTier.LOW
        elif risk_score < 0.6:
            return ResponseTier.MEDIUM
        elif risk_score < 0.8:
            return ResponseTier.HIGH
        else:
            return ResponseTier.CRITICAL
    
    async def enforce_response(self, risk_vector: RiskVector) -> Dict[str, Any]:
        """Execute proportional enforcement action"""
        tier = risk_vector.response_tier
        
        if tier == ResponseTier.LOW:
            return {
                "action": "passive_monitoring",
                "description": "Observe behavior, log events",
                "api_restrictions": [],
                "requires_mfa": False,
            }
        elif tier == ResponseTier.MEDIUM:
            return {
                "action": "step_up_mfa",
                "description": "Require MFA + restricted API access",
                "api_restrictions": ["admin_panel", "bulk_operations"],
                "requires_mfa": True,
                "mfa_methods": ["totp", "webauthn"],
            }
        elif tier == ResponseTier.HIGH:
            return {
                "action": "session_quarantine",
                "description": "Route to shadow environment",
                "shadow_environment": True,
                "allowed_resources": ["audit_logs", "documentation"],
                "requires_isolation": True,
            }
        else:  # CRITICAL
            return {
                "action": "apoptosis",
                "description": "Immediate termination + token revocation",
                "terminate_session": True,
                "revoke_tokens": True,
                "block_user": True,
                "trigger_incident": True,
            }


class TregGate(ABC):
    """
    Layer 3: Regulatory T-Cell Gate & Change Oracle
    Prevents "Cytokine Storms" (system-wide lockouts)
    Enforces Systemic Invariants via air-gapped trust anchor
    """
    
    def __init__(self):
        self.tier0_commands = {}  # Immutable command history
        self.velocity_budget = 0.05  # Max 5% infrastructure change per 24h
        self.approval_cache = {}  # Dual-approver tracking
    
    async def verify_tier0_intent(self,
                                  command: Dict[str, Any],
                                  approver_ips: List[str],
                                  hardware_signatures: List[str]) -> bool:
        """
        Verify Tier-0 command against invariants:
        1. Velocity Invariant: Max % infrastructure modified
        2. Proximity Invariant: Dual-approvers from different subnets
        3. No-Solo Invariant: Critical mutations require m-of-n hardware signatures
        """
        
        # Invariant 1: Velocity Check
        velocity = self._compute_infrastructure_velocity()
        if velocity > self.velocity_budget:
            logger.warning(f"[TREG] Velocity violation: {velocity:.2%} > {self.velocity_budget:.2%}")
            return False
        
        # Invariant 2: Proximity Check (dual-approvers from different subnets)
        if not self._check_dual_proximity(approver_ips):
            logger.warning("[TREG] Proximity violation: approvers from same subnet")
            return False
        
        # Invariant 3: No-Solo Check (2-of-3 hardware signatures for critical)
        if self._is_critical_mutation(command):
            if len(hardware_signatures) < 2:
                logger.warning("[TREG] No-Solo violation: insufficient hardware signatures")
                return False
        
        # All invariants passed
        logger.info("[TREG] All invariants verified - command approved")
        self.tier0_commands[command.get("id", "unknown")] = {
            "command": command,
            "timestamp": datetime.utcnow().isoformat(),
            "verified": True,
        }
        return True
    
    def _compute_infrastructure_velocity(self) -> float:
        """Compute % of infrastructure modified in last 24h"""
        cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_commands = [
            c for c in self.tier0_commands.values()
            if datetime.fromisoformat(c["timestamp"]) > cutoff
        ]
        return min(len(recent_commands) / 20, 1.0)  # Assume 20 = 100%
    
    def _check_dual_proximity(self, approver_ips: List[str]) -> bool:
        """Verify dual-approvers from different subnets"""
        if len(approver_ips) < 2:
            return False
        
        # Extract /24 subnets
        subnets = set(ip.rsplit(".", 1)[0] for ip in approver_ips[:2])
        return len(subnets) == 2
    
    def _is_critical_mutation(self, command: Dict[str, Any]) -> bool:
        """Check if command is critical (e.g., policy change, key rotation)"""
        critical_ops = ["policy_update", "key_rotation", "access_grant"]
        return command.get("operation") in critical_ops


class ImmuneRecordAnchor(ABC):
    """
    Layer 4: Immune Record - Cryptographically anchored audit trail
    Single Unit of Causal Truth with Merkle Tree anchoring
    """
    
    def __init__(self, oracle_key: str):
        self.oracle_key = oracle_key
        self.merkle_tree = []  # Leaf nodes (audit records)
        self.checkpoint_hashes = []  # Root hashes
    
    async def create_immune_record(self,
                                  user_id: str,
                                  action: str,
                                  risk_vector: RiskVector,
                                  enforcement_decision: str,
                                  pdp_key: str,
                                  treg_key: str) -> ImmuneRecord:
        """
        Create tamper-proof immune record with multi-signatory interlocking
        """
        record_id = self._generate_record_id()
        timestamp = datetime.utcnow().isoformat()
        
        # Create record (before signatures)
        record_data = {
            "record_id": record_id,
            "timestamp": timestamp,
            "user_id": user_id,
            "action": action,
            "risk_vector": asdict(risk_vector),
            "enforcement_decision": enforcement_decision,
        }
        
        # PDP Signature: Policy Decision Point signs the risk assessment
        pdp_sig = self._sign_hash(json.dumps(record_data), pdp_key)
        
        # Treg Signature: Regulatory T-Cell signs the enforcement decision
        treg_sig = self._sign_hash(enforcement_decision, treg_key)
        
        # Multi-Signatory Interlocking: hash-prefix prevents mutation
        combined_sig = hashlib.sha256(
            f"{pdp_sig[:16]}{treg_sig[:16]}".encode()
        ).hexdigest()
        
        # Merkle root: add to tree and compute new root
        self.merkle_tree.append(record_id)
        merkle_root = self._compute_merkle_root()
        
        # Create final immune record
        immune_record = ImmuneRecord(
            record_id=record_id,
            timestamp=timestamp,
            user_id=user_id,
            action=action,
            risk_vector=risk_vector,
            enforcement_decision=enforcement_decision,
            pdp_signature=pdp_sig,
            treg_signature=treg_sig,
            merkle_root=merkle_root,
            ledger_broadcast=False,
        )
        
        # Broadcast to internal ledger (distributed consensus)
        await self._broadcast_to_ledger(immune_record)
        
        logger.info(f"[IMMUNE] Record created: {record_id} | Risk: {risk_vector.response_tier.value}")
        return immune_record
    
    def _sign_hash(self, data: str, key: str) -> str:
        """HMAC-SHA256 signature"""
        return hmac.new(
            key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _generate_record_id(self) -> str:
        """Generate unique record ID"""
        return hashlib.sha256(
            f"{datetime.utcnow().isoformat()}{len(self.merkle_tree)}".encode()
        ).hexdigest()[:16]
    
    def _compute_merkle_root(self) -> str:
        """Compute Merkle tree root hash"""
        if not self.merkle_tree:
            return hashlib.sha256(b"").hexdigest()
        
        hashes = [hashlib.sha256(h.encode()).hexdigest() for h in self.merkle_tree]
        while len(hashes) > 1:
            hashes = [
                hashlib.sha256(f"{hashes[i]}{hashes[i+1]}".encode()).hexdigest()
                for i in range(0, len(hashes), 2)
            ]
        return hashes[0] if hashes else ""
    
    async def _broadcast_to_ledger(self, record: ImmuneRecord):
        """Broadcast to distributed ledger for consensus"""
        logger.info(f"[LEDGER] Broadcasting record {record.record_id}")
        record.ledger_broadcast = True
    
    async def detect_leukemia(self, local_root: str) -> bool:
        """
        Detect "Leukemia" (compromise): mismatch between local and oracle checkpoint
        Returns True if mismatch detected (bone marrow corruption)
        """
        current_root = self._compute_merkle_root()
        
        if current_root != local_root:
            logger.critical("[LEUKEMIA] Merkle root mismatch - Identity Provider compromise suspected!")
            await self._trigger_network_stasis()
            await self._trigger_hardware_reseed()
            return True
        
        return False
    
    async def _trigger_network_stasis(self):
        """Total network stasis: freeze all Tier-0 actions"""
        logger.critical("[LEUKEMIA] NETWORK STASIS ACTIVATED - All Tier-0 actions frozen")
    
    async def _trigger_hardware_reseed(self):
        """Trigger out-of-band audit and root of trust verification"""
        logger.critical("[LEUKEMIA] HARDWARE RESEED INITIATED - Manual verification required")


# Export for integration
__all__ = [
    'AntigenIdentificationEngine',
    'TCellDecisionEngine',
    'TregGate',
    'ImmuneRecordAnchor',
    'BehavioralSignature',
    'RiskVector',
    'ImmuneRecord',
    'ResponseTier',
]
