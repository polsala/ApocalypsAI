import datetime
import unittest
from unittest import mock

# Mock rationale: we patch datetime.date.today to return a fixed date for deterministic test.

from utils.nightly_zen_quote_of_the_day.src.quote import get_quote

class TestZenQuote(unittest.TestCase):
    def test_fixed_date(self):
        fixed_date = datetime.date(2023, 1, 1)
        with mock.patch.object(datetime.date, "today", return_value=fixed_date):
            quote = get_quote()
        expected = "When the mind is still, the universe surrenders."
        self.assertEqual(quote, expected)

    def test_direct_date_argument(self):
        # Directly passing a date should bypass the today() call.
        date = datetime.date(2024, 2, 29)  # Leap day
        quote = get_quote(date)
        # Compute expected using the same algorithm.
        index = date.toordinal() % 5
        expected = [
            "The journey of a thousand miles begins with one step.",
            "When the mind is still, the universe surrenders.",
            "Simplicity is the ultimate sophistication.",
            "Let go of the illusion of control.",
            "Silence is the language of the soul.",
        ][index]
        self.assertEqual(quote, expected)

if __name__ == "__main__":
    unittest.main()
