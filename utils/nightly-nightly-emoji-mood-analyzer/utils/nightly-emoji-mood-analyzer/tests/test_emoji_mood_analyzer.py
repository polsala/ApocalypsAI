import unittest
from unittest.mock import patch
import sys

# Import the module under test
from src.emoji_mood_analyzer import get_mood_emoji, main

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_direct_mapping(self):
        self.assertEqual(get_mood_emoji("I am very happy today"), "😊")
        self.assertEqual(get_mood_emoji("Feeling sad about the news"), "😢")
        self.assertEqual(get_mood_emoji("She is excited!"), "🤩")
        self.assertEqual(get_mood_emoji("I love Python"), "❤️")

    def test_no_match_returns_default(self):
        self.assertEqual(get_mood_emoji("Just a neutral statement"), "🤔")

    @patch.object(sys, "argv", ["emoji_mood_analyzer.py", "I am angry"])
    def test_cli_argument_parsing(self):
        # Mock rationale: we replace sys.argv to simulate CLI call without real process launch.
        with patch('builtins.print') as mock_print:
            exit_code = main()
            mock_print.assert_called_once_with("😠")
            self.assertEqual(exit_code, 0)

    @patch.object(sys, "argv", ["emoji_mood_analyzer.py"])
    @patch('sys.stdin')
    def test_cli_stdin_input(self, mock_stdin):
        # Mock rationale: provide stdin content via mock object.
        mock_stdin.read.return_value = "I feel sleepy now"
        with patch('builtins.print') as mock_print:
            exit_code = main()
            mock_print.assert_called_once_with("😴")
            self.assertEqual(exit_code, 0)

if __name__ == "__main__":
    unittest.main()
