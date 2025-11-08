import unittest
from src.sanitizer import sanitize_branch_name

class TestSanitizeBranchName(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(sanitize_branch_name("Feature/Add New_Stuff!"), "feature-add-new-stuff")

    def test_leading_trailing_hyphens(self):
        self.assertEqual(sanitize_branch_name("---My Branch---"), "my-branch")

    def test_multiple_spaces_and_underscores(self):
        self.assertEqual(sanitize_branch_name("  many   spaces___and___underscores  "), "many-spaces-and-underscores")

    def test_invalid_characters(self):
        self.assertEqual(sanitize_branch_name("$%^&*()"), "")

    def test_already_clean(self):
        self.assertEqual(sanitize_branch_name("release-1.2.3"), "release-123")

    def test_empty_input(self):
        self.assertEqual(sanitize_branch_name("   "), "")

    def test_numeric(self):
        self.assertEqual(sanitize_branch_name("Version_2025"), "version-2025")

# Mock rationale: All tests use only the pure function `sanitize_branch_name` which has no external I/O.
# This guarantees deterministic, offline execution.

if __name__ == "__main__":
    unittest.main()
