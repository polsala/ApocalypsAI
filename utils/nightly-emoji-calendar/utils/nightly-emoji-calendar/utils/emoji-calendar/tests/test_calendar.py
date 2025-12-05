import unittest
# Mock rationale: deterministic test using a fixed month/year; no external I/O.
from src.calendar import generate_calendar

class TestEmojiCalendar(unittest.TestCase):
    def test_known_month(self):
        # March 2023: starts on Wednesday, 31 days.
        expected = (
            "     March 2023     \n"
            "🌞 🚀 🌱 📚 🎉 🛌 ☕\n"
            "       1  2  3  4 \n"
            " 5  6  7  8  9 10 11\n"
            "12 13 14 15 16 17 18\n"
            "19 20 21 22 23 24 25\n"
            "26 27 28 29 30 31   "
        )
        result = generate_calendar(2023, 3)
        self.assertEqual(result, expected)

    def test_invalid_month_raises(self):
        # month 13 is out of range; calendar.month_name will raise IndexError.
        with self.assertRaises(IndexError):
            generate_calendar(2023, 13)

if __name__ == "__main__":
    unittest.main()
