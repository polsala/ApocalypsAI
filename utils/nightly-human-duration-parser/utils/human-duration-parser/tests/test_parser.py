import unittest
from utils.human-duration-parser.src.parser import parse_duration

class TestParseDuration(unittest.TestCase):
    def test_simple_cases(self):
        self.assertEqual(parse_duration("1d"), 86400)
        self.assertEqual(parse_duration("2h"), 7200)
        self.assertEqual(parse_duration("30m"), 1800)
        self.assertEqual(parse_duration("45s"), 45)

    def test_combined_cases(self):
        self.assertEqual(parse_duration("1d2h30m"), 86400 + 7200 + 1800)
        self.assertEqual(parse_duration("2h45m10s"), 7200 + 2700 + 10)
        self.assertEqual(parse_duration("5m 3d"), 5 * 60 + 3 * 86400)
        self.assertEqual(parse_duration("  4h   5s  "), 4 * 3600 + 5)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            parse_duration("")
        with self.assertRaises(ValueError):
            parse_duration("abc")
        with self.assertRaises(ValueError):
            parse_duration("10x")  # unsupported unit
        with self.assertRaises(ValueError):
            parse_duration("1.5h")  # floats not allowed

    def test_non_string_input(self):
        with self.assertRaises(ValueError):
            parse_duration(123)  # type: ignore

if __name__ == "__main__":
    unittest.main()
