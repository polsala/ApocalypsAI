import unittest
from src.convert import convert

class TestTimezoneConverter(unittest.TestCase):
    def test_utc_to_new_york(self):
        # Fixed input ensures deterministic output.
        dt = "2023-01-01T12:00:00"
        result = convert(dt, "UTC", "America/New_York")
        self.assertEqual(result, "2023-01-01T07:00:00-05:00")

    def test_new_york_to_utc(self):
        dt = "2023-06-01T15:30:00"
        result = convert(dt, "America/New_York", "UTC")
        # June 1st is daylight saving time (EDT, UTC‑4)
        self.assertEqual(result, "2023-06-01T19:30:00+00:00")

    def test_invalid_datetime(self):
        with self.assertRaises(ValueError):
            convert("not-a-date", "UTC", "UTC")

    def test_invalid_timezone(self):
        with self.assertRaises(ValueError):
            convert("2023-01-01T00:00:00", "Invalid/Zone", "UTC")

if __name__ == "__main__":
    unittest.main()
