import datetime
import unittest
import sys
import pathlib

# Ensure the src package is on the path.
sys.path.append(str(pathlib.Path(__file__).parent.parent / "src"))

from main import get_quote_of_the_day

class TestQuoteOfTheDay(unittest.TestCase):
    def test_fixed_date(self):
        # Mock rationale: using a known date to ensure deterministic output.
        test_date = datetime.date(2023, 1, 1)  # 2023-01-01
        quote, author = get_quote_of_the_day(test_date)
        # days since epoch = (2023-01-01 - 1970-01-01).days = 19358
        # 19358 % 6 = 2 -> third quote in the list
        expected = ("Simplicity is the ultimate sophistication.", "Leonardo da Vinci")
        self.assertEqual((quote, author), expected)

    def test_today_default(self):
        # Mock rationale: patch datetime.date.today to a fixed date.
        class MockDate(datetime.date):
            @classmethod
            def today(cls):
                return datetime.date(2022, 12, 31)

        original_date = datetime.date
        try:
            datetime.date = MockDate  # type: ignore
            quote, author = get_quote_of_the_day()
            # days since epoch for 2022-12-31 = 19357, 19357 % 6 = 1
            expected = ("When the mind is still, the universe surrenders.", "Unknown")
            self.assertEqual((quote, author), expected)
        finally:
            datetime.date = original_date

if __name__ == "__main__":
    unittest.main()
