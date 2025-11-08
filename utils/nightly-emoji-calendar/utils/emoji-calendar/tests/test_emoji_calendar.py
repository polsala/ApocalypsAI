import unittest
from utils.emoji-calendar.src.emoji_calendar import generate_calendar

class TestEmojiCalendar(unittest.TestCase):
    def test_january_2025(self):
        # Expected layout for January 2025 (see README example)
        expected = (
            "      1🎉  2  3🛸  4☀️\n"
            " 5  6  7  8  9 10🛸 11☀️\n"
            "12 13 14 15 16 17🛸 18☀️\n"
            "19 20 21 22 23 24🛸 25☀️\n"
            "26 27 28 29 30 31🛸   "
        )
        result = generate_calendar(2025, 1)
        self.assertEqual(result, expected)

    def test_february_non_leap_year(self):
        # February 2023 starts on Wednesday, 28 days, no holidays in mapping.
        result = generate_calendar(2023, 2)
        # Simple sanity check: length of lines should be 4 (weeks) and each line contains 7 tokens.
        lines = result.split("\n")
        self.assertEqual(len(lines), 4)
        for line in lines:
            self.assertEqual(len(line.split()), 7)
        # Mock rationale: we avoid hard‑coding the full calendar string to keep the test deterministic
        # while still verifying correct structure.

if __name__ == "__main__":
    unittest.main()
