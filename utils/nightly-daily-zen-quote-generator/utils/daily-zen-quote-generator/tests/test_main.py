import unittest
from unittest.mock import patch
import datetime
import sys
from pathlib import Path

# Ensure the src directory is on the import path.
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from main import get_quote, load_quotes  # noqa: E402

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Fixed list of quotes matching the bundled JSON.
        self.quotes = [
            "The journey of a thousand miles begins with one step.",
            "Be yourself; everyone else is already taken.",
            "Simplicity is the ultimate sophistication.",
            "What you think, you become.",
            "The only constant is change."
        ]

    @patch("main.load_quotes")
    def test_fixed_date(self, mock_load):
        """Quote for a known date should be deterministic."""
        mock_load.return_value = self.quotes
        test_date = datetime.date(2023, 1, 3)  # Day 3 → index 2
        quote = get_quote(test_date)
        self.assertEqual(quote, self.quotes[2])

    @patch("main.load_quotes")
    def test_wrap_around(self, mock_load):
        """When day_of_year exceeds the list length, it wraps around."""
        mock_load.return_value = self.quotes
        test_date = datetime.date(2023, 1, 7)  # Day 7 → (7‑1)%5 = 1
        quote = get_quote(test_date)
        self.assertEqual(quote, self.quotes[1])

    @patch("main.load_quotes")
    def test_today_mock(self, mock_load):
        """Mock ``datetime.date.today`` to verify default behaviour."""
        mock_load.return_value = self.quotes
        fake_today = datetime.date(2023, 12, 31)  # Day 365
        with patch("datetime.date") as mock_date:
            mock_date.today.return_value = fake_today
            # Preserve other ``date`` constructor behaviour.
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            quote = get_quote()
            index = (fake_today.timetuple().tm_yday - 1) % len(self.quotes)
            self.assertEqual(quote, self.quotes[index])

if __name__ == "__main__":
    unittest.main()
