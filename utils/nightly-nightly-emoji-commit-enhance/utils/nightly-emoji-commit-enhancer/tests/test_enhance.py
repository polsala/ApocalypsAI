import unittest
from unittest.mock import patch

# Import the function from the src module
from src.enhance import enhance_message, _select_emoji, DEFAULT_EMOJI

class TestEmojiCommitEnhancer(unittest.TestCase):
    def test_enhance_basic_keyword(self):
        msg = "Fix typo in README"
        result = enhance_message(msg)
        self.assertTrue(result.startswith("🐛 "))
        self.assertIn("Fix typo in README", result)

    def test_enhance_multiple_keywords_uses_first_match(self):
        msg = "Add docs and fix bug"
        result = enhance_message(msg)
        # "add" appears before "fix" in the mapping order, so ✨ should be chosen
        self.assertTrue(result.startswith("✨ "))

    def test_enhance_no_keyword_uses_default(self):
        msg = "Update configuration files"
        result = enhance_message(msg)
        self.assertTrue(result.startswith(f"{DEFAULT_EMOJI} "))

    def test_already_has_emoji(self):
        msg = "🚀 Launch new version"
        result = enhance_message(msg)
        self.assertEqual(result, msg)

    def test_select_emoji_mocked(self):
        # Mock the keyword map to ensure deterministic behavior
        with patch('src.enhance.KEYWORD_EMOJI_MAP', {'test': '✅'}):
            self.assertEqual(_select_emoji('Run tests'), '✅')
            self.assertEqual(_select_emoji('No match here'), DEFAULT_EMOJI)

if __name__ == '__main__':
    unittest.main()
