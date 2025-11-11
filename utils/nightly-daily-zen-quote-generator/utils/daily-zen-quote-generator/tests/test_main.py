import unittest
from unittest.mock import patch
import datetime
from src.main import get_quote_of_the_day

class TestQuoteOfTheDay(unittest.TestCase):
    def test_fixed_date(self):
        # Fixed date for deterministic expectation
        test_date = datetime.date(2023, 1, 1)
        days = (test_date - datetime.date(1970, 1, 1)).days
        expected_index = days % 5  # there are 5 quotes
        expected_quote = [
            "The journey of a thousand miles begins with one step.",
            "Simplicity is the ultimate sophistication.",
            "What you think, you become.",
            "The only constant is change.",
            "Be yourself; everyone else is already taken."
        ][expected_index]

        # Mock rationale: patch datetime.date.today to return the fixed test_date
        with patch('datetime.date.today', return_value=test_date):
            quote = get_quote_of_the_day()
            self.assertEqual(quote, expected_quote)

    def test_none_date_uses_today(self):
        # Ensure the function works when no date is supplied (uses real today)
        today = datetime.date.today()
        days = (today - datetime.date(1970, 1, 1)).days
        expected_index = days % 5
        expected_quote = [
            "The journey of a thousand miles begins with one step.",
            "Simplicity is the ultimate sophistication.",
            "What you think, you become.",
            "The only constant is change.",
            "Be yourself; everyone else is already taken."
        ][expected_index]
        quote = get_quote_of_the_day()
        self.assertEqual(quote, expected_quote)

if __name__ == "__main__":
    unittest.main()
