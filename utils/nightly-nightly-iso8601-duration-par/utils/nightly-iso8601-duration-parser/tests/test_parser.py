import unittest
from src.parser import parse_iso8601_duration

class TestISO8601DurationParser(unittest.TestCase):
    def test_basic_components(self):
        cases = {
            "PT0S": 0,
            "PT45S": 45,
            "PT2M": 120,
            "PT2M30S": 150,
            "PT1H": 3600,
            "PT1H15M": 4500,
            "PT1H15M30S": 4530,
            "P1DT2H": 90000,  # 1 day + 2 hours
            "P3DT4H5M6S": 277506,
        }
        for iso, expected in cases.items():
            with self.subTest(iso=iso):
                self.assertEqual(parse_iso8601_duration(iso), expected)

    def test_invalid_formats(self):
        invalid = ["", "P", "PT", "1H30M", "P-1DT", "PT1M60S"]
        for iso in invalid:
            with self.subTest(iso=iso):
                # Mock rationale: ensure deterministic failure without external calls.
                with self.assertRaises(ValueError):
                    parse_iso8601_duration(iso)

if __name__ == "__main__":
    unittest.main()
