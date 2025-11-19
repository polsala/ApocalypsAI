import unittest
from utils.nightly-emoji-calendar.src.calendar import generate_emoji_calendar

class TestEmojiCalendar(unittest.TestCase):
    def test_february_2023(self):
        # Expected output for February 2023 (non‑leap year)
        expected = (
            "   1🌈 2🍀 3🎉 4🌙\n"
            "5🌞 6🌜 7🌟 8🌈 9🍀 10🎉 11🌙\n"
            "12🌞 13🌜 14🌟 15🌈 16🍀 17🎉 18🌙\n"
            "19🌞 20🌜 21🌟 22🌈 23🍀 24🎉 25🌙\n"
            "26🌞 27🌜 28🌟"
        )
        result = generate_emoji_calendar(2023, 2)
        self.assertEqual(result, expected)

    def test_january_2021(self):
        # Mock rationale: deterministic check for a different month
        expected = (
            "   1🌈 2🍀 3🎉 4🌙\n"
            "5🌞 6🌜 7🌟 8🌈 9🍀 10🎉 11🌙\n"
            "12🌞 13🌜 14🌟 15🌈 16🍀 17🎉 18🌙\n"
            "19🌞 20🌜 21🌟 22🌈 23🍀 24🎉 25🌙\n"
            "26🌞 27🌜 28🌟 29🌈 30🍀 31🎉"
        )
        result = generate_emoji_calendar(2021, 1)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
