import unittest
from utils.emoji-calendar.src.main import generate_month

class TestEmojiCalendar(unittest.TestCase):
    def test_january_2024(self):
        """Validate the calendar output for January 2024.

        Expected layout (weekends and New Year's Day emoji):
        Mo Tu We Th Fr Sa Su
        🎉  2  3  4  5 🌞 🌜
         8  9 10 11 12 🌞 🌜
        15 16 17 18 19 🌞 🌜
        22 23 24 25 26 🌞 🌜
        29 30 31               
        """
        expected = (
            "Mo Tu We Th Fr Sa Su\n"
            "🎉  2  3  4  5 🌞 🌜\n"
            " 8  9 10 11 12 🌞 🌜\n"
            "15 16 17 18 19 🌞 🌜\n"
            "22 23 24 25 26 🌞 🌜\n"
            "29 30 31               "
        )
        result = generate_month(2024, 1)
        self.assertEqual(result, expected)

    def test_holiday_mapping(self):
        """# Mock rationale: Ensure holiday emojis are applied correctly.
        No external calls are needed; we simply verify the mapping.
        """
        # Christmas (Dec 25) should appear as 🎄
        calendar_str = generate_month(2023, 12)
        self.assertIn("🎄", calendar_str)

if __name__ == "__main__":
    unittest.main()
