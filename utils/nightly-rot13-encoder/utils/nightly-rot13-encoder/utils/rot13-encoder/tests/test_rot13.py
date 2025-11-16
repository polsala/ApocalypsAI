# Mock rationale: tests are deterministic, offline, and only depend on the pure rot13 function.
import os
import sys
import unittest

# Ensure the src directory is on the import path
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from rot13 import rot13

class TestROT13(unittest.TestCase):
    def test_basic_transformation(self):
        self.assertEqual(rot13("Hello World!"), "Uryyb Jbeyq!")

    def test_idempotence(self):
        # Applying ROT13 twice should yield the original string
        original = "ApocalypsAI Nightly"
        self.assertEqual(rot13(rot13(original)), original)

    def test_non_alpha_characters(self):
        self.assertEqual(rot13("1234!@#$"), "1234!@#$")

    def test_empty_string(self):
        self.assertEqual(rot13(""), "")

if __name__ == "__main__":
    unittest.main()
