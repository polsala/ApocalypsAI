import unittest
import sys
import os

# Add the src directory to sys.path so we can import parser directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from parser import parse_duration

class TestISO8601DurationParser(unittest.TestCase):
    def test_simple_hour(self):
        self.assertEqual(parse_duration("PT1H"), 3600)

    def test_complex(self):
        # P2W3DT4H5M6S => 2 weeks, 3 days, 4 hours, 5 minutes, 6 seconds
        expected = (
            2 * 7 * 24 * 3600 +
            3 * 24 * 3600 +
            4 * 3600 +
            5 * 60 +
            6
        )
        self.assertEqual(parse_duration("P2W3DT4H5M6S"), expected)

    def test_minutes_only(self):
        self.assertEqual(parse_duration("PT15M"), 15 * 60)

    def test_zero_seconds(self):
        self.assertEqual(parse_duration("PT0S"), 0)

    def test_invalid_string(self):
        with self.assertRaises(ValueError):
            parse_duration("invalid")

if __name__ == "__main__":
    unittest.main()
