import os
import sys
import unittest
from datetime import date

# Adjust path so we can import the utility's src module
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from main import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_known_date(self):
        # Mock rationale: Using a fixed date ensures deterministic output.
        test_date = date(2023, 1, 1)
        quote = get_quote(test_date)
        expected = "The journey of a thousand miles begins with one step."
        self.assertEqual(quote, expected)

    def test_another_date(self):
        test_date = date(2023, 12, 31)
        quote = get_quote(test_date)
        expected = "Simplicity is the ultimate sophistication."
        self.assertEqual(quote, expected)

if __name__ == "__main__":
    unittest.main()
