import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import sys
import subprocess

# Mock rationale: This allows the test to import storyteller.py as if it were a package.
# It ensures that the 'src' directory is in the Python path for module resolution.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from storyteller import get_git_log, parse_commit_line, generate_story, is_git_repository, main

class TestStoryteller(unittest.TestCase):

    # Mock rationale: We don't want to actually run git commands during tests.
    # This mock simulates the output of `git log`.
    @patch('subprocess.run')
    def test_get_git_log_success(self, mock_subprocess_run):
        mock_result = MagicMock()
        mock_result.stdout = (
            '"a1b2c3d|Alice|2023-01-01 10:00:00 +0000|Initial commit"\n' +
            '"e4f5g6h|Bob|2023-01-02 11:00:00 +0000|feat: Add new feature"\n' +
            '"i7j8k9l|Alice|2023-01-03 12:00:00 +0000|fix: Bug squashed"'
        )
        mock_result.stderr = ''
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        log_lines = get_git_log()
        self.assertEqual(len(log_lines), 3)
        self.assertEqual(log_lines[0], 'a1b2c3d|Alice|2023-01-01 10:00:00 +0000|Initial commit')
        mock_subprocess_run.assert_called_once()

    # Mock rationale: Simulate a scenario where git command fails (e.g., not a git repository).
    @patch('subprocess.run')
    def test_get_git_log_failure(self, mock_subprocess_run):
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'git log', stderr='fatal: not a git repository')
        with self.assertRaisesRegex(RuntimeError, "Error fetching git log: fatal: not a git repository"):
            get_git_log()

    # Mock rationale: Simulate a scenario where the 'git' executable is not found in PATH.
    @patch('subprocess.run')
    def test_get_git_log_git_not_found(self, mock_subprocess_run):
        mock_subprocess_run.side_effect = FileNotFoundError()
        with self.assertRaisesRegex(FileNotFoundError, "Error: 'git' command not found"):
            get_git_log()

    def test_parse_commit_line_valid(self):
        line = 'a1b2c3d|Alice|2023-01-01 10:00:00 +0000|Initial commit'
        commit = parse_commit_line(line)
        self.assertIsNotNone(commit)
        self.assertEqual(commit['hash'], 'a1b2c3d')
        self.assertEqual(commit['author'], 'Alice')
        self.assertEqual(commit['date'], datetime.datetime(2023, 1, 1, 10, 0, 0))
        self.assertEqual(commit['subject'], 'Initial commit')

    def test_parse_commit_line_malformed(self):
        self.assertIsNone(parse_commit_line('a1b2c3d|Alice|Invalid Date|Subject'))
        self.assertIsNone(parse_commit_line('a1b2c3d|Alice|2023-01-01')) # Not enough parts
        self.assertIsNone(parse_commit_line('a1b2c3d|Alice|2023-01-01 10:00:00 +0000')) # Missing subject

    def test_generate_story_empty_commits(self):
        story = generate_story([])
        self.assertEqual(story, "The repository is a blank scroll, awaiting its first tale. No commits have been made yet.")

    def test_generate_story_single_commit(self):
        commits = [
            {
                'hash': 'a1b2c3d',
                'author': 'Alice',
                'date': datetime.datetime(2023, 1, 1, 10, 0, 0),
                'subject': 'Initial commit'
            }
        ]
        story = generate_story(commits)
        self.assertIn("a new saga began on 2023-01-01", story)
        self.assertIn("first whisper of creation was 'Initial commit', penned by the legendary Alice.", story)
        self.assertIn("This grand endeavor was meticulously crafted by a single visionary, Alice, who cast 1 spells upon it.", story)

    def test_generate_story_multiple_commits(self):
        commits = [
            {
                'hash': 'a1b2c3d',
                'author': 'Alice',
                'date': datetime.datetime(2023, 1, 1, 10, 0, 0),
                'subject': 'Initial commit'
            },
            {
                'hash': 'e4f5g6h',
                'author': 'Bob',
                'date': datetime.datetime(2023, 1, 2, 11, 0, 0),
                'subject': 'feat: Add new feature'
            },
            {
                'hash': 'i7j8k9l',
                'author': 'Alice',
                'date': datetime.datetime(2023, 1, 3, 12, 0, 0),
                'subject': 'fix: Bug squashed'
            },
            {
                'hash': 'm0n1o2p',
                'author': 'Charlie',
                'date': datetime.datetime(2023, 1, 4, 13, 0, 0),
                'subject': 'docs: Update README'
            }
        ]
        story = generate_story(commits)
        self.assertIn("a new saga began on 2023-01-01", story)
        self.assertIn("Over a span of 3 days, 4 magical incantations (commits) were cast upon this project.", story)
        self.assertIn("A fellowship of 3 brave souls contributed to this epic.", story)
        self.assertIn("The most prolific among them, with 2 contributions, was none other than Alice!", story)
        self.assertIn("feat: Add new feature", story)
        self.assertIn("fix: Bug squashed", story)
        self.assertIn("docs: Update README", story)
        self.assertIn("The latest chapter, 'docs: Update README', was sealed on 2023-01-04 by Charlie.", story)

    # Mock rationale: We need to mock subprocess.run to control the output of `git rev-parse`.
    def test_is_git_repository_true(self):
        with patch('subprocess.run') as mock_subprocess_run:
            mock_subprocess_run.return_value = MagicMock(stdout='true\n', stderr='', returncode=0)
            self.assertTrue(is_git_repository('.'))
            mock_subprocess_run.assert_called_once_with(['git', '-C', '.', 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True, check=True)

    # Mock rationale: Simulate `git rev-parse` failing, indicating not a git repo.
    def test_is_git_repository_false(self):
        with patch('subprocess.run') as mock_subprocess_run:
            mock_subprocess_run.side_effect = subprocess.CalledProcessError(128, 'git rev-parse', stderr='fatal: not a git repository')
            self.assertFalse(is_git_repository('.'))

    # Mock rationale: Simulate 'git' command not found for `is_git_repository`.
    def test_is_git_repository_git_not_found(self):
        with patch('subprocess.run') as mock_subprocess_run:
            mock_subprocess_run.side_effect = FileNotFoundError()
            with self.assertRaisesRegex(FileNotFoundError, "Error: 'git' command not found"):
                is_git_repository('.')

    # Mock rationale: We need to mock os.getcwd and subprocess.run for the main function
    # to prevent actual file system and git operations during testing. Also mock print.
    @patch('os.getcwd', return_value='/mock/repo')
    @patch('subprocess.run')
    @patch('builtins.print') # Mock print to capture output
    def test_main_success(self, mock_print, mock_subprocess_run, mock_getcwd):
        # Mock subprocess.run for is_git_repository and get_git_log calls
        mock_subprocess_run.side_effect = [
            MagicMock(stdout='true\n', stderr='', returncode=0), # For 'git rev-parse'
            MagicMock(stdout=(
                '"a1b2c3d|Alice|2023-01-01 10:00:00 +0000|Initial commit"\n' +
                '"e4f5g6h|Bob|2023-01-02 11:00:00 +0000|feat: Add new feature"'
            ), stderr='', returncode=0) # For 'git log'
        ]

        main()

        mock_print.assert_called_once()
        output = mock_print.call_args[0][0]
        self.assertIn("a new saga began on 2023-01-01", output)
        self.assertIn("Over a span of 1 days, 2 magical incantations (commits) were cast upon this project.", output)
        self.assertIn("A fellowship of 2 brave souls contributed to this epic.", output)

    @patch('os.getcwd', return_value='/mock/repo')
    @patch('subprocess.run')
    @patch('builtins.print')
    def test_main_not_git_repo(self, mock_print, mock_subprocess_run, mock_getcwd):
        # Mock git rev-parse to fail, indicating not a git repo
        mock_subprocess_run.return_value = MagicMock(stdout='', stderr='fatal: not a git repository', returncode=128) # For 'git rev-parse'

        main()

        mock_print.assert_called_once_with("Error: '/mock/repo' is not a git repository.")

    @patch('os.getcwd', return_value='/mock/repo')
    @patch('subprocess.run')
    @patch('builtins.print')
    def test_main_git_not_found(self, mock_print, mock_subprocess_run, mock_getcwd):
        # Mock git rev-parse to raise FileNotFoundError
        mock_subprocess_run.side_effect = FileNotFoundError()

        main()

        mock_print.assert_called_once_with("Error: 'git' command not found. Please ensure Git is installed and in your PATH.")

if __name__ == '__main__':
    unittest.main()
