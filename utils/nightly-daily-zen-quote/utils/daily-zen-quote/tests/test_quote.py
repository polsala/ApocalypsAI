import unittest
import datetime
import sys
from io import StringIO

# Mock rationale: we replace datetime.date.today() to a fixed date so the test is deterministic.
# This avoids any network or external state.

# Import the module under test.
from daily_zen_quote import get_quote

class TestDailyZenQuote(unittest.TestCase):
    def test_get_quote_fixed_date(self):
        # Mock rationale: use a known date where we can compute the expected index.
        fixed_date = datetime.date(2023, 1, 1)  # ordinal = 738156
        expected_index = fixed_date.toordinal() % 10  # there are 10 quotes
        # Expected quote from the list defined in the source.
        expected_quotes = [
            "The obstacle is the path.",
            "When the mind is still, the whole universe surrenders.",
            "Let go, or be dragged.",
            "Silence is a source of great strength.",
            "The journey itself is home.",
            "A single step is enough to begin.",
            "In the stillness, everything is revealed.",
            "Patience is the companion of wisdom.",
            "The moon does not fight the night; it simply shines.",
            "When you realize nothing is lacking, you have everything.",
        ]
        self.assertEqual(get_quote(fixed_date), expected_quotes[expected_index])

    def test_cli_output(self):
        # Mock rationale: capture stdout of the CLI while mocking today’s date.
        fixed_date = datetime.date(2022, 12, 31)
        # Patch datetime.date.today to return fixed_date.
        class MockDate(datetime.date):
            @classmethod
            def today(cls):
                return fixed_date
        original_date = datetime.date
        datetime.date = MockDate
        try:
            # Capture stdout.
            captured = StringIO()
            sys_stdout_original = sys.stdout
            sys.stdout = captured
            # Import the module as a script.
            import importlib
            import daily_zen_quote
            importlib.reload(daily_zen_quote)
            daily_zen_quote._main()
            output = captured.getvalue().strip()
            # Compute expected quote.
            expected = daily_zen_quote.get_quote(fixed_date)
            self.assertEqual(output, expected)
        finally:
            # Restore patches.
            datetime.date = original_date
            sys.stdout = sys_stdout_original

if __name__ == "__main__":
    unittest.main()
