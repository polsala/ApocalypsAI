import unittest
from datetime import datetime

# Mock rationale: we import the function directly; no external I/O.
from utils.nightly-emoji-mood-tracker.src.mood import get_mood

class TestEmojiMoodTracker(unittest.TestCase):
    def test_morning_fixed_date(self):
        # 2023‑04‑01 08:30 -> morning segment
        dt = datetime(2023, 4, 1, 8, 30)
        emoji = get_mood(dt)
        # Seed = 20230401, deterministic choice from morning pool
        self.assertIn(emoji, ["☀️", "🌅", "🥐", "😊"])
        # Verify exact expected emoji for this seed
        self.assertEqual(emoji, "🌅")

    def test_afternoon_fixed_date(self):
        dt = datetime(2023, 12, 25, 15, 0)  # afternoon segment
        emoji = get_mood(dt)
        self.assertIn(emoji, ["😎", "🌞", "🍹", "😁"])
        self.assertEqual(emoji, "🍹")

    def test_evening_fixed_date(self):
        dt = datetime(2024, 1, 2, 19, 45)  # evening segment
        emoji = get_mood(dt)
        self.assertIn(emoji, ["🌇", "🌙", "🍷", "🙂"])
        self.assertEqual(emoji, "🌙")

    def test_night_fixed_date(self):
        dt = datetime(2025, 7, 15, 23, 10)  # night segment
        emoji = get_mood(dt)
        self.assertIn(emoji, ["🌌", "🌃", "🛌", "😴"])
        self.assertEqual(emoji, "🌃")

if __name__ == "__main__":
    unittest.main()
