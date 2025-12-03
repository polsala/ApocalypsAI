import unittest
from unittest.mock import patch, MagicMock
import os
import subprocess
from datetime import datetime, timedelta

# Adjust the path to import the module from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from git_glimpse import get_git_glimpse_summary, _run_git_command

class TestGitGlimpse(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('subprocess.run')
    def test_not_a_directory(self, mock_subprocess_run, mock_isdir):
        # Mock rationale: Simulate os.path.isdir returning False for a non-existent path.
        mock_isdir.return_value = False
        repo_path = "/non/existent/path"
        summary = get_git_glimpse_summary(repo_path)
        self.assertIn(f"Error: Repository path '{repo_path}' does not exist.", summary)
        mock_isdir.assert_called_once_with(repo_path)
        mock_subprocess_run.assert_not_called()

    @patch('os.path.isdir')
    @patch('subprocess.run')
    def test_not_a_git_repo(self, mock_subprocess_run, mock_isdir):
        # Mock rationale: Simulate os.path.isdir returning True, but 'git rev-parse' failing,
        # indicating it's not a Git repository.
        mock_isdir.return_value = True
        mock_subprocess_run.side_effect = [
            subprocess.CalledProcessError(128, ['git', 'rev-parse', '--is-inside-work-tree'], stderr="fatal: not a git repository"),
        ]
        repo_path = "/path/to/not/a/repo"
        summary = get_git_glimpse_summary(repo_path)
        self.assertIn(f"Error: '{repo_path}' is not a valid Git repository.", summary)
        mock_isdir.assert_called_once_with(repo_path)
        mock_subprocess_run.assert_called_once() # Only the initial check should run

    @patch('os.path.isdir')
    @patch('subprocess.run')
    def test_empty_repo_activity(self, mock_subprocess_run, mock_isdir):
        # Mock rationale: Simulate a valid Git repository with no commits or branches.
        mock_isdir.return_value = True
        mock_subprocess_run.side_effect = [
            # git rev-parse --is-inside-work-tree
            MagicMock(stdout="true", stderr="", returncode=0),
            # git rev-list --count HEAD (no commits yet)
            MagicMock(stdout="0", stderr="", returncode=0),
            # git log --pretty=format:%h %an %s --since=... (no recent commits)
            MagicMock(stdout="", stderr="", returncode=0),
            # git log --pretty=format:%an --since=... (no recent authors)
            MagicMock(stdout="", stderr="", returncode=0),
            # git branch --list --sort=-committerdate --format=... (no branches)
            MagicMock(stdout="", stderr="", returncode=0),
        ]
        repo_path = "/path/to/empty/repo"
        summary = get_git_glimpse_summary(repo_path)

        self.assertIn("Total Commits: 0", summary)
        self.assertIn("Recent Commits (last 7 days): 0", summary)
        self.assertIn("No recent commits.", summary)
        self.assertIn("Top Active Authors (last 7 days):", summary)
        self.assertIn("No active authors.", summary)
        self.assertIn("Recently Active Branches:", summary)
        self.assertIn("No branches found.", summary)
        self.assertEqual(mock_subprocess_run.call_count, 5)

    @patch('os.path.isdir')
    @patch('subprocess.run')
    def test_repo_with_activity(self, mock_subprocess_run, mock_isdir):
        # Mock rationale: Simulate a Git repository with various commits, authors, and branches
        # to test the parsing and summary generation logic.
        mock_isdir.return_value = True

        # Define mock outputs for git commands
        def mock_run_git_command(cmd, **kwargs):
            cmd_str = ' '.join(cmd)
            if 'rev-parse --is-inside-work-tree' in cmd_str:
                return MagicMock(stdout="true", stderr="", returncode=0)
            elif 'rev-list --count HEAD' in cmd_str:
                return MagicMock(stdout="100", stderr="", returncode=0)
            elif 'log --pretty=format:%h %an %s --since=' in cmd_str:
                return MagicMock(
                    stdout=(
                        "abcde1 Author One Commit message 1\n"
                        "fghij2 Author Two Commit message 2\n"
                        "klmno3 Author One Commit message 3\n"
                        "pqrst4 Author Three Commit message 4\n"
                        "uvwxy5 Author One Commit message 5\n"
                        "z12346 Author Two Commit message 6"
                    ),
                    stderr="", returncode=0
                )
            elif 'log --pretty=format:%an --since=' in cmd_str:
                return MagicMock(
                    stdout=(
                        "Author One\n"
                        "Author Two\n"
                        "Author One\n"
                        "Author Three\n"
                        "Author One\n"
                        "Author Two"
                    ),
                    stderr="", returncode=0
                )
            elif 'branch --list --sort=-committerdate --format=' in cmd_str:
                return MagicMock(
                    stdout=(
                        "main (last commit: 2 days ago)\n"
                        "feature/new-thing (last commit: 3 days ago)\n"
                        "bugfix/old-issue (last commit: 5 days ago)\n"
                        "stale-branch (last commit: 100 days ago)"
                    ),
                    stderr="", returncode=0
                )
            raise ValueError(f"Unexpected git command: {cmd_str}")

        mock_subprocess_run.side_effect = mock_run_git_command

        repo_path = "/path/to/active/repo"
        summary = get_git_glimpse_summary(repo_path, days=7, top_authors=2)

        self.assertIn("Total Commits: 100", summary)
        self.assertIn("Recent Commits (last 7 days): 6", summary)
        self.assertIn("abcde1 Author One Commit message 1", summary)
        self.assertIn("... and 1 more.", summary) # 6 commits, shows 5 + "... and 1 more"

        self.assertIn("Top Active Authors (last 7 days):", summary)
        self.assertIn("Author One (3 commits)", summary)
        self.assertIn("Author Two (2 commits)", summary)
        self.assertNotIn("Author Three", summary) # Only top 2 requested

        self.assertIn("Recently Active Branches:", summary)
        self.assertIn("main (last commit: 2 days ago)", summary)
        self.assertIn("feature/new-thing (last commit: 3 days ago)", summary)
        self.assertIn("bugfix/old-issue (last commit: 5 days ago)", summary)
        self.assertIn("... and 1 more.", summary) # 4 branches, shows 3 + "... and 1 more"

        # Check that subprocess.run was called for each expected git command
        self.assertEqual(mock_subprocess_run.call_count, 5) # rev-parse, rev-list, log (recent), log (authors), branch

    @patch('os.path.isdir')
    @patch('subprocess.run')
    def test_git_command_not_found(self, mock_subprocess_run, mock_isdir):
        # Mock rationale: Simulate 'git' command not being found in PATH.
        mock_isdir.return_value = True
        mock_subprocess_run.side_effect = FileNotFoundError("git not found")
        repo_path = "/path/to/repo"
        summary = get_git_glimpse_summary(repo_path)
        self.assertIn("Git command not found. Is Git installed and in your PATH?", summary)
        mock_isdir.assert_called_once_with(repo_path)
        mock_subprocess_run.assert_called_once() # Only the initial check should run

    @patch('os.path.isdir', return_value=True)
    @patch('subprocess.run')
    def test_run_git_command_failure(self, mock_subprocess_run, mock_isdir):
        # Mock rationale: Simulate a generic failure of a git command (e.g., bad arguments).
        mock_subprocess_run.side_effect = [
            MagicMock(stdout="true", stderr="", returncode=0), # Initial check passes
            subprocess.CalledProcessError(1, ['git', 'bad-command'], stderr="fatal: unknown command"),
        ]
        repo_path = "/path/to/repo"
        summary = get_git_glimpse_summary(repo_path)
        self.assertIn("Total Commits: N/A (Git command failed: git rev-list --count HEAD", summary)
        self.assertIn("fatal: unknown command", summary)
        self.assertEqual(mock_subprocess_run.call_count, 2) # Initial check + first command attempt
