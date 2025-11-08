import datetime
import unittest
from unittest.mock import patch

# Mock rationale: ensure deterministic behavior without network or real date.

from src.quote import get_daily_quote, QUOTES

class TestDailyZenQuote(unittest.TestCase):
    def test_fixed_date(self):
        # Use a known date and compute the expected quote manually.
        fixed_date = datetime.date(2023, 1, 1)  # ordinal = 738156
        expected_index = fixed_date.toordinal() % len(QUOTES)
        expected_quote = QUOTES[expected_index]
        self.assertEqual(get_daily_quote(fixed_date), expected_quote)

    def test_default_today_mocked(self):
        # Patch datetime.date.today to return a deterministic date.
        mock_date = datetime.date(2025, 12, 31)
        with patch('src.quote.datetime.date') as mock_date_class:
            mock_date_class.today.return_value = mock_date
            mock_date_class.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            expected_index = mock_date.toordinal() % len(QUOTES)
            expected_quote = QUOTES[expected_index]
            self.assertEqual(get_daily_quote(), expected_quote)

if __name__ == "__main__":
    unittest.main()
