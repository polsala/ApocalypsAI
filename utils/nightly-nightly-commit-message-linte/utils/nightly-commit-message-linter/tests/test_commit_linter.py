# Mock rationale: deterministic test data – using static commit strings ensures offline, repeatable tests.
import unittest
from src.commit_linter import lint_message

class TestCommitLinter(unittest.TestCase):
    def test_valid_simple(self):
        msg = "feat: add new login button"
        self.assertEqual(lint_message(msg), [])

    def test_valid_with_scope_and_breaking(self):
        msg = "fix(parser)!: handle null pointer\n\nFixes crash on empty input."
        self.assertEqual(lint_message(msg), [])

    def test_invalid_type(self):
        msg = "unknown: something"
        errors = lint_message(msg)
        self.assertTrue(any("Invalid header" in e for e in errors))

    def test_missing_blank_line(self):
        msg = "feat: improve UI\nAdded new colors."
        errors = lint_message(msg)
        self.assertTrue(any("Second line should be blank" in e for e in errors))

    def test_empty_message(self):
        msg = ""
        errors = lint_message(msg)
        self.assertTrue(any("Commit message is empty" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
