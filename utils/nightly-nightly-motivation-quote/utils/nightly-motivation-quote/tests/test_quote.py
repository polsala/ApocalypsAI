import unittest
import datetime
from src.quote import get_quote_of_the_day

class TestQuoteOfTheDay(unittest.TestCase):
    def test_known_date(self):
        # 2023-01-01 should map to the second quote in the list
        date = datetime.date(2023, 1, 1)
        expected = "Life is 10% what happens to us and 90% how we react to it. – Charles R. Swindoll"
        self.assertEqual(get_quote_of_the_day(date), expected)

    def test_today_consistency(self):
        # Mock today's date to a fixed value to ensure deterministic output
        fixed_date = datetime.date(2022, 12, 25)
        # Mock rationale: we replace datetime.date.today via monkeypatch
        original_today = datetime.date.today
        datetime.date.today = lambda: fixed_date  # Mock rationale: replace today for test
        try:
            expected = get_quote_of_the_day(fixed_date)
            self.assertEqual(get_quote_of_the_day(), expected)
        finally:
            datetime.date.today = original_today  # Restore original method

if __name__ == "__main__":
    unittest.main()
