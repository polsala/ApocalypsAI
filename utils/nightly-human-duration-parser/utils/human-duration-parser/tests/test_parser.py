import unittest
from utils.human-duration-parser.src.parser import parse_duration

class TestParseDuration(unittest.TestCase):
    def test_simple_seconds(self):
        self.assertEqual(parse_duration("45s"), 45)

    def test_minutes_and_seconds(self):
        self.assertEqual(parse_duration("3m15s"), 3 * 60 + 15)

    def test_hours(self):
        self.assertEqual(parse_duration("2h"), 2 * 3600)

    def test_days_hours_minutes(self):
        self.assertEqual(parse_duration("1d4h30m"), 1 * 86400 + 4 * 3600 + 30 * 60)

    def test_whitespace_and_case_insensitivity(self):
        self.assertEqual(parse_duration(" 2H  30M "), 2 * 3600 + 30 * 60)

    def test_unordered_units(self):
        self.assertEqual(parse_duration("30m2h"), 2 * 3600 + 30 * 60)

    def test_invalid_string_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("invalid")

    def test_unsupported_unit_raises(self):
        # Mock rationale: regex prevents unsupported units, but we test defensive path.
        with self.assertRaises(ValueError):
            parse_duration("5x")

if __name__ == "__main__":
    unittest.main()
