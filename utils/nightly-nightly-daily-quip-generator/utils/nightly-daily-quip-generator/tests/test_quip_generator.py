import unittest
from datetime import date

# Import the function from the utility package.
from src.quip_generator import get_daily_quip

class TestDailyQuipGenerator(unittest.TestCase):
    def test_known_date(self):
        # Mock rationale: deterministic based on date ordinal, no external randomness.
        test_date = date(2023, 1, 1)
        expected = "Debugging: where you become a detective in a world of zeros and ones."
        self.assertEqual(get_daily_quip(test_date), expected)

    def test_consistency(self):
        # Ensure repeated calls for the same date return the same quip.
        test_date = date(2025, 12, 31)
        first = get_daily_quip(test_date)
        second = get_daily_quip(test_date)
        self.assertEqual(first, second)

if __name__ == "__main__":
    unittest.main()
