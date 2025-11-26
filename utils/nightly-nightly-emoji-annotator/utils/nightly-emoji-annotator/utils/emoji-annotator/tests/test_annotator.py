import unittest
from unittest.mock import patch

# Import the function from the sibling src directory
import sys
import os

# Adjust path so the src module can be imported when tests run directly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "src"))
sys.path.insert(0, SRC_DIR)

from annotator import annotate

class TestEmojiAnnotator(unittest.TestCase):
    def test_basic_annotation_without_seed(self):
        # We mock random.choice to return a predictable sequence of emojis.
        # Mock rationale: ensure deterministic output without relying on actual randomness.
        mock_emojis = ["😀", "🚀", "🌟"]
        with patch("annotator.random.choice", side_effect=mock_emojis):
            result = annotate("Hello world test")
        self.assertEqual(result, "Hello 😀 world 🚀 test 🌟")

    def test_annotation_with_seed(self):
        # When a seed is provided, the function should be deterministic even without mocking.
        result1 = annotate("foo bar baz", seed=123)
        result2 = annotate("foo bar baz", seed=123)
        self.assertEqual(result1, result2)
        # Verify that the output contains three emojis from the pool.
        parts = result1.split()
        self.assertEqual(len(parts), 6)  # word, emoji, word, emoji, ...
        # Ensure emojis are from the defined pool.
        from annotator import EMOJIS
        emojis_in_result = parts[1::2]
        for e in emojis_in_result:
            self.assertIn(e, EMOJIS)

    def test_empty_string(self):
        self.assertEqual(annotate(""), "")

if __name__ == "__main__":
    unittest.main()
