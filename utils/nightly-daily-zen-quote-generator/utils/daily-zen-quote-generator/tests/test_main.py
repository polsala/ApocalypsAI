import unittest
from unittest.mock import patch
import sys
import pathlib

# Mock rationale: we adjust sys.path to import the local module without external dependencies.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from main import get_zen_quote


class TestZenQuote(unittest.TestCase):
    @patch('random.choice')
    def test_get_zen_quote_returns_mocked(self, mock_choice):
        mock_choice.return_value = "Mocked Zen Quote"
        quote = get_zen_quote()
        self.assertEqual(quote, "Mocked Zen Quote")
        mock_choice.assert_called_once()


if __name__ == "__main__":
    unittest.main()
