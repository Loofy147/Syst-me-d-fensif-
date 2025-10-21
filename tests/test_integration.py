import unittest
from unittest.mock import Mock, patch
from src.orchestration import AutonomousLearningSystem
from src.attacks.orchestration import ScenarioOrchestrator, AdaptiveArsenalScenario
from src.attacks.advanced import AdvancedRedTeamExecutor
from src.attacks.intelligence import AttackerIntelligence
from src.core.models import EvolvableSeed

class TestScenarioIntegration(unittest.TestCase):

    def setUp(self):
        """Set up components needed for scenario tests."""
        self.mock_seed = Mock(spec=EvolvableSeed)
        self.mock_seed.test_defense.return_value = (True, "Blocked by mock defense")

        self.attacker_intel = AttackerIntelligence()
        self.red_team_executor = AdvancedRedTeamExecutor(self.mock_seed, self.attacker_intel)
        self.orchestrator = ScenarioOrchestrator(self.red_team_executor)

    def test_adaptive_arsenal_scenario_generation(self):
        """
        Test that the AdaptiveArsenalScenario correctly generates a wave of attacks.
        """
        scenario = AdaptiveArsenalScenario(self.red_team_executor)
        wave = scenario.generate_adaptive_wave(generation=1, num_attacks=5)

        self.assertEqual(len(wave), 5)
        self.assertIsInstance(wave[0], tuple)
        self.assertIsNotNone(wave[0][1]) # Check that payload is not None

    def test_orchestrator_includes_adaptive_attacks(self):
        """
        Test that the main ScenarioOrchestrator includes attacks from the
        AdaptiveArsenalScenario in its campaigns.
        """
        campaign = self.orchestrator.generate_orchestrated_campaign(generation=1)

        adaptive_attacks_found = any(scenario_name == "adaptive_arsenal" for scenario_name, _, _, _ in campaign)
        self.assertTrue(adaptive_attacks_found, "Campaign should include attacks from AdaptiveArsenalScenario")

class TestFullSystemIntegration(unittest.TestCase):

    def test_learning_cycle_runs_with_new_intelligence(self):
        """
        Test that the full AutonomousLearningSystem runs and the new attacker
        intelligence module is actively used.
        """
        from src.config import config
        config.settings['simulation']['max_generations'] = 1

        system = AutonomousLearningSystem("IntegrationTestSystem")
        initial_attack_count = system.attacker_intelligence.total_attacks

        system.run_learning_cycle()

        self.assertEqual(len(system.learning_history), 1)
        # Verify that the intelligence module was engaged and recorded attacks
        self.assertGreater(system.attacker_intelligence.total_attacks, initial_attack_count)

if __name__ == '__main__':
    unittest.main()
