import unittest
from unittest.mock import patch
import datetime
import pathlib
import json

# Import the module under test
from ..src import main

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Load the known quotes list for reference
        quotes_path = pathlib.Path(__file__).parents[1] / 'src' / 'quotes.json'
        self.quotes = json.loads(quotes_path.read_text(encoding='utf-8'))

    def _expected_quote(self, target_date: datetime.date) -> str:
        # Replicate the selection logic used in the utility
        epoch = datetime.date(1970, 1, 1)
        idx = (target_date - epoch).days % len(self.quotes)
        q = self.quotes[idx]
        return f'"{q["text"]}" – {q["author"]}'

    @patch('datetime.date')
    def test_fixed_date(self, mock_date):
        """# Mock rationale: Force today to be 2023‑03‑14 so the result is deterministic.
        """
        mock_date.today.return_value = datetime.date(2023, 3, 14)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        result = main.get_quote_of_day()
        expected = self._expected_quote(datetime.date(2023, 3, 14))
        self.assertEqual(result, expected)

    @patch('datetime.date')
    def test_another_fixed_date(self, mock_date):
        """# Mock rationale: Verify a different date maps to the correct quote.
        """
        mock_date.today.return_value = datetime.date(1999, 12, 31)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        result = main.get_quote_of_day()
        expected = self._expected_quote(datetime.date(1999, 12, 31))
        self.assertEqual(result, expected)

    def test_empty_quotes_raises(self):
        """# Mock rationale: Simulate an empty quote file to ensure graceful error handling.
        """
        with patch.object(main, '_load_quotes', return_value=[]):
            with self.assertRaises(ValueError) as ctx:
                main.get_quote_of_day(datetime.date(2022, 1, 1))
            self.assertIn('Quote list is empty', str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
