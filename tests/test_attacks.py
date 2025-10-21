import unittest
from src.attacks.advanced import AdvancedAttackLibrary

class TestAttacks(unittest.TestCase):

    def test_polymorphic_sql_injection(self):
        """Test that polymorphic_sql_injection generates different payloads."""
        payload1 = AdvancedAttackLibrary.polymorphic_sql_injection(0)
        payload2 = AdvancedAttackLibrary.polymorphic_sql_injection(1)
        self.assertNotEqual(payload1, payload2)

    def test_base64_encoded_injection(self):
        """Test that base64_encoded_injection generates a valid base64 string."""
        import base64
        payload = AdvancedAttackLibrary.base64_encoded_injection()
        try:
            base64.b64decode(payload)
        except Exception:
            self.fail("base64_encoded_injection did not generate a valid base64 string.")

if __name__ == '__main__':
    unittest.main()
