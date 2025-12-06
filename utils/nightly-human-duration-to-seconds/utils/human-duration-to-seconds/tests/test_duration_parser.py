import unittest
from utils.human-duration-to-seconds.src.duration_parser import parse_duration

class TestParseDuration(unittest.TestCase):
    def test_simple_hours_minutes(self):
        self.assertEqual(parse_duration("2h30m"), 2 * 3600 + 30 * 60)

    def test_days_and_hours(self):
        self.assertEqual(parse_duration("1d 4h"), 1 * 86400 + 4 * 3600)

    def test_seconds_only(self):
        self.assertEqual(parse_duration("45s"), 45)

    def test_minutes_and_seconds(self):
        self.assertEqual(parse_duration("3m 15s"), 3 * 60 + 15)

    def test_zero_components(self):
        self.assertEqual(parse_duration("2h 0m 0s"), 2 * 3600)

    def test_case_insensitivity(self):
        self.assertEqual(parse_duration("1D2H"), 1 * 86400 + 2 * 3600)

    def test_invalid_string(self):
        with self.assertRaises(ValueError):
            parse_duration("invalid")

    def test_mixed_order(self):
        self.assertEqual(parse_duration("5s 1d 2h"), 1 * 86400 + 2 * 3600 + 5)

# Mock rationale: No external services are called; all logic is pure and deterministic.

if __name__ == "__main__":
    unittest.main()
