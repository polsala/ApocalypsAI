import unittest
from weekday_lookup import get_weekday

class TestWeekdayLookup(unittest.TestCase):
    def test_known_dates(self):
        # Known weekdays for reference dates
        cases = [
            ((2025, 11, 9), "Sunday"),   # today (as of writing)
            ((2000, 1, 1), "Saturday"),
            ((1999, 12, 31), "Friday"),
            ((2020, 2, 29), "Saturday"),  # leap day
            ((1583, 10, 15), "Friday"),   # first Gregorian date in many regions
        ]
        for (y, m, d), expected in cases:
            with self.subTest(date=(y, m, d)):
                self.assertEqual(get_weekday(y, m, d), expected)

    def test_invalid_month(self):
        with self.assertRaises(ValueError):
            get_weekday(2025, 0, 10)  # month out of range
        with self.assertRaises(ValueError):
            get_weekday(2025, 13, 10)  # month out of range

    def test_invalid_day(self):
        with self.assertRaises(ValueError):
            get_weekday(2025, 5, 0)
        with self.assertRaises(ValueError):
            get_weekday(2025, 5, 32)

    def test_pre_gregorian(self):
        # Mock rationale: ensure we guard against dates before Gregorian reform.
        with self.assertRaises(ValueError):
            get_weekday(1500, 1, 1)

if __name__ == "__main__":
    unittest.main()
