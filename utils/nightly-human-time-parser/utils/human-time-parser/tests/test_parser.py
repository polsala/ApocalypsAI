import unittest
import datetime
from src.parser import parse_human_time

class TestHumanTimeParser(unittest.TestCase):
    def setUp(self):
        # Fixed reference point for deterministic tests
        self.fixed_now = datetime.datetime(2023, 1, 1, 12, 0, 0)

    def test_now(self):
        result = parse_human_time("now", now=self.fixed_now)
        self.assertEqual(result, self.fixed_now)

    def test_in_seconds(self):
        result = parse_human_time("in 5 seconds", now=self.fixed_now)
        expected = self.fixed_now + datetime.timedelta(seconds=5)
        self.assertEqual(result, expected)

    def test_minutes_ago(self):
        result = parse_human_time("10 minutes ago", now=self.fixed_now)
        expected = self.fixed_now - datetime.timedelta(minutes=10)
        self.assertEqual(result, expected)

    def test_invalid_expression(self):
        with self.assertRaises(ValueError):
            parse_human_time("tomorrow", now=self.fixed_now)

    def test_plural_and_singular_units(self):
        # Mock rationale: ensure both singular and plural forms work identically
        result_singular = parse_human_time("in 1 day", now=self.fixed_now)
        result_plural = parse_human_time("in 1 days", now=self.fixed_now)
        expected = self.fixed_now + datetime.timedelta(days=1)
        self.assertEqual(result_singular, expected)
        self.assertEqual(result_plural, expected)

if __name__ == "__main__":
    unittest.main()
