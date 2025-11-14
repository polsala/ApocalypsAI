import unittest
from unittest.mock import patch
from datetime import datetime, timezone
import pathlib
import sys

# Adjust import path to src directory
sys.path.append(str(pathlib.Path(__file__).parents[2] / "src"))
from main import quote_of_the_day


class TestQuoteOfTheDay(unittest.TestCase):
    def setUp(self):
        # Known static list of quotes for deterministic testing
        self.quotes = [
            "The journey of a thousand miles begins with one step.",
            "When the mind is still, the universe surrenders.",
            "Simplicity is the ultimate sophistication.",
            "Let go or be dragged.",
            "The obstacle is the path."
        ]

    @patch("main.load_quotes")
    def test_deterministic_selection(self, mock_load):
        # Mock rationale: replace file I/O with a static list for deterministic test.
        mock_load.return_value = self.quotes
        # Mock date: Jan 3 (day 3) -> index 2 -> third quote
        mock_date = datetime(2023, 1, 3, tzinfo=timezone.utc)
        result = quote_of_the_day(mock_date)
        self.assertEqual(result, self.quotes[2])

    @patch("main.load_quotes")
    def test_wrap_around(self, mock_load):
        # Mock rationale: test modulo behavior when day exceeds list length.
        mock_load.return_value = self.quotes
        # Mock date: Jan 8 (day 8) -> index 7 -> 7 % 5 = 2
        mock_date = datetime(2023, 1, 8, tzinfo=timezone.utc)
        result = quote_of_the_day(mock_date)
        self.assertEqual(result, self.quotes[2])


if __name__ == "__main__":
    unittest.main()
