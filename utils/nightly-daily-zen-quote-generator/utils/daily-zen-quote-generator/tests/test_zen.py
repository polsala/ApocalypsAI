import unittest
from unittest.mock import patch
from pathlib import Path
import sys

# Ensure the src module can be imported
src_path = Path(__file__).resolve().parents[2] / "src"
sys.path.append(str(src_path))

from zen import get_random_quote, load_quotes

class TestZenQuoteGenerator(unittest.TestCase):
    def test_load_quotes(self):
        quotes = load_quotes()
        self.assertIsInstance(quotes, list)
        self.assertGreaterEqual(len(quotes), 1)

    @patch("random.choice")
    def test_get_random_quote_mocked(self, mock_choice):
        # Mock rationale: ensure deterministic output without randomness
        mock_choice.return_value = "Mocked Zen Quote"
        quote = get_random_quote()
        mock_choice.assert_called_once()
        self.assertEqual(quote, "Mocked Zen Quote")

if __name__ == "__main__":
    unittest.main()
