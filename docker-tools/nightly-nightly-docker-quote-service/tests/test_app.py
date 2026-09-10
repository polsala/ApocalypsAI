import unittest
import sys, os
# Ensure the src package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.app import get_quote
from datetime import datetime, timezone

class TestQuoteDeterminism(unittest.TestCase):
    def test_known_dates(self):
        # Jan 1 -> day 1 -> index 1 % 5 = 1
        date1 = datetime(2023, 1, 1, tzinfo=timezone.utc)
        self.assertEqual(
            get_quote(date1),
            "Radiation roses bloom in the night."
        )
        # Dec 31 (non‑leap year) -> day 365 -> 365 % 5 = 0
        date2 = datetime(2023, 12, 31, tzinfo=timezone.utc)
        self.assertEqual(
            get_quote(date2),
            "The ashes whisper, \"Tomorrow is a myth.\""
        )
        # Leap year Feb 29 -> day 60 -> 60 % 5 = 0
        date3 = datetime(2024, 2, 29, tzinfo=timezone.utc)
        self.assertEqual(
            get_quote(date3),
            "The ashes whisper, \"Tomorrow is a myth.\""
        )

if __name__ == "__main__":
    unittest.main()
