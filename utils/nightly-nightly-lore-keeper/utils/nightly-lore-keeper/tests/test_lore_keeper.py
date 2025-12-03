import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import subprocess
from src.lore_keeper import get_recent_commit_messages, parse_commit_message, check_commit_message, main

class TestLoreKeeper(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_recent_commit_messages_success(self, mock_subprocess_run):
        # Mock rationale: Simulate successful 'git log' command output for testing.
        mock_subprocess_run.return_value = MagicMock(
            stdout="feat: Add new feature\n\nThis is the body.\x00fix: Fix a bug\x00",
            stderr="",
            returncode=0
        )
        messages = get_recent_commit_messages(2)
        self.assertEqual(len(messages), 2)
        self.assertIn("feat: Add new feature\n\nThis is the body.", messages)
        self.assertIn("fix: Fix a bug", messages)
        mock_subprocess_run.assert_called_once_with(
            ['git', 'log', '-n2', '--no-merges', '--pretty=format:%B%x00'],
            capture_output=True, text=True, check=True, encoding='utf-8'
        )

    @patch('subprocess.run')
    def test_get_recent_commit_messages_no_commits(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git log' returning no commits (only the null byte separator).
        mock_subprocess_run.return_value = MagicMock(
            stdout="\x00", # Only the separator, meaning no actual messages
            stderr="",
            returncode=0
        )
        messages = get_recent_commit_messages(1)
        self.assertEqual(len(messages), 0)

    @patch('subprocess.run')
    def test_get_recent_commit_messages_git_not_found(self, mock_subprocess_run):
        # Mock rationale: Simulate Git not being installed or in PATH by raising FileNotFoundError.
        mock_subprocess_run.side_effect = FileNotFoundError
        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            messages = get_recent_commit_messages(1)
            self.assertEqual(len(messages), 0)
            self.assertIn("Git command not found", mock_stderr.getvalue())

    @patch('subprocess.run')
    def test_get_recent_commit_messages_git_error(self, mock_subprocess_run):
        # Mock rationale: Simulate a Git command error (e.g., bad arguments) by raising CalledProcessError.
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=128, cmd=['git', 'log'], stderr="fatal: bad object"
        )
        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            messages = get_recent_commit_messages(1)
            self.assertEqual(len(messages), 0)
            self.assertIn("Error running git command", mock_stderr.getvalue())
            self.assertIn("fatal: bad object", mock_stderr.getvalue())

    def test_parse_commit_message_with_body(self):
        raw_msg = "feat: Implement new login flow\n\nThis commit introduces a new login flow with OAuth2 support."
        parsed = parse_commit_message(raw_msg)
        self.assertEqual(parsed['subject'], "feat: Implement new login flow")
        self.assertEqual(parsed['body'], "This commit introduces a new login flow with OAuth2 support.")

    def test_parse_commit_message_no_body(self):
        raw_msg = "fix: Correct typo"
        parsed = parse_commit_message(raw_msg)
        self.assertEqual(parsed['subject'], "fix: Correct typo")
        self.assertEqual(parsed['body'], "")

    def test_check_commit_message_all_good(self):
        commit_data = {
            'subject': "feat: Add user profile page",
            'body': "This adds a new page for users to view and edit their profiles.",
            'raw': "..."
        }
        config = {
            'max_subject_length': 72,
            'conventional_commit_prefixes': ['feat:', 'fix:'],
            'min_body_length': 10,
            'require_body_for_short_subject': False
        }
        violations = check_commit_message(commit_data, config)
        self.assertEqual(violations, [])

    def test_check_commit_message_long_subject(self):
        commit_data = {
            'subject': "feat: This is a very very very very very very very very very very very very very very very very very long subject line that exceeds the limit",
            'body': "Some body.",
            'raw': "..."
        }
        config = {
            'max_subject_length': 72,
            'conventional_commit_prefixes': ['feat:'],
            'min_body_length': 0,
            'require_body_for_short_subject': False
        }
        violations = check_commit_message(commit_data, config)
        self.assertIn("Subject line exceeds 72 characters", violations[0])

    def test_check_commit_message_missing_prefix(self):
        commit_data = {
            'subject': "Add user profile page",
            'body': "Some body.",
            'raw': "..."
        }
        config = {
            'max_subject_length': 72,
            'conventional_commit_prefixes': ['feat:', 'fix:'],
            'min_body_length': 0,
            'require_body_for_short_subject': False
        }
        violations = check_commit_message(commit_data, config)
        self.assertIn("Subject line does not follow conventional commit format", violations[0])

    def test_check_commit_message_short_body_required(self):
        commit_data = {
            'subject': "feat: Short subject",
            'body': "short",
            'raw': "..."
        }
        config = {
            'max_subject_length': 72,
            'conventional_commit_prefixes': ['feat:'],
            'min_body_length': 10,
            'require_body_for_short_subject': False
        }
        violations = check_commit_message(commit_data, config)
        self.assertIn("Commit body is too short", violations[0])

    def test_check_commit_message_require_body_for_short_subject(self):
        commit_data = {
            'subject': "feat: Short subject", # Length < 20
            'body': "",
            'raw': "..."
        }
        config = {
            'max_subject_length': 72,
            'conventional_commit_prefixes': ['feat:'],
            'min_body_length': 0,
            'require_body_for_short_subject': True
        }
        violations = check_commit_message(commit_data, config)
        self.assertIn("Commit body is required for short subject lines", violations[0])

    @patch('src.lore_keeper.get_recent_commit_messages')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_success(self, mock_stderr, mock_stdout, mock_get_commits):
        # Mock rationale: Simulate a scenario where all commits are valid according to default rules.
        mock_get_commits.return_value = [
            "feat: Add new feature\n\nThis is a good body.",
            "fix: Resolve critical bug",
            "docs: Update README"
        ]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("All recent commit messages adhere to the lore.", mock_stdout.getvalue())
        self.assertNotIn("VIOLATION", mock_stdout.getvalue())

    @patch('src.lore_keeper.get_recent_commit_messages')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_failure_with_violations(self, mock_stderr, mock_stdout, mock_get_commits):
        # Mock rationale: Simulate a scenario with commit message violations to trigger exit code 1.
        mock_get_commits.return_value = [
            "feat: This is a very very very very very very very very very very very very very very very very very long subject line that exceeds the limit",
            "Missing prefix: Add feature", # Missing conventional commit prefix
            "fix: Another good commit",
            "chore: Yet another good commit"
        ]
        # Default config for main() has require_body_for_short_subject=False, min_body_length=0
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        output = mock_stdout.getvalue()
        self.assertIn("Subject line exceeds 72 characters", output)
        self.assertIn("Subject line does not follow conventional commit format", output)
        self.assertIn("Lore Keeper detected 2 commit message violations.", output)

    @patch('src.lore_keeper.get_recent_commit_messages')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_no_commits_found(self, mock_stderr, mock_stdout, mock_get_commits):
        # Mock rationale: Simulate no commits being found by get_recent_commit_messages to trigger exit code 2.
        mock_get_commits.return_value = []
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2) # No-op
        self.assertIn("No commit messages found or unable to retrieve them.", mock_stdout.getvalue())
