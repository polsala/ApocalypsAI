import unittest
from unittest import mock
from src.commit_linter import lint_message

class TestCommitLinter(unittest.TestCase):
    def test_valid_message(self):
        msg = "feat(parser): add support for YAML"
        issues = lint_message(msg)
        self.assertEqual(issues, [])

    def test_invalid_type_and_length(self):
        # Message longer than 72 chars and with an unknown type
        msg = (
            "unknown(scope): this description is deliberately made very long to exceed the seventy-two character limit set by the linter"
        )
        issues = lint_message(msg)
        # Expect two issues: type not allowed and length exceeded
        self.assertIn("Header exceeds 72 characters", issues[0])
        self.assertIn("Commit type 'unknown' is not allowed", issues[1])

    def test_missing_pattern(self):
        msg = "Just a plain commit message without pattern"
        issues = lint_message(msg)
        self.assertIn(
            "Header does not match '<type>(<scope>): <description>' pattern.",
            issues,
        )

    @mock.patch('builtins.print')  # Mock rationale: avoid actual stdout during test run
    def test_cli_entrypoint(self, mock_print):
        # Simulate CLI call via __main__ guard
        test_args = ["commit_linter.py", "fix: correct typo"]
        with mock.patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                # Import inside the patch to trigger the guard
                import importlib
                import src.commit_linter as cl
                importlib.reload(cl)
            # Exit code should be 0 (no issues)
            self.assertEqual(cm.exception.code, 0)

if __name__ == "__main__":
    unittest.main()
