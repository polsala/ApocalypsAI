import unittest
import sys
import pathlib
import random

# Adjust path to import the src module
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from compliment import get_compliment

class TestCompliment(unittest.TestCase):
    def test_general_category(self):
        # Mock rationale: deterministic choice by patching random.choice to return the first element.
        original_choice = random.choice
        random.choice = lambda seq: seq[0]
        try:
            result = get_compliment("general")
            self.assertEqual(result, "You are awesome!")
        finally:
            random.choice = original_choice

    def test_unknown_category(self):
        with self.assertRaises(ValueError):
            get_compliment("unknown")

if __name__ == "__main__":
    unittest.main()
