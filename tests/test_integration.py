import unittest
from unittest.mock import Mock, patch
from src.orchestration import AutonomousLearningSystem
from src.attacks.orchestration import ScenarioOrchestrator, AdaptiveArsenalScenario
from src.attacks.scenarios import CounterIntelligenceScenario
from src.attacks.advanced import AdvancedRedTeamExecutor
from src.attacks.intelligence import AttackerIntelligence
from src.core.models import EvolvableSeed

class TestScenarioIntegration(unittest.TestCase):

    def setUp(self):
        """Set up components needed for scenario tests."""
        self.mock_seed = Mock(spec=EvolvableSeed)
        # Mock the test_defense method to return a consistent result
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

        # Should generate the requested number of attacks
        self.assertEqual(len(wave), 5)
        # Each item should be a tuple of (attack_type_str, payload)
        self.assertIsInstance(wave[0], tuple)
        self.assertIsInstance(wave[0][0], str)
        self.assertIsNotNone(wave[0][1])

    def test_orchestrator_includes_adaptive_attacks(self):
        """
        Test that the main ScenarioOrchestrator includes attacks from the
        AdaptiveArsenalScenario in its campaigns.
        """
        campaign = self.orchestrator.generate_orchestrated_campaign(generation=1)

        # Check if the 'adaptive_arsenal' scenario was included in the campaign
        adaptive_attacks_found = any(scenario_name == "adaptive_arsenal" for scenario_name, _, _ in campaign)
        self.assertTrue(adaptive_attacks_found, "Campaign should include attacks from AdaptiveArsenalScenario")

    def test_counter_intelligence_scenario_execution_flow(self):
        """
        Test the execution flow of the CounterIntelligenceScenario.
        """
        # We need a real executor for this, but can patch its execute_advanced_suite
        with patch.object(self.red_team_executor, 'execute_advanced_suite', return_value=([], 0, 0, 0)) as mock_execute:
            ci_scenario = CounterIntelligenceScenario(self.red_team_executor, generations=5)

            # The scenario should have chosen a bait and exploit type
            self.assertIsNotNone(ci_scenario.bait_type)
            self.assertIsNotNone(ci_scenario.exploit_type)
            self.assertNotEqual(ci_scenario.bait_type, ci_scenario.exploit_type)

            # Run the scenario
            ci_scenario.run()

            # Check that the attack suite was called for each generation
            self.assertEqual(mock_execute.call_count, 5)

            # Check if the attack patterns were filtered for baiting
            first_call_args, _ = mock_execute.call_args_list[0]
            initial_patterns = self.red_team_executor.advanced_patterns
            self.assertLess(len(initial_patterns), 25, "Should be filtered for baiting phase")

class TestFullSystemIntegration(unittest.TestCase):

    def test_learning_cycle_runs_with_new_orchestrator(self):
        """
        Test that the full AutonomousLearningSystem runs without errors
        with the newly integrated adaptive attack orchestrator.
        """
        from src.config import config

        # Use a low number of generations for a quick integration test
        config.settings['simulation']['max_generations'] = 2

        try:
            # The system now initializes all the attacker components internally
            system = AutonomousLearningSystem("IntegrationTestSystem")
            system.run_learning_cycle()
        except Exception as e:
            self.fail(f"AutonomousLearningSystem failed to run with integrated orchestrator: {e}")

        # Check that the learning history was populated
        self.assertEqual(len(system.learning_history), 2)
        self.assertIn("fitness", system.learning_history[0])

if __name__ == '__main__':
    unittest.main()
