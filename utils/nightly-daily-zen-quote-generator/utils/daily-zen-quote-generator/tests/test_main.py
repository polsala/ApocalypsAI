import builtins
import io
import json
import unittest
from unittest import mock

# Mock rationale: we replace file I/O and randomness to make the test deterministic and offline.

from utils.daily_zen_quote_generator.src import main as quote_mod

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Sample quotes data used for all tests
        self.sample_quotes = [
            {"text": "Test quote one", "author": "Author A", "category": "mindfulness"},
            {"text": "Test quote two", "author": "Author B", "category": "humor"},
        ]
        self.quotes_json = json.dumps(self.sample_quotes)

    @mock.patch('utils.daily_zen_quote_generator.src.main.open', new_callable=mock.mock_open, read_data='')
    @mock.patch('utils.daily_zen_quote_generator.src.main.random.choice')
    def test_default_random_quote(self, mock_choice, mock_open):
        # Mock file read to return our sample JSON
        mock_open.return_value.__enter__.return_value.read.return_value = self.quotes_json
        # Force random.choice to return the first quote
        mock_choice.return_value = self.sample_quotes[0]

        with mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            quote_mod.main([])
            output = fake_out.getvalue().strip()
        expected = '\"Test quote one\" — Author A'
        self.assertEqual(output, expected)

    @mock.patch('utils.daily_zen_quote_generator.src.main.open', new_callable=mock.mock_open, read_data='')
    @mock.patch('utils.daily_zen_quote_generator.src.main.random.choice')
    def test_category_filter(self, mock_choice, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = self.quotes_json
        # After filtering to "humor", only the second quote remains; random.choice returns it.
        mock_choice.return_value = self.sample_quotes[1]

        with mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            quote_mod.main(['--category', 'humor'])
            output = fake_out.getvalue().strip()
        expected = '\"Test quote two\" — Author B'
        self.assertEqual(output, expected)

    @mock.patch('utils.daily_zen_quote_generator.src.main.open', new_callable=mock.mock_open, read_data='')
    def test_invalid_category_exits(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = self.quotes_json
        with self.assertRaises(SystemExit) as cm:
            quote_mod.main(['--category', 'nonexistent'])
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
