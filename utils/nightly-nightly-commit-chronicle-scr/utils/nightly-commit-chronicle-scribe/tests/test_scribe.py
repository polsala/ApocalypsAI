import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import os
import subprocess

# Add the src directory to the Python path to allow importing scribe.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import scribe

class TestScribe(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = io.StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('subprocess.run')
    def test_run_git_log_success(self, mock_subprocess_run):
        # Mock rationale: Simulate a successful git log command without actual git execution.
        mock_subprocess_run.return_value = MagicMock(
            stdout='abcde12|John Doe|feat: Add new feature\n1234567|Jane Smith|fix: Fix bug\n',
            stderr='',
            returncode=0
        )
        output = scribe.run_git_log(count=2)
        self.assertIn('feat: Add new feature', output)
        mock_subprocess_run.assert_called_once_with(
            ['git', 'log', '--pretty=format:"%h|%an|%s"', '--no-merges', '-2'],
            capture_output=True, text=True, check=True, cwd=os.getcwd()
        )

    @patch('subprocess.run')
    def test_run_git_log_error(self, mock_subprocess_run):
        # Mock rationale: Simulate a failed git log command.
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'git log', stderr='fatal: not a git repository')
        output = scribe.run_git_log()
        self.assertEqual(output, "")
        self.assertIn("Error running git log", self.mock_stdout.getvalue())

    @patch('subprocess.run')
    def test_run_git_log_git_not_found(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git' command not being found.
        mock_subprocess_run.side_effect = FileNotFoundError
        output = scribe.run_git_log()
        self.assertEqual(output, "")
        self.assertIn("Error: 'git' command not found", self.mock_stdout.getvalue())

    def test_parse_commit_log(self):
        log_output = (
            'abcde12|John Doe|feat: Add new feature\n'
            '1234567|Jane Smith|fix: Fix bug\n'
            'fedcba9|Alice Wonderland|chore(deps): Update dependency\n'
            'invalid-line-format'
        )
        commits = scribe.parse_commit_log(log_output)
        self.assertEqual(len(commits), 3)
        self.assertEqual(commits[0]['hash'], 'abcde12')
        self.assertEqual(commits[0]['author'], 'John Doe')
        self.assertEqual(commits[0]['message'], 'feat: Add new feature')
        self.assertEqual(commits[2]['message'], 'chore(deps): Update dependency')

    def test_categorize_commits(self):
        commits = [
            {'hash': 'h1', 'author': 'A', 'message': 'feat: New awesome feature'},
            {'hash': 'h2', 'author': 'B', 'message': 'fix(scope): Resolve critical bug'},
            {'hash': 'h3', 'author': 'C', 'message': 'docs: Update installation guide'},
            {'hash': 'h4', 'author': 'D', 'message': 'chore: Clean up temporary files'},
            {'hash': 'h5', 'author': 'E', 'message': 'refactor: Improve performance of X'},
            {'hash': 'h6', 'author': 'F', 'message': 'Initial commit'},
            {'hash': 'h7', 'author': 'G', 'message': 'FEAT: Another feature (case insensitive)'},
        ]
        categorized = scribe.categorize_commits(commits)

        self.assertEqual(len(categorized['feat']['commits']), 2)
        self.assertEqual(categorized['feat']['commits'][0]['description'], 'New awesome feature')
        self.assertEqual(categorized['feat']['commits'][1]['description'], 'Another feature (case insensitive)')
        self.assertEqual(len(categorized['fix']['commits']), 1)
        self.assertEqual(categorized['fix']['commits'][0]['description'], 'Resolve critical bug')
        self.assertEqual(len(categorized['docs']['commits']), 1)
        self.assertEqual(len(categorized['chore']['commits']), 1)
        self.assertEqual(len(categorized['refactor']['commits']), 1)
        self.assertEqual(len(categorized['other']['commits']), 1)
        self.assertEqual(categorized['other']['commits'][0]['description'], 'Initial commit')

    def test_format_markdown_output(self):
        categorized = {
            'feat': {'title': '✨ Features', 'commits': [
                {'hash': 'h1', 'author': 'A', 'description': 'New feature'}
            ]},
            'fix': {'title': '🐛 Bug Fixes', 'commits': [
                {'hash': 'h2', 'author': 'B', 'description': 'Critical bug fix'}
            ]},
            'other': {'title': '📝 Other Changes', 'commits': [
                {'hash': 'h3', 'author': 'C', 'description': 'Miscellaneous change'}
            ]},
            'docs': {'title': '📚 Documentation', 'commits': []},
            'chore': {'title': '🧹 Chores', 'commits': []},
            'refactor': {'title': '🔨 Refactors', 'commits': []},
            'perf': {'title': '⚡ Performance', 'commits': []},
            'test': {'title': '🧪 Tests', 'commits': []},
            'build': {'title': '📦 Builds', 'commits': []},
            'ci': {'title': '⚙️ CI/CD', 'commits': []},
            'revert': {'title': '⏪ Reverts', 'commits': []},
            'style': {'title': '🎨 Styles', 'commits': []},
        }
        output = scribe.format_markdown_output(categorized)
        expected_output = (
            "# Commit Chronicle\n\n"
            "## ✨ Features\n"
            "*   `h1` (A) New feature\n\n"
            "## 🐛 Bug Fixes\n"
            "*   `h2` (B) Critical bug fix\n\n"
            "## 📝 Other Changes\n"
            "*   `h3` (C) Miscellaneous change\n\n"
        )
        self.assertEqual(output, expected_output)

    @patch('scribe.run_git_log')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_count(self, mock_parse_args, mock_run_git_log):
        # Mock rationale: Simulate command-line arguments and git log output for main function.
        mock_parse_args.return_value = MagicMock(count=1, since=None, until=None, format='markdown')
        mock_run_git_log.return_value = 'abcde12|John Doe|feat: First commit\n'

        scribe.main()
        self.assertIn("## ✨ Features", self.mock_stdout.getvalue())
        self.assertIn("First commit", self.mock_stdout.getvalue())
        mock_run_git_log.assert_called_once_with(count=1, since=None, until=None)

    @patch('scribe.run_git_log')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_since_date(self, mock_parse_args, mock_run_git_log):
        # Mock rationale: Simulate command-line arguments and git log output for main function.
        mock_parse_args.return_value = MagicMock(count=10, since='2023-01-01', until=None, format='markdown')
        mock_run_git_log.return_value = 'abcde12|John Doe|feat: Commit since date\n'

        scribe.main()
        self.assertIn("## ✨ Features", self.mock_stdout.getvalue())
        self.assertIn("Commit since date", self.mock_stdout.getvalue())
        mock_run_git_log.assert_called_once_with(count=10, since='2023-01-01', until=None)

    @patch('scribe.run_git_log')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_commits(self, mock_parse_args, mock_run_git_log):
        # Mock rationale: Simulate no commits returned by git log.
        mock_parse_args.return_value = MagicMock(count=10, since=None, until=None, format='markdown')
        mock_run_git_log.return_value = '' # Empty log output

        scribe.main()
        self.assertIn("No git log output or an error occurred.", self.mock_stdout.getvalue())

    @patch('scribe.run_git_log')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_since_date(self, mock_parse_args, mock_run_git_log):
        # Mock rationale: Simulate invalid date format for --since argument.
        mock_parse_args.return_value = MagicMock(count=10, since='2023/01/01', until=None, format='markdown')

        scribe.main()
        self.assertIn("Error: --since date must be in YYYY-MM-DD format.", self.mock_stdout.getvalue())
        mock_run_git_log.assert_not_called()

    @patch('scribe.run_git_log')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_until_date(self, mock_parse_args, mock_run_git_log):
        # Mock rationale: Simulate invalid date format for --until argument.
        mock_parse_args.return_value = MagicMock(count=10, since=None, until='01-01-2023', format='markdown')

        scribe.main()
        self.assertIn("Error: --until date must be in YYYY-MM-DD format.", self.mock_stdout.getvalue())
        mock_run_git_log.assert_not_called()
