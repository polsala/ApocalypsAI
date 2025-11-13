import os
import sys
import unittest

# Adjust path so the src module can be imported when tests are run from the repository root.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from emoji_commit_helper import suggest_emoji

class TestEmojiCommitHelper(unittest.TestCase):
    def test_feature_keyword(self):
        self.assertEqual(suggest_emoji("Add new feature to API"), "✨")

    def test_fix_keyword(self):
        self.assertEqual(suggest_emoji("Fix typo in README"), "🐛")

    def test_refactor_keyword(self):
        self.assertEqual(suggest_emoji("Refactor authentication module"), "🔧")

    def test_no_matching_keyword(self):
        self.assertEqual(suggest_emoji("Update dependencies"), "🎉")

    def test_multiple_keywords_first_match_wins(self):
        # 'fix' appears before 'add' in the mapping, so 🐛 should be returned.
        self.assertEqual(suggest_emoji("Fix and add docs"), "🐛")

    # Mock rationale: No external services are called, so no mocks are required.

if __name__ == "__main__":
    unittest.main()
