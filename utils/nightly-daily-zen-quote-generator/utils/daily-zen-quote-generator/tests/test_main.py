import unittest
import datetime
from utils.daily-zen-quote-generator.src.main import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_known_dates(self):
        # Pre‑computed expected quotes for specific dates based on the algorithm.
        cases = [
            (datetime.date(2023, 1, 1), "The journey of a thousand miles begins with a single step."),
            (datetime.date(2023, 1, 2), "When the mind is still, the universe surrenders."),
            (datetime.date(2023, 12, 31), "A candle loses nothing by lighting another candle."),
            (datetime.date(1999, 12, 31), "The obstacle is the path."),
        ]
        for date_obj, expected in cases:
            with self.subTest(date=date_obj):
                self.assertEqual(get_quote(date_obj), expected)

    def test_consistency(self):
        # The same date should always return the same quote, even across multiple calls.
        date = datetime.date(2025, 5, 17)
        first = get_quote(date)
        for _ in range(5):
            self.assertEqual(get_quote(date), first)

    # Mock rationale: No external resources are used, so no network mocking is required.

if __name__ == "__main__":
    unittest.main()
