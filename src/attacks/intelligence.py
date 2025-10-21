from collections import defaultdict
from typing import Dict, Any

class AttackerIntelligence:
    """Tracks the effectiveness of different attack strategies."""
    def __init__(self):
        self.payload_effectiveness: Dict[str, Dict[str, int]] = defaultdict(lambda: {"success": 0, "fail": 0})
        self.characteristic_effectiveness: Dict[str, Dict[str, int]] = defaultdict(lambda: {"success": 0, "fail": 0})

    def record_outcome(self, payload: Any, characteristics: Dict[str, Any], success: bool):
        """Records the outcome of an attack."""
        payload_str = str(payload)
        outcome = "success" if success else "fail"

        self.payload_effectiveness[payload_str][outcome] += 1

        for char, value in characteristics.items():
            if value:
                key = f"{char}:{value}"
                self.characteristic_effectiveness[key][outcome] += 1

    def get_most_effective_characteristic(self) -> str:
        """Returns the most effective characteristic seen so far."""
        best_char = ""
        max_ratio = -1

        for char, outcomes in self.characteristic_effectiveness.items():
            total = outcomes["success"] + outcomes["fail"]
            if total > 0:
                ratio = outcomes["success"] / total
                if ratio > max_ratio:
                    max_ratio = ratio
                    best_char = char

        return best_char
