import os
import sys
import unittest

# Ensure the src directory is on the import path
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
sys.path.append(SRC_DIR)

from emoji_calendar import date_to_emoji, emoji_to_date

class TestEmojiCalendar(unittest.TestCase):
    def test_known_conversion(self):
        date = "2023-10-31"
        emoji = date_to_emoji(date)
        expected = "2️⃣0️⃣2️⃣3️⃣➖1️⃣0️⃣➖3️⃣1️⃣"
        self.assertEqual(emoji, expected)

    def test_roundtrip(self):
        dates = ["1999-12-31", "2000-01-01", "2025-07-04"]
        for d in dates:
            with self.subTest(date=d):
                self.assertEqual(emoji_to_date(date_to_emoji(d)), d)

    def test_invalid_input(self):
        # Invalid date format should raise ValueError
        with self.assertRaises(ValueError):
            date_to_emoji("31-12-1999")

        # Unknown emoji sequence should raise ValueError
        with self.assertRaises(ValueError):
            emoji_to_date("invalidemoji")

if __name__ == "__main__":
    unittest.main()
