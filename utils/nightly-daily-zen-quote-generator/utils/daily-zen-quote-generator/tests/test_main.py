import unittest
import datetime
from daily_zen_quote_generator.main import get_zen_quote, _date_to_index

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_deterministic_output(self):
        # Fixed dates should always map to the same quote.
        date1 = datetime.date(2025, 11, 8)
        date2 = datetime.date(2025, 11, 9)
        quote1 = get_zen_quote(date1)
        quote2 = get_zen_quote(date2)
        # Re‑invoke to ensure determinism.
        self.assertEqual(quote1, get_zen_quote(date1))
        self.assertEqual(quote2, get_zen_quote(date2))
        # Ensure different dates can produce different quotes (most likely).
        self.assertNotEqual(quote1, quote2)

    def test_index_range(self):
        # Verify that the internal index is always within bounds.
        for year in (2020, 2023, 2025):
            for month in (1, 6, 12):
                for day in (1, 15, 28):
                    d = datetime.date(year, month, day)
                    idx = _date_to_index(d)
                    self.assertGreaterEqual(idx, 0)
                    self.assertLess(idx, 10)  # len(_QUOTES) == 10

    def test_invalid_date_parsing(self):
        # Mock rationale: we test the CLI parsing indirectly via exception handling.
        # Since the CLI parsing lives in ``_parse_cli_arg`` which raises ValueError on bad format,
        # we ensure that the main() function returns a non‑zero exit code for bad input.
        from daily_zen_quote_generator.main import main
        exit_code = main(["not-a-date"])
        self.assertNotEqual(exit_code, 0)

if __name__ == "__main__":
    unittest.main()
