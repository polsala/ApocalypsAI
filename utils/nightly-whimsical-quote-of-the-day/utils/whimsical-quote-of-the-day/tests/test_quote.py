import unittest
from datetime import date
from unittest.mock import patch

from src.quote import get_quote, QUOTES


class TestQuoteOfTheDay(unittest.TestCase):
    def test_explicit_date(self):
        """Pass an explicit date and verify deterministic selection."""
        test_date = date(2023, 2, 1)  # Day 32 of the year
        expected_index = (32 - 1) % len(QUOTES)
        self.assertEqual(get_quote(test_date), QUOTES[expected_index])

    @patch('src.quote.datetime')
    def test_today_mocked(self, mock_datetime):
        """# Mock rationale: Ensure the function returns the correct quote when
        datetime.date.today() is mocked to a known value, keeping the test offline
        and deterministic.
        """
        # Mock datetime.date.today() to return January 10, 2023 (day 10)
        mock_today = date(2023, 1, 10)
        mock_datetime.date.today.return_value = mock_today
        # Preserve other datetime functionalities used by the module
        mock_datetime.date.side_effect = lambda *args, **kw: date(*args, **kw)
        mock_datetime.timedelta = datetime.timedelta
        expected_index = (10 - 1) % len(QUOTES)
        self.assertEqual(get_quote(), QUOTES[expected_index])


if __name__ == "__main__":
    unittest.main()
