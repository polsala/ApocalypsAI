import unittest
from unittest.mock import patch
import datetime

# Mock rationale: We patch ``datetime.date.today`` to make the test deterministic without external I/O.
from src.main import get_zen_quote, QUOTES

class TestDailyZenQuote(unittest.TestCase):
    def test_fixed_date(self):
        # January 15, 2023 is the 15th day of the year.
        fixed_date = datetime.date(2023, 1, 15)
        expected_index = fixed_date.timetuple().tm_yday % len(QUOTES)
        expected_quote = QUOTES[expected_index]
        self.assertEqual(get_zen_quote(fixed_date), expected_quote)

    @patch('src.main.datetime.date')
    def test_today_patched(self, mock_date_class):
        # Mock ``datetime.date.today()`` to return March 3, 2024 (day 63).
        mock_today = datetime.date(2024, 3, 3)
        mock_date_class.today.return_value = mock_today
        mock_date_class.timetuple.return_value = mock_today.timetuple()
        expected_index = mock_today.timetuple().tm_yday % len(QUOTES)
        expected_quote = QUOTES[expected_index]
        self.assertEqual(get_zen_quote(), expected_quote)

if __name__ == '__main__':
    unittest.main()
