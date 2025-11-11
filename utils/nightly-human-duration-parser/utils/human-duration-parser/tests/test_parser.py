import unittest
from src.parser import parse_duration

class TestParseDuration(unittest.TestCase):
    def test_simple_units(self):
        self.assertEqual(parse_duration("1w"), 7 * 24 * 60 * 60)
        self.assertEqual(parse_duration("2d"), 2 * 24 * 60 * 60)
        self.assertEqual(parse_duration("3h"), 3 * 60 * 60)
        self.assertEqual(parse_duration("45m"), 45 * 60)
        self.assertEqual(parse_duration("30s"), 30)

    def test_compound_without_spaces(self):
        self.assertEqual(parse_duration("1d2h30m"), 1 * 86400 + 2 * 3600 + 30 * 60)
        self.assertEqual(parse_duration("2h15m10s"), 2 * 3600 + 15 * 60 + 10)

    def test_compound_with_spaces(self):
        self.assertEqual(parse_duration("1d 2h 30m"), 1 * 86400 + 2 * 3600 + 30 * 60)
        self.assertEqual(parse_duration("  3h   5m  " ), 3 * 3600 + 5 * 60)

    def test_float_values(self):
        self.assertEqual(parse_duration("1.5h"), int(1.5 * 3600))
        self.assertEqual(parse_duration("0.5d"), int(0.5 * 86400))

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            parse_duration("")
        with self.assertRaises(ValueError):
            parse_duration("abc")
        with self.assertRaises(ValueError):
            parse_duration("10x")  # unknown unit
        with self.assertRaises(ValueError):
            parse_duration("5")   # missing unit

    def test_non_string_input(self):
        with self.assertRaises(ValueError):
            parse_duration(123)

if __name__ == "__main__":
    unittest.main()
