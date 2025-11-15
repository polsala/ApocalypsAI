import unittest
import os
import runpy


def load_module():
    """Load the emoji_helper module without importing it as a package.

    This approach works even though the utility directory name contains hyphens,
    which are not valid in Python package names.
    """
    module_path = os.path.join(os.path.dirname(__file__), "..", "src", "emoji_helper.py")
    return runpy.run_path(module_path)


class TestEmojiHelper(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()
        self.suggest = self.mod["suggest_emoji"]

    def test_fix_bug(self):
        self.assertEqual(self.suggest("Fix bug in parser"), "🐛")

    def test_add_feature(self):
        self.assertEqual(self.suggest("Add new authentication feature"), "✨")

    def test_docs(self):
        self.assertEqual(self.suggest("Update docs for API"), "📝")

    def test_no_match(self):
        self.assertEqual(self.suggest("Improve overall code quality"), "💡")

    # Mock rationale: No external services are called; the function is pure and deterministic.

if __name__ == "__main__":
    unittest.main()
