import unittest
import datetime
from unittest.mock import patch

# Import the module under test
from daily_zen_quote import get_today_quote, QUOTES

class TestDailyZenQuote(unittest.TestCase):
    def test_deterministic_index(self):
        """Ensure the same date always yields the same quote."""
        sample_date = datetime.date(2023, 4, 1)
        first = get_today_quote(sample_date)
        second = get_today_quote(sample_date)
        self.assertEqual(first, second)
        # Verify that the quote actually comes from the list
        self.assertIn(first, QUOTES)

    def test_wrap_around(self):
        """When the ordinal exceeds the list length, it wraps correctly."""
        # Choose a date far in the future to force wrap‑around
        far_date = datetime.date(2100, 1, 1)
        idx = far_date.toordinal() % len(QUOTES)
        expected = QUOTES[idx]
        self.assertEqual(get_today_quote(far_date), expected)

    @patch('datetime.date')
    def test_today_default_uses_date_today(self, mock_date):
        """# Mock rationale: replace datetime.date.today() to a fixed date without network.
        The mock ensures get_today_quote() without arguments uses the patched today.
        """
        mock_date.today.return_value = datetime.date(2025, 12, 31)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        # Expected quote for the mocked date
        expected = get_today_quote(datetime.date(2025, 12, 31))
        # Call without explicit date – should hit the mock
        result = get_today_quote()
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
