import unittest
from src.intelligence import AutonomousIntelligence
from src.core.models import EvolvableSeed, DefenseType

class TestIntelligence(unittest.TestCase):

    def setUp(self):
        """Set up an intelligence module for testing."""
        self.seed = EvolvableSeed("TestSeed")
        self.intelligence = AutonomousIntelligence(self.seed)

    def test_process_attack_result_learns_new_signature(self):
        """Test that a new signature is learned when an attack is processed."""
        initial_signatures = len(self.intelligence.knowledge_base.signatures)
        self.intelligence.process_attack_result("' OR 1=1--", "sql_injection", False)
        new_signatures = len(self.intelligence.knowledge_base.signatures)
        self.assertEqual(new_signatures, initial_signatures + 1)

    def test_process_attack_result_synthesizes_defense(self):
        """Test that a new defense is synthesized when an attack is successful."""
        initial_strength = self.seed.defense_framework.defenses[DefenseType.SANITIZATION].config.strength
        self.intelligence.process_attack_result("'; DROP TABLE users--", "sql_injection", False)
        new_strength = self.seed.defense_framework.defenses[DefenseType.SANITIZATION].config.strength
        self.assertGreater(new_strength, initial_strength)

if __name__ == '__main__':
    unittest.main()
