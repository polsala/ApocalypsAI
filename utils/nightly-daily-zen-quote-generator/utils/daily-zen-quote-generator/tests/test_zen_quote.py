import unittest
from unittest import mock
from pathlib import Path
import sys

# Ensure the src directory is on the import path
src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_path))

from zen_quote import load_quotes, pick_quote, format_quote

class TestZenQuote(unittest.TestCase):
    def setUp(self):
        # Load the real quotes once for reuse
        self.quotes = load_quotes()

    def test_load_quotes_returns_list(self):
        self.assertIsInstance(self.quotes, list)
        self.assertGreater(len(self.quotes), 0)
        self.assertIn("text", self.quotes[0])
        self.assertIn("author", self.quotes[0])

    def test_pick_quote_randomness_mocked(self):
        # Mock random.choice to return the first quote deterministically
        with mock.patch('random.choice', return_value=self.quotes[0]) as mock_choice:  # Mock rationale: ensure deterministic test outcome
            chosen = pick_quote(self.quotes)
            mock_choice.assert_called_once_with(self.quotes)
            self.assertEqual(chosen, self.quotes[0])

    def test_pick_quote_with_max_length_filters(self):
        # Choose a max length that only allows short quotes
        short_quotes = [q for q in self.quotes if len(q["text"]) <= 30]
        self.assertTrue(short_quotes)  # sanity check
        with mock.patch('random.choice', side_effect=lambda seq: seq[0]) as mock_choice:  # Mock rationale: deterministic first element
            chosen = pick_quote(self.quotes, max_length=30)
            self.assertIn(chosen, short_quotes)
            # Ensure the filtered list was passed to random.choice
            mock_choice.assert_called_once()
            args_passed = mock_choice.call_args[0][0]
            self.assertTrue(all(len(q["text"]) <= 30 for q in args_passed))

    def test_format_quote(self):
        quote = {"text": "Test quote", "author": "Tester"}
        formatted = format_quote(quote)
        self.assertEqual(formatted, '"Test quote" — Tester')

    def test_pick_quote_no_match_raises_systemexit(self):
        # Use a max_length that is smaller than any quote
        with self.assertRaises(SystemExit) as cm:
            pick_quote(self.quotes, max_length=1)
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
