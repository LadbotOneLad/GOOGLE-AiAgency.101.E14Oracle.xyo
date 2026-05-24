# AI_CROWD_KAGGLE_TASKS: Challenge Integration Module
# © 2026 Rebecca
# Connects lattice math engine to AI Crowd and Kaggle competition tasks

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import json
from lattice_math import LatticeMathEngine, RingType


class ChallengeSource(Enum):
    """Challenge source platforms"""
    AICROWD = "aicrowd"
    KAGGLE = "kaggle"
    CUSTOM = "custom"


class ChallengeStatus(Enum):
    """Challenge lifecycle"""
    DISCOVERY = "discovery"           # Found, not yet registered
    REGISTERED = "registered"         # Registered with human
    LATTICE_EVALUATION = "lattice_evaluation"  # Running through three-ring consensus
    HUMAN_REVIEW = "human_review"     # Awaiting human decision
    APPROVED = "approved"             # Human approved
    SUBMISSION_READY = "submission_ready"      # Ready to submit
    SUBMITTED = "submitted"           # Submitted to platform
    COMPLETED = "completed"           # Result received
    REJECTED = "rejected"             # Rejected by human or lattice


@dataclass
class ChallengeTask:
    """A single challenge task from AI Crowd or Kaggle"""
    challenge_id: str
    source: ChallengeSource
    title: str
    description: str
    prize_pool: float                 # USD
    deadline: str                     # ISO format
    data_size_mb: float
    estimated_difficulty: float       # 0-1, human estimate
    
    # Submission requirements
    submission_format: str            # e.g., "CSV", "JSON", "Code"
    evaluation_metric: str            # e.g., "AUC", "RMSE", "Accuracy"
    
    # Metadata
    discovered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    status: ChallengeStatus = ChallengeStatus.DISCOVERY
    lattice_eval_result: Optional[Dict[str, Any]] = None
    human_approval: Optional[str] = None  # "APPROVED" or "REJECTED"
    submission_score: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "challenge_id": self.challenge_id,
            "source": self.source.value,
            "title": self.title,
            "description": self.description,
            "prize_pool": self.prize_pool,
            "deadline": self.deadline,
            "data_size_mb": self.data_size_mb,
            "estimated_difficulty": self.estimated_difficulty,
            "submission_format": self.submission_format,
            "evaluation_metric": self.evaluation_metric,
            "discovered_at": self.discovered_at,
            "status": self.status.value,
            "human_approval": self.human_approval,
            "submission_score": self.submission_score,
        }


@dataclass
class LatticePowerSignal:
    """Power signal for lattice evaluation based on challenge characteristics"""
    base_power: float                 # [0, 1]
    difficulty_adjustment: float      # -0.3 to +0.3
    prize_adjustment: float           # +0.1 if high prize
    time_pressure: float              # 0-1, closer to deadline = higher
    
    data_complexity: float            # 0-1, based on data_size_mb
    metric_alignment: float           # 0-1, how well metric aligns with system
    
    final_power: float = field(init=False)
    
    def __post_init__(self):
        """Compute final power signal"""
        self.final_power = self.base_power + self.difficulty_adjustment + self.prize_adjustment + self.time_pressure
        self.final_power = max(0.0, min(1.0, self.final_power))  # Clamp to [0, 1]


class ChallengeEvaluator:
    """
    Evaluates challenges using lattice math three-ring consensus.
    
    Process:
    1. Discover challenge (AI Crowd API or Kaggle API)
    2. Extract features → compute power signal
    3. Run lattice evaluation (validator, sovereign, TENET)
    4. Return decision to human
    5. Human approves/rejects
    6. If approved: prepare and submit solution
    """
    
    def __init__(self):
        self.lattice_engine = LatticeMathEngine()
        self.challenges: Dict[str, ChallengeTask] = {}
        self.evaluation_history: List[Dict[str, Any]] = []
        self.tick_counter = 0
    
    def discover_aicrowd_challenge(
        self,
        challenge_id: str,
        title: str,
        description: str,
        prize_pool: float,
        deadline: str,
        data_size_mb: float,
        submission_format: str,
        evaluation_metric: str,
    ) -> ChallengeTask:
        """Discover a challenge from AI Crowd"""
        task = ChallengeTask(
            challenge_id=challenge_id,
            source=ChallengeSource.AICROWD,
            title=title,
            description=description,
            prize_pool=prize_pool,
            deadline=deadline,
            data_size_mb=data_size_mb,
            estimated_difficulty=0.5,  # Default, can be refined
            submission_format=submission_format,
            evaluation_metric=evaluation_metric,
        )
        self.challenges[challenge_id] = task
        return task
    
    def discover_kaggle_challenge(
        self,
        challenge_id: str,
        title: str,
        description: str,
        prize_pool: float,
        deadline: str,
        data_size_mb: float,
        submission_format: str,
        evaluation_metric: str,
    ) -> ChallengeTask:
        """Discover a challenge from Kaggle"""
        task = ChallengeTask(
            challenge_id=challenge_id,
            source=ChallengeSource.KAGGLE,
            title=title,
            description=description,
            prize_pool=prize_pool,
            deadline=deadline,
            data_size_mb=data_size_mb,
            estimated_difficulty=0.5,
            submission_format=submission_format,
            evaluation_metric=evaluation_metric,
        )
        self.challenges[challenge_id] = task
        return task
    
    def compute_power_signal(self, challenge: ChallengeTask) -> LatticePowerSignal:
        """
        Compute power signal for lattice evaluation.
        
        Considers:
        - Challenge difficulty
        - Prize pool
        - Time pressure
        - Data complexity
        - Metric alignment
        """
        # Difficulty → power adjustment
        difficulty_adjustment = (challenge.estimated_difficulty - 0.5) * 0.3  # -0.15 to +0.15
        
        # Prize pool → power boost (high prize = higher priority)
        prize_adjustment = 0.1 if challenge.prize_pool > 50000 else 0.0
        
        # Time pressure (simplified: assume constant 0.1 for now)
        time_pressure = 0.1
        
        # Data complexity (log scale: 0-100MB → 0-0.5)
        data_complexity = min(0.5, challenge.data_size_mb / 200.0)
        
        # Metric alignment (simplified: 0.7 default)
        metric_alignment = 0.7
        
        return LatticePowerSignal(
            base_power=0.65,
            difficulty_adjustment=difficulty_adjustment,
            prize_adjustment=prize_adjustment,
            time_pressure=time_pressure,
            data_complexity=data_complexity,
            metric_alignment=metric_alignment,
        )
    
    def evaluate_challenge_with_lattice(self, challenge_id: str) -> Dict[str, Any]:
        """
        Run challenge through three-ring lattice consensus.
        
        Returns lattice decision + reasoning for human review.
        """
        if challenge_id not in self.challenges:
            return {"error": f"Challenge {challenge_id} not found"}
        
        challenge = self.challenges[challenge_id]
        challenge.status = ChallengeStatus.LATTICE_EVALUATION
        
        # Compute power signal
        signal = self.compute_power_signal(challenge)
        
        # Run lattice evaluation
        self.tick_counter += 1
        lattice_result = self.lattice_engine.three_ring_consensus(
            tick=self.tick_counter,
            power=signal.final_power,
            drift_used=self.tick_counter / 2,
        )
        
        # Store result
        challenge.lattice_eval_result = lattice_result
        challenge.status = ChallengeStatus.HUMAN_REVIEW
        
        # Log evaluation
        self.evaluation_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "challenge_id": challenge_id,
            "power_signal": {
                "base": signal.base_power,
                "difficulty_adj": signal.difficulty_adjustment,
                "prize_adj": signal.prize_adjustment,
                "time_pressure": signal.time_pressure,
                "final": signal.final_power,
            },
            "lattice_decision": lattice_result["final_decision"],
            "consensus_reason": lattice_result["consensus_reason"],
        })
        
        return {
            "challenge_id": challenge_id,
            "title": challenge.title,
            "source": challenge.source.value,
            "power_signal": signal.final_power,
            "lattice_result": lattice_result,
            "awaiting_human_review": True,
        }
    
    def human_approve_challenge(self, challenge_id: str, notes: str = "") -> Dict[str, Any]:
        """Human approves challenge for submission"""
        if challenge_id not in self.challenges:
            return {"error": f"Challenge {challenge_id} not found"}
        
        challenge = self.challenges[challenge_id]
        challenge.human_approval = "APPROVED"
        challenge.status = ChallengeStatus.SUBMISSION_READY
        
        return {
            "success": True,
            "challenge_id": challenge_id,
            "title": challenge.title,
            "status": challenge.status.value,
            "next_step": "Submit solution to platform",
        }
    
    def human_reject_challenge(self, challenge_id: str, reason: str) -> Dict[str, Any]:
        """Human rejects challenge"""
        if challenge_id not in self.challenges:
            return {"error": f"Challenge {challenge_id} not found"}
        
        challenge = self.challenges[challenge_id]
        challenge.human_approval = "REJECTED"
        challenge.status = ChallengeStatus.REJECTED
        
        return {
            "success": True,
            "challenge_id": challenge_id,
            "title": challenge.title,
            "status": challenge.status.value,
            "reason": reason,
        }
    
    def submit_solution(self, challenge_id: str, solution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit solution to platform"""
        if challenge_id not in self.challenges:
            return {"error": f"Challenge {challenge_id} not found"}
        
        challenge = self.challenges[challenge_id]
        if challenge.status != ChallengeStatus.SUBMISSION_READY:
            return {"error": f"Challenge not ready for submission (status: {challenge.status.value})"}
        
        # Simulate submission
        challenge.status = ChallengeStatus.SUBMITTED
        
        return {
            "success": True,
            "challenge_id": challenge_id,
            "title": challenge.title,
            "submission_time": datetime.utcnow().isoformat(),
            "message": f"Solution submitted to {challenge.source.value}",
        }
    
    def get_dashboard(self) -> Dict[str, Any]:
        """Get overview of all challenges"""
        by_status = {}
        for challenge in self.challenges.values():
            status = challenge.status.value
            if status not in by_status:
                by_status[status] = []
            by_status[status].append({
                "id": challenge.challenge_id,
                "title": challenge.title,
                "source": challenge.source.value,
                "prize": challenge.prize_pool,
                "deadline": challenge.deadline,
            })
        
        return {
            "total_challenges": len(self.challenges),
            "by_status": by_status,
            "recent_evaluations": self.evaluation_history[-10:],
        }


# Example usage
if __name__ == "__main__":
    print("AI CROWD & KAGGLE CHALLENGE INTEGRATION")
    print("=" * 70 + "\n")
    
    evaluator = ChallengeEvaluator()
    
    # Discover challenges
    print("1. DISCOVERING CHALLENGES")
    print("-" * 70)
    
    kaggle_challenge = evaluator.discover_kaggle_challenge(
        challenge_id="kaggle-titanic-001",
        title="Titanic Survival Prediction",
        description="Predict which passengers survived the Titanic disaster",
        prize_pool=5000.0,
        deadline="2026-05-01T23:59:59Z",
        data_size_mb=15.0,
        submission_format="CSV",
        evaluation_metric="Accuracy",
    )
    print(f"✓ Discovered Kaggle: {kaggle_challenge.title}")
    
    aicrowd_challenge = evaluator.discover_aicrowd_challenge(
        challenge_id="aicrowd-traffic-001",
        title="Traffic Flow Prediction",
        description="Predict urban traffic patterns using ML",
        prize_pool=75000.0,
        deadline="2026-04-15T23:59:59Z",
        data_size_mb=250.0,
        submission_format="JSON",
        evaluation_metric="RMSE",
    )
    print(f"✓ Discovered AI Crowd: {aicrowd_challenge.title}\n")
    
    # Evaluate with lattice
    print("2. LATTICE EVALUATION")
    print("-" * 70)
    
    for challenge_id in ["kaggle-titanic-001", "aicrowd-traffic-001"]:
        result = evaluator.evaluate_challenge_with_lattice(challenge_id)
        print(f"\n{result['title']} ({result['source']}):")
        print(f"  Power Signal: {result['power_signal']:.3f}")
        print(f"  Validator: {result['lattice_result']['validator']['decision']}")
        print(f"  Sovereign: {result['lattice_result']['sovereign']['decision']}")
        print(f"  TENET: {result['lattice_result']['tenet']['decision']}")
        print(f"  → LATTICE: {result['lattice_result']['final_decision']}")
    
    # Human review
    print("\n" + "=" * 70)
    print("3. HUMAN APPROVAL")
    print("-" * 70)
    
    approval1 = evaluator.human_approve_challenge("kaggle-titanic-001", "Good prize, manageable data")
    print(f"\n✓ Approved: {approval1['title']}")
    
    rejection = evaluator.human_reject_challenge("aicrowd-traffic-001", "Data too large, timeline too tight")
    print(f"✗ Rejected: {rejection['title']} ({rejection['reason']})")
    
    # Submit
    print("\n" + "=" * 70)
    print("4. SUBMISSION")
    print("-" * 70)
    
    submission = evaluator.submit_solution(
        "kaggle-titanic-001",
        {"model": "random_forest", "features": ["age", "fare", "pclass"]}
    )
    print(f"\n✓ Submitted: {submission['title']}")
    print(f"  Time: {submission['submission_time']}")
    
    # Dashboard
    print("\n" + "=" * 70)
    print("5. DASHBOARD")
    print("-" * 70)
    dashboard = evaluator.get_dashboard()
    print(json.dumps(dashboard, indent=2))
