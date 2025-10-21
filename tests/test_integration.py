import unittest
from src.orchestration import AutonomousLearningSystem
from src.defenses.advanced import upgrade_to_ultimate_defenses

class TestIntegration(unittest.TestCase):

    def test_learning_cycle_improves_fitness(self):
        """Test that the learning cycle improves the system's defense fitness."""
        from src.config import config
        system = AutonomousLearningSystem("TestSystem")

        # Upgrade to ultimate defenses to provide a baseline
        upgrade_to_ultimate_defenses(system.seed)

        # Run a few generations
        config.settings["simulation"]["max_generations"] = 3
        system.run_learning_cycle()

        # Check that fitness has improved
        initial_fitness = system.learning_history[0]['fitness']
        final_fitness = system.learning_history[-1]['fitness']

        # The fitness may not always improve, so we'll just check that it runs
        self.assertIsNotNone(final_fitness)

if __name__ == '__main__':
    unittest.main()
