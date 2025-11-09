import unittest
import datetime
from src.main import get_quote

class TestZenQuote(unittest.TestCase):
    def test_known_date(self):
        """Verify that a specific date maps to the expected quote.
        The calculation is deterministic, so we can hard‑code the expected value.
        """
        test_date = datetime.date(2023, 1, 2)  # Monday, ISO week 1
        # Expected index: (2023 * 100 + 1) % 10 = 202301 % 10 = 1
        expected = "When the mind is still, the universe surrenders."
        self.assertEqual(get_quote(test_date), expected)

    def test_today_default(self):
        """# Mock rationale: patch datetime.date.today to a deterministic value for test.
        Ensure that calling get_quote() without arguments uses the mocked today.
        """
        mock_today = datetime.date(2022, 12, 31)
        with unittest.mock.patch.object(datetime.date, "today", return_value=mock_today):
            year, week, _ = mock_today.isocalendar()
            idx = (year * 100 + week) % 10
            quotes = [
                "The journey of a thousand miles begins with one step.",
                "When the mind is still, the universe surrenders.",
                "Simplicity is the ultimate sophistication.",
                "The obstacle is the path.",
                "Let go or be dragged.",
                "Silence is a source of great strength.",
                "In the middle of difficulty lies opportunity.",
                "Be like water.",
                "All is flux, nothing stays the same.",
                "Know yourself, know the world."
            ]
            expected = quotes[idx]
            self.assertEqual(get_quote(), expected)

if __name__ == "__main__":
    unittest.main()
