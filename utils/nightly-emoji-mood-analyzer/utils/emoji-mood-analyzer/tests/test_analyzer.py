import unittest
from unittest.mock import patch

# Mock rationale: we patch the internal tokenization to control word detection without relying on regex behavior.
# This ensures deterministic tests even if the implementation changes.

from utils.emoji-mood-analyzer.src.analyzer import analyze_mood

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_happy_mood(self):
        text = "I am feeling great and wonderful today!"
        self.assertEqual(analyze_mood(text), "😊")

    def test_sad_mood(self):
        text = "It is a sad, down day."
        self.assertEqual(analyze_mood(text), "😢")

    def test_angry_mood(self):
        text = "I'm so angry about the traffic jam."
        self.assertEqual(analyze_mood(text), "😠")

    def test_neutral_mood(self):
        text = "Just an ordinary statement with no emotion."
        self.assertEqual(analyze_mood(text), "🤔")

    def test_multiple_moods_priority(self):
        # Contains both happy and sad keywords; happy should win due to priority order.
        text = "I am happy but also sad about the news."
        self.assertEqual(analyze_mood(text), "😊")

    @patch('utils.emoji-mood-analyzer.src.analyzer._tokenize')
    def test_tokenize_mock(self, mock_tokenize):
        # Mock rationale: force token set to a known value to test keyword detection path.
        mock_tokenize.return_value = {"mad", "fantastic"}
        # Even though "mad" maps to angry, "fantastic" maps to happy and has higher priority.
        self.assertEqual(analyze_mood("irrelevant"), "😊")
        mock_tokenize.assert_called_once()

if __name__ == "__main__":
    unittest.main()
