import unittest
from src.annotator import annotate

class TestEmojiAnnotator(unittest.TestCase):
    def test_basic_replacements(self):
        # Simple sentence with known keywords
        input_text = "I love coffee and cats"
        expected = "I ❤️ love ☕ coffee and 🐱 cats"
        # Mock rationale: No external calls; deterministic mapping ensures stable output.
        self.assertEqual(annotate(input_text), expected)

    def test_case_insensitivity(self):
        input_text = "Python code FIRE"
        expected = "Python 🐍 code 💻 FIRE 🔥"
        self.assertEqual(annotate(input_text), expected)

    def test_unknown_words(self):
        input_text = "This sentence has no matches"
        expected = "This sentence has no matches"
        self.assertEqual(annotate(input_text), expected)

    def test_punctuation_preserved(self):
        input_text = "Wow! Fire? Yes, fire."
        expected = "Wow! Fire 🔥? Yes, fire 🔥."
        self.assertEqual(annotate(input_text), expected)

if __name__ == "__main__":
    unittest.main()
