import unittest
from src.calendar import generate_emoji_calendar

class TestEmojiCalendar(unittest.TestCase):
    def test_january_2021(self):
        # January 2021 calendar expected emojis
        expected = [
            ["", "", "", "", "🌜", "🌞", "🌞"],  # 1 Fri, 2 Sat, 3 Sun
            ["🌜", "🌜", "🌜", "🌜", "🌜", "🌞", "🌞"],  # 4‑10
            ["🌜", "🌜", "🌜", "🌜", "🌜", "🌞", "🌞"],  # 11‑17
            ["🌜", "🌜", "🌜", "🌜", "🌜", "🌞", "🌞"],  # 18‑24
            ["🌜", "🌜", "🌜", "🌜", "🌜", "🌞", "🌞"],  # 25‑31
        ]
        result = generate_emoji_calendar(2021, 1)
        self.assertEqual(result, expected)

    def test_february_2020_leap_year(self):
        # Mock rationale: Ensure leap year handling without external calls.
        result = generate_emoji_calendar(2020, 2)
        # February 2020 starts on Saturday, 29 days.
        # Verify length of weeks and that there are 29 non‑empty entries.
        non_empty = sum(day != "" for week in result for day in week)
        self.assertEqual(non_empty, 29)

if __name__ == "__main__":
    unittest.main()
