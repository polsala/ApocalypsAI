import unittest
from unittest.mock import patch
import datetime
import sys
import os

# Ensure the src package is importable
CURRENT_DIR = os.path.abspath(os.path.join(__file__, '..', '..', 'src'))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# Mock rationale: we patch datetime.date.today to a fixed date to make the test deterministic.
from quote import get_quote, QUOTES, _date_string, _select_index

class TestQuoteOfTheDay(unittest.TestCase):
    @patch('datetime.date')
    def test_fixed_date(self, mock_date):
        # Set today to 2023-01-01
        mock_date.today.return_value = datetime.date(2023, 1, 1)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)

        quote = get_quote()
        expected_idx = _select_index(_date_string(datetime.date(2023, 1, 1)))
        expected_quote = QUOTES[expected_idx]
        self.assertEqual(quote, expected_quote)

    def test_custom_date(self):
        custom_date = datetime.date(1999, 12, 31)
        quote = get_quote(custom_date)
        expected_idx = _select_index(_date_string(custom_date))
        expected_quote = QUOTES[expected_idx]
        self.assertEqual(quote, expected_quote)

if __name__ == '__main__':
    unittest.main()
