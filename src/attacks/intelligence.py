"""
ATTACKER INTELLIGENCE MODULE
=============================

An intelligent adversarial system that learns, adapts, and evolves attack strategies.

Core Capabilities:
------------------
1. ATTACK MEMORY: Tracks success/failure of every payload variant
2. PARAMETER OPTIMIZATION: Tunes attack parameters (size, encoding, nesting)
3. DEFENSE PROFILING: Builds model of defender's strengths/weaknesses
4. STRATEGIC PLANNING: Plans multi-step attack campaigns
5. DECEPTION: Intentionally triggers defenses to gather intelligence
6. ADAPTATION: Evolves attack genome based on outcomes
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Tuple, Optional, Set
from enum import Enum
from collections import defaultdict
import random
import hashlib
import json


# ============================================================================
# ATTACK INTELLIGENCE CORE
# ============================================================================

class AttackVector(Enum):
    """Attack vector categories"""
    INJECTION = "injection"
    OVERFLOW = "overflow"
    TYPE_CONFUSION = "type_confusion"
    ENCODING = "encoding"
    STATE_CORRUPTION = "state_corruption"
    LOGIC_BOMB = "logic_bomb"
    RESOURCE_EXHAUSTION = "resource_exhaustion"


@dataclass
class PayloadCharacteristics:
    """Characteristics of an attack payload"""
    vector: AttackVector
    size: int
    encoding_layers: int
    complexity: int  # Nesting depth
    obfuscation_level: int  # 0-10
    uses_quotes: bool
    uses_special_chars: bool
    is_polymorphic: bool

    def to_dict(self) -> Dict:
        return {
            "vector": self.vector.value,
            "size": self.size,
            "encoding_layers": self.encoding_layers,
            "complexity": self.complexity,
            "obfuscation_level": self.obfuscation_level,
            "uses_quotes": self.uses_quotes,
            "uses_special_chars": self.uses_special_chars,
            "is_polymorphic": self.is_polymorphic,
        }


@dataclass
class AttackOutcome:
    """Result of an attack attempt"""
    payload_hash: str
    characteristics: PayloadCharacteristics
    blocked: bool
    defense_type_triggered: str
    defense_reason: str
    timestamp: int

    @property
    def success(self) -> bool:
        return not self.blocked


@dataclass
class DefenseProfile:
    """Intelligence profile of a defense mechanism"""
    defense_type: str
    strength_estimate: float  # 0.0-1.0
    sensitivity_to_size: float
    sensitivity_to_encoding: float
    sensitivity_to_complexity: float
    known_weaknesses: List[str] = field(default_factory=list)
    bypass_success_rate: Dict[str, float] = field(default_factory=dict)
    times_encountered: int = 0

    def update_from_outcome(self, outcome: AttackOutcome):
        """Update profile based on attack outcome"""
        self.times_encountered += 1

        if outcome.blocked:
            # Defense worked - estimate it's stronger
            self.strength_estimate = min(1.0, self.strength_estimate + 0.05)

            # Update sensitivities
            if outcome.characteristics.size > 1000:
                self.sensitivity_to_size += 0.1
            if outcome.characteristics.encoding_layers > 0:
                self.sensitivity_to_encoding += 0.1
            if outcome.characteristics.complexity > 2:
                self.sensitivity_to_complexity += 0.1
        else:
            # Attack succeeded - defense has weakness
            self.strength_estimate = max(0.0, self.strength_estimate - 0.1)

            # Record bypass technique
            technique = self._describe_technique(outcome.characteristics)
            if technique not in self.bypass_success_rate:
                self.bypass_success_rate[technique] = 0.0

            # Increase success rate for this technique
            current_rate = self.bypass_success_rate[technique]
            self.bypass_success_rate[technique] = min(1.0, current_rate + 0.2)

    def _describe_technique(self, chars: PayloadCharacteristics) -> str:
        """Describe the technique that worked"""
        parts = [chars.vector.value]
        if chars.encoding_layers > 0:
            parts.append(f"encoded_{chars.encoding_layers}x")
        if chars.complexity > 2:
            parts.append(f"nested_{chars.complexity}")
        if chars.obfuscation_level > 5:
            parts.append("obfuscated")
        return "_".join(parts)


class AttackerIntelligence:
    """Central intelligence system for attacker"""

    def __init__(self):
        self.attack_history: List[AttackOutcome] = []
        self.defense_profiles: Dict[str, DefenseProfile] = {}
        self.successful_payloads: Dict[str, PayloadCharacteristics] = {}
        self.failed_payloads: Dict[str, PayloadCharacteristics] = {}
        self.generation = 0
        self.total_attacks = 0
        self.total_successes = 0

        # Parameter optimization state
        self.optimal_parameters: Dict[AttackVector, Dict[str, Any]] = {
            vector: self._default_parameters() for vector in AttackVector
        }

        # Strategic intelligence
        self.defender_pattern_memory: List[str] = []
        self.deception_targets: Set[str] = set()

    def _default_parameters(self) -> Dict[str, Any]:
        """Default attack parameters"""
        return {
            "size": 500,
            "encoding_layers": 0,
            "complexity": 1,
            "obfuscation_level": 3,
        }

    def record_attack(self, payload: Any, payload_chars: PayloadCharacteristics,
                     blocked: bool, defense_type: str, reason: str) -> AttackOutcome:
        """Record attack outcome and learn from it"""

        payload_hash = self._hash_payload(payload, payload_chars)

        outcome = AttackOutcome(
            payload_hash=payload_hash,
            characteristics=payload_chars,
            blocked=blocked,
            defense_type_triggered=defense_type,
            defense_reason=reason,
            timestamp=self.generation
        )

        self.attack_history.append(outcome)
        self.total_attacks += 1

        if not blocked:
            self.total_successes += 1
            self.successful_payloads[payload_hash] = payload_chars
        else:
            self.failed_payloads[payload_hash] = payload_chars

        # Update defense profile
        if defense_type not in self.defense_profiles:
            self.defense_profiles[defense_type] = DefenseProfile(
                defense_type=defense_type,
                strength_estimate=0.5,
                sensitivity_to_size=0.5,
                sensitivity_to_encoding=0.5,
                sensitivity_to_complexity=0.5
            )

        self.defense_profiles[defense_type].update_from_outcome(outcome)

        # Optimize parameters
        self._optimize_parameters(outcome)

        return outcome

    def _hash_payload(self, payload: Any, chars: PayloadCharacteristics) -> str:
        """Generate unique hash for payload"""
        content = f"{payload}_{chars.to_dict()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def _optimize_parameters(self, outcome: AttackOutcome):
        """Optimize attack parameters based on outcome"""

        vector = outcome.characteristics.vector
        current_params = self.optimal_parameters[vector]

        if outcome.success:
            # This configuration worked - reinforce it
            current_params["size"] = int(outcome.characteristics.size * 0.9 + current_params["size"] * 0.1)
            current_params["encoding_layers"] = max(
                outcome.characteristics.encoding_layers,
                current_params["encoding_layers"]
            )
            current_params["complexity"] = max(
                outcome.characteristics.complexity,
                current_params["complexity"]
            )
            current_params["obfuscation_level"] = max(
                outcome.characteristics.obfuscation_level,
                current_params["obfuscation_level"]
            )
        else:
            # Failed - try different parameters
            if "size" in outcome.defense_reason.lower():
                # Size was the issue - reduce it
                current_params["size"] = int(current_params["size"] * 0.7)

            if "encoded" in outcome.defense_reason.lower() or "decode" in outcome.defense_reason.lower():
                # Encoding detected - add more layers
                current_params["encoding_layers"] += 1

            if "type" in outcome.defense_reason.lower() or "complex" in outcome.defense_reason.lower():
                # Type issue - increase complexity to confuse
                current_params["complexity"] += 1

    def get_optimal_parameters(self, vector: AttackVector) -> Dict[str, Any]:
        """Get optimal parameters for attack vector"""
        return self.optimal_parameters[vector].copy()

    def identify_weakest_defense(self) -> Optional[str]:
        """Identify the weakest defense mechanism"""
        if not self.defense_profiles:
            return None

        weakest = min(
            self.defense_profiles.items(),
            key=lambda x: x[1].strength_estimate
        )

        return weakest[0]

    def identify_strongest_defense(self) -> Optional[str]:
        """Identify the strongest defense mechanism"""
        if not self.defense_profiles:
            return None

        strongest = max(
            self.defense_profiles.items(),
            key=lambda x: x[1].strength_estimate
        )

        return strongest[0]

    def plan_deception_attack(self) -> List[Tuple[str, str]]:
        """Plan attacks to deceive defender"""

        strongest = self.identify_strongest_defense()
        weakest = self.identify_weakest_defense()

        if not strongest or not weakest:
            return []

        # Strategy: Bait defender into over-strengthening strong defense
        # Then exploit the weak defense

        plan = [
            ("bait", strongest),  # Intentionally trigger strong defense
            ("bait", strongest),  # Multiple times to draw attention
            ("bait", strongest),
            ("exploit", weakest),  # Then hit the weak point
        ]

        self.deception_targets.add(strongest)

        return plan

    def get_success_rate(self) -> float:
        """Get overall success rate"""
        if self.total_attacks == 0:
            return 0.0
        return self.total_successes / self.total_attacks

    def get_intelligence_report(self) -> Dict[str, Any]:
        """Generate comprehensive intelligence report"""

        report = {
            "generation": self.generation,
            "total_attacks": self.total_attacks,
            "total_successes": self.total_successes,
            "success_rate": self.get_success_rate(),
            "defense_profiles": {},
            "optimal_parameters": {},
            "strategic_insights": []
        }

        # Defense profiles
        for defense_type, profile in self.defense_profiles.items():
            report["defense_profiles"][defense_type] = {
                "strength": profile.strength_estimate,
                "sensitivity_size": profile.sensitivity_to_size,
                "sensitivity_encoding": profile.sensitivity_to_encoding,
                "sensitivity_complexity": profile.sensitivity_to_complexity,
                "bypass_techniques": profile.bypass_success_rate,
            }

        # Optimal parameters
        for vector, params in self.optimal_parameters.items():
            report["optimal_parameters"][vector.value] = params

        # Strategic insights
        weakest = self.identify_weakest_defense()
        strongest = self.identify_strongest_defense()

        if weakest:
            report["strategic_insights"].append(f"Weakest defense: {weakest}")
        if strongest:
            report["strategic_insights"].append(f"Strongest defense: {strongest}")

        if self.get_success_rate() > 0.5:
            report["strategic_insights"].append("High success rate - consider increasing difficulty")
        elif self.get_success_rate() < 0.2:
            report["strategic_insights"].append("Low success rate - need strategy pivot")

        return report

    def next_generation(self):
        """Advance to next generation"""
        self.generation += 1

    def print_intelligence_state(self):
        """Print current intelligence state"""

        print(f"\n🎯 ATTACKER INTELLIGENCE STATE (Gen {self.generation})")
        print(f"{'='*90}")

        print(f"\n📊 Attack Statistics:")
        print(f"  Total Attacks: {self.total_attacks}")
        print(f"  Successful: {self.total_successes}")
        print(f"  Success Rate: {self.get_success_rate()*100:.1f}%")

        if self.defense_profiles:
            print(f"\n🛡️  Defense Intelligence:")
            sorted_defenses = sorted(
                self.defense_profiles.items(),
                key=lambda x: x[1].strength_estimate
            )

            for defense_type, profile in sorted_defenses:
                bar = "█" * int(profile.strength_estimate * 10) + "░" * (10 - int(profile.strength_estimate * 10))
                print(f"  {defense_type:25} {bar} Strength: {profile.strength_estimate:.2f}")

                if profile.bypass_success_rate:
                    best_technique = max(profile.bypass_success_rate.items(), key=lambda x: x[1])
                    print(f"    → Best bypass: {best_technique[0]} ({best_technique[1]*100:.0f}% success)")

        print(f"\n⚙️  Optimal Parameters:")
        for vector, params in list(self.optimal_parameters.items())[:3]:
            print(f"  {vector.value:20} Size:{params['size']:5d} | Enc:{params['encoding_layers']} | Complex:{params['complexity']} | Obfusc:{params['obfuscation_level']}")

        weakest = self.identify_weakest_defense()
        strongest = self.identify_strongest_defense()

        if weakest or strongest:
            print(f"\n🎯 Strategic Assessment:")
            if weakest:
                print(f"  WEAKEST: {weakest} - Priority target")
            if strongest:
                print(f"  STRONGEST: {strongest} - Avoid or use deception")

        print(f"{'='*90}\n")