import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we mock datetime.date.today to control output without network.

from utils.daily_zen_quote_generator.src.quote import get_quote, _QUOTES


class TestDailyZenQuote(unittest.TestCase):
    def test_fixed_date_selection(self):
        # Choose a known date and compute expected quote
        test_date = datetime.date(2023, 1, 1)  # ordinal = 738156
        expected_index = test_date.toordinal() % len(_QUOTES)
        expected_quote = _QUOTES[expected_index]
        self.assertEqual(get_quote(test_date), expected_quote)

    @patch('utils.daily_zen_quote_generator.src.quote.datetime.date')
    def test_today_mocked(self, mock_date):
        # Mock today to a specific date
        mock_today = datetime.date(2025, 12, 31)
        mock_date.today.return_value = mock_today
        # Ensure get_quote() uses the mocked today
        expected_index = mock_today.toordinal() % len(_QUOTES)
        expected_quote = _QUOTES[expected_index]
        self.assertEqual(get_quote(), expected_quote)


if __name__ == "__main__":
    unittest.main()
