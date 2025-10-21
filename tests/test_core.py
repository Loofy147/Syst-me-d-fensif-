import unittest
from src.core.models import EvolvableSeed, DefenseType, DefenseFramework, DefenseConfig

class TestCoreModels(unittest.TestCase):

    def test_evolvable_seed_initialization(self):
        """Test that the EvolvableSeed initializes correctly."""
        seed = EvolvableSeed("TestSeed")
        self.assertEqual(seed.name, "TestSeed")
        self.assertIsInstance(seed.defense_framework, DefenseFramework)

    def test_strengthen_defense(self):
        """Test strengthening a defense mechanism."""
        seed = EvolvableSeed("TestSeed")
        initial_strength = seed.defense_framework.defenses[DefenseType.SANITIZATION].config.strength
        seed.strengthen_defense(DefenseType.SANITIZATION, 2)
        new_strength = seed.defense_framework.defenses[DefenseType.SANITIZATION].config.strength
        self.assertEqual(new_strength, initial_strength + 2)

    def test_strengthen_defense_cap(self):
        """Test that defense strength is capped at 10."""
        seed = EvolvableSeed("TestSeed")
        seed.strengthen_defense(DefenseType.SANITIZATION, 10)  # Max it out
        new_strength = seed.defense_framework.defenses[DefenseType.SANITIZATION].config.strength
        self.assertLessEqual(new_strength, 10)

    def test_activate_defense(self):
        """Test activating a defense mechanism."""
        seed = EvolvableSeed("TestSeed")
        seed.defense_framework.defenses[DefenseType.SANITIZATION].config.active = False
        seed.activate_defense(DefenseType.SANITIZATION)
        self.assertTrue(seed.defense_framework.defenses[DefenseType.SANITIZATION].config.active)

    def test_get_defense_snapshot(self):
        """Test getting a snapshot of the defense framework."""
        seed = EvolvableSeed("TestSeed")
        snapshot = seed.get_defense_snapshot()
        self.assertIn("SANITIZATION", snapshot)
        self.assertEqual(snapshot["SANITIZATION"]["strength"], 5)
        self.assertTrue(snapshot["SANITIZATION"]["active"])

    def test_defense_framework_initialization(self):
        """Test that the DefenseFramework initializes with all defense types."""
        framework = DefenseFramework()
        self.assertEqual(len(framework.defenses), len(DefenseType))
        for defense_type in DefenseType:
            self.assertIn(defense_type, framework.defenses)

if __name__ == '__main__':
    unittest.main()
