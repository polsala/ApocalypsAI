import unittest
from utils.emoji-annotator.src.annotator import annotate

class TestEmojiAnnotator(unittest.TestCase):
    def test_basic_replacements(self):
        self.assertEqual(
            annotate("I love coffee and cats"),
            "I love coffee ❤️ ☕ and cats 🐱"
        )

    def test_case_insensitivity(self):
        self.assertEqual(
            annotate("Happy BIRTHDAY!"),
            "Happy 😊 BIRTHDAY! 🎂"
        )

    def test_word_boundaries(self):
        # "cat" inside "cater" should NOT be replaced.
        self.assertEqual(
            annotate("cater to the cat"),
            "cater to the cat 🐱"
        )

    def test_no_keywords(self):
        self.assertEqual(
            annotate("Just a plain sentence."),
            "Just a plain sentence."
        )

    def test_multiple_occurrences(self):
        self.assertEqual(
            annotate("pizza pizza pizza"),
            "pizza 🍕 pizza 🍕 pizza 🍕"
        )

if __name__ == "__main__":
    unittest.main()
