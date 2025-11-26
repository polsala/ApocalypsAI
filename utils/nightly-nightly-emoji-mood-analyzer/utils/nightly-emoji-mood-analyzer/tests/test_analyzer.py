import os
import sys
import unittest

# Ensure the src directory is on the import path.
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from analyzer import analyze_mood

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_positive_sentiment(self):
        text = "I love sunny days and wonderful friends."
        result = analyze_mood(text)
        self.assertEqual(result["sentiment"], "positive")
        self.assertEqual(result["emoji"], "😊")
        # Mock rationale: the text contains more words from POSITIVE_WORDS than NEGATIVE_WORDS.

    def test_negative_sentiment(self):
        text = "I hate rainy days and terrible traffic."
        result = analyze_mood(text)
        self.assertEqual(result["sentiment"], "negative")
        self.assertEqual(result["emoji"], "😞")
        # Mock rationale: the text contains more NEGATIVE_WORDS than POSITIVE_WORDS.

    def test_neutral_sentiment(self):
        text = "The cat sits on the mat."
        result = analyze_mood(text)
        self.assertEqual(result["sentiment"], "neutral")
        self.assertEqual(result["emoji"], "😐")
        # Mock rationale: no sentiment‑bearing words are present, leading to a tie.

if __name__ == "__main__":
    unittest.main()
