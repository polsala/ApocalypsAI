import unittest
from unittest.mock import patch
import datetime
from src.quote import get_daily_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_fixed_date(self):
        """# Mock rationale: Use a known date to verify deterministic selection."""
        test_date = datetime.date(2023, 1, 1)  # Day 1
        quote = get_daily_quote(test_date)
        self.assertEqual(
            quote,
            "The journey of a thousand miles begins with one step."
        )

    def test_wrap_around(self):
        """# Mock rationale: Ensure day numbers larger than the quote list wrap correctly."""
        test_date = datetime.date(2023, 1, 5)  # Day 5, with 4 quotes -> wraps to index 0
        quote = get_daily_quote(test_date)
        self.assertEqual(
            quote,
            "The journey of a thousand miles begins with one step."
        )

    @patch('src.quote.datetime.date')
    def test_today_mock(self, mock_date):
        """# Mock rationale: Patch datetime.date.today() to a fixed value for CLI‑style call."""
        # Mock today() to return Jan 2, 2023 (day 2)
        mock_date.today.return_value = datetime.date(2023, 1, 2)
        # Ensure other datetime.date constructors still work
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        quote = get_daily_quote()
        self.assertEqual(
            quote,
            "When the mind is still, the universe surrenders."
        )

if __name__ == "__main__":
    unittest.main()
