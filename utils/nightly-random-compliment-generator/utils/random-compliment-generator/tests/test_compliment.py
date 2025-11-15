import unittest
from unittest.mock import patch
import os
import sys

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Mock rationale: we replace random.choice to return a known value,
# ensuring the test does not depend on the actual random module.

class TestCompliment(unittest.TestCase):
    def test_get_compliment_without_seed(self):
        with patch("random.choice", return_value="Mocked compliment"):
            from compliment import get_compliment
            self.assertEqual(get_compliment(), "Mocked compliment")

    def test_get_compliment_with_seed(self):
        # Even with a seed, we mock choice to control output.
        with patch("random.choice", return_value="Seeded compliment"):
            from compliment import get_compliment
            self.assertEqual(get_compliment(seed=123), "Seeded compliment")

    def test_cli_consistency(self):
        # Verify that providing the same seed yields the same result when not mocked.
        from compliment import get_compliment
        first = get_compliment(seed=42)
        second = get_compliment(seed=42)
        self.assertEqual(first, second)

if __name__ == "__main__":
    unittest.main()
