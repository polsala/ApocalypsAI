import unittest
from unittest.mock import patch
import datetime

from utils.daily_zen_quote_generator.src.main import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_deterministic_quote_for_fixed_date(self):
        # Mock rationale:
        # We patch datetime.date.today to return a known date so the function
        # produces a predictable output without external dependencies.
        fixed_date = datetime.date(2023, 1, 1)  # 2023-01-01
        expected_quote = "Do not seek to follow in the footsteps of the wise; seek what they sought."

        with patch('datetime.date') as mock_date:
            mock_date.today.return_value = fixed_date
            # Allow constructing new date objects via the patched class.
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            quote = get_quote()
            self.assertEqual(quote, expected_quote)

    def test_custom_date_parameter(self):
        # Directly pass a date without mocking.
        date = datetime.date(2022, 12, 31)
        # Compute expected index manually.
        days = (date - datetime.date(1970, 1, 1)).days
        quotes = [
            "The journey of a thousand miles begins with one step.",
            "Simplicity is the ultimate sophistication.",
            "What you think, you become.",
            "The only constant is change.",
            "Be yourself; everyone else is already taken.",
            "In the middle of difficulty lies opportunity.",
            "Do not seek to follow in the footsteps of the wise; seek what they sought.",
            "When the mind is still, the universe surrenders.",
        ]
        expected = quotes[days % len(quotes)]
        self.assertEqual(get_quote(date), expected)

if __name__ == "__main__":
    unittest.main()
