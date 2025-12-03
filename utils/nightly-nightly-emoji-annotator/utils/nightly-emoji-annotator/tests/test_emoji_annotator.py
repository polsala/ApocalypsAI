import unittest
import os
import sys

# Add the src directory to the import path so we can import the module directly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from emoji_annotator import annotate

class TestEmojiAnnotator(unittest.TestCase):
    def test_basic_keywords(self):
        self.assertEqual(
            annotate("I love coffee and coding."),
            "I love❤️ coffee☕ and coding💻."
        )

    def test_punctuation_preserved(self):
        self.assertEqual(
            annotate("Python! Tea, and music?"),
            "Python🐍! Tea🍵, and music🎵?"
        )

    def test_no_keywords(self):
        self.assertEqual(
            annotate("Just a plain sentence."),
            "Just a plain sentence."
        )

    # Mock rationale: No external calls; deterministic mapping.

if __name__ == "__main__":
    unittest.main()
