import unittest
import datetime
from unittest.mock import patch

# Mock rationale: we patch datetime.date.today to control the current date without network.
from src.main import get_quote_of_the_day, format_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_known_date(self):
        test_date = datetime.date(2023, 1, 1)  # Day 1 of the year
        quote = get_quote_of_the_day(test_date)
        # Day 1 % 5 == 1, expecting second quote (index 1)
        expected = {
            "text": "The only way to do great work is to love what you do.",
            "author": "Steve Jobs",
        }
        self.assertEqual(quote, expected)

    @patch('src.main.datetime.date')
    def test_today_mocked(self, mock_date):
        # Mock today to be 2023-12-31 (day 365)
        mock_date.today.return_value = datetime.date(2023, 12, 31)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        quote = get_quote_of_the_day()
        # 365 % 5 == 0, expecting first quote (index 0)
        expected = {
            "text": "Be yourself; everyone else is already taken.",
            "author": "Oscar Wilde",
        }
        self.assertEqual(quote, expected)

    def test_format_output(self):
        quote = {"text": "Test quote", "author": "Tester"}
        formatted = format_quote(quote)
        self.assertEqual(formatted, '"Test quote" — Tester')

if __name__ == "__main__":
    unittest.main()
