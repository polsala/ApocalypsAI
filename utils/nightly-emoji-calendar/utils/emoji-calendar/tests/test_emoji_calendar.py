import unittest
import os
import sys

# Add the src directory to sys.path so we can import the module.
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from emoji_calendar import render_month, get_weekday_emoji

class TestEmojiCalendar(unittest.TestCase):
    def test_weekday_emoji_mapping(self):
        # Monday -> 🌞, Tuesday -> 🌜, Wednesday -> 🌛
        self.assertEqual(get_weekday_emoji(0), "🌞")
        self.assertEqual(get_weekday_emoji(1), "🌜")
        self.assertEqual(get_weekday_emoji(2), "🌛")

    def test_render_fixed_month(self):
        # October 2023: the 1st is a Sunday, which maps to 🌞
        output = render_month(2023, 10)
        lines = output.splitlines()
        # Header line
        self.assertEqual(lines[0], "October 2023")
        # Weekday header line
        self.assertEqual(lines[1], "Mo Tu We Th Fr Sa Su")
        # Ensure the first day appears with the correct emoji
        self.assertIn("🌞 1", output)
        # October 2023 spans 6 weeks in the calendar representation
        self.assertEqual(len(lines), 2 + 6)

if __name__ == "__main__":
    unittest.main()
