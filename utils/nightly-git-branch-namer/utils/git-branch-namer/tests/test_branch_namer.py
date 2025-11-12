import unittest
import sys
import os

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from branch_namer import generate_branch_name

class TestBranchNamer(unittest.TestCase):
    def test_default_type(self):
        self.assertEqual(
            generate_branch_name("Add user login page"),
            "feat/add-user-login-page"
        )

    def test_explicit_type(self):
        self.assertEqual(
            generate_branch_name("Fix: typo in README"),
            "fix/typo-in-readme"
        )
        self.assertEqual(
            generate_branch_name("Docs - update changelog"),
            "docs/update-changelog"
        )

    def test_mixed_case_and_punctuation(self):
        self.assertEqual(
            generate_branch_name("ReFACTOR! Clean up code."),
            "refactor/clean-up-code"
        )

    def test_emoji_and_non_ascii(self):
        self.assertEqual(
            generate_branch_name("Add 🚀 new feature"),
            "feat/add-new-feature"
        )

    def test_empty_title(self):
        self.assertEqual(
            generate_branch_name("   "),
            "feat/unnamed"
        )

if __name__ == "__main__":
    unittest.main()
