import unittest
from utils.nightly_emoji_mood_analyzer.src.emoji_mood import analyze_sentiment

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_positive_sentiment(self):
        self.assertEqual(analyze_sentiment("I love this awesome product!"), "😊")

    def test_negative_sentiment(self):
        self.assertEqual(analyze_sentiment("This is the worst, terrible experience."), "😞")

    def test_neutral_sentiment(self):
        self.assertEqual(analyze_sentiment("It is a day."), "😐")

    def test_case_insensitivity(self):
        self.assertEqual(analyze_sentiment("I LOVE it but also hate the price"), "😐")

    def test_tie_breaker_defaults_to_neutral(self):
        # One positive, one negative word → tie
        self.assertEqual(analyze_sentiment("good but bad"), "😐")

    def test_multiple_occurrences(self):
        self.assertEqual(analyze_sentiment("good good good bad"), "😊")
        self.assertEqual(analyze_sentiment("bad bad terrible good"), "😞")

if __name__ == "__main__":
    unittest.main()
