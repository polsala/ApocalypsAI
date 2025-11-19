import unittest
from src.emoji_calendar import generate_calendar, WEEKDAY_EMOJIS

class TestEmojiCalendar(unittest.TestCase):
    def test_february_2023(self):
        """February 2023 layout verification.
        Expected weeks (Monday‑Sunday) with emojis; empty strings for padding days.
        """
        expected = [
            ["", "", WEEKDAY_EMOJIS[2], WEEKDAY_EMOJIS[3], WEEKDAY_EMOJIS[4], WEEKDAY_EMOJIS[5], WEEKDAY_EMOJIS[6]],
            [WEEKDAY_EMOJIS[0], WEEKDAY_EMOJIS[1], WEEKDAY_EMOJIS[2], WEEKDAY_EMOJIS[3], WEEKDAY_EMOJIS[4], WEEKDAY_EMOJIS[5], WEEKDAY_EMOJIS[6]],
            [WEEKDAY_EMOJIS[0], WEEKDAY_EMOJIS[1], WEEKDAY_EMOJIS[2], WEEKDAY_EMOJIS[3], WEEKDAY_EMOJIS[4], WEEKDAY_EMOJIS[5], WEEKDAY_EMOJIS[6]],
            [WEEKDAY_EMOJIS[0], WEEKDAY_EMOJIS[1], WEEKDAY_EMOJIS[2], WEEKDAY_EMOJIS[3], WEEKDAY_EMOJIS[4], WEEKDAY_EMOJIS[5], WEEKDAY_EMOJIS[6]],
            [WEEKDAY_EMOJIS[0], WEEKDAY_EMOJIS[1], "", "", "", "", ""]
        ]
        result = generate_calendar(2023, 2)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
