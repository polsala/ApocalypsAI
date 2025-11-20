import unittest
from src.calendar import generate_emoji_calendar

class TestEmojiCalendar(unittest.TestCase):
    def test_march_2023(self):
        expected = (
            "| Mon | Tue | Wed | Thu | Fri | Sat | Sun |\n"
            "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
            "|  |  | 🌱 1 | 🔥 2 | 🎉 3 | 🛌 4 | ☕ 5 |\n"
            "| 🌞 6 | 🚀 7 | 🌱 8 | 🔥 9 | 🎉 10 | 🛌 11 | ☕ 12 |\n"
            "| 🌞 13 | 🚀 14 | 🌱 15 | 🔥 16 | 🎉 17 | 🛌 18 | ☕ 19 |\n"
            "| 🌞 20 | 🚀 21 | 🌱 22 | 🔥 23 | 🎉 24 | 🛌 25 | ☕ 26 |\n"
            "| 🌞 27 | 🚀 28 | 🌱 29 | 🔥 30 | 🎉 31 |  |  |\n"
        )
        result = generate_emoji_calendar(2023, 3)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
