import datetime
import unittest
from src.emoji_mood import get_mood, WEEKDAY_EMOJI_MAP

class TestEmojiMood(unittest.TestCase):
    def test_known_dates(self):
        # Monday, 2024-01-01 -> ☕
        self.assertEqual(get_mood(datetime.date(2024, 1, 1)), WEEKDAY_EMOJI_MAP[0])
        # Tuesday, 2024-01-02 -> 🚀
        self.assertEqual(get_mood(datetime.date(2024, 1, 2)), WEEKDAY_EMOJI_MAP[1])
        # Wednesday, 2024-01-03 -> 🌱
        self.assertEqual(get_mood(datetime.date(2024, 1, 3)), WEEKDAY_EMOJI_MAP[2])
        # Thursday, 2024-01-04 -> 🎯
        self.assertEqual(get_mood(datetime.date(2024, 1, 4)), WEEKDAY_EMOJI_MAP[3])
        # Friday, 2024-01-05 -> 🍻
        self.assertEqual(get_mood(datetime.date(2024, 1, 5)), WEEKDAY_EMOJI_MAP[4])
        # Saturday, 2024-01-06 -> 🏖️
        self.assertEqual(get_mood(datetime.date(2024, 1, 6)), WEEKDAY_EMOJI_MAP[5])
        # Sunday, 2024-01-07 -> 🎄
        self.assertEqual(get_mood(datetime.date(2024, 1, 7)), WEEKDAY_EMOJI_MAP[6])

    def test_invalid_input(self):
        # The utility does not raise for non‑date objects; we ensure type safety.
        with self.assertRaises(AttributeError):
            # Mock rationale: we deliberately pass a wrong type to trigger an AttributeError.
            get_mood("not-a-date")

if __name__ == "__main__":
    unittest.main()
