import unittest
import os
import sys

# Adjust path so we can import the module under src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from convert import convert

class TestTimezoneConverter(unittest.TestCase):
    def test_basic_conversion(self):
        # 2025-01-01 12:00 UTC -> America/New_York (EST, UTC‑5)
        result = convert("2025-01-01 12:00", "UTC", "America/New_York")
        self.assertTrue(result.startswith("2025-01-01T07:00:00-05:00"))

    def test_invalid_datetime(self):
        with self.assertRaises(ValueError):
            convert("not-a-date", "UTC", "UTC")

    def test_invalid_timezone(self):
        with self.assertRaises(ValueError):
            convert("2025-01-01 12:00", "Invalid/Zone", "UTC")

if __name__ == "__main__":
    unittest.main()
