import unittest
from unittest.mock import patch
import datetime
import sys
import os

# Add the src directory to sys.path so we can import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from quote import get_quote


class TestDailyZenQuote(unittest.TestCase):
    def test_deterministic_selection(self):
        """Same date should always return the same quote."""
        test_date = datetime.date(2023, 1, 1)
        quote1 = get_quote(test_date)
        quote2 = get_quote(test_date)
        self.assertEqual(quote1, quote2)

    @patch("quote.datetime.date")
    def test_today_used_when_no_date(self, mock_date):
        """When no date is supplied, the function should use datetime.date.today()."""
        # Mock today to a known date
        mock_date.today.return_value = datetime.date(2022, 12, 25)
        # Ensure other datetime.date constructors still work
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        quote = get_quote()
        expected = get_quote(datetime.date(2022, 12, 25))
        self.assertEqual(quote, expected)


if __name__ == "__main__":
    unittest.main()
