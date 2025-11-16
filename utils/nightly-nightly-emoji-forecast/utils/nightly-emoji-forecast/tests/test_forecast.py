import datetime
import unittest
from utils.nightly-emoji-forecast.src.forecast import get_daily_emoji

class TestEmojiForecast(unittest.TestCase):
    def test_known_dates(self):
        # 2025-01-01 is Wednesday -> base emoji ⭐
        self.assertEqual(get_daily_emoji(datetime.date(2025, 1, 1)), "⭐")
        # 2025-02-14 is Friday -> base emoji ❄️
        self.assertEqual(get_daily_emoji(datetime.date(2025, 2, 14)), "❄️")
        # 2025-07-04 is Friday -> base emoji ❄️
        self.assertEqual(get_daily_emoji(datetime.date(2025, 7, 4)), "❄️")
        # 2025-12-25 is Thursday -> base emoji ⚡
        self.assertEqual(get_daily_emoji(datetime.date(2025, 12, 25)), "⚡")

    def test_month_modifier_does_not_change_output(self):
        # Ensure month modifiers do not affect the single‑emoji output
        date_jan = datetime.date(2025, 1, 6)   # Tuesday
        date_feb = datetime.date(2025, 2, 6)   # Tuesday
        self.assertEqual(get_daily_emoji(date_jan), get_daily_emoji(date_feb))

if __name__ == "__main__":
    unittest.main()
