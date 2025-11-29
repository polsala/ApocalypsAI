import datetime
import unittest
from unittest.mock import patch

# Mock rationale: we replace ``datetime.date.today`` with a fixed date to make the test deterministic.

from src.quote_of_the_day import get_quote


class TestQuoteOfTheDay(unittest.TestCase):
    def test_known_date_returns_expected_quote(self):
        # 2023-01-01 has ordinal 738156; using the internal list and the seeding algorithm,
        # the expected quote is the one that ``random.Random(738156)`` would pick.
        fixed_date = datetime.date(2023, 1, 1)
        expected_quote = "The best way to predict the future is to invent it. – Alan Kay"
        # Patch ``datetime.date.today`` to return our fixed date.
        with patch.object(datetime.date, "today", return_value=fixed_date):
            quote = get_quote()
        self.assertEqual(quote, expected_quote)

    def test_custom_date_parameter(self):
        # Directly pass a date without patching.
        fixed_date = datetime.date(2022, 12, 25)
        expected_quote = "What we think, we become. – Buddha"
        quote = get_quote(fixed_date)
        self.assertEqual(quote, expected_quote)

    def test_consistency_across_calls(self):
        # Ensure that multiple calls on the same date yield the same result.
        today = datetime.date.today()
        first = get_quote(today)
        second = get_quote(today)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
