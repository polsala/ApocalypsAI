import unittest
from unittest.mock import patch
import datetime

# Mock rationale: we patch datetime.date.today to return a fixed date,
# ensuring deterministic behavior without external time dependencies.
from src.zen_quote import get_today_quote, _deterministic_index


class TestZenQuote(unittest.TestCase):
    def test_deterministic_index_consistency(self):
        """Same date should always map to the same index."""
        date = datetime.date(2023, 1, 1)
        idx1 = _deterministic_index(date)
        idx2 = _deterministic_index(date)
        self.assertEqual(idx1, idx2)

    def test_known_date_returns_expected_quote(self):
        """For a known date, verify the exact quote."""
        test_date = datetime.date(2023, 1, 1)
        expected_quote = "The journey of a thousand miles begins with one step."
        self.assertEqual(get_today_quote(test_date), expected_quote)

    @patch('src.zen_quote.datetime.date')
    def test_today_quote_uses_today(self, mock_date):
        """When no date is supplied, function should use datetime.date.today()."""
        mock_date.today.return_value = datetime.date(2022, 12, 31)
        # Compute expected using the same logic
        expected = get_today_quote(datetime.date(2022, 12, 31))
        self.assertEqual(get_today_quote(), expected)


if __name__ == '__main__':
    unittest.main()
