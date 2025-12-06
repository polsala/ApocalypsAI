import unittest
from src.commit_emoji import suggest_emoji

class TestCommitEmoji(unittest.TestCase):
    def test_fix_bug(self):
        self.assertEqual(suggest_emoji("Fix bug in authentication"), "🐛")

    def test_add_feature(self):
        self.assertEqual(suggest_emoji("Add new endpoint for payments"), "✨")

    def test_remove_deprecated(self):
        self.assertEqual(suggest_emoji("Remove old config files"), "🗑️")

    def test_refactor_code(self):
        self.assertEqual(suggest_emoji("Refactor user service"), "🛠️")

    def test_tests_added(self):
        self.assertEqual(suggest_emoji("Add tests for order model"), "✅")

    def test_documentation(self):
        self.assertEqual(suggest_emoji("Update README and docs"), "📚")

    def test_performance(self):
        self.assertEqual(suggest_emoji("Improve performance of query engine"), "🚀")

    def test_merge(self):
        self.assertEqual(suggest_emoji("Merge branch 'feature/login'"), "🔀")

    def test_ci_pipeline(self):
        self.assertEqual(suggest_emoji("Update CI pipeline configuration"), "🤖")

    def test_security(self):
        self.assertEqual(suggest_emoji("Fix security vulnerability in auth"), "🔒")

    def test_no_match(self):
        # Mock rationale: No keyword matches, should return default emoji.
        self.assertEqual(suggest_emoji("Random commit with no keywords"), "🔧")

if __name__ == "__main__":
    unittest.main()
