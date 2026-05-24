import unittest
import os
import sys

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import select_quote, QUOTES

class TestQuoteSelection(unittest.TestCase):
    def test_seed_zero_returns_first(self):
        self.assertEqual(select_quote(0), QUOTES[0])

    def test_seed_wraps_around(self):
        self.assertEqual(select_quote(len(QUOTES)), QUOTES[0])

    def test_arbitrary_seed(self):
        seed = 7
        expected = QUOTES[seed % len(QUOTES)]
        self.assertEqual(select_quote(seed), expected)

if __name__ == "__main__":
    unittest.main()
