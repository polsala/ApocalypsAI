import unittest
from unittest.mock import patch
import sys
import pathlib

# Ensure the src directory is on the import path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from compliment import get_compliment

class TestComplimentGenerator(unittest.TestCase):
    def test_fixed_choice(self):
        # Mock random.choice to return a known compliment
        with patch('random.choice', return_value="you are a dazzling comet of curiosity!"):
            result = get_compliment("Alice")
            self.assertEqual(result, "Alice, you are a dazzling comet of curiosity!")

    def test_default_name(self):
        # Ensure default name works with mocked choice
        with patch('random.choice', return_value="your smile could power a small city!"):
            result = get_compliment()
            self.assertEqual(result, "Friend, your smile could power a small city!")

    def test_randomness_with_seed(self):
        # Using a fixed seed should produce deterministic output
        random_seed = 42
        import random
        random.seed(random_seed)
        result = get_compliment("Bob")
        # With seed 42, random.choice picks the third element in the list
        # # Mock rationale: deterministic due to seed
        expected = "Bob, you have the wisdom of a thousand owls!"
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
