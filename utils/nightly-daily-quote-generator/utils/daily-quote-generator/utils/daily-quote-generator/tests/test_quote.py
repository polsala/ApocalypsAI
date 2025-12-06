import unittest
from unittest.mock import patch
import sys
import pathlib

# Mock rationale: Ensure deterministic output by mocking random.choice
# This keeps the test offline and repeatable.
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from quote import get_random_quote

class TestQuoteGenerator(unittest.TestCase):
    def test_specific_category(self):
        with patch('random.choice', return_value="Dream big, act bigger."):
            self.assertEqual(get_random_quote("motivation"), "Dream big, act bigger.")

    def test_unknown_category_fallback(self):
        with patch('random.choice', return_value="Life is what happens when you’re busy making other plans."):
            self.assertEqual(get_random_quote("unknown"), "Life is what happens when you’re busy making other plans.")

if __name__ == "__main__":
    unittest.main()
