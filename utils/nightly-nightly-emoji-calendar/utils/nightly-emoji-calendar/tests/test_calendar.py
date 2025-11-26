import unittest
from datetime import datetime
from src.calendar import generate_calendar

class TestEmojiCalendar(unittest.TestCase):
    def test_output_contains_both_emojis(self):
        """Ensure the generated calendar includes both weekday and weekend emojis.

        This deterministic test runs offline and does not depend on external data.
        """
        year, month = 2022, 1  # January 2022 has both weekdays and weekends
        output = generate_calendar(year, month)
        self.assertIn("📅", output)  # at least one weekday
        self.assertIn("🌞", output)  # at least one weekend

    def test_current_month_runs_without_error(self):
        """Calling the function with the current month should not raise.

        # Mock rationale: we rely on the system date, which is deterministic within the test run.
        """
        now = datetime.now()
        try:
            generate_calendar(now.year, now.month)
        except Exception as e:
            self.fail(f"generate_calendar raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
