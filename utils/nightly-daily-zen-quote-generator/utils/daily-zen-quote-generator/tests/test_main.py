import unittest
from unittest.mock import patch
import datetime
import sys
import pathlib

# Ensure the src directory is on the import path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

# Mock rationale: we patch datetime.date.today to return a fixed date,
# ensuring deterministic output without network or external state.

from main import get_quote_of_the_day, _QUOTES


class TestQuoteOfTheDay(unittest.TestCase):
    def test_fixed_date(self):
        fixed_date = datetime.date(2023, 1, 1)  # known ordinal
        expected_index = fixed_date.toordinal() % len(_QUOTES)
        expected_quote = _QUOTES[expected_index]

        with patch('datetime.date') as mock_date:
            mock_date.today.return_value = fixed_date
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            quote = get_quote_of_the_day()
            self.assertEqual(quote, expected_quote)

    def test_explicit_date(self):
        date = datetime.date(2022, 12, 31)
        expected = _QUOTES[date.toordinal() % len(_QUOTES)]
        self.assertEqual(get_quote_of_the_day(date), expected)


if __name__ == "__main__":
    unittest.main()
