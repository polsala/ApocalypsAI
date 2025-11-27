import unittest
from src.branch_linter import is_kebab_case, suggest_kebab_case, lint_branch

class TestBranchLinter(unittest.TestCase):
    def test_is_kebab_case_valid(self):
        valid_names = [
            "feature-login",
            "bugfix-123",
            "release",
            "hotfix-2024-01-01",
            "a1-b2-c3",
        ]
        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(is_kebab_case(name))

    def test_is_kebab_case_invalid(self):
        invalid_names = [
            "FeatureLogin",   # camel case
            "bug_fix",        # underscore
            "-leading",       # leading hyphen
            "trailing-",      # trailing hyphen
            "multiple--dash", # consecutive hyphens
            "UPPERCASE",      # uppercase letters
            "space bar",      # space
        ]
        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(is_kebab_case(name))

    def test_suggest_kebab_case(self):
        cases = {
            "FeatureLogin": "featurelogin",
            "bug_fix": "bug-fix",
            "  spaced  out  ": "spaced-out",
            "Multiple---Dashes": "multiple-dashes",
            "UPPER_case-MIX": "upper-case-mix",
            "***": "default-branch",
        }
        for original, expected in cases.items():
            with self.subTest(original=original):
                self.assertEqual(suggest_kebab_case(original), expected)

    def test_lint_branch(self):
        # Valid case
        self.assertEqual(lint_branch("feature-login"), (True, "feature-login"))
        # Invalid case – suggestion should be deterministic
        self.assertEqual(lint_branch("FeatureLogin"), (False, "featurelogin"))
        self.assertEqual(lint_branch("bug_fix"), (False, "bug-fix"))

if __name__ == "__main__":
    unittest.main()
