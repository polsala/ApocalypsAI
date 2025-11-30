import unittest
from datetime import date

# Mock rationale: The tests use fixed dates with known moon phases accordingn to the Conway algorithm.
# No external network calls are required; the algorithm is deterministic.

from src.moon_phase import get_moon_phase_emoji

class TestMoonPhaseEmoji(unittest.TestCase):
    def test_new_moon(self):
        # 2025-01-09 was a New Moon (phase 0)
        self.assertEqual(get_moon_phase_emoji(date(2025, 1, 9)), "🌑")

    def test_first_quarter(self):
        # 2025-01-17 was a First Quarter (phase 2)
        self.assertEqual(get_moon_phase_emoji(date(2025, 1, 17)), "🌓")

    def test_full_moon(self):
        # 2025-01-24 was a Full Moon (phase 4)
        self.assertEqual(get_moon_phase_emoji(date(2025, 1, 24)), "🌕")

    def test_last_quarter(self):
        # 2025-02-01 was a Last Quarter (phase 6)
        self.assertEqual(get_moon_phase_emoji(date(2025, 2, 1)), "🌗")

    def test_today_consistency(self):
        # Ensure that calling the function twice for the same date yields the same emoji.
        today = date.today()
        first = get_moon_phase_emoji(today)
        second = get_moon_phase_emoji(today)
        self.assertEqual(first, second)

if __name__ == "__main__":
    unittest.main()
