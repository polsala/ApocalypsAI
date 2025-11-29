import unittest
from src.annotator import annotate

class TestEmojiAnnotator(unittest.TestCase):
    def test_basic_annotation(self):
        input_text = "I love coffee and coding"
        expected = "I love ❤️ coffee ☕ and coding 💻"
        self.assertEqual(annotate(input_text), expected)

    def test_no_keywords(self):
        input_text = "Just a plain sentence."
        self.assertEqual(annotate(input_text), input_text)

    def test_mixed_case_and_punctuation(self):
        input_text = "Python, bugs, and fire!"
        expected = "Python, 🐍 bugs, 🐛 and fire! 🔥"
        self.assertEqual(annotate(input_text), expected)

if __name__ == "__main__":
    unittest.main()
