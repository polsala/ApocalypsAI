import unittest
from unittest.mock import patch
import datetime
import sys
import pathlib

# Ensure the src directory is on sys.path so we can import ``main``
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

from main import get_quote

class TestDailyZenQuote(unittest.TestCase):
    @patch('main.datetime.date')
    def test_fixed_date(self, mock_date):
        """# Mock rationale: we patch datetime.date.today to return a fixed date,
        ensuring deterministic output without network or external state.
        """
        mock_date.today.return_value = datetime.date(2023, 1, 1)  # Day 1
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        expected = "The journey of a thousand miles begins with one step."
        self.assertEqual(get_quote(), expected)

    @patch('main.datetime.date')
    def test_wrap_around(self, mock_date):
        """# Mock rationale: test that day 11 wraps back to the first quote
        because we have 10 quotes total.
        """
        mock_date.today.return_value = datetime.date(2023, 1, 11)  # Day 11
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        expected = "The journey of a thousand miles begins with one step."
        self.assertEqual(get_quote(), expected)

if __name__ == '__main__':
    unittest.main()
