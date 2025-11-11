import datetime
import unittest
from unittest.mock import patch

# Import the module under test
from daily_zen_quote_generator import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_known_date_returns_expected_quote(selfn        # Mock date: 2023-01-01 -> seed 20230101
        mock_date = datetime.date(2023, 1, 1)
        expected_index = int(mock_date.strftime("%Y%m%d")) % 10  # we know there are 10 quotes
        # Load the same quotes list used by the module for verification
        from daily_zen_quote_generator import _QUOTES
        expected_quote = _QUOTES[expected_index]
        self.assertEqual(get_quote(mock_date), expected_quote)

    def test_today_uses_datetime_date_today(selfn        # Mock datetime.date.today() to a fixed date
        fixed_today = datetime.date(2025, 12, 31)
        with patch('datetime.date') as mock_date_class:
            mock_date_class.today.return_value = fixed_today
            mock_date_class.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            # Compute expected quote using the same logic as the module
            expected_index = int(fixed_today.strftime("%Y%m%d")) % 10
            from daily_zen_quote_generator import _QUOTES
            expected_quote = _QUOTES[expected_index]
            self.assertEqual(get_quote(), expected_quote)

if __name__ == "__main__":
    unittest.main()
