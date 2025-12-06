import unittest
import datetime
import sys
import os

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from moon_phase import moon_phase

class TestMoonPhase(unittest.TestCase):
    def test_known_phases(self):
        # Known phases from astronomical tables
        cases = {
            datetime.date(2023, 1, 21): "New Moon",
            datetime.date(2023, 1, 28): "First Quarter",
            datetime.date(2023, 2, 5): "Full Moon",
            datetime.date(2023, 2, 13): "Last Quarter",
        }
        for date, expected in cases.items():
            with self.subTest(date=date):
                self.assertEqual(moon_phase(date), expected)
        # Mock rationale: we use fixed calendar dates to keep the test deterministic
        # and avoid any external network calls.

if __name__ == "__main__":
    unittest.main()
