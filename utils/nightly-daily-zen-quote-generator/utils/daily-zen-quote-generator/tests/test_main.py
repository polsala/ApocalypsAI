import datetime
import unittest
from unittest.mock import patch

# Import the utility under test.
from daily_zen_quote_generator import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_deterministic_selection(self):
        """Ensure the same date always yields the same quote."""
        test_date = datetime.date(2023, 3, 14)  # Pi Day – arbitrary choice
        expected = get_quote(test_date)  # Compute once
        # Re‑compute to verify determinism
        self.assertEqual(get_quote(test_date), expected)

    def test_today_mocked(self):
        """Mock ``datetime.date.today`` to a known value and verify output."""
        mock_today = datetime.date(2022, 12, 25)  # Christmas
        with patch.object(datetime.date, "today", return_value=mock_today):
            # # Mock rationale: we replace the system date to make the test
            # # deterministic without any network calls.
            quote = get_quote()
            # Compute expected using the same algorithm for clarity.
            expected_index = mock_today.toordinal() % len(
                [
                    "The journey of a thousand miles begins with one step.",
                    "What you think, you become.",
                    "Simplicity is the ultimate sophistication.",
                    "Be yourself; everyone else is already taken.",
                ]
            )
            expected_quote = [
                "The journey of a thousand miles begins with one step.",
                "What you think, you become.",
                "Simplicity is the ultimate sophistication.",
                "Be yourself; everyone else is already taken.",
            ][expected_index]
            self.assertEqual(quote, expected_quote)

if __name__ == "__main__":
    unittest.main()
