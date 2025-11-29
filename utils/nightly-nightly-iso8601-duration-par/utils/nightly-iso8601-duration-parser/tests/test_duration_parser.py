import unittest
from nightly_iso8601_duration_parser import parse_duration

class TestISO8601DurationParser(unittest.TestCase):
    def test_simple_time(self):
        self.assertEqual(parse_duration("PT1H"), 3600)
        self.assertEqual(parse_duration("PT30M"), 1800)
        self.assertEqual(parse_duration("PT45S"), 45)
        self.assertEqual(parse_duration("PT1H30M45S"), 5445)

    def test_date_and_time(self):
        # 2 days, 3 hours, 4 minutes, 5 seconds
        self.assertEqual(parse_duration("P2DT3H4M5S"), 2*86400 + 3*3600 + 4*60 + 5)
        # 1 year (365d) + 2 months (60d) + 1 week + 1 day
        self.assertEqual(parse_duration("P1Y2M1W1D"), 365*86400 + 2*30*86400 + 7*86400 + 86400)

    def test_fractional_values(self):
        # Fractional hours -> truncated seconds
        self.assertEqual(parse_duration("PT1.5H"), int(1.5 * 3600))
        # Fractional minutes
        self.assertEqual(parse_duration("PT2.75M"), int(2.75 * 60))

    def test_invalid_strings(self):
        with self.assertRaises(ValueError):
            parse_duration("1H30M")  # missing leading 'P'
        with self.assertRaises(ValueError):
            parse_duration("P")  # no components
        with self.assertRaises(ValueError):
            parse_duration("PT-1H")  # negative not allowed

    def test_zero_duration(self):
        self.assertEqual(parse_duration("PT0S"), 0)
        self.assertEqual(parse_duration("P0D"), 0)

# Mock rationale: No external services are called; all logic is pure and deterministic.

if __name__ == "__main__":
    unittest.main()
