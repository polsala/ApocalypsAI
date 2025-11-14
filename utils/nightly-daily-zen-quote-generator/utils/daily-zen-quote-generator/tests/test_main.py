import unittest
from unittest.mock import patch
import datetime
import sys, pathlib

# Add the src directory to sys.path so we can import the module.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2] / "src"))
from main import get_quote_of_day


class TestQuoteOfDay(unittest.TestCase):
    def test_fixed_date(self):
        # Mock rationale: ensure deterministic selection without relying on real date.
        test_date = datetime.date(2023, 1, 1)  # ordinal 738156
        expected = "Less is more."
        self.assertEqual(get_quote_of_day(test_date), expected)

    @patch('main.datetime.date')
    def test_today_mocked(self, mock_date):
        # Mock rationale: simulate today being 2024-02-29 (leap year) to test modulo logic.
        mock_date.today.return_value = datetime.date(2024, 2, 29)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        expected = "The journey of a thousand miles begins with one step."
        self.assertEqual(get_quote_of_day(), expected)


if __name__ == "__main__":
    unittest.main()
