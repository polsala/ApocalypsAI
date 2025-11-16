import unittest
from src.calendar import generate_calendar, day_with_emoji

class TestEmojiCalendar(unittest.TestCase):
    def test_day_with_emoji(self):
        # March 1, 2023 is Wednesday -> 🌱
        self.assertEqual(day_with_emoji(2023, 3, 1), " 1🌱")
        # March 5, 2023 is Sunday -> ☕
        self.assertEqual(day_with_emoji(2023, 3, 5), " 5☕")
        # March 6, 2023 is Monday -> 🌞
        self.assertEqual(day_with_emoji(2023, 3, 6), " 6🌞")

    def test_generate_calendar_contains_expected_days(self):
        output = generate_calendar(2023, 3)
        # Verify a few known mappings appear in the output
        self.assertIn(" 1🌱", output)  # Wednesday
        self.assertIn(" 5☕", output)  # Sunday
        self.assertIn(" 6🌞", output)  # Monday
        self.assertIn(" 7🚀", output)  # Tuesday
        self.assertIn(" 8🌱", output)  # Wednesday

if __name__ == "__main__":
    unittest.main()
