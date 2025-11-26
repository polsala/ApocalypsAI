import unittest
from nightly_emoji_clock.src.clock import time_to_emoji

class TestEmojiClock(unittest.TestCase):
    def test_full_hour(self):
        self.assertEqual(time_to_emoji("00:00"), "\U0001F55B")  # 🕛
        self.assertEqual(time_to_emoji("12:00"), "\U0001F55B")  # 🕛
        self.assertEqual(time_to_emoji("03:00"), "\U0001F552")  # 🕒
        self.assertEqual(time_to_emoji("15:00"), "\U0001F552")  # 🕒 (3 PM)

    def test_half_hour(self):
        self.assertEqual(time_to_emoji("01:30"), "\U0001F55D")  # 🕝
        self.assertEqual(time_to_emoji("13:30"), "\U0001F55D")  # 🕝 (1:30 PM)
        self.assertEqual(time_to_emoji("23:30"), "\U0001F567")  # 🕧

    def test_rounding_down(self):
        # Minutes < 15 round down to full hour
        self.assertEqual(time_to_emoji("04:10"), "\U0001F553")  # 🕓

    def test_rounding_up(self):
        # Minutes 15‑44 round to half hour
        self.assertEqual(time_to_emoji("04:20"), "\U0001F560")  # 🕠 (5:30?) actually 4:20 -> 4:30 -> hour+1 => 5 half hour 🕠
        # Minutes >=45 round up to next hour
        self.assertEqual(time_to_emoji("04:50"), "\U0001F553")  # 🕓 (5:00) full hour emoji for 5

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            time_to_emoji("25:00")
        with self.assertRaises(ValueError):
            time_to_emoji("12:60")
        with self.assertRaises(ValueError):
            time_to_emoji("invalid")

# Mock rationale: No external services are called; all logic is pure and deterministic.

if __name__ == "__main__":
    unittest.main()
