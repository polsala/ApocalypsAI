import unittest
import datetime
from src.calendar import (
    get_emoji_for_date,
    get_description_for_date,
    format_for_cli,
    _parse_date,
)

class TestEmojiCalendar(unittest.TestCase):
    def test_weekday_mapping(self):
        # Monday
        d = datetime.date(2023, 1, 2)
        self.assertEqual(get_emoji_for_date(d), "🟦")
        self.assertEqual(get_description_for_date(d), "Start of the week!")
        # Tuesday
        d = datetime.date(2023, 1, 3)
        self.assertEqual(get_emoji_for_date(d), "🟪")
        self.assertEqual(get_description_for_date(d), "Mid‑week magic!")
        # Wednesday
        d = datetime.date(2023, 1, 4)
        self.assertEqual(get_emoji_for_date(d), "🟩")
        self.assertEqual(get_description_for_date(d), "Hump day vibes!")
        # Thursday
        d = datetime.date(2023, 1, 5)
        self.assertEqual(get_emoji_for_date(d), "🟧")
        self.assertEqual(get_description_for_date(d), "Almost there!")
        # Friday
        d = datetime.date(2023, 1, 6)
        self.assertEqual(get_emoji_for_date(d), "🟥")
        self.assertEqual(get_description_for_date(d), "Weekend is near!")
        # Saturday
        d = datetime.date(2023, 1, 7)
        self.assertEqual(get_emoji_for_date(d), "🟨")
        self.assertEqual(get_description_for_date(d), "Saturday sunshine!")
        # Sunday
        d = datetime.date(2023, 1, 8)
        self.assertEqual(get_emoji_for_date(d), "⬜️")
        self.assertEqual(get_description_for_date(d), "Sunday serenity.")

    def test_cli_format(self):
        d = datetime.date(2023, 10, 31)  # Tuesday
        self.assertEqual(format_for_cli(d), "🟪 – Mid‑week magic!")

    def test_parse_date_valid(self):
        self.assertEqual(_parse_date("2023-12-25"), datetime.date(2023, 12, 25))

    def test_parse_date_invalid(self):
        with self.assertRaises(ValueError):
            _parse_date("12/25/2023")
        with self.assertRaises(ValueError):
            _parse_date("2023-13-01")

if __name__ == "__main__":
    unittest.main()
