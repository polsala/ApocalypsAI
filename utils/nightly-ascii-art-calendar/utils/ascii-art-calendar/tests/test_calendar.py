import unittest
from src.calendar import render_calendar

class TestAsciiArtCalendar(unittest.TestCase):
    def test_contains_emojis_and_header(self):
        # March 2023 is a good test month
        cal = render_calendar(2023, 3)
        # Header should contain month and year
        self.assertIn("March 2023", cal)
        # Saturdays (4th) should have a sun emoji, Sundays (5th) a moon emoji
        self.assertIn("4☀", cal)
        self.assertIn("5🌙", cal)
        # Ensure the calendar has the correct number of lines (header + week header + weeks)
        lines = cal.splitlines()
        self.assertGreaterEqual(len(lines), 3)

if __name__ == "__main__":
    unittest.main()
