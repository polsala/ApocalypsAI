import builtins
import json
import unittest
from unittest import mock
from pathlib import Path

# Import the module under test
from utils.daily_zen_quote_generator.src import main as quote_mod

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def setUp(self):
        # Sample quotes data used for all tests
        self.sample_quotes = [
            {"text": "Test quote one", "author": "Alice"},
            {"text": "Test quote two", "author": "Bob"},
        ]
        # JSON representation
        self.sample_json = json.dumps(self.sample_quotes)

    @mock.patch.object(Path, "open")
    @mock.patch("random.choice")
    def test_get_random_quote_no_author(self, mock_choice, mock_open):
        # Mock file read to return our sample JSON
        mock_open.return_value.__enter__.return_value.read.return_value = self.sample_json
        # Mock random.choice to always return the first quote
        mock_choice.side_effect = lambda seq: seq[0]
        # # Mock rationale: ensure deterministic output without real randomness
        quote = quote_mod.get_random_quote()
        self.assertEqual(quote, self.sample_quotes[0])
        mock_open.assert_called_once()
        mock_choice.assert_called_once_with(self.sample_quotes)

    @mock.patch.object(Path, "open")
    @mock.patch("random.choice")
    def test_get_random_quote_with_author(self, mock_choice, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = self.sample_json
        mock_choice.side_effect = lambda seq: seq[0]
        quote = quote_mod.get_random_quote(author="Bob")
        self.assertEqual(quote, self.sample_quotes[1])
        # Ensure filtering worked (only Bob's quote passed to random.choice)
        mock_choice.assert_called_once_with([self.sample_quotes[1]])

    @mock.patch.object(Path, "open")
    def test_get_random_quote_unknown_author_raises(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = self.sample_json
        with self.assertRaises(ValueError) as ctx:
            quote_mod.get_random_quote(author="Charlie")
        self.assertIn("No quotes found for author", str(ctx.exception))

    @mock.patch.object(Path, "open")
    def test_load_quotes_file_missing(self, mock_open):
        # Simulate FileNotFoundError when opening the file
        mock_open.side_effect = FileNotFoundError
        with self.assertRaises(RuntimeError) as ctx:
            quote_mod.load_quotes()
        self.assertIn("Quotes file not found", str(ctx.exception))

    def test_format_quote(self):
        quote = {"text": "Just a test", "author": "Tester"}
        formatted = quote_mod.format_quote(quote)
        self.assertEqual(formatted, "\"Just a test\" — Tester")

if __name__ == "__main__":
    unittest.main()
