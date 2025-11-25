import unittest
from src.converter import convert

class TestChronoChameleon(unittest.TestCase):
    def test_basic_conversion(self):
        # Mock rationale: using a fixed datetime string ensures deterministic test.
        dt = "2023-10-31T15:00:00"
        src = "America/New_York"
        tgt = "Europe/London"
        # On 2023‑10‑31 New York is UTC‑4 (EDT), London is UTC+0 (GMT)
        expected = "2023-10-31T20:00:00+00:00"
        self.assertEqual(convert(dt, src, tgt), expected)

    def test_invalid_datetime(self):
        with self.assertRaises(ValueError):
            convert("not-a-datetime", "UTC", "UTC")

    def test_invalid_timezone(self):
        with self.assertRaises(ValueError):
            convert("2023-01-01T00:00:00", "Invalid/Zone", "UTC")
        with self.assertRaises(ValueError):
            convert("2023-01-01T00:00:00", "UTC", "Invalid/Zone")

if __name__ == "__main__":
    unittest.main()
