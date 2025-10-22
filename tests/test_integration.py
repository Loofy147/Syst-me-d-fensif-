import unittest
import docker
from src.orchestration import AutonomousLearningSystem
from src.config import config

class TestLiveSystemIntegration(unittest.TestCase):

    def setUp(self):
        """Clean up any leftover containers before the test."""
        client = docker.from_env()
        try:
            container = client.containers.get("vulnerable-app-instance")
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            pass

    def test_live_learning_cycle_runs_and_records_attacks(self):
        """
        Test that the full live AutonomousLearningSystem runs and the attacker
        intelligence module records the outcomes of live HTTP attacks.
        """
        # Configure for a single, quick generation
        config.settings['simulation']['max_generations'] = 1

        system = AutonomousLearningSystem("LiveTestSystem")
        initial_attack_count = system.attacker_intelligence.total_attacks

        # This will start the container, proxy, and run one generation of live attacks
        system.run_learning_cycle()

        # Verify that the system ran for one generation
        self.assertEqual(len(system.learning_history), 1)

        # The most important check: verify that the intelligence module was
        # engaged and recorded the live attacks it performed.
        final_attack_count = system.attacker_intelligence.total_attacks
        self.assertGreater(final_attack_count, initial_attack_count,
                           "Attacker intelligence should have recorded live attacks.")

if __name__ == '__main__':
    unittest.main()
