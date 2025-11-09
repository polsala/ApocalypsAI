import unittest
from unittest.mock import mock_open, patch
from pathlib import Path
import json

# Import the module under test
from utils.daily-zen-quote-generator.src.quote_generator import (
    load_quotes,
    get_random_quote,
    format_quote,
)

# Mock rationale: we replace file I/O and randomness to keep tests deterministic and offline.
MOCK_QUOTES = [
    {"quote": "Mocked quote one.", "author": "Author A"},
    {"quote": "Mocked quote two.", "author": "Author B"},
]

class TestQuoteGenerator(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(MOCK_QUOTES))
    @patch.object(Path, "open")
    def test_load_quotes(self, mock_path_open, mock_file):
        # Mock Path.open to use our mock file object
        mock_path_open.return_value = mock_file.return_value
        quotes = load_quotes()
        self.assertEqual(quotes, MOCK_QUOTES)

    @patch("random.choice")
    def test_get_random_quote(self, mock_choice):
        mock_choice.return_value = MOCK_QUOTES[1]
        result = get_random_quote(MOCK_QUOTES)
        self.assertEqual(result, MOCK_QUOTES[1])
        mock_choice.assert_called_once_with(MOCK_QUOTES)

    def test_format_quote(self):
        quote = {"quote": "Test quote", "author": "Tester"}
        formatted = format_quote(quote)
        self.assertEqual(formatted, "\"Test quote\" – Tester")

if __name__ == "__main__":
    unittest.main()
