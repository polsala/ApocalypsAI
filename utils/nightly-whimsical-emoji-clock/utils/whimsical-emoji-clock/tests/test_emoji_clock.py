import unittest
from emoji_clock import get_emoji_for_time

class TestEmojiClock(unittest.TestCase):
    def test_night_range(self):
        self.assertEqual(get_emoji_for_time("00:00"), "🌙")
        self.assertEqual(get_emoji_for_time("05:59"), "🌙")

    def test_sunrise_range(self):
        self.assertEqual(get_emoji_for_time("06:00"), "🌅")
        self.assertEqual(get_emoji_for_time("11:59"), "🌅")

    def test_day_range(self):
        self.assertEqual(get_emoji_for_time("12:00"), "☀️")
        self.assertEqual(get_emoji_for_time("17:59"), "☀️")

    def test_sunset_range(self):
        self.assertEqual(get_emoji_for_time("18:00"), "🌇")
        self.assertEqual(get_emoji_for_time("23:59"), "🌇")

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            get_emoji_for_time("24:00")  # hour out of range
        with self.assertRaises(ValueError):
            get_emoji_for_time("invalid")

# Mock rationale: No external services are called; all logic is pure and deterministic.

if __name__ == "__main__":
    unittest.main()
