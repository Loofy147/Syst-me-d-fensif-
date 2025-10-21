from typing import Callable, Any
from src.core.models import DefenseType


class AttackPattern:
    def __init__(
        self,
        defense_type: DefenseType,
        payload_generator: Callable[[], Any],
        description: str,
        difficulty: int,
    ):
        self.defense_type = defense_type
        self.payload_generator = payload_generator
        self.description = description
        self.difficulty = difficulty
        self.attempts = 0
        self.successes = 0

    def record_attempt(self, success: bool):
        self.attempts += 1
        if success:
            self.successes += 1
