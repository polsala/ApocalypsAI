import unittest
from unittest.mock import patch
import sys
import pathlib

# Ensure the src directory is on the import path.
SRC_PATH = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_PATH))

from quote import get_random_quote


class TestQuote(unittest.TestCase):
    def test_random_quote_without_theme(self):
        with patch('random.choice') as mock_choice:
            mock_choice.side_effect = lambda seq: seq[0]  # Mock rationale: deterministic first element.
            quote = get_random_quote()
            self.assertEqual(quote, "The journey of a thousand miles begins with one step.")

    def test_random_quote_with_theme(self):
        with patch('random.choice') as mock_choice:
            def chooser(seq):
                # For theme 'nature', filtered list has two quotes; return second.
                return seq[1]  # Mock rationale: deterministic second element.
            mock_choice.side_effect = chooser
            quote = get_random_quote(theme="nature")
            self.assertEqual(quote, "Even the tallest tree was once a seed.")

    def test_invalid_theme_raises(self):
        with self.assertRaises(ValueError):
            get_random_quote(theme="nonexistent")


if __name__ == "__main__":
    unittest.main()
