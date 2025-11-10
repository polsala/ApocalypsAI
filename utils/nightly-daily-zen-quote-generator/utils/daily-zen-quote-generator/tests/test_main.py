import unittest
from unittest.mock import patch
import sys
from pathlib import Path

# Adjust sys.path to import src.main
src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from main import get_random_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    @patch("random.choice")
    def test_get_random_quote_returns_mocked(self, mock_choice):
        # Mock rationale: we patch random.choice to return a deterministic quote,
        # ensuring the test runs offline and is repeatable.
        mock_choice.return_value = "Mocked Zen Quote"
        quote = get_random_quote()
        self.assertEqual(quote, "Mocked Zen Quote")
        mock_choice.assert_called_once()

if __name__ == "__main__":
    unittest.main()
