import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

# Import the function from the utility package
from utils.timezone_converter_cli.src.convert import convert

class TestTimezoneConverter(unittest.TestCase):
    def test_basic_conversion(self):
        # 2025-01-01 12:00 in New York (EST, UTC‑5) -> London (GMT, UTC+0)
        src_ts = "2025-01-01T12:00:00"
        result = convert(src_ts, "America/New_York", "Europe/London")
        # Expected: 2025-01-01T17:00:00+00:00 (because NY is UTC‑5 in winter)
        self.assertEqual(result, "2025-01-01T17:00:00+00:00")

    def test_daylight_saving_transition(self):
        # 2025-07-01 12:00 in New York (EDT, UTC‑4) -> London (BST, UTC+1)
        src_ts = "2025-07-01T12:00:00"
        result = convert(src_ts, "America/New_York", "Europe/London")
        # Expected offset difference: +5 hours (UTC‑4 -> UTC+1)
        self.assertEqual(result, "2025-07-01T17:00:00+01:00")

    def test_invalid_timestamp(self):
        with self.assertRaises(ValueError):
            convert("not-a-date", "America/New_York", "Europe/London")

    def test_invalid_source_tz(self):
        with self.assertRaises(ValueError):
            convert("2025-01-01T12:00:00", "Invalid/Zone", "Europe/London")

    def test_invalid_target_tz(self):
        with self.assertRaises(ValueError):
            convert("2025-01-01T12:00:00", "America/New_York", "Invalid/Zone")

# Mock rationale: All tests use the standard library only; no external network calls.

if __name__ == "__main__":
    unittest.main()
