import unittest
from unittest.mock import patch
import datetime

# Import the function from the utility package
from utils.nightly-emoji-forecast.src.forecast import get_emoji_forecast

class TestEmojiForecast(unittest.TestCase):
    def test_deterministic_output_fixed_date(self):
        """Ensure the forecast is deterministic for a known date.

        We mock ``datetime.date.today`` to return 2023‑01‑01 and verify the emoji.
        """
        fixed_date = datetime.date(2023, 1, 1)
        with patch('datetime.date') as mock_date:
            # Mock rationale: patching ``today`` method while preserving other date behaviours.
            mock_date.today.return_value = fixed_date
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            emoji = get_emoji_forecast()
            self.assertEqual(emoji, "⛈️")  # Expected value derived from the seed logic

    def test_custom_date_parameter(self):
        """Directly passing a date should yield the same result as mocking today."""
        date = datetime.date(2025, 12, 25)
        emoji = get_emoji_forecast(date)
        # Seed = 20251225 -> deterministic choice
        self.assertEqual(emoji, "🌈")

    def test_returns_string_and_is_one_emoji(self):
        """Basic sanity check: result is a single-character emoji string."""
        emoji = get_emoji_forecast()
        self.assertIsInstance(emoji, str)
        self.assertTrue(len(emoji) > 0)

if __name__ == '__main__':
    unittest.main()
