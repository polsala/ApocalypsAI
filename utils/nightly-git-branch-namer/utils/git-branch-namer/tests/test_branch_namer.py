import os
import sys
import unittest

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from branch_namer import generate_branch_name

class TestBranchNamer(unittest.TestCase):
    def test_basic(self):
        name = generate_branch_name("ABC-123", "Add login page")
        self.assertEqual(name, "feature/ABC-123-add-login-page")

    def test_custom_prefix(self):
        name = generate_branch_name("XYZ-9", "Fix typo", prefix="bugfix")
        self.assertEqual(name, "bugfix/XYZ-9-fix-typo")

    def test_slugify_complex(self):
        name = generate_branch_name("TCK-42", "   Refactor   API!! endpoints   ")
        self.assertEqual(name, "feature/TCK-42-refactor-api-endpoints")

    def test_truncate(self):
        long_title = (
            "Implement a very long description that exceeds the maximum allowed length "
            "for a branch name"
        )
        name = generate_branch_name("LONG-1", long_title, max_len=40)
        # Expected length <= 40
        self.assertTrue(len(name) <= 40)
        # Ensure it starts correctly
        self.assertTrue(name.startswith("feature/LONG-1-"))

    def test_max_len_smaller_than_prefix_ticket(self):
        # Mock rationale: when max_len is tiny, title is dropped and ticket may be truncated.
        name = generate_branch_name("BIG-12345", "Anything", max_len=10)
        self.assertTrue(len(name) <= 10)
        # The result should still contain the prefix
        self.assertTrue(name.startswith("feature"))

if __name__ == "__main__":
    unittest.main()
