import unittest
from typing import List

# Mock rationale: Import the module under test. No external I/O occurs.
from src.branch_name import generate_branch_name


class TestBranchNameGenerator(unittest.TestCase):
    def test_basic_slug(self):
        self.assertEqual(
            generate_branch_name("Add new feature"), "add-new-feature"
        )

    def test_underscore_and_spaces(self):
        self.assertEqual(
            generate_branch_name("Fix_user_login   bug"), "fix-user-login-bug"
        )

    def test_special_characters_removed(self):
        self.assertEqual(
            generate_branch_name("Release v1.2.3!"), "release-v123"
        )

    def test_multiple_hyphens_collapsed(self):
        self.assertEqual(
            generate_branch_name("---Crazy---Title---"), "crazy-title"
        )

    def test_truncation(self):
        long_title = "a" * 60  # 60 characters
        expected = "a" * 50  # truncated to 50
        self.assertEqual(generate_branch_name(long_title), expected)

    def test_conflict_resolution(self):
        existing: List[str] = ["feature-x", "feature-x-1", "feature-x-2"]
        # The base slug would be "feature-x" which already exists, so we expect "feature-x-3"
        self.assertEqual(
            generate_branch_name("Feature X", existing), "feature-x-3"
        )

    def test_no_conflict(self):
        existing = ["bugfix-typo"]
        self.assertEqual(
            generate_branch_name("Improve docs", existing), "improve-docs"
        )

    def test_empty_title(self):
        # Edge case: empty string should result in an empty branch name (still valid for our logic)
        self.assertEqual(generate_branch_name(""), "")


if __name__ == "__main__":
    unittest.main()
