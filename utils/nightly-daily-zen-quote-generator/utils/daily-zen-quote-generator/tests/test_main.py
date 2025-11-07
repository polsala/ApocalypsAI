import unittest
import datetime
import sys
import os
from unittest.mock import patch

# Ensure the src directory is on the import path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from main import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_known_date(self):
        """January 1 should map to the first quote."""
        test_date = datetime.date(2023, 1, 1)
        self.assertEqual(
            get_quote(test_date),
            "The journey of a thousand miles begins with one step."
        )

    def test_wrap_around(self):
        """Day 8 wraps around to the first quote (7 quotes total)."""
        test_date = datetime.date(2023, 1, 8)
        self.assertEqual(
            get_quote(test_date),
            "The journey of a thousand miles begins with one step."
        )

    @patch('datetime.date')
    def test_today_mock(self, mock_date):
        """# Mock rationale: Freeze today to March 15, 2023 (day 74) to verify deterministic selection.
        Expected index: (74‑1) % 7 = 4 → fifth quote.
        """
        mock_date.today.return_value = datetime.date(2023, 3, 15)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        expected = "Let go or be dragged."
        self.assertEqual(get_quote(), expected)

if __name__ == "__main__":
    unittest.main()
