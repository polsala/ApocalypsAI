import os
import unittest
from unittest.mock import patch

# Import the module under test
from utils.nightly-emoji-annotator.src.annotator import annotate_line, get_sentiment

class TestEmojiAnnotator(unittest.TestCase):
    def test_positive_sentiment(self):
        line = "I had a great day"
        self.assertEqual(get_sentiment(line), "positive")
        self.assertTrue(annotate_line(line).endswith("😊\n"))

    def test_negative_sentiment(self):
        line = "This is the worst experience"
        self.assertEqual(get_sentiment(line), "negative")
        self.assertTrue(annotate_line(line).endswith("😞\n"))

    def test_neutral_sentiment(self):
        line = "Just an ordinary sentence"
        self.assertEqual(get_sentiment(line), "neutral")
        self.assertTrue(annotate_line(line).endswith("😐\n"))

    def test_extra_positive_via_env(self):
        line = "The movie was splendid"
        # Mock rationale: we want to ensure the utility respects the EXTRA_POSITIVE env var
        with patch.dict(os.environ, {"EXTRA_POSITIVE": "splendid,marvelous"}):
            self.assertEqual(get_sentiment(line), "positive")
            self.assertTrue(annotate_line(line).endswith("😊\n"))

if __name__ == "__main__":
    unittest.main()
