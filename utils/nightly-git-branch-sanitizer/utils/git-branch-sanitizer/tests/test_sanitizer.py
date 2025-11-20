import unittest
import sys
import pathlib

# Add the src directory to sys.path so we can import the module directly
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from sanitizer import sanitize_branch

class TestSanitizeBranch(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(sanitize_branch("Feature: Add New UI!"), "feature-add-new-ui")

    def test_spaces_and_underscores(self):
        self.assertEqual(sanitize_branch("my_feature name"), "my-feature-name")

    def test_multiple_hyphens(self):
        self.assertEqual(sanitize_branch("---Weird---Name---"), "weird-name")

    def test_allowed_chars(self):
        self.assertEqual(sanitize_branch("release/v1.2.3"), "release/v1.2.3")

    def test_disallowed_chars(self):
        self.assertEqual(sanitize_branch("Fix#123$%^&*()"), "fix123")

    def test_leading_trailing_hyphens(self):
        self.assertEqual(sanitize_branch("-Start and End-"), "start-and-end")

if __name__ == "__main__":
    unittest.main()
