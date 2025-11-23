import unittest
from src.emoji_mood_analyzer import analyze_mood

class TestEmojiMoodAnalyzer(unittest.TestCase):
    # Mock rationale: using fixed input strings ensures deterministic behavior.

    def test_positive_sentiment(self):
        text = "I love this awesome and fantastic product!"
        self.assertEqual(analyze_mood(text), "😊")

    def test_negative_sentiment(self):
        text = "This is the worst, terrible, and awful experience."
        self.assertEqual(analyze_mood(text), "😞")

    def test_neutral_sentiment(self):
        # Contains only neutral words from the list.
        text = "The quick brown fox jumps over the lazy dog."
        self.assertEqual(analyze_mood(text), "😐")

    def test_mixed_tie_breaker_neutral(self):
        # Equal positive and negative counts, but neutral words present – should fall back to neutral.
        text = "I love it but also hate it and the the the"
        self.assertEqual(analyze_mood(text), "😐")

    def test_no_recognizable_words(self):
        text = "xyzzy plugh plover"
        self.assertEqual(analyze_mood(text), "😐")

if __name__ == "__main__":
    unittest.main()
