import unittest
from unittest.mock import Mock
from typing import Any
from src.attacks.intelligence import AttackerIntelligence
from src.attacks.advanced import AdaptiveAttackGenerator, AdvancedRedTeamExecutor
from src.core.models import EvolvableSeed

class TestAttackerIntelligence(unittest.TestCase):

    def setUp(self):
        self.intel = AttackerIntelligence()

    def test_record_outcome(self):
        """Test that attack outcomes are recorded correctly."""
        self.intel.record_outcome("payload1", {"encoding": "base64"}, success=True)
        self.intel.record_outcome("payload1", {"encoding": "base64"}, success=True)
        self.intel.record_outcome("payload1", {"encoding": "unicode"}, success=False)

        self.assertEqual(self.intel.payload_effectiveness["payload1"]["success"], 2)
        self.assertEqual(self.intel.payload_effectiveness["payload1"]["fail"], 1)

        self.assertEqual(self.intel.characteristic_effectiveness["encoding:base64"]["success"], 2)
        self.assertEqual(self.intel.characteristic_effectiveness["encoding:unicode"]["fail"], 1)

    def test_get_most_effective_characteristic(self):
        """Test retrieval of the most effective characteristic."""
        self.intel.record_outcome("p1", {"type": "sql"}, success=True)
        self.intel.record_outcome("p2", {"type": "xss"}, success=True)
        self.intel.record_outcome("p3", {"type": "xss"}, success=False)

        # SQL is 100% effective (1/1), XSS is 50% effective (1/2)
        most_effective = self.intel.get_most_effective_characteristic()
        self.assertEqual(most_effective, "type:sql")

class TestAdaptiveAttackGenerator(unittest.TestCase):

    def setUp(self):
        # Mock intelligence module is sufficient for generator tests
        mock_intel = Mock()
        self.generator = AdaptiveAttackGenerator(mock_intel)

    def test_polymorphic_sql_injection(self):
        """Test polymorphic SQL injection generation."""
        payload = self.generator.polymorphic_sql_injection(gen=0, encoding_layers=2)
        # Should be double base64 encoded
        import base64
        decoded1 = base64.b64decode(payload.encode()).decode()
        decoded2 = base64.b64decode(decoded1.encode()).decode()
        self.assertIn("OR", decoded2)

    def test_polymorphic_buffer_overflow(self):
        """Test polymorphic buffer overflow with parameterization."""
        payload = self.generator.polymorphic_buffer_overflow(gen=1, size=50)
        self.assertEqual(len(payload), 50)
        self.assertTrue(all(c == "B" for c in payload))

    def test_nested_type_confusion(self):
        """Test nested type confusion payload structure."""

        def get_depth(p: Any) -> int:
            """Recursively calculates the nesting depth of the payload."""
            if not isinstance(p, (list, dict, set)):
                return 0

            if isinstance(p, dict):
                p = list(p.values())

            max_child_depth = 0
            for item in p:
                max_child_depth = max(max_child_depth, get_depth(item))

            return 1 + max_child_depth

        payload = self.generator.nested_type_confusion(depth=5)

        # The recursive function will accurately measure the depth
        actual_depth = get_depth(payload)
        self.assertEqual(actual_depth, 5)

    def test_class_injection(self):
        """Test that class injection returns an object with malicious methods."""
        payload_obj = self.generator.class_injection()
        self.assertEqual(str(payload_obj), "1' OR '1'='1")
        self.assertEqual(len(payload_obj), 99999)

class TestAdvancedRedTeamExecutor(unittest.TestCase):

    def setUp(self):
        # Requires a target seed and intelligence for initialization
        mock_seed = Mock(spec=EvolvableSeed)
        mock_intel = Mock(spec=AttackerIntelligence)
        self.executor = AdvancedRedTeamExecutor(mock_seed, mock_intel)

    def test_initialization(self):
        """Test that the executor initializes its attack patterns."""
        self.assertGreater(len(self.executor.advanced_patterns), 0)
        # Check if a few known patterns are present
        descriptions = [p.description for p in self.executor.advanced_patterns]
        self.assertIn("Polymorphic SQL injection", descriptions)
        self.assertIn("Metaclass injection", descriptions)
        self.assertIn("Chained overflow + state corruption", descriptions)

if __name__ == '__main__':
    unittest.main()
