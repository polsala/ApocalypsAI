import unittest
import subprocess
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the path for importing quill.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from quill import generate_changelog, parse_commit_message, run_git_command

class TestQuill(unittest.TestCase):

    @patch('subprocess.run')
    def test_run_git_command_success(self, mock_subprocess_run):
        # Mock rationale: Simulate a successful git command execution.
        mock_result = MagicMock()
        mock_result.stdout = "git output\n"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_result.strip.return_value = "git output" # For the .strip() call in run_git_command
        mock_subprocess_run.return_value = mock_result

        output = run_git_command(["git", "status"])
        self.assertEqual(output, "git output")
        mock_subprocess_run.assert_called_once_with(
            ["git", "status"], capture_output=True, text=True, check=True, cwd=None
        )

    @patch('subprocess.run')
    def test_run_git_command_failure(self, mock_subprocess_run):
        # Mock rationale: Simulate a failed git command execution.
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "fatal: not a git repository\n"
        mock_result.returncode = 1
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=["git", "log"], stderr="fatal: not a git repository\n"
        )

        with self.assertRaises(subprocess.CalledProcessError):
            run_git_command(["git", "log"])

    def test_parse_commit_message_feat(self):
        message = "feat(scope): Add new feature\n\nThis is the body."
        parsed = parse_commit_message(message)
        self.assertEqual(parsed["type"], "feat")
        self.assertEqual(parsed["scope"], "scope")
        self.assertEqual(parsed["subject"], "Add new feature")
        self.assertEqual(parsed["body"], "This is the body.")
        self.assertFalse(parsed["is_breaking"])

    def test_parse_commit_message_fix_no_scope(self):
        message = "fix: Fix a bug"
        parsed = parse_commit_message(message)
        self.assertEqual(parsed["type"], "fix")
        self.assertIsNone(parsed["scope"])
        self.assertEqual(parsed["subject"], "Fix a bug")
        self.assertFalse(parsed["is_breaking"])

    def test_parse_commit_message_breaking_bang(self):
        message = "feat!: Introduce breaking change\n\nBREAKING CHANGE: This changes everything."
        parsed = parse_commit_message(message)
        self.assertEqual(parsed["type"], "feat")
        self.assertIsNone(parsed["scope"])
        self.assertEqual(parsed["subject"], "Introduce breaking change")
        self.assertTrue(parsed["is_breaking"])

    def test_parse_commit_message_breaking_body(self):
        message = "refactor: Refactor old code\n\nThis is a refactor.\n\nBREAKING CHANGE: Old API is gone."
        parsed = parse_commit_message(message)
        self.assertEqual(parsed["type"], "refactor")
        self.assertIsNone(parsed["scope"])
        self.assertEqual(parsed["subject"], "Refactor old code")
        self.assertTrue(parsed["is_breaking"])

    def test_parse_commit_message_non_conventional(self):
        message = "Just a regular commit message"
        parsed = parse_commit_message(message)
        self.assertEqual(parsed["type"], "chore") # Default to chore
        self.assertIsNone(parsed["scope"])
        self.assertEqual(parsed["subject"], "Just a regular commit message")
        self.assertFalse(parsed["is_breaking"])

    @patch('quill.run_git_command')
    def test_generate_changelog_basic(self, mock_run_git_command):
        # Mock rationale: Simulate git log output for a few conventional commits.
        mock_run_git_command.return_value = """
a1b2c3d
feat(auth): Implement user login
Adds a new login flow.
---COMMIT-SEPARATOR---
e4f5g6h
fix: Resolve critical bug
Fixes issue #123.
---COMMIT-SEPARATOR---
i7j8k9l
docs: Update README
Improved installation instructions.
---COMMIT-SEPARATOR---
"""
        expected_changelog = """
## ✨ Features
- Implement user login (auth) (a1b2c3d)

## 🐛 Bug Fixes
- Resolve critical bug (e4f5g6h)

## 📝 Documentation
- Update README (i7j8k9l)
"""
        changelog = generate_changelog("v1.0.0", "HEAD")
        self.assertEqual(changelog.strip(), expected_changelog.strip())
        mock_run_git_command.assert_called_once_with(
            ["git", "log", "--pretty=format:%H%n%s%n%b%n---COMMIT-SEPARATOR---", "v1.0.0..HEAD"],
            cwd=None
        )

    @patch('quill.run_git_command')
    def test_generate_changelog_with_breaking_change(self, mock_run_git_command):
        # Mock rationale: Simulate git log output including a breaking change.
        mock_run_git_command.return_value = """
a1b2c3d
feat!: Introduce new API
This is the body.

BREAKING CHANGE: The old API is no longer supported.
---COMMIT-SEPARATOR---
e4f5g6h
fix: Resolve critical bug
---COMMIT-SEPARATOR---
"""
        expected_changelog = """
## 💥 Breaking Changes
- **Introduce new API** (a1b2c3d)
  The old API is no longer supported.

## ✨ Features
- Introduce new API (a1b2c3d)

## 🐛 Bug Fixes
- Resolve critical bug (e4f5g6h)
"""
        # Note: The breaking change commit will also appear under its type (feat)
        # This is standard for conventional changelogs.
        changelog = generate_changelog("v1.0.0", "HEAD")
        self.assertEqual(changelog.strip(), expected_changelog.strip())

    @patch('quill.run_git_command')
    def test_generate_changelog_empty(self, mock_run_git_command):
        # Mock rationale: Simulate no commits between references.
        mock_run_git_command.return_value = ""
        changelog = generate_changelog("v1.0.0", "HEAD")
        self.assertEqual(changelog.strip(), "")

    @patch('quill.run_git_command')
    def test_generate_changelog_git_error(self, mock_run_git_command):
        # Mock rationale: Simulate an error during git log execution.
        mock_run_git_command.side_effect = subprocess.CalledProcessError(
            returncode=128, cmd=["git", "log"], stderr="fatal: bad object v1.0.0"
        )
        changelog = generate_changelog("v1.0.0", "HEAD")
        self.assertEqual(changelog, "Error: Could not retrieve git history.")

    @patch('quill.run_git_command')
    def test_generate_changelog_mixed_types(self, mock_run_git_command):
        # Mock rationale: Simulate a mix of commit types to ensure correct grouping.
        mock_run_git_command.return_value = """
c1c1c1c
chore: Update dependencies
---COMMIT-SEPARATOR---
f2f2f2f
feat(ui): Add dark mode toggle
---COMMIT-SEPARATOR---
d3d3d3d
docs: Fix typo in contributing guide
---COMMIT-SEPARATOR---
p4p4p4p
perf: Optimize image loading
---COMMIT-SEPARATOR---
r5r5r5r
refactor: Simplify data fetching logic
---COMMIT-SEPARATOR---
"""
        expected_changelog = """
## ✨ Features
- Add dark mode toggle (ui) (f2f2f2f)

## 📝 Documentation
- Fix typo in contributing guide (d3d3d3d)

## ♻️ Refactors
- Simplify data fetching logic (r5r5r5r)

## ⚡ Performance Improvements
- Optimize image loading (p4p4p4p)

## 🧹 Chores
- Update dependencies to latest versions (c1c1c1c)
"""
        changelog = generate_changelog("start", "end")
        self.assertEqual(changelog.strip(), expected_changelog.strip())

    @patch('quill.run_git_command')
    def test_generate_changelog_with_other_commit_type(self, mock_run_git_command):
        # Mock rationale: Simulate a commit with an unrecognized type.
        mock_run_git_command.return_value = """
o1o1o1o
unknown: This is an unknown commit type
---COMMIT-SEPARATOR---
"""
        expected_changelog = """
## 🤷 Other Changes
- This is an unknown commit type (o1o1o1o)
"""
        changelog = generate_changelog("start", "end")
        self.assertEqual(changelog.strip(), expected_changelog.strip())

if __name__ == '__main__':
    unittest.main()
