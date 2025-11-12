import unittest
import sys
import pathlib
from unittest.mock import patch

# Add the src directory to sys.path so we can import the module under test
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

import main


class TestZenQuoteGenerator(unittest.TestCase):
    @patch('main.random.choice')
    def test_get_random_quote(self, mock_choice):
        # Mock rationale: deterministic output without randomness
        mock_choice.return_value = "Mocked Zen Quote"
        self.assertEqual(main.get_random_quote(), "Mocked Zen Quote")
        mock_choice.assert_called_once()

    @patch('main.random.choice')
    def test_get_multiple_quotes(self, mock_choice):
        # Mock rationale: side_effect to simulate sequential random choices
        mock_choice.side_effect = ["First", "Second", "Third"]
        quotes = main.get_multiple_quotes(3)
        self.assertEqual(quotes, ["First", "Second", "Third"])
        self.assertEqual(mock_choice.call_count, 3)


if __name__ == "__main__":
    unittest.main()
