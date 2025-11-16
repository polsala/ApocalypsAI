import unittest
from utils.nightly-iso8601-duration-parser.src.duration_parser import parse_iso8601_duration

class TestIso8601DurationParser(unittest.TestCase):
    def test_full_duration(self):
        iso = "P1Y2M3W4DT5H6M7S"
        expected = {
            "years": 1,
            "months": 2,
            "weeks": 3,
            "days": 4,
            "hours": 5,
            "minutes": 6,
            "seconds": 7,
        }
        self.assertEqual(parse_iso8601_duration(iso), expected)

    def test_date_only(self):
        iso = "P10D"
        expected = {
            "years": 0,
            "months": 0,
            "weeks": 0,
            "days": 10,
            "hours": 0,
            "minutes": 0,
            "seconds": 0,
        }
        self.assertEqual(parse_iso8601_duration(iso), expected)

    def test_time_only(self):
        iso = "PT15M30S"
        expected = {
            "years": 0,
            "months": 0,
            "weeks": 0,
            "days": 0,
            "hours": 0,
            "minutes": 15,
            "seconds": 30,
        }
        self.assertEqual(parse_iso8601_duration(iso), expected)

    def test_mixed_without_weeks(self):
        iso = "P2Y3M5DT12H"
        expected = {
            "years": 2,
            "months": 3,
            "weeks": 0,
            "days": 5,
            "hours": 12,
            "minutes": 0,
            "seconds": 0,
        }
        self.assertEqual(parse_iso8601_duration(iso), expected)

    def test_invalid_format_raises(self):
        with self.assertRaises(ValueError):
            parse_iso8601_duration("INVALID")

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            parse_iso8601_duration("")

# Mock rationale: No external network calls are performed; all tests are deterministic and run offline.

if __name__ == "__main__":
    unittest.main()
