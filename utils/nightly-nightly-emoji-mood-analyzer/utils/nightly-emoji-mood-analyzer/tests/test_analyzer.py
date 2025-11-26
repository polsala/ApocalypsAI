import unittest
from src.analyzer import analyze_mood

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_positive_sentiment(selfn):
        # Mock rationale: the phrase contains two positive words, score > 0.
        sentiment, emoji = analyze_mood("I love this awesome project!")
        self.assertEqual(sentiment, "positive")
        self.assertEqual(emoji, "😊")

    def test_negative_sentiment(selfn):
        # Mock rationale: the phrase contains a negative word, score < 0.
        sentiment, emoji = analyze_mood("This is the worst experience ever.")
        self.assertEqual(sentiment, "negative")
        self.assertEqual(emoji, "😞")

    def test_neutral_sentiment(selfn):
        # Mock rationale: no sentiment‑bearing words, score == 0.
        sentiment, emoji = analyze_mood("The sky is blue.")
        self.assertEqual(sentiment, "neutral")
        self.assertEqual(emoji, "😐")

    def test_mixed_sentiment(selfn):
        # Mock rationale: equal number of positive and negative words → neutral.
        sentiment, emoji = analyze_mood("I love it but also hate the bugs.")
        self.assertEqual(sentiment, "neutral")
        self.assertEqual(emoji, "😐")

if __name__ == "__main__":
    unittest.main()
