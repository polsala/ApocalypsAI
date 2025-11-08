import pathlib
import sys
import unittest
from unittest import mock

# Ensure the src directory is on the import path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from enhance import enhance_message, _select_emoji

class TestEmojiEnhancer(unittest.TestCase):
    def test_keyword_fix(self):
        self.assertEqual(
            enhance_message("Fix typo in README"),
            "Fix typo in README 🐛",
        )

    def test_keyword_add(self):
        self.assertEqual(
            enhance_message("Add user authentication"),
            "Add user authentication ✨",
        )

    def test_keyword_remove(self):
        self.assertEqual(
            enhance_message("Remove deprecated API"),
            "Remove deprecated API ❌",
        )

    @mock.patch("enhance.random.choice")
    def test_random_fallback(self, mock_choice):
        # Mock rationale: deterministic emoji selection for test.
        mock_choice.return_value = "🚀"
        self.assertEqual(
            enhance_message("Refactor codebase"),
            "Refactor codebase 🚀",
        )
        mock_choice.assert_called_once_with(["🎉", "🚀", "🤖"])

if __name__ == "__main__":
    unittest.main()
