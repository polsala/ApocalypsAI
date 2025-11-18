import unittest
from unittest.mock import patch

# Import the function under test
from utils.emoji-annotator.src.annotator import annotate, get_emoji

class TestEmojiAnnotator(unittest.TestCase):
    def test_annotate_basic(self):
        # Direct test without mocking – uses the real map
        self.assertEqual(
            annotate("I love pizza"),
            "I love ❤️ pizza 🍕"
        )

    def test_annotate_no_emoji(self):
        self.assertEqual(
            annotate("plain text without matches"),
            "plain text without matches"
        )

    def test_annotate_with_mock(self):
        # Mock rationale: ensure deterministic mapping regardless of the real dict
        with patch('utils.emoji-annotator.src.annotator.get_emoji') as mock_get:
            # Define mock return values for specific inputs
            def side_effect(word):
                mapping = {
                    "hello": "👋",
                    "world": "🌍",
                }
                return mapping.get(word.lower(), "")
            mock_get.side_effect = side_effect

            result = annotate("Hello brave world")
            # Expected: each known word gets the mocked emoji, others stay unchanged
            self.assertEqual(result, "Hello 👋 brave world 🌍")

    def test_get_emoji_case_insensitivity(self):
        self.assertEqual(get_emoji("CoFfEe"), "☕")
        self.assertEqual(get_emoji("UNKNOWN"), "")

if __name__ == "__main__":
    unittest.main()
