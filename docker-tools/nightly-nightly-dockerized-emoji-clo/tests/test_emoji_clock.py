import unittest
import os
import sys

# Ensure the src package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import emoji_clock


class TestEmojiClock(unittest.TestCase):
    def test_hour_to_emoji(self):
        self.assertEqual(emoji_clock.hour_to_emoji(0), "\uD83D\uDD1B")  # 🕛
        self.assertEqual(emoji_clock.hour_to_emoji(13), "\uD83D\uDD50")  # 13 % 12 == 1 → 🕐
        self.assertEqual(emoji_clock.hour_to_emoji(23), "\uD83D\uDD5A")  # 23 % 12 == 11 → 🕚

    def test_get_time_with_env(self):
        os.environ["TIME"] = "09:45"
        dt = emoji_clock.get_time()
        self.assertEqual(dt.hour, 9)
        self.assertEqual(dt.minute, 45)
        del os.environ["TIME"]

    def test_invalid_time_format(self):
        os.environ["TIME"] = "invalid"
        with self.assertRaises(SystemExit) as cm:
            emoji_clock.get_time()
        self.assertEqual(cm.exception.code, 1)
        del os.environ["TIME"]


if __name__ == "__main__":
    unittest.main()
