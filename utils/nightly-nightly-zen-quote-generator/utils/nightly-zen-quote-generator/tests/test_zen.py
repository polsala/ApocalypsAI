import unittest
import datetime
import os
import sys

# Mock rationale: adjust path to import the module from src directory.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from zen import get_zen_quote

class TestZenQuote(unittest.TestCase):
    def test_fixed_date(self):
        # Mock rationale: using a known date to ensure deterministic output.
        test_date = datetime.date(2023, 1, 1)  # 2023-01-01
        quote = get_zen_quote(test_date)
        expected_index = test_date.toordinal() % 10
        expected_quotes = [
            "The journey of a thousand miles begins with one step.",
            "When the mind is pure, joy follows like a shadow.",
            "Simplicity is the ultimate sophistication.",
            "Let go of the past, embrace the present.",
            "Silence is a source of great strength.",
            "The obstacle is the path.",
            "Be like water: adaptable and resilient.",
            "In the middle of difficulty lies opportunity.",
            "Patience is the companion of wisdom.",
            "A single moment can change everything."
        ]
        self.assertEqual(quote, expected_quotes[expected_index])

    def test_today_consistency(self):
        # Mock rationale: ensure calling twice on same day yields same result.
        today = datetime.date.today()
        self.assertEqual(get_zen_quote(today), get_zen_quote(today))

if __name__ == "__main__":
    unittest.main()
