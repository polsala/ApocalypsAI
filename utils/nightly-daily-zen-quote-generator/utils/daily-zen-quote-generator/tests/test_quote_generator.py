import unittest
from unittest import mock
import pathlib
import json

# Mock rationale: we replace file I/O and randomness to make the test deterministic and offline.

# Import the module under test
from src.quote_generator import get_random_quote, _load_quotes

class TestQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Sample data used for mocking the JSON file
        self.sample_quotes = {
            "quotes": [
                {"quote": "Test quote one", "author": "Author A"},
                {"quote": "Test quote two", "author": "Author B"}
            ]
        }
        # Path to the real quotes.json (will be patched)
        self.quote_path = pathlib.Path(__file__).parents[2] / "src" / "quotes.json"

    @mock.patch("src.quote_generator._QUOTE_FILE", new=pathlib.Path("dummy_path"))
    @mock.patch("builtins.open")
    def test_load_quotes(self, mock_open):
        # Mock rationale: simulate opening the dummy_path and returning our sample JSON.
        mock_file = mock.mock_open(read_data=json.dumps(self.sample_quotes))
        mock_open.side_effect = mock_file.side_effect
        quotes = _load_quotes()
        self.assertEqual(len(quotes), 2)
        self.assertEqual(quotes[0]["quote"], "Test quote one")
        self.assertEqual(quotes[1]["author"], "Author B")

    @mock.patch("src.quote_generator._QUOTE_FILE", new=pathlib.Path("dummy_path"))
    @mock.patch("builtins.open")
    @mock.patch("src.quote_generator.random.choice")
    def test_get_random_quote(self, mock_choice, mock_open):
        # Mock rationale: control both file loading and random.choice.
        mock_file = mock.mock_open(read_data=json.dumps(self.sample_quotes))
        mock_open.side_effect = mock_file.side_effect
        # Force random.choice to return the second entry
        mock_choice.return_value = self.sample_quotes["quotes"][1]
        result = get_random_quote()
        expected = '"Test quote two" – Author B'
        self.assertEqual(result, expected)

    @mock.patch("src.quote_generator._QUOTE_FILE", new=pathlib.Path("dummy_path"))
    @mock.patch("builtins.open")
    def test_no_quotes_error(self, mock_open):
        # Mock rationale: simulate an empty quotes list to trigger the error path.
        empty_data = {"quotes": []}
        mock_file = mock.mock_open(read_data=json.dumps(empty_data))
        mock_open.side_effect = mock_file.side_effect
        with self.assertRaises(RuntimeError) as cm:
            get_random_quote()
        self.assertIn("No quotes available", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
