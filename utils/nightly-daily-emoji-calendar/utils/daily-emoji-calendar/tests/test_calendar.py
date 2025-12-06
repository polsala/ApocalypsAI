import unittest
from src.calendar import generate_calendar


class TestDailyEmojiCalendar(unittest.TestCase):
    def test_march_2023_structure(self):
        """Validate that the generated calendar for March 2023 contains the expected emojis and layout.

        # Mock rationale: No external resources are needed; the function is pure and deterministic.
        """
        year, month = 2023, 3
        output = generate_calendar(year, month)
        lines = output.split("\n")
        # March 2023 spans 5 weeks
        self.assertEqual(len(lines), 5)
        # Ensure weekend emojis appear
        self.assertIn("🌞", output)  # Saturday
        self.assertIn("🌜", output)  # Sunday
        # Check that a known day appears (e.g., 31)
        self.assertIn("31", output)
        # Verify that padding is represented by two spaces
        self.assertTrue(any(line.startswith("  ") for line in lines))

    def test_february_non_leap_year(self):
        """February 2021 should have 28 days and correct emoji placement.

        # Mock rationale: Deterministic input, no network calls.
        """
        output = generate_calendar(2021, 2)
        # February 2021 has 4 weeks + 1 extra line for padding (total 4 weeks in monthcalendar)
        self.assertTrue(output.count("🌞") > 0)
        self.assertTrue(output.count("🌜") > 0)
        self.assertNotIn("29", output)  # Not a leap year

if __name__ == "__main__":
    unittest.main()
