import io
import sys
import unittest
from unittest import mock

# Mock rationale: No external services are used; we only need to import the module under test.
from utils.nightly-emoji-mood-tracker.src import emoji_mood

class TestEmojiMood(unittest.TestCase):
    def test_extract_emojis(self):
        text = "I love 🍕 and 🎉! But sometimes 😢."
        # Only emojis present in EMOJI_SCORES should be extracted.
        expected = ["🎉", "😢"]
        self.assertEqual(emoji_mood.extract_emojis(text), expected)

    def test_mood_score(self):
        emojis = ["😀", "😢", "❤️", "💩"]
        # Scores: +1, -1, +1, -1 => total 0
        self.assertEqual(emoji_mood.mood_score(emojis), 0)

    def test_mood_summary(self):
        cases = [
            (4, "Very Happy"),
            (2, "Happy"),
            (0, "Neutral"),
            (-1, "Sad"),
            (-4, "Very Sad"),
        ]
        for score, expected in cases:
            with self.subTest(score=score):
                self.assertEqual(emoji_mood.mood_summary(score), expected)

    def test_cli_stdout(self):
        # Simulate command‑line execution with --text argument.
        test_text = "Great job! 🎉👍"
        with mock.patch.object(sys, "argv", ["prog", "--text", test_text]):
            with mock.patch("builtins.print") as mock_print:
                emoji_mood.main()
                mock_print.assert_called_once_with("Very Happy")

    def test_cli_stdin(self):
        # Simulate reading from stdin when --text is omitted.
        test_text = "I am sad 😢"
        with mock.patch.object(sys, "argv", ["prog"]):
            with mock.patch.object(sys, "stdin", io.StringIO(test_text)):
                with mock.patch("builtins.print") as mock_print:
                    emoji_mood.main()
                    mock_print.assert_called_once_with("Sad")

if __name__ == "__main__":
    unittest.main()
