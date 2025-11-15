import unittest
from unittest import mock
import pathlib

# Mock rationale: we replace file I/O and random.choice to make the test deterministic and offline.

class TestDailyZenQuoteGenerator(unittest.TestCase):
    @mock.patch('daily_zen_quote_generator.src.main._QUOTE_FILE', new=pathlib.Path('dummy_path'))
    @mock.patch('builtins.open')
    @mock.patch('daily_zen_quote_generator.src.main.random.choice')
    def test_get_random_quote(self, mock_choice, mock_open):
        # Mock the JSON content that would be read from quotes.json
        mock_file = mock.mock_open(read_data='["Quote A", "Quote B", "Quote C"]')
        mock_open.side_effect = mock_file.side_effect

        # Force random.choice to always return the second quote for predictability
        mock_choice.side_effect = lambda seq: seq[1]

        from daily_zen_quote_generator.src.main import get_random_quote
        result = get_random_quote()
        self.assertEqual(result, "Quote B")
        # Ensure the file was opened correctly
        mock_open.assert_called_once_with('dummy_path', 'r', encoding='utf-8')
        # Ensure random.choice was called with the loaded list
        mock_choice.assert_called_once_with(["Quote A", "Quote B", "Quote C"])

    def test_empty_quotes_raises(self):
        with mock.patch('daily_zen_quote_generator.src.main._load_quotes', return_value=[]):
            from daily_zen_quote_generator.src.main import get_random_quote
            with self.assertRaises(ValueError):
                get_random_quote()

if __name__ == '__main__':
    unittest.main()
