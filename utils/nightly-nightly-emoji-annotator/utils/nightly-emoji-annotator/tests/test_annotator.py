import unittest
from unittest.mock import patch

# Mock rationale: Ensure deterministic emoji selection without external randomness.
from src.annotator import annotate_text

class TestEmojiAnnotator(unittest.TestCase):
    @patch("random.choice", lambda _: "😀")
    def test_annotate_simple(self):
        input_text = "Hello world! How are you? I am fine."
        expected = "Hello world! 😀 How are you? 😀 I am fine. 😀"
        self.assertEqual(annotate_text(input_text), expected)

    @patch("random.choice", lambda _: "🚀")
    def test_annotate_single_sentence(self):
        input_text = "Just one sentence."
        expected = "Just one sentence. 🚀"
        self.assertEqual(annotate_text(input_text), expected)

if __name__ == "__main__":
    unittest.main()
