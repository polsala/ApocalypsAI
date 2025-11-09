import unittest
import os, sys

# Add src directory to path so we can import the module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sanitize_branch import sanitize_branch


class TestSanitizeBranch(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(sanitize_branch("Feature/Add New_Stuff!"), "feature-add-new-stuff")

    def test_leading_trailing(self):
        self.assertEqual(sanitize_branch("  /bugfix/issue-42  "), "bugfix-issue-42")

    def test_multiple_hyphens(self):
        self.assertEqual(sanitize_branch("release---candidate"), "release-candidate")

    def test_invalid_chars(self):
        self.assertEqual(sanitize_branch("hotfix@#%$"), "hotfix")

    def test_preserve_dots(self):
        self.assertEqual(sanitize_branch("v1.2.3_release"), "v1.2.3-release")


if __name__ == "__main__":
    unittest.main()
