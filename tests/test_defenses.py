import unittest
from src.defenses.advanced import AdvancedSanitizationDefense
from src.core.models import DefenseConfig, DefenseType

class TestDefenses(unittest.TestCase):

    def setUp(self):
        """Set up a defense mechanism for testing."""
        config = DefenseConfig(DefenseType.SANITIZATION, active=True, strength=10)
        self.defense = AdvancedSanitizationDefense(config)

    def test_dangerous_pattern_raw(self):
        """Test that dangerous raw patterns are blocked."""
        blocked, _ = self.defense.evaluate("' OR 1=1--")
        self.assertTrue(blocked)

    def test_dangerous_pattern_base64(self):
        """Test that dangerous base64-encoded patterns are blocked."""
        import base64
        payload = base64.b64encode(b"' OR 1=1--").decode('utf-8')
        blocked, _ = self.defense.evaluate(payload)
        self.assertTrue(blocked)

    def test_safe_payload(self):
        """Test that a safe payload is not blocked."""
        blocked, _ = self.defense.evaluate("this is a safe string")
        self.assertFalse(blocked)

if __name__ == '__main__':
    unittest.main()
