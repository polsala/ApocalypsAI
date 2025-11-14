import unittest
from unittest.mock import patch
import sys, os

# Add src directory to path so we can import the module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from quote import get_zen_quote

class TestZenQuote(unittest.TestCase):
    def test_random_choice_mock(self):
        # Mock rationale: ensure deterministic output by fixing random.choice
        with patch('random.choice', return_value="Simplicity is the ultimate sophistication.") as mock_choice:
            quote = get_zen_quote()
            self.assertEqual(quote, "Simplicity is the ultimate sophistication.")
            mock_choice.assert_called_once()

    def test_max_length_filter(self):
        # Mock rationale: control random.choice to return the first eligible quote
        with patch('random.choice', side_effect=lambda seq: seq[0]) as mock_choice:
            quote = get_zen_quote(max_length=30)
            # Expected eligible quotes (<=30 chars)
            expected = [
                "Let go or be dragged.",
                "Silence is a source of great strength."
            ]
            self.assertIn(quote, expected)
            # Verify that random.choice received the filtered list of length 2
            self.assertEqual(len(mock_choice.call_args[0][0]), 2)

    def test_no_quote_fits(self):
        with self.assertRaises(ValueError):
            get_zen_quote(max_length=5)

if __name__ == "__main__":
    unittest.main()
