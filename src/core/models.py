from enum import Enum
from typing import Dict, Any, Tuple


class DefenseType(Enum):
    """Enumeration of the different types of defense mechanisms."""

    SANITIZATION = "sanitization"
    INPUT_VALIDATION = "input_validation"
    TYPE_CHECKING = "type_checking"
    BOUNDS_ENFORCEMENT = "bounds_enforcement"
    STATE_PROTECTION = "state_protection"
    RATE_LIMITING = "rate_limiting"
    CRYPTOGRAPHY = "cryptography"


class SeverityLevel(Enum):
    """Enumeration of the different severity levels of an exploit."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DefenseConfig:
    """Configuration for a defense mechanism."""

    def __init__(self, defense_type: DefenseType, active: bool, strength: int):
        self.defense_type = defense_type
        self.active = active
        self.strength = strength


class DefenseMechanism:
    """Abstract base class for a defense mechanism."""

    def __init__(self, config: DefenseConfig):
        self.config = config

    def evaluate(self, value: Any) -> Tuple[bool, str]:
        """
        Evaluates a given value. The default mechanism is permissive.
        This method should be overridden by concrete defense mechanisms.
        """
        return False, "Passed by default permissive mechanism"


class EvolvableSeed:
    """Represents the core of the autonomous learning system."""

    def __init__(self, name: str):
        self.name = name
        self.defense_framework = DefenseFramework()

    def test_defense(self, defense_type: DefenseType, payload: Any) -> Tuple[bool, str]:
        """Tests a given defense mechanism with a given payload."""
        return self.defense_framework.test_defense(defense_type, payload)

    def strengthen_defense(self, defense_type: DefenseType, amount: int):
        """Strengthens a given defense mechanism by a given amount."""
        self.defense_framework.strengthen_defense(defense_type, amount)

    def activate_defense(self, defense_type: DefenseType):
        """Activates a given defense mechanism."""
        self.defense_framework.activate_defense(defense_type)

    def get_defense_snapshot(self) -> Dict[str, Any]:
        """Returns a snapshot of the current state of the defense framework."""
        return self.defense_framework.get_snapshot()


class DefenseFramework:
    def __init__(self):
        self.defenses: Dict[DefenseType, DefenseMechanism] = {
            dt: DefenseMechanism(DefenseConfig(dt, active=True, strength=5))
            for dt in DefenseType
        }

    def test_defense(self, defense_type: DefenseType, payload: Any) -> Tuple[bool, str]:
        defense = self.defenses.get(defense_type)
        if defense and defense.config.active:
            return defense.evaluate(payload)
        return False, "Defense inactive"

    def strengthen_defense(self, defense_type: DefenseType, amount: int):
        if defense_type in self.defenses:
            self.defenses[defense_type].config.strength = min(
                10, self.defenses[defense_type].config.strength + amount
            )

    def activate_defense(self, defense_type: DefenseType):
        if defense_type in self.defenses:
            self.defenses[defense_type].config.active = True

    def get_snapshot(self) -> Dict[str, Any]:
        return {
            dt.name: {
                "active": d.config.active,
                "strength": d.config.strength,
            }
            for dt, d in self.defenses.items()
        }


class Exploit:
    def __init__(
        self,
        vector: DefenseType,
        description: str,
        payload: Any,
        severity: SeverityLevel,
        difficulty: int,
        blocked: bool,
        defense_reason: str,
    ):
        self.vector = vector
        self.description = description
        self.payload = payload
        self.severity = severity
        self.difficulty = difficulty
        self.blocked = blocked
        self.defense_reason = defense_reason
