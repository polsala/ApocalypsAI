import unittest
from src.emoji_mood import analyze_mood

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_happy_mood(self):
        text = "I am so excited! 😄👍"
        self.assertEqual(analyze_mood(text), "happy")

    def test_sad_mood(self):
        text = "Feeling down... 😢👎"
        self.assertEqual(analyze_mood(text), "sad")

    def test_neutral_equal_counts(self):
        text = "Mixed feelings 😄😢"
        self.assertEqual(analyze_mood(text), "neutral")

    def test_neutral_no_emojis(self):
        text = "Just a plain sentence without emojis."
        self.assertEqual(analyze_mood(text), "neutral")

    def test_multiple_emojis(self):
        text = "Great job! 😄😄👍👍"
        self.assertEqual(analyze_mood(text), "happy")

    # Mock rationale: No external services are called; tests are fully deterministic.

if __name__ == "__main__":
    unittest.main()
