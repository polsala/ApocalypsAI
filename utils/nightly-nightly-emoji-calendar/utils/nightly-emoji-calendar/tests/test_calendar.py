import unittest
from utils.nightly_emoji_calendar.src.calendar import render_calendar

class TestEmojiCalendar(unittest.TestCase):
    def test_february_2023_counts(self):
        """February 2023 has 28 days, 4 Saturdays and 4 Sundays.
        Verify that the rendered string contains the expected emoji counts.
        """
        output = render_calendar(2023, 2)
        # Count emojis – we only care about the three we use
        saturday_count = output.count("🌞")
        sunday_count = output.count("🌛")
        weekday_count = output.count("📚")
        self.assertEqual(saturday_count, 4, "There should be 4 Saturdays in Feb 2023")
        self.assertEqual(sunday_count, 4, "There should be 4 Sundays in Feb 2023")
        self.assertEqual(weekday_count, 20, "20 weekdays (Mon‑Fri) should be present")
        # Total days represented by emojis should be 28
        total_emoji = saturday_count + sunday_count + weekday_count
        self.assertEqual(total_emoji, 28, "All 28 days must be rendered as emojis")

    def test_current_month_no_error(self):
        """Calling the function with the current month should never raise.
        This is a sanity check for default arguments in the CLI.
        """
        from datetime import datetime
        now = datetime.now()
        try:
            render_calendar(now.year, now.month)
        except Exception as e:
            self.fail(f"render_calendar raised an exception for the current month: {e}")

if __name__ == "__main__":
    unittest.main()
