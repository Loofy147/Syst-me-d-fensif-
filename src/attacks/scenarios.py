"""
ADVANCED ATTACK SCENARIOS
===========================

This module defines strategic scenarios for the Red Team to execute, moving beyond
simple attack suites to sophisticated, multi-stage campaigns that test the
defender's adaptability and intelligence.
"""

import random
from src.core.models import DefenseType
from src.attacks.advanced import AdvancedRedTeamExecutor

class CounterIntelligenceScenario:
    """
    A scenario designed to mislead the defense AI.

    It operates in two stages:
    1. Baiting Phase: Repeatedly attacks a specific defense type with noticeable,
       low-to-mid difficulty attacks to encourage the defender to over-invest.
    2. Exploit Phase: Abruptly switches to a different, high-difficulty attack
       vector, exploiting the fact that the defender's resources have been
       misallocated.
    """
    def __init__(self, red_team_executor: AdvancedRedTeamExecutor, generations: int = 10):
        self.red_team_executor = red_team_executor
        self.total_generations = generations
        self.bait_phase_duration = max(3, generations // 2)

        # Select bait and exploit targets
        self.bait_type = random.choice([
            DefenseType.SANITIZATION,
            DefenseType.INPUT_VALIDATION,
            DefenseType.TYPE_CHECKING
        ])
        self.exploit_type = random.choice([
            DefenseType.STATE_PROTECTION,
            DefenseType.BOUNDS_ENFORCEMENT,
            DefenseType.RATE_LIMITING
        ])

        # Ensure they are different
        while self.bait_type == self.exploit_type:
            self.exploit_type = random.choice(list(DefenseType))

        print("="*50)
        print("COUNTER-INTELLIGENCE SCENARIO INITIALIZED")
        print(f"  Baiting Defense: {self.bait_type.name}")
        print(f"  Exploit Target:  {self.exploit_type.name}")
        print(f"  Duration:        {self.total_generations} generations")
        print("="*50)

    def run(self):
        """Executes the full bait-and-switch scenario."""
        for gen in range(self.total_generations):
            self.red_team_executor.generation = gen
            if gen < self.bait_phase_duration:
                print(f"\n--- SCENARIO: Baiting Phase (Generation {gen+1}/{self.total_generations}) ---")
                self._execute_baiting_run()
            else:
                print(f"\n--- SCENARIO: Exploit Phase (Generation {gen+1}/{self.total_generations}) ---")
                self._execute_exploit_run()

            # Here, we would normally pass the results to the orchestrator to evolve the defense.
            # For this simulation, we are just running the attack side.

    def _execute_baiting_run(self):
        """Focuses attacks on the bait defense type."""
        original_patterns = self.red_team_executor.advanced_patterns

        # Filter for bait attacks, including some noise
        bait_patterns = [
            p for p in original_patterns
            if p.defense_type == self.bait_type and p.difficulty <= 7
        ]
        noise_patterns = random.sample(
            [p for p in original_patterns if p.defense_type != self.bait_type],
            k=2
        )

        self.red_team_executor.advanced_patterns = bait_patterns + noise_patterns
        print(f"  Focusing {len(bait_patterns)} attacks on {self.bait_type.name} to bait the defense.")
        self.red_team_executor.execute_advanced_suite()

        # Restore original patterns
        self.red_team_executor.advanced_patterns = original_patterns

    def _execute_exploit_run(self):
        """Focuses attacks on the exploit defense type."""
        original_patterns = self.red_team_executor.advanced_patterns

        # Filter for high-difficulty exploit attacks
        exploit_patterns = [
            p for p in original_patterns
            if p.defense_type == self.exploit_type and p.difficulty >= 8
        ]

        # If no high-difficulty exploits, take any from that category
        if not exploit_patterns:
            exploit_patterns = [
                p for p in original_patterns if p.defense_type == self.exploit_type
            ]

        self.red_team_executor.advanced_patterns = exploit_patterns
        print(f"  Switching to {len(exploit_patterns)} high-difficulty attacks on {self.exploit_type.name}.")
        self.red_team_executor.execute_advanced_suite()

        # Restore original patterns
        self.red_team_executor.advanced_patterns = original_patterns
