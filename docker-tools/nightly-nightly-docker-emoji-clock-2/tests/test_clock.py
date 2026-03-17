import unittest
from datetime import datetime
from src.clock import get_clock_emoji

class TestClockEmoji(unittest.TestCase):
    def test_exact_hour(self):
        dt = datetime(2023, 1, 1, 3, 0)  # 03:00 UTC → 🕒
        self.assertEqual(get_clock_emoji(dt), "\U0001F552")

    def test_half_hour(self):
        dt = datetime(2023, 1, 1, 4, 30)  # 04:30 UTC → 🕟
        self.assertEqual(get_clock_emoji(dt), "\U0001F55F")

    def test_round_up(self):
        dt = datetime(2023, 1, 1, 5, 50)  # 05:50 rounds to 06:00 → 🕕
        self.assertEqual(get_clock_emoji(dt), "\U0001F555")

    def test_round_down_to_half(self):
        dt = datetime(2023, 1, 1, 7, 20)  # 07:20 rounds to 07:30 → 🕢
        self.assertEqual(get_clock_emoji(dt), "\U0001F562")

if __name__ == "__main__":
    unittest.main()
