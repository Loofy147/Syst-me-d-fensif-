from typing import List
from src.core.models import DefenseType, EvolvableSeed


class BreakthroughDefenseEvolution:
    """Evolves defenses to handle advanced attacks"""

    @staticmethod
    def evolve_encoding_detection(seed: EvolvableSeed) -> str:
        """Add encoding detection capability"""
        seed.strengthen_defense(DefenseType.SANITIZATION, 5)
        return "🧬 Evolved: Multi-layer encoding detection"

    @staticmethod
    def evolve_type_depth_analysis(seed: EvolvableSeed) -> str:
        """Add deep type inspection"""
        seed.strengthen_defense(DefenseType.TYPE_CHECKING, 5)
        return "🧬 Evolved: Deep type inspection (nested structures)"

    @staticmethod
    def evolve_state_lockdown(seed: EvolvableSeed) -> str:
        """Add aggressive state protection"""
        seed.strengthen_defense(DefenseType.STATE_PROTECTION, 5)
        seed.activate_defense(DefenseType.CRYPTOGRAPHY)
        return "🧬 Evolved: State lockdown + cryptographic validation"

    @staticmethod
    def evolve_resource_limits(seed: EvolvableSeed) -> str:
        """Add resource exhaustion protection"""
        seed.strengthen_defense(DefenseType.BOUNDS_ENFORCEMENT, 5)
        seed.activate_defense(DefenseType.RATE_LIMITING)
        return "🧬 Evolved: Resource limits + rate limiting"

    @staticmethod
    def apply_all_evolutions(seed: EvolvableSeed) -> List[str]:
        """Apply all breakthrough evolutions"""
        evolutions = [
            BreakthroughDefenseEvolution.evolve_encoding_detection(seed),
            BreakthroughDefenseEvolution.evolve_type_depth_analysis(seed),
            BreakthroughDefenseEvolution.evolve_state_lockdown(seed),
            BreakthroughDefenseEvolution.evolve_resource_limits(seed),
        ]
        return evolutions
