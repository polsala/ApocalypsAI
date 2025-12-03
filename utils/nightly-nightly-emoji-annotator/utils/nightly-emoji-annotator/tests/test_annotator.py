import unittest
import sys
import os

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from annotator import annotate

class TestEmojiAnnotator(unittest.TestCase):
    def test_basic(self):
        input_text = "I love Python. It makes me happy!"
        expected = "I love Python ❤️. It makes me happy! 😊"
        self.assertEqual(annotate(input_text), expected)

    def test_fire(self):
        input_text = "The fire burned."
        expected = "The fire burned 🔥."
        self.assertEqual(annotate(input_text), expected)

    def test_no_match(self):
        input_text = "Nothing special here."
        expected = "Nothing special here."
        self.assertEqual(annotate(input_text), expected)

    def test_multiple_sentences_mixed(self):
        input_text = "We had a party. Then it got sad."
        expected = "We had a party 🥳. Then it got sad 😢."
        self.assertEqual(annotate(input_text), expected)

if __name__ == "__main__":
    unittest.main()
