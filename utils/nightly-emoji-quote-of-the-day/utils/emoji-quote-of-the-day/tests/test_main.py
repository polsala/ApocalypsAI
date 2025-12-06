import unittest
from unittest.mock import patch
import sys
import os

# Add src directory to sys.path for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Mock rationale: Ensure deterministic output by fixing random.choice selections.
from main import get_emoji_quote

class TestEmojiQuote(unittest.TestCase):
    @patch('random.choice')
    def test_get_emoji_quote_deterministic(self, mock_choice):
        # Always return the first element of the provided sequence.
        mock_choice.side_effect = lambda seq: seq[0]
        emoji, quote = get_emoji_quote()
        self.assertEqual(emoji, "🌞")
        self.assertEqual(quote, "Keep your face always toward the sunshine—and shadows will fall behind you.")

if __name__ == "__main__":
    unittest.main()
