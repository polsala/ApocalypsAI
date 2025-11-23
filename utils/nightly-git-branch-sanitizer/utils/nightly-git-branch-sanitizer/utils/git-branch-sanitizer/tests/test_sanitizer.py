import unittest
import sys
import pathlib

# Add the src directory to sys.path so we can import the module under test.
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from sanitizer import sanitize_branch


class TestSanitizeBranch(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(sanitize_branch("Feature: Add New UI"), "feature-add-new-ui")

    def test_underscores_and_spaces(self):
        self.assertEqual(sanitize_branch("bug_fix 2023_09"), "bug-fix-2023-09")

    def test_invalid_chars(self):
        self.assertEqual(sanitize_branch("Release!@#Version$%^"), "releaseversion")

    def test_multiple_hyphens(self):
        self.assertEqual(sanitize_branch("---Crazy---Name---"), "crazy-name")

    def test_slashes_and_dots(self):
        self.assertEqual(sanitize_branch("path/to.branch"), "path/to.branch")

    def test_leading_trailing(self):
        self.assertEqual(sanitize_branch("-/Start-End-/"), "start-end")


if __name__ == "__main__":
    unittest.main()
