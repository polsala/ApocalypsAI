import unittest
from src.logger import get_mood_emoji

class TestEmojiMoodLogger(unittest.TestCase):
    def test_positive_sentiment(self):
        text = "I am feeling great and wonderful after the awesome sprint."
        self.assertEqual(get_mood_emoji(text), "😊")

    def test_negative_sentiment(self):
        text = "This bug is terrible and makes me sad."
        self.assertEqual(get_mood_emoji(text), "😢")

    def test_neutral_sentiment(self):
        text = "The meeting was okay, nothing special."
        self.assertEqual(get_mood_emoji(text), "😐")

    def test_mixed_but_positive(self):
        # Mock rationale: more positive keywords than negative ones
        text = "I love the new feature but hate the documentation."
        self.assertEqual(get_mood_emoji(text), "😊")

    def test_mixed_but_negative(self):
        # Mock rationale: more negative keywords than positive ones
        text = "The performance is bad, but the UI looks good."
        self.assertEqual(get_mood_emoji(text), "😢")

if __name__ == "__main__":
    unittest.main()
