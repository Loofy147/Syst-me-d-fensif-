import unittest
from unittest.mock import Mock
from src.attacks.intelligence import (
    AttackerIntelligence,
    AttackVector,
    PayloadCharacteristics,
    DefenseProfile
)
from src.attacks.advanced import AdaptiveAttackGenerator
from src.core.models import EvolvableSeed

class TestAttackerIntelligence(unittest.TestCase):

    def setUp(self):
        self.intel = AttackerIntelligence()
        self.sample_chars = PayloadCharacteristics(
            vector=AttackVector.INJECTION,
            size=100,
            encoding_layers=1,
            complexity=2,
            obfuscation_level=5,
            uses_quotes=True,
            uses_special_chars=True,
            is_polymorphic=False
        )

    def test_record_attack_and_create_profile(self):
        """Test that recording an attack creates a defense profile and updates history."""
        self.assertNotIn("SANITIZATION", self.intel.defense_profiles)

        self.intel.record_attack("payload", self.sample_chars, True, "SANITIZATION", "Blocked by filter")

        self.assertEqual(len(self.intel.attack_history), 1)
        self.assertIn("SANITIZATION", self.intel.defense_profiles)
        self.assertIsInstance(self.intel.defense_profiles["SANITIZATION"], DefenseProfile)
        self.assertEqual(self.intel.defense_profiles["SANITIZATION"].times_encountered, 1)

    def test_defense_profile_updates_on_outcome(self):
        """Test that defense profile strength estimates change based on outcomes."""
        self.intel.record_attack("p1", self.sample_chars, True, "SANITIZATION", "Blocked")
        initial_strength = self.intel.defense_profiles["SANITIZATION"].strength_estimate
        self.assertGreater(initial_strength, 0.5)

        self.intel.record_attack("p2", self.sample_chars, False, "SANITIZATION", "Bypassed")
        final_strength = self.intel.defense_profiles["SANITIZATION"].strength_estimate
        self.assertLess(final_strength, initial_strength)

    def test_parameter_optimization_on_success(self):
        """Test that parameters are reinforced on a successful attack."""
        initial_params = self.intel.get_optimal_parameters(AttackVector.INJECTION)

        successful_chars = PayloadCharacteristics(
            vector=AttackVector.INJECTION, size=200, encoding_layers=2,
            complexity=3, obfuscation_level=7, uses_quotes=True,
            uses_special_chars=True, is_polymorphic=False
        )

        self.intel.record_attack("p_success", successful_chars, False, "INPUT_VALIDATION", "Bypassed")

        new_params = self.intel.get_optimal_parameters(AttackVector.INJECTION)

        self.assertNotEqual(initial_params, new_params)
        self.assertGreater(new_params["encoding_layers"], initial_params["encoding_layers"])
        self.assertGreater(new_params["complexity"], initial_params["complexity"])

    def test_parameter_optimization_on_failure(self):
        """Test that parameters are adjusted on a failed attack."""
        initial_params = self.intel.get_optimal_parameters(AttackVector.INJECTION)

        self.intel.record_attack("p_fail", self.sample_chars, True, "SANITIZATION", "Blocked due to size")

        new_params = self.intel.get_optimal_parameters(AttackVector.INJECTION)

        self.assertLess(new_params["size"], initial_params["size"])

    def test_identify_weakest_defense(self):
        """Test the identification of the weakest defense profile."""
        self.intel.record_attack("p1", self.sample_chars, True, "STRONG_DEFENSE", "Blocked")
        self.intel.record_attack("p2", self.sample_chars, False, "WEAK_DEFENSE", "Bypassed")

        weakest = self.intel.identify_weakest_defense()
        self.assertEqual(weakest, "WEAK_DEFENSE")

class TestAdaptiveAttackGeneratorIntegration(unittest.TestCase):

    def setUp(self):
        self.intel = AttackerIntelligence()
        self.generator = AdaptiveAttackGenerator(self.intel)

    def test_generator_uses_optimized_parameters(self):
        """
        Test that the generator creates a larger payload after the intelligence
        module optimizes for size.
        """
        # First, generate a baseline attack
        _, initial_chars = self.generator.generate_overflow_attack(optimized=True)

        # Now, simulate a scenario where larger attacks are successful
        large_payload_chars = PayloadCharacteristics(
            vector=AttackVector.OVERFLOW, size=5000, encoding_layers=0,
            complexity=1, obfuscation_level=0, uses_quotes=False,
            uses_special_chars=False, is_polymorphic=False
        )
        self.intel.record_attack("large_payload", large_payload_chars, False, "BOUNDS_ENFORCEMENT", "Bypassed")

        # Generate a new attack, which should now be larger
        _, new_chars = self.generator.generate_overflow_attack(optimized=True)

        self.assertGreater(new_chars.size, initial_chars.size)

if __name__ == '__main__':
    unittest.main()
