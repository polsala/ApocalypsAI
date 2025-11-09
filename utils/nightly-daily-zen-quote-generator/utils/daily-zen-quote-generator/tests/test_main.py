import unittest
from unittest import mock
import datetime

# Mock rationale: we replace the system date to guarantee deterministic output.
from src import main as quote_mod

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Load quotes once for reference
        self.quotes = quote_mod._load_quotes()
        self.assertTrue(self.quotes, "Quote list should not be empty")

    def test_deterministic_selection_with_fixed_date(self):
        fixed_date = datetime.date(2023, 1, 1)
        # Direct call with explicit date
        explicit = quote_mod.get_quote_of_the_day(fixed_date)
        # Call without date after mocking datetime.date.today()
        with mock.patch('src.main.datetime.date') as mock_date:
            mock_date.today.return_value = fixed_date
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            mocked = quote_mod.get_quote_of_the_day()
        self.assertEqual(explicit, mocked, "Quote should be identical when date is mocked")

    def test_quote_is_from_list(self):
        # Use today's real date (no mocking) – just ensure the result is in the list
        today_quote = quote_mod.get_quote_of_the_day()
        self.assertIn(today_quote, self.quotes)

    def test_format_output(self):
        sample = {"quote": "Test quote", "author": "Tester"}
        formatted = quote_mod._format_quote(sample)
        self.assertEqual(formatted, '"Test quote" — Tester')

if __name__ == '__main__':
    unittest.main()
