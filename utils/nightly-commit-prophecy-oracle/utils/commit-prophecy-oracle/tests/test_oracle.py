import unittest
import subprocess
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the path for importing oracle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from oracle import get_commit_messages, divine_prophecy

class TestCommitProphecyOracle(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_commit_messages_success(self, mock_subprocess_run):
        # Mock rationale: Simulates successful 'git log' output without needing a real git repo.
        mock_subprocess_run.return_value = MagicMock(
            stdout="feat: Add new prophecy type\nfix: Correct typo in README\nchore: Update dependencies",
            stderr="",
            returncode=0
        )
        messages = get_commit_messages()
        self.assertEqual(len(messages), 3)
        self.assertIn("feat: Add new prophecy type", messages)
        mock_subprocess_run.assert_called_once_with(
            ['git', '-C', '.', 'log', '--oneline', '-n', '10', '--pretty=format:%s'],
            capture_output=True, text=True, check=True
        )

    @patch('subprocess.run')
    def test_get_commit_messages_empty(self, mock_subprocess_run):
        # Mock rationale: Simulates an empty 'git log' output.
        mock_subprocess_run.return_value = MagicMock(
            stdout="",
            stderr="",
            returncode=0
        )
        messages = get_commit_messages()
        self.assertEqual(len(messages), 0)

    @patch('subprocess.run')
    def test_get_commit_messages_git_error(self, mock_subprocess_run):
        # Mock rationale: Simulates a 'git log' command failing.
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'git log', stderr='fatal: not a git repository')
        messages = get_commit_messages()
        self.assertEqual(len(messages), 0)

    @patch('subprocess.run')
    def test_get_commit_messages_git_not_found(self, mock_subprocess_run):
        # Mock rationale: Simulates the 'git' command not being found.
        mock_subprocess_run.side_effect = FileNotFoundError
        messages = get_commit_messages()
        self.assertEqual(len(messages), 0)

    def test_divine_prophecy_empty_messages(self):
        prophecy = divine_prophecy([])
        self.assertIn("The scrolls are blank.", prophecy)

    def test_divine_prophecy_breaking_changes(self):
        messages = [
            "feat(api): Introduce breaking change for v2",
            "fix: Minor bug fix",
            "chore: Update docs"
        ]
        prophecy = divine_prophecy(messages)
        self.assertIn("A great upheaval is foretold!", prophecy)

    def test_divine_prophecy_bug_fixes(self):
        messages = [
            "fix: Critical security vulnerability",
            "bug: UI glitch on login",
            "fix: Database connection issue",
            "feat: New user profile page" # One feature, but fixes dominate
        ]
        prophecy = divine_prophecy(messages)
        self.assertIn("The spirits of past transgressions linger.", prophecy)

    def test_divine_prophecy_new_features(self):
        messages = [
            "feat: Implement dark mode",
            "feat: Add user registration flow",
            "feat: Integrate payment gateway",
            "fix: Small typo" # One fix, but features dominate
        ]
        prophecy = divine_prophecy(messages)
        self.assertIn("The winds of innovation blow strong!", prophecy)

    def test_divine_prophecy_refactoring(self):
        messages = [
            "refactor: Extract common utility functions",
            "clean: Remove dead code",
            "improve: Optimize database queries",
            "feat: Minor UI tweak" # One feature, but refactors dominate
        ]
        prophecy = divine_prophecy(messages)
        self.assertIn("The ancient texts speak of a great cleansing.", prophecy)

    def test_divine_prophecy_testing_docs_ci(self):
        messages = [
            "test: Add unit tests for new module",
            "ci: Update workflow for faster builds",
            "docs: Improve API documentation",
            "test: Fix flaky test"
        ]
        prophecy = divine_prophecy(messages)
        self.assertIn("The scribes and guardians are diligent!", prophecy)

    def test_divine_prophecy_chores_config(self):
        messages = [
            "chore: Update dependencies",
            "config: Adjust logging levels",
            "build: Upgrade webpack configuration",
            "feat: Small button change" # One feature, but chores dominate
        ]
        prophecy = divine_prophecy(messages)
        self.assertIn("The gears of the machine are being oiled and adjusted.", prophecy)

    def test_divine_prophecy_mixed_or_unclear(self):
        messages = [
            "Update README",
            "Adjust styling",
            "Small change",
            "Another minor update"
        ]
        prophecy = divine_prophecy(messages)
        self.assertIn("The cosmic energies are balanced, yet subtle.", prophecy)

    def test_divine_prophecy_mixed_with_some_keywords(self):
        messages = [
            "feat: Add new endpoint",
            "fix: Typo",
            "chore: Linting",
            "refactor: Rename variable"
        ]
        # This should fall into the 'mixed' category as no single type dominates >= 50%
        prophecy = divine_prophecy(messages)
        self.assertIn("The cosmic energies are balanced, yet subtle.", prophecy)
