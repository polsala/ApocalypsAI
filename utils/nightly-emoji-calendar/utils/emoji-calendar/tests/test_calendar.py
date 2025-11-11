import unittest
import datetime
from utils.emoji-calendar.src.calendar import generate_calendar

class TestEmojiCalendar(unittest.TestCase):
    def test_basic_month(self):
        """Deterministic test for April 2023 with a single holiday.

        # Mock rationale: April 2023 is fixed; no network calls.
        """
        year = 2023
        month = 4
        holidays = [datetime.date(2023, 4, 7)]  # Good Friday (example)
        expected_output = (
            "Mo Tu We Th Fr Sa Su\n"
            " 1🟦  2🟦  3🟦  4🟦  5🟦  6🟧  7🎉\n"
            " 8🟦  9🟦 10🟦 11🟦 12🟦 13🟧 14🟧\n"
            "15🟦 16🟦 17🟦 18🟦 19🟦 20🟧 21🟧\n"
            "22🟦 23🟦 24🟦 25🟦 26🟦 27🟧 28🟧\n"
            "29🟦 30🟦                "
        )
        result = generate_calendar(year, month, holidays)
        self.assertEqual(result, expected_output)

    def test_month_start_on_sunday(self):
        """Check that leading empty slots are rendered correctly for May 2022 (starts on Sunday)."""
        year = 2022
        month = 5
        result = generate_calendar(year, month)
        # May 2022: first week has only Sunday = 1
        first_line = result.split('\n')[1]
        self.assertTrue(first_line.startswith("      1🟧"))

if __name__ == "__main__":
    unittest.main()
