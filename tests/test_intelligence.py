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

    def test_process_attack_result_synthesizes_defense_dynamically(self):
        """Test that defense strength is increased dynamically based on effectiveness."""
        # This attack should trigger a principle with an initial effectiveness of 0.5
        self.intelligence.process_attack_result("'; DROP TABLE users--", "sql_injection", False)
        strength1 = self.seed.defense_framework.defenses[DefenseType.SANITIZATION].config.strength

        # After a few more similar attacks, the effectiveness should increase
        for _ in range(5):
            self.intelligence.process_attack_result("'; DROP TABLE users--", "sql_injection", False)

        strength2 = self.seed.defense_framework.defenses[DefenseType.SANITIZATION].config.strength
        self.assertGreater(strength2, strength1)

    def test_granular_analysis_recommends_specific_principles(self):
        """Test that granular analysis recommends specific principles based on characteristics."""
        result = self.intelligence.process_attack_result("' OR 1=1--", "sql_injection", False)
        recommended_principles = result['analysis']['recommended_principles']
        self.assertIn("pattern_blacklist_expansion", recommended_principles)

if __name__ == '__main__':
    unittest.main()
