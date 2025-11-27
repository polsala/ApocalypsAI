import unittest
from unittest.mock import patch
import sys
import pathlib

# Add the src directory to sys.path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

# Mock rationale: ensure deterministic output without external randomness.
from quote_generator import get_random_quote

class TestQuoteGenerator(unittest.TestCase):
    @patch('random.choice')
    def test_get_random_quote_returns_mocked(self, mock_choice):
        mock_choice.return_value = "Mocked Zen Quote"
        quote = get_random_quote()
        mock_choice.assert_called_once()
        self.assertEqual(quote, "Mocked Zen Quote")

if __name__ == "__main__":
    unittest.main()
