import unittest
from unittest.mock import patch
import datetime
import sys
import pathlib

# Add the src directory to ``sys.path`` so we can import ``main``.
src_path = pathlib.Path(__file__).resolve().parents[1] / 'src'
sys.path.append(str(src_path))

from main import get_quote_of_the_day, load_quotes

class TestDailyZenQuoteGenerator(unittest.TestCase):
    @patch('datetime.date')
    def test_fixed_date_returns_expected_quote(self, mock_date):
        """# Mock rationale: ensure deterministic date without network.
        We force ``datetime.date.today()`` to return 2023‑01‑01 and verify the
        selected quote matches the algorithm used in production code.
        """
        # Configure the mock to behave like the real ``date`` class for construction.
        mock_date.today.return_value = datetime.date(2023, 1, 1)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)

        # Call the function under test.
        quote = get_quote_of_the_day()

        # Compute the expected quote using the same algorithm.
        quotes = load_quotes()
        expected_index = datetime.date(2023, 1, 1).toordinal() % len(quotes)
        expected_quote = quotes[expected_index]

        self.assertEqual(quote, expected_quote)

if __name__ == '__main__':
    unittest.main()
