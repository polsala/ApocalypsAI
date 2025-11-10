import unittest
from unittest.mock import patch

# Mock rationale: Import using the package path that mirrors the repo layout.
from utils.emoji-commit-enhancer.src.enhance import enhance_message

class TestEmojiCommitEnhancer(unittest.TestCase):
    def test_keyword_mapping(self):
        self.assertTrue(enhance_message("Fix bug in parser").startswith("🐛"))
        self.assertTrue(enhance_message("Add new feature").startswith("➕"))
        self.assertTrue(enhance_message("Update docs for API").startswith("📚"))
        self.assertTrue(enhance_message("Refactor authentication flow").startswith("♻️"))
        self.assertTrue(enhance_message("Run tests for module").startswith("✅"))

    @patch('utils.emoji-commit-enhancer.src.enhance.random.choice')
    def test_default_random_emoji(self, mock_choice):
        # Mock rationale: Ensure deterministic output when no keyword matches.
        mock_choice.return_value = "✨"
        result = enhance_message("Unrelated commit message")
        self.assertEqual(result, "✨ Unrelated commit message")
        mock_choice.assert_called_once()

if __name__ == "__main__":
    unittest.main()
