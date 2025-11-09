import sys
import pathlib
import datetime
import unittest

# Ensure the src directory is on the import path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from src.quote import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_fixed_date(self):
        # 2023-01-01 should map to "Stay hungry."
        test_date = datetime.date(2023, 1, 1)
        expected = "Stay hungry."
        self.assertEqual(get_quote(test_date), expected)

    def test_consistency(self):
        # Same date should always return the same quote
        test_date = datetime.date(2025, 12, 31)
        first = get_quote(test_date)
        second = get_quote(test_date)
        self.assertEqual(first, second)

if __name__ == "__main__":
    unittest.main()
