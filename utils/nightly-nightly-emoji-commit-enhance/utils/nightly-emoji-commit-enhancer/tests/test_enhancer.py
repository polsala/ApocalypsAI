import os
import sys
import unittest

# Ensure the src directory is on the import path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from enhancer import enhance_message, select_emoji  # type: ignore

class TestEmojiEnhancer(unittest.TestCase):
    def test_select_emoji_known(self):
        self.assertEqual(select_emoji("Fix typo in README"), "🛠️")
        self.assertEqual(select_emoji("Add new feature X"), "➕")
        self.assertEqual(select_emoji("Remove deprecated API"), "❌")
        self.assertEqual(select_emoji("Refactor module Y"), "♻️")
        self.assertEqual(select_emoji("Update docs for Z"), "📚")
        self.assertEqual(select_emoji("Improve performance of loop"), "⚡")
        self.assertEqual(select_emoji("Patch security issue"), "🔒")
        self.assertEqual(select_emoji("Write tests for edge cases"), "🧪")

    def test_select_emoji_default(self):
        self.assertEqual(select_emoji("Miscellaneous changes"), "✨")

    def test_enhance_message(self):
        self.assertEqual(enhance_message("Fix bug in parser"), "🛠️ Fix bug in parser")
        self.assertEqual(enhance_message("Add support for JSON"), "➕ Add support for JSON")
        self.assertEqual(enhance_message("Random change"), "✨ Random change")

    def test_enhance_message_idempotent(self):
        # If the message already starts with an emoji, leave it unchanged.
        self.assertEqual(enhance_message("🛠️ Fix bug"), "🛠️ Fix bug")

if __name__ == "__main__":
    unittest.main()
