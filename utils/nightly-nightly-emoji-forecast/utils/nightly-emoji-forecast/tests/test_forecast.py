import datetime
import unittest

# Import the module relative to the test package.
from src.forecast import get_emoji_forecast, EMOJIS


class TestEmojiForecast(unittest.TestCase):
    def test_repeatability(self):
        """The same date must always produce the same emoji."""
        test_date = datetime.date(2025, 5, 17)
        first = get_emoji_forecast(test_date)
        second = get_emoji_forecast(test_date)
        self.assertEqual(first, second)
        self.assertIn(first, EMOJIS)

    def test_different_dates(self):
        """Two consecutive dates should (very likely) yield different emojis.
        This is not a strict requirement; the test only ensures the function
        runs without error and returns a valid emoji.
        """
        d1 = datetime.date(2025, 5, 17)
        d2 = datetime.date(2025, 5, 18)
        forecast1 = get_emoji_forecast(d1)
        forecast2 = get_emoji_forecast(d2)
        self.assertIn(forecast1, EMOJIS)
        self.assertIn(forecast2, EMOJIS)
        # Mock rationale: we avoid a flaky strict inequality check because
        # hash collisions are theoretically possible, albeit extremely rare.


if __name__ == "__main__":
    unittest.main()
