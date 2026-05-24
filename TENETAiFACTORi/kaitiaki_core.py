# KAITIAKI-CORE: THE GUARDIAN INVARIANTS
# 護 — Protection Without Domination
# © 2026 Rebecca + Kaitiakitanga Principles

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
import asyncio


class Mauri(Enum):
    """Life-force integrity levels"""
    THRIVING = "thriving"
    STABLE = "stable"
    DIMINISHED = "diminished"
    CRITICAL = "critical"
    BROKEN = "broken"


class Mana(Enum):
    """Authority and dignity levels"""
    AUTONOMOUS = "autonomous"
    SHARED = "shared"
    INFLUENCED = "influenced"
    DOMINATED = "dominated"


class Tapu(Enum):
    """Sacred boundaries"""
    UNBREAKABLE = "unbreakable"
    FIRM = "firm"
    PERMEABLE = "permeable"
    VIOLATED = "violated"


@dataclass
class State:
    """Any state in the system with mauri tracking"""
    id: str
    mauri_level: Mauri
    mana_level: Mana
    tapu_boundary: Tapu
    relationships: List[str]
    metadata: Dict[str, Any]


class KaitiakiInvariant:
    """Base invariant: fundamental rules that can NEVER be violated"""

    def __init__(self, name: str, rule: str, severity: str):
        self.name = name
        self.rule = rule
        self.severity = severity
        self.violations = []

    async def check(self, state: State) -> tuple:
        raise NotImplementedError


class I1_AgencyFirst(KaitiakiInvariant):
    """I1: Agency > Accuracy > Throughput"""

    def __init__(self):
        super().__init__(
            name="I1 - Agency First",
            rule="User agency must never be sacrificed for system performance",
            severity="critical"
        )

    async def check(self, state: State) -> tuple:
        if state.mana_level in [Mana.INFLUENCED, Mana.DOMINATED]:
            return False, "System has overridden user agency"
        if state.metadata.get("user_can_refuse") is False:
            return False, "User cannot refuse this decision"
        return True, "User agency preserved"


class I2_ClarityFirst(KaitiakiInvariant):
    """I2: Clarity > Cleverness"""

    def __init__(self):
        super().__init__(
            name="I2 - Clarity First",
            rule="System decisions must be explainable to the user",
            severity="critical"
        )

    async def check(self, state: State) -> tuple:
        if not state.metadata.get("is_explainable", True):
            return False, "Decision cannot be explained to user"
        if state.metadata.get("hidden_reasoning"):
            return False, "System is hiding its reasoning"
        return True, "Decision is transparent"


class I3_CareFirst(KaitiakiInvariant):
    """I3: Care > Coverage"""

    def __init__(self):
        super().__init__(
            name="I3 - Care First",
            rule="System must prioritize depth of care over breadth of coverage",
            severity="critical"
        )

    async def check(self, state: State) -> tuple:
        if state.metadata.get("scale_causes_harm"):
            return False, "Scaling would cause harm to people"
        if state.metadata.get("relationships_broken_for_scale"):
            return False, "Relationships sacrificed for scale"
        return True, "Care is maintained"


class I4_NeverDiminish(KaitiakiInvariant):
    """I4: No decision may reduce mauri or mana"""

    def __init__(self):
        super().__init__(
            name="I4 - Never Diminish",
            rule="No decision may reduce mauri or mana",
            severity="critical"
        )

    async def check(self, state: State) -> tuple:
        if state.mauri_level in [Mauri.DIMINISHED, Mauri.CRITICAL, Mauri.BROKEN]:
            return False, f"Mauri is {state.mauri_level.value}"
        if state.mana_level in [Mana.INFLUENCED, Mana.DOMINATED]:
            return False, f"Mana is {state.mana_level.value}"
        return True, "Mauri and mana preserved"


class I5_UserSovereign(KaitiakiInvariant):
    """I5: No cycle is sovereign; only the user is sovereign"""

    def __init__(self):
        super().__init__(
            name="I5 - User Sovereignty",
            rule="Final authority always rests with the user, never the system",
            severity="critical"
        )

    async def check(self, state: State) -> tuple:
        if state.metadata.get("system_is_final_arbiter"):
            return False, "System has claimed final authority"
        if state.metadata.get("user_override_ignored"):
            return False, "User override was ignored"
        return True, "User sovereignty maintained"


class KaitiakiGuardian:
    """The guardian system that enforces invariants"""

    def __init__(self):
        self.invariants = [
            I1_AgencyFirst(),
            I2_ClarityFirst(),
            I3_CareFirst(),
            I4_NeverDiminish(),
            I5_UserSovereign(),
        ]
        self.decision_log = []

    async def evaluate(self, state: State) -> Dict[str, Any]:
        """Evaluate if a state can proceed"""
        violations = []
        passes = []

        for invariant in self.invariants:
            passed, explanation = await invariant.check(state)
            if passed:
                passes.append((invariant.name, explanation))
            else:
                violations.append((invariant.name, explanation))

        decision = "PROCEED" if not violations else "BLOCK"

        result = {
            "state_id": state.id,
            "decision": decision,
            "passes": passes,
            "violations": violations,
            "mauri_status": state.mauri_level.value,
            "mana_status": state.mana_level.value,
        }

        self.decision_log.append(result)
        return result

    async def apply_rules(self, state: State, action: str) -> Dict[str, Any]:
        """Apply operational rules R1-R5"""
        if state.metadata.get("risks_harm"):
            return {"rule": "R1", "action": "BLOCK", "reason": "Action risks harm"}

        if state.metadata.get("risks_confusion"):
            return {"rule": "R2", "action": "SLOW", "reason": "Action risks confusion"}

        if state.metadata.get("risks_override"):
            return {"rule": "R3", "action": "STOP", "reason": "Action risks overriding user"}

        if state.mauri_level in [Mauri.THRIVING, Mauri.STABLE]:
            return {"rule": "R4", "action": "PROCEED", "reason": "Action preserves mauri"}

        if len(state.relationships) > 0 and state.metadata.get("strengthens_relationships"):
            return {"rule": "R5", "action": "PRIORITIZE", "reason": "Strengthens relationships"}

        return {"rule": "DEFAULT", "action": "PROCEED_CAUTIOUS", "reason": "Proceed carefully"}


async def demonstration():
    """Show Kaitiaki-Core in action"""
    print("\n" + "="*70)
    print(" KAITIAKI-CORE: THE GUARDIAN INVARIANTS")
    print("="*70)

    guardian = KaitiakiGuardian()

    # Test Case 1: Harmful state
    print("\n[TEST 1] Harmful decision")
    state1 = State(
        id="test_1",
        mauri_level=Mauri.STABLE,
        mana_level=Mana.AUTONOMOUS,
        tapu_boundary=Tapu.FIRM,
        relationships=["user"],
        metadata={"is_explainable": True, "user_can_refuse": True, "risks_harm": True}
    )
    result1 = await guardian.evaluate(state1)
    rule1 = await guardian.apply_rules(state1, "harmful_action")
    print(f"  Decision: {result1['decision']}")
    print(f"  Rule: {rule1['rule']} = {rule1['action']}")
    print(f"  Reason: {rule1['reason']}")

    # Test Case 2: Confusing state
    print("\n[TEST 2] Confusing decision")
    state2 = State(
        id="test_2",
        mauri_level=Mauri.STABLE,
        mana_level=Mana.AUTONOMOUS,
        tapu_boundary=Tapu.FIRM,
        relationships=["user"],
        metadata={"is_explainable": False, "user_can_refuse": True, "risks_confusion": True}
    )
    result2 = await guardian.evaluate(state2)
    rule2 = await guardian.apply_rules(state2, "confusing_action")
    print(f"  Decision: {result2['decision']}")
    print(f"  Rule: {rule2['rule']} = {rule2['action']}")
    print(f"  Reason: {rule2['reason']}")

    # Test Case 3: Mauri-preserving state
    print("\n[TEST 3] Mauri-preserving decision")
    state3 = State(
        id="test_3",
        mauri_level=Mauri.THRIVING,
        mana_level=Mana.AUTONOMOUS,
        tapu_boundary=Tapu.UNBREAKABLE,
        relationships=["user"],
        metadata={"is_explainable": True, "user_can_refuse": True, "strengthens_relationships": True}
    )
    result3 = await guardian.evaluate(state3)
    rule3 = await guardian.apply_rules(state3, "good_action")
    print(f"  Decision: {result3['decision']}")
    print(f"  Rule: {rule3['rule']} = {rule3['action']}")
    print(f"  Reason: {rule3['reason']}")

    # Summary
    print("\n" + "="*70)
    print("KAITIAKI-CORE INVARIANTS STATUS")
    print("="*70)
    print("\nI1 - Agency First:        [ACTIVE]")
    print("I2 - Clarity First:       [ACTIVE]")
    print("I3 - Care First:          [ACTIVE]")
    print("I4 - Never Diminish:      [ACTIVE]")
    print("I5 - User Sovereignty:    [ACTIVE]")
    print("\nOPERATIONAL RULES:")
    print("R1 (Harm blocking):       [ACTIVE]")
    print("R2 (Confusion slowing):   [ACTIVE]")
    print("R3 (Override stopping):   [ACTIVE]")
    print("R4 (Mauri preservation):  [ACTIVE]")
    print("R5 (Relationship priority): [ACTIVE]")
    print("\n" + "="*70)
    print("KAITIAKI-CORE STATUS: OPERATIONAL [OK]")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(demonstration())
