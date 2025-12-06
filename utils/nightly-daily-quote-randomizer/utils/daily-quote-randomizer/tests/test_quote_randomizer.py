import unittest
import sys
import pathlib
import json
from unittest.mock import patch, mock_open

# Adjust path to import the module from src
UTIL_ROOT = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(UTIL_ROOT))

from quote_randomizer import get_random_quote

# Mock rationale: Provide deterministic random.choice and file content without hitting the real filesystem.

MOCK_QUOTES = [
    {
        "text": "Mock quote one.",
        "author": "Author One",
        "tags": ["test"]
    },
    {
        "text": "Mock quote two.",
        "author": "Author Two",
        "tags": ["example", "test"]
    }
]

class TestQuoteRandomizer(unittest.TestCase):
    @patch("quote_randomizer.pathlib.Path.open")
    @patch("quote_randomizer.json.load")
    @patch("quote_randomizer.random.choice")
    def test_get_random_quote_no_tag(self, mock_choice, mock_json_load, mock_open):
        # Mock rationale: Ensure load returns our mock data and choice returns first element.
        mock_json_load.return_value = MOCK_QUOTES
        mock_choice.return_value = MOCK_QUOTES[0]

        quote = get_random_quote()
        self.assertEqual(quote, MOCK_QUOTES[0])
        mock_json_load.assert_called_once()
        mock_choice.assert_called_once_with(MOCK_QUOTES)

    @patch("quote_randomizer.pathlib.Path.open")
    @patch("quote_randomizer.json.load")
    @patch("quote_randomizer.random.choice")
    def test_get_random_quote_with_tag(self, mock_choice, mock_json_load, mock_open):
        mock_json_load.return_value = MOCK_QUOTES
        # Expect filtered list to contain only second quote (has tag 'example')
        mock_choice.return_value = MOCK_QUOTES[1]

        quote = get_random_quote(tag="example")
        self.assertEqual(quote, MOCK_QUOTES[1])
        # Verify that random.choice was called with filtered list
        mock_choice.assert_called_once()
        args, _ = mock_choice.call_args
        filtered = args[0]
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["text"], "Mock quote two.")

    def test_get_random_quote_invalid_tag(self):
        with patch("quote_randomizer.pathlib.Path.open", mock_open(read_data=json.dumps(MOCK_QUOTES))):
            with patch("quote_randomizer.json.load", return_value=MOCK_QUOTES):
                with self.assertRaises(ValueError) as cm:
                    get_random_quote(tag="nonexistent")
                self.assertIn("No quotes found with tag", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
