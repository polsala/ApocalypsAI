import unittest
from src.annotator import annotate

class TestAnnotator(unittest.TestCase):
    def test_basic_annotation(self):
        input_text = "I love coffee and sunshine."
        expected = "I love ❤️ coffee ☕ and sunshine 🌞."
        self.assertEqual(annotate(input_text), expected)

    def test_case_insensitivity(self):
        input_text = "Pizza is great, but I also like CAT videos."
        expected = "Pizza 🍕 is great, but I also like CAT 🐱 videos."
        self.assertEqual(annotate(input_text), expected)

    def test_no_keywords(self):
        input_text = "Just a plain sentence."
        self.assertEqual(annotate(input_text), input_text)

if __name__ == "__main__":
    unittest.main()
