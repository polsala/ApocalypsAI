import unittest
from unittest.mock import patch
import datetime
import sys
import os

# Ensure the src package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.quote_of_the_day import get_quote

class TestQuoteOfTheDay(unittest.TestCase):
    @patch('src.quote_of_the_day.datetime.date')
    def test_known_date(self, mock_date):
        # Mock rationale: force a known date to make the test deterministic.
        mock_date.today.return_value = datetime.date(2023, 1, 1)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        expected = "The early bird gets the worm, but the second mouse gets the cheese."
        self.assertEqual(get_quote(), expected)

    @patch('src.quote_of_the_day.datetime.date')
    def test_another_date(self, mock_date):
        # Mock rationale: test a different date mapping.
        mock_date.today.return_value = datetime.date(2023, 12, 31)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        day_number = int(datetime.date(2023, 12, 31).strftime("%Y%m%d"))
        quotes = get_quote.__globals__['_QUOTES']
        expected = quotes[day_number % len(quotes)]
        self.assertEqual(get_quote(), expected)

if __name__ == "__main__":
    unittest.main()
