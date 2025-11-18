import unittest
from src.annotator import annotate


class TestEmojiAnnotator(unittest.TestCase):
    def test_single_keyword(self):
        input_text = "I am happy. It is raining."
        expected = "I am happy 😊. It is raining."
        self.assertEqual(annotate(input_text), expected)

    def test_multiple_keywords(self):
        input_text = "Fire! What a star."
        expected = "Fire! 🔥 What a star ⭐."
        self.assertEqual(annotate(input_text), expected)

    def test_no_keywords(self):
        input_text = "Just a plain sentence without magic."
        expected = "Just a plain sentence without magic."
        self.assertEqual(annotate(input_text), expected)

    def test_mixed_case_and_whitespace(self):
        input_text = "  LOVE is powerful!  sad?"
        # The leading spaces are preserved; emojis are added after each sentence.
        expected = "  LOVE is powerful! ❤️  sad? 😢"
        self.assertEqual(annotate(input_text), expected)

    def test_sentence_without_delimiter(self):
        # Mock rationale: ensure function gracefully handles trailing text without punctuation.
        input_text = "I love coding"
        expected = "I love coding ❤️"
        self.assertEqual(annotate(input_text), expected)


if __name__ == "__main__":
    unittest.main()
