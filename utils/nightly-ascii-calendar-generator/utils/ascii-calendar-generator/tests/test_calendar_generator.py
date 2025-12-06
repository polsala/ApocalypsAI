import unittest
import datetime
from unittest import mock
from src.calendar_generator import generate_calendar


class TestCalendarGenerator(unittest.TestCase):
    def test_basic_calendar_contains_month(self):
        cal = generate_calendar(month=3, year=2023)
        self.assertIn("March 2023", cal)

    def test_highlight_today(self):
        # Mock today's date to March 15, 2023
        mock_today = datetime.date(2023, 3, 15)
        with mock.patch('datetime.date') as mock_date:
            # Mock rationale: replace date.today() with a fixed date for deterministic testing
            mock_date.today.return_value = mock_today
            # Ensure other date constructors behave normally
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            cal = generate_calendar(month=3, year=2023, highlight_today=True)
            self.assertIn("*15*", cal)


if __name__ == "__main__":
    unittest.main()
