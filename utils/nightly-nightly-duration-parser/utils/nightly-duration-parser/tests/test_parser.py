import unittest

# Mock rationale: No external services are called; all logic is pure and deterministic.

from utils.nightly-duration-parser.src.parser import parse_duration, format_duration

class TestDurationParser(unittest.TestCase):
    def test_parse_simple(self):
        self.assertEqual(parse_duration("45s"), 45)
        self.assertEqual(parse_duration("2m"), 120)
        self.assertEqual(parse_duration("1h"), 3600)
        self.assertEqual(parse_duration("1d"), 86400)

    def test_parse_combined(self):
        self.assertEqual(parse_duration("1h30m"), 5400)
        self.assertEqual(parse_duration("2d 5h 10m 5s"), 2*86400 + 5*3600 + 10*60 + 5)
        self.assertEqual(parse_duration("3h   15s"), 3*3600 + 15)
        self.assertEqual(parse_duration("0d0h0m0s"), 0)

    def test_parse_invalid(self):
        with self.assertRaises(ValueError):
            parse_duration("10x")  # unknown unit
        with self.assertRaises(ValueError):
            parse_duration("5")   # missing unit
        with self.assertRaises(ValueError):
            parse_duration(123)   # not a string
        with self.assertRaises(ValueError):
            parse_duration("")

    def test_format_simple(self):
        self.assertEqual(format_duration(45), "45s")
        self.assertEqual(format_duration(120), "2m")
        self.assertEqual(format_duration(3600), "1h")
        self.assertEqual(format_duration(86400), "1d")

    def test_format_combined(self):
        self.assertEqual(format_duration(5400), "1h 30m")
        self.assertEqual(format_duration(2*86400 + 5*3600 + 10*60 + 5), "2d 5h 10m 5s")
        self.assertEqual(format_duration(0), "0s")

    def test_roundtrip(self):
        cases = [
            "45s",
            "2m",
            "1h30m",
            "3d 4h 5m 6s",
            "0s",
            "7h 0m 0s",
        ]
        for case in cases:
            secs = parse_duration(case)
            formatted = format_duration(secs)
            # Parsing the formatted string should give the same seconds
            self.assertEqual(parse_duration(formatted), secs)

    def test_format_invalid(self):
        with self.assertRaises(ValueError):
            format_duration(-5)
        with self.assertRaises(ValueError):
            format_duration(3.14)

if __name__ == "__main__":
    unittest.main()
