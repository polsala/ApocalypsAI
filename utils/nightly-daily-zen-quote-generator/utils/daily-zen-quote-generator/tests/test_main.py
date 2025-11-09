import unittest
from unittest.mock import patch
import datetime

# Import the module under test
from daily_zen_quote_generator import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_known_date_returns_expected_quote(self):
        """# Mock rationale:
        We patch ``datetime.date.today`` to return a fixed date (2023‑01‑01).
        The expected quote is pre‑computed using the same algorithm as the
        implementation, ensuring the test is deterministic and offline.
        """
        fixed_date = datetime.date(2023, 1, 1)
        with patch.object(datetime.date, "today", return_value=fixed_date):
            quote = get_quote()
        # Compute expected index manually (mirrors _index_for_date logic)
        day_of_year = fixed_date.timetuple().tm_yday  # 1
        combined = fixed_date.year * 366 + day_of_year
        expected_idx = combined % len(
            [
                "The journey of a thousand miles begins with one step.",
                "Simplicity is the ultimate sophistication.",
                "When the mind is still, the whole universe surrenders.",
                "Let go of what you cannot change.",
                "Silence is a source of great strength.",
                "Be present; the now is all we ever have.",
                "Patience is the companion of wisdom.",
                "A calm mind brings inner power.",
                "Nature does not hurry, yet everything is accomplished.",
                "Kindness is a language the deaf can hear and the blind can see.",
            ]
        )
        expected_quote = [
            "The journey of a thousand miles begins with one step.",
            "Simplicity is the ultimate sophistication.",
            "When the mind is still, the whole universe surrenders.",
            "Let go of what you cannot change.",
            "Silence is a source of great strength.",
            "Be present; the now is all we ever have.",
            "Patience is the companion of wisdom.",
            "A calm mind brings inner power.",
            "Nature does not hurry, yet everything is accomplished.",
            "Kindness is a language the deaf can hear and the blind can see.",
        ][expected_idx]
        self.assertEqual(quote, expected_quote)

    def test_explicit_date_parameter(self):
        """# Mock rationale:
        Directly pass a date object to ``get_quote`` without any patching.
        This verifies that the function works for arbitrary dates.
        """
        date = datetime.date(2025, 12, 31)
        quote = get_quote(date)
        # Manual calculation for expected quote
        day_of_year = date.timetuple().tm_yday
        combined = date.year * 366 + day_of_year
        expected_idx = combined % 10  # there are 10 quotes
        expected_quote = [
            "The journey of a thousand miles begins with one step.",
            "Simplicity is the ultimate sophistication.",
            "When the mind is still, the whole universe surrenders.",
            "Let go of what you cannot change.",
            "Silence is a source of great strength.",
            "Be present; the now is all we ever have.",
            "Patience is the companion of wisdom.",
            "A calm mind brings inner power.",
            "Nature does not hurry, yet everything is accomplished.",
            "Kindness is a language the deaf can hear and the blind can see.",
        ][expected_idx]
        self.assertEqual(quote, expected_quote)

if __name__ == "__main__":
    unittest.main()
