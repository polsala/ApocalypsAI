import unittest
from src.emoji_clock import get_clock_emoji

class TestEmojiClock(unittest.TestCase):
    def test_exact_hours(self):
        self.assertEqual(get_clock_emoji(0, 0), "\U0001F55B")   # 🕛 12:00
        self.assertEqual(get_clock_emoji(13, 0), "\U0001F550")  # 🕐 1:00
        self.assertEqual(get_clock_emoji(23, 0), "\U0001F559")  # 🕙 11:00

    def test_half_hours(self):
        self.assertEqual(get_clock_emoji(0, 30), "\U0001F567")   # 🕧 12:30
        self.assertEqual(get_clock_emoji(14, 30), "\U0001F55D")  # 🕝 2:30
        self.assertEqual(get_clock_emoji(22, 30), "\U0001F564")  # 🕤 10:30

    def test_rounding_down(self):
        # Minutes <15 round down to the hour
        self.assertEqual(get_clock_emoji(9, 10), "\U0001F558")   # 🕘 9:00

    def test_rounding_to_half(self):
        # 15‑44 minutes round to half hour
        self.assertEqual(get_clock_emoji(9, 20), "\U0001F564")   # 🕤 9:30

    def test_rounding_up(self):
        # Minutes >=45 round up to next hour
        self.assertEqual(get_clock_emoji(9, 50), "\U0001F559")   # 🕙 10:00
        # Edge case: 23:50 rolls over to 0:00 (🕛)
        self.assertEqual(get_clock_emoji(23, 50), "\U0001F55B")

    def test_negative_and overflow(self):
        # Negative hour wraps correctly
        self.assertEqual(get_clock_emoji(-1, 0), "\U0001F559")   # 🕙 11:00
        # Minute overflow wraps
        self.assertEqual(get_clock_emoji(10, 75), "\U0001F55E")  # 11:30 (75 min -> 1h15m -> round to half)

if __name__ == "__main__":
    unittest.main()
