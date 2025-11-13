import datetime
import unittest
from unittest.mock import patch

# Import the module under test
from src.main import get_quote, _select_quote

class TestDailyZenQuoteDisplayer(unittest.TestCase):
    def setUp(self):
        # Fixed date to make the random choice deterministic
        self.fixed_date = datetime.date(2023, 1, 1)

    @patch('datetime.date')
    def test_deterministic_quote_without_theme(self, mock_date):
        # Mock rationale: force datetime.date.today() to return a known date
        mock_date.today.return_value = self.fixed_date
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        quote1 = get_quote()
        quote2 = get_quote()
        self.assertEqual(quote1, quote2, "Quotes should be deterministic for the same day")
        self.assertIsInstance(quote1, str)

    @patch('datetime.date')
    def test_theme_filter_returns_correct_theme(self, mock_date):
        # Mock rationale: ensure today is the fixed date for reproducibility
        mock_date.today.return_value = self.fixed_date
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        quote = get_quote(theme="nature")
        # The returned quote must belong to the 'nature' theme
        self.assertIn("nature", quote.lower() or "")
        # Verify that the internal selector picks from the filtered list
        # (no direct access to internal list, but the call should not raise)
        self.assertIsInstance(quote, str)

    def test_invalid_theme_raises(selfn):
        # No mocking needed – the function does not depend on the date when the theme list is empty
        with self.assertRaises(ValueError) as ctx:
            _select_quote(self.fixed_date, theme="nonexistent")
        self.assertIn("No quotes found for theme", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
