import unittest

# Mock rationale: Importing from the relative path ensures the test runs offline
# without needing the package to be installed globally.
from src.rot13 import rot13

class TestRot13(unittest.TestCase):
    def test_basic_transformation(self):
        self.assertEqual(rot13("Hello, World!"), "Uryyb, Jbeyq!")

    def test_symmetry(self):
        original = "ApocalypsAI Nightly Integrator"
        encoded = rot13(original)
        decoded = rot13(encoded)
        self.assertEqual(decoded, original)

    def test_empty_string(self):
        self.assertEqual(rot13(""), "")

    def test_non_alpha_characters(self):
        self.assertEqual(rot13("1234!@#$"), "1234!@#$")

if __name__ == "__main__":
    unittest.main()
