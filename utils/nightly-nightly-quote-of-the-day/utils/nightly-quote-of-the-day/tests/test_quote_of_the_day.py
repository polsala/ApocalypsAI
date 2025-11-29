import unittest
import datetime
from src.quote_of_the_day import get_quote

class TestQuoteOfTheDay(unittest.TestCase):
    def test_specific_date(self):
        # Mock rationale: we provide a fixed date to ensure deterministic output.
        test_date = datetime.date(2023, 1, 1)  # Day 1 of the year
        expected = "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt"
        self.assertEqual(get_quote(test_date), expected)

    def test_wrap_around(self):
        # Mock rationale: test that day_of_year wraps correctly when exceeding quote list length.
        # Choose a date where day_of_year % len(_QUOTES) == 3 (len(_QUOTES) == 10, so day 13 gives index 3).
        test_date = datetime.date(2023, 1, 13)  # 13th day of year
        expected = "Turn your wounds into wisdom. – Oprah Winfrey"
        self.assertEqual(get_quote(test_date), expected)

if __name__ == "__main__":
    unittest.main()
