import unittest
from utils.human-duration-parser.src.parser import parse_duration

class TestParseDuration(unittest.TestCase):
    def test_simple_minutes(self):
        self.assertEqual(parse_duration("5m"), 300)

    def test_hours_and_minutes(self):
        self.assertEqual(parse_duration("2h30m"), 2 * 3600 + 30 * 60)

    def test_spaces_and_mixed_case(self):
        self.assertEqual(parse_duration("1D 4h 5M"), 1 * 86400 + 4 * 3600 + 5 * 60)

    def test_weeks_days(self):
        self.assertEqual(parse_duration("1w2d"), 1 * 7 * 86400 + 2 * 86400)

    def test_multiple_same_units(self):
        self.assertEqual(parse_duration("30m15m"), 45 * 60)

    def test_invalid_input(self):
        # Should return 0 for unknown units, not raise
        self.assertEqual(parse_duration("10x"), 0)

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            parse_duration(123)

if __name__ == "__main__":
    unittest.main()
