import unittest
import sys
import os

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from emoji_commit_helper import get_emoji

class TestEmojiCommitHelper(unittest.TestCase):
    def test_fix_keyword(self):
        self.assertEqual(get_emoji("Fix bug in parser"), "🐛")  # Mock rationale: deterministic mapping

    def test_add_keyword(self):
        self.assertEqual(get_emoji("Add new feature to API"), "✨")

    def test_no_keyword(self):
        self.assertEqual(get_emoji("Update configuration"), "🔧")

    def test_multiple_keywords_first_match(self):
        self.assertEqual(get_emoji("Refactor and add docs"), "♻️")  # first matching keyword in order

if __name__ == "__main__":
    unittest.main()
