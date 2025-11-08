import unittest
from unittest.mock import patch
from datetime import date

# Import the module using its package path
from importlib import import_module

# Load the utility module dynamically (ensures relative imports work)
main = import_module('daily_zen_quote_generator.src.main')

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Ensure the quotes list is known and stable for tests
        self.quotes = [
            "The journey of a thousand miles begins with a single step.",
            "When the mind is still, the universe surrenders its secrets.",
            "Silence is the language of the soul.",
            "A river cuts through rock not by force, but by persistence.",
            "The moon does not fight the sun; it simply reflects its own light."
        ]

    @patch('daily_zen_quote_generator.src.main._load_quotes')
    def test_known_date_returns_expected_quote(self, mock_load):
        # Mock rationale: replace file I/O with a static list to keep test offline.
        mock_load.return_value = [{"quote": q} for q in self.quotes]
        test_date = date(2023, 4, 1)  # ISO date for reproducibility
        # Compute expected index manually
        expected_index = test_date.toordinal() % len(self.quotes)
        expected_quote = self.quotes[expected_index]
        result = main.get_quote(test_date)
        self.assertEqual(result, expected_quote)

    @patch('daily_zen_quote_generator.src.main._load_quotes')
    def test_today_uses_date_today(self, mock_load):
        # Mock rationale: freeze today's date to a known value.
        mock_load.return_value = [{"quote": q} for q in self.quotes]
        fake_today = date(2025, 1, 1)
        with patch('daily_zen_quote_generator.src.main.date') as mock_date:
            mock_date.today.return_value = fake_today
            mock_date.fromisoformat.side_effect = date.fromisoformat
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            expected_index = fake_today.toordinal() % len(self.quotes)
            expected_quote = self.quotes[expected_index]
            self.assertEqual(main.get_quote(), expected_quote)

    @patch('daily_zen_quote_generator.src.main._load_quotes')
    def test_empty_quotes_returns_placeholder(self, mock_load):
        # Mock rationale: simulate an empty quotes file.
        mock_load.return_value = []
        self.assertEqual(main.get_quote(date(2023, 1, 1)), "No quotes available.")

if __name__ == '__main__':
    unittest.main()
