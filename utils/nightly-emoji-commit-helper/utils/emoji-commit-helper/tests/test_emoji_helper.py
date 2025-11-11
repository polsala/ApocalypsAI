import unittest
from pathlib import Path

# Import the function from the utility's source directory.
# Adjust sys.path so the test can locate the module without installing the package.
import sys
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from emoji_helper import get_emoji_for_message

class TestEmojiHelper(unittest.TestCase):
    def test_bug_fix(self):
        self.assertEqual(get_emoji_for_message("Fix typo in README"), "🐛")
        self.assertEqual(get_emoji_for_message("bug: resolve crash on startup"), "🐛")

    def test_feature_addition(self):
        self.assertEqual(get_emoji_for_message("Add new login feature"), "✨")
        self.assertEqual(get_emoji_for_message("Implement OAuth support"), "✨")

    def test_removal(self):
        self.assertEqual(get_emoji_for_message("Remove deprecated API"), "🗑️")
        self.assertEqual(get_emoji_for_message("Cleanup old config files"), "🗑️")

    def test_documentation(self):
        self.assertEqual(get_emoji_for_message("Update docs for installation"), "📚")
        self.assertEqual(get_emoji_for_message("README: add contribution guide"), "📚")

    def test_testing(self):
        self.assertEqual(get_emoji_for_message("Add tests for edge cases"), "✅")
        self.assertEqual(get_emoji_for_message("testing: improve coverage"), "✅")

    def test_default(self):
        # No matching keywords → default wrench.
        self.assertEqual(get_emoji_for_message("Refactor code base"), "🔧")
        self.assertEqual(get_emoji_for_message("Improve performance"), "🔧")

if __name__ == "__main__":
    # Mock rationale: Running via pytest in CI; this block ensures the file can also be executed directly.
    unittest.main()
