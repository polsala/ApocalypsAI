import unittest
from unittest.mock import patch, MagicMock
import json
import os
from io import StringIO
import sys

# Adjust sys.path to allow importing from src/ for testing
# This assumes the test is run from the `repo-mood-ring` directory or its parent.
# For the purpose of generating the JSON, this setup is illustrative.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, os.path.join(project_root, 'src'))

from mood_ring import get_commit_messages, analyze_mood, main

class TestRepoMoodRing(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_commit_messages_success(self, mock_subprocess_run):
        # Mock rationale: Simulate successful `git log` command output with multiple commit messages.
        mock_subprocess_run.return_value = MagicMock(
            stdout="feat: Add new feature\nfix: Resolve critical bug\nchore: Update dependencies",
            stderr="",
            returncode=0
        )
        
        messages = get_commit_messages("/fake/repo")
        self.assertEqual(len(messages), 3)
        self.assertIn("feat: Add new feature", messages)
        mock_subprocess_run.assert_called_once()

    @patch('subprocess.run')
    def test_get_commit_messages_no_commits(self, mock_subprocess_run):
        # Mock rationale: Simulate `git log` returning no output (e.g., empty repo or no commits).
        mock_subprocess_run.return_value = MagicMock(
            stdout="", # Empty stdout means no commits
            stderr="",
            returncode=0
        )
        
        messages = get_commit_messages("/fake/repo")
        self.assertEqual(messages, [])
        mock_subprocess_run.assert_called_once()

    @patch('builtins.print') # Mock print to capture output
    @patch('subprocess.run')
    def test_get_commit_messages_error(self, mock_subprocess_run, mock_print):
        # Mock rationale: Simulate `git log` command failing (e.g., not a git repository, or git not installed).
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(128, ['git', 'log'], stderr="fatal: not a git repository")
        
        messages = get_commit_messages("/fake/repo")
        self.assertEqual(messages, [])
        mock_print.assert_called_once() # Check if error message was printed

    @patch('builtins.print') # Mock print to capture output
    @patch('subprocess.run', side_effect=FileNotFoundError) # Mock rationale: Simulate git command not found.
    def test_get_commit_messages_git_not_found(self, mock_subprocess_run, mock_print):
        messages = get_commit_messages("/fake/repo")
        self.assertEqual(messages, [])
        mock_print.assert_called_once_with("Git command not found. Please ensure Git is installed and in your PATH.")

    def test_analyze_mood_joyful(self):
        messages = [
            "feat: Add awesome new feature 🎉",
            "improve: Performance boost",
            "refactor: Clean up old code for better readability",
            "docs: Update README"
        ]
        mood, summary = analyze_mood(messages)
        self.assertEqual(mood, "Joyful/Optimistic")
        self.assertIn("vibrant glow", summary)

    def test_analyze_mood_stressed(self):
        messages = [
            "fix(critical): Database connection error",
            "urgent: Hotfix for production bug",
            "bug: Login broken on mobile",
            "chore: Update dependencies" # Neutral, but stressed should dominate
        ]
        mood, summary = analyze_mood(messages)
        self.assertEqual(mood, "Stressed/Urgent")
        self.assertIn("flickering red light", summary)

    def test_analyze_mood_calm(self):
        messages = [
            "docs: Add comprehensive API documentation",
            "chore: Linting fixes",
            "style: Format code with black",
            "test: Add unit tests for new module"
        ]
        mood, summary = analyze_mood(messages)
        self.assertEqual(mood, "Calm/Steady")
        self.assertIn("serene blue hue", summary)

    def test_analyze_mood_confused(self):
        messages = [
            "wip: Experimenting with new authentication flow",
            "question: How to handle edge cases in parser?",
            "explore: Investigate alternative database solutions",
            "feat: Initial setup" # Positive, but confused should dominate
        ]
        mood, summary = analyze_mood(messages)
        self.assertEqual(mood, "Confused/Uncertain")
        self.assertIn("swirling grey mist", summary)

    def test_analyze_mood_neutral(self):
        messages = [
            "chore: Update build script",
            "docs: Fix typo in CONTRIBUTING.md",
            "build: Bump version to 1.0.1"
        ]
        mood, summary = analyze_mood(messages)
        self.assertEqual(mood, "Neutral/Routine")
        self.assertIn("gentle hum", summary)

    def test_analyze_mood_empty_messages(self):
        mood, summary = analyze_mood([])
        self.assertEqual(mood, "Mysterious (No recent commits)")
        self.assertIn("blank slate", summary)

    @patch('os.path.isdir')
    @patch('subprocess.run')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_success(self, mock_stdout, mock_subprocess_run, mock_isdir):
        # Mock rationale: Simulate a valid Git repository and successful commit log retrieval.
        # os.path.isdir is called twice: once for the repo_path itself, once for repo_path/.git
        mock_isdir.side_effect = [True, True] 
        mock_subprocess_run.return_value = MagicMock(
            stdout="feat: Implement new feature\nchore: Update docs",
            stderr="",
            returncode=0
        )

        # Mock argparse.ArgumentParser.parse_args to control CLI arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(repo_path="/fake/repo", num_commits=2)):
            main()
            output = json.loads(mock_stdout.getvalue())
            self.assertEqual(output["mood"], "Joyful/Optimistic")
            self.assertIn("vibrant glow", output["summary"])
            self.assertEqual(output["analyzed_commits"], 2)
            mock_subprocess_run.assert_called_once()
            self.assertEqual(mock_isdir.call_count, 2) # For repo_path and .git check

    @patch('sys.exit') # Mock sys.exit to prevent actual program termination during test
    @patch('os.path.isdir')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_invalid_repo_path(self, mock_stdout, mock_isdir, mock_exit):
        # Mock rationale: Simulate an invalid repository path that does not exist.
        mock_isdir.return_value = False # First call for repo_path returns False
        
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(repo_path="/nonexistent/repo", num_commits=50)):
            main()
            self.assertIn("Error: Repository path '/nonexistent/repo' does not exist or is not a directory.", mock_stdout.getvalue())
            mock_exit.assert_called_once_with(1)

    @patch('sys.exit') # Mock sys.exit to prevent actual program termination during test
    @patch('os.path.isdir')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_not_git_repo(self, mock_stdout, mock_isdir, mock_exit):
        # Mock rationale: Simulate a directory that exists but is not a Git repository.
        mock_isdir.side_effect = [True, False] # First call for repo_path is True, second for .git is False
        
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(repo_path="/valid/dir", num_commits=50)):
            main()
            self.assertIn("Error: '/valid/dir' is not a Git repository.", mock_stdout.getvalue())
            mock_exit.assert_called_once_with(1)

    @patch('sys.exit')
    @patch('os.path.isdir', return_value=True)
    @patch('subprocess.run')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_git_command_error(self, mock_stdout, mock_subprocess_run, mock_isdir, mock_exit):
        # Mock rationale: Simulate an error when running the git command (e.g., corrupted repo).
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(128, ['git', 'log'], stderr="fatal: bad default revision 'HEAD'")
        
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(repo_path="/fake/repo", num_commits=50)):
            main()
            output = json.loads(mock_stdout.getvalue())
            self.assertEqual(output["mood"], "Mysterious (No recent commits)")
            self.assertEqual(output["analyzed_commits"], 0)
            mock_exit.assert_not_called() # Should not exit(1) for git command errors, just report mysterious mood
