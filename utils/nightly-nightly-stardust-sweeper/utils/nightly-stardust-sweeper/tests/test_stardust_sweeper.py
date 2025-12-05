import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import sys

# Add the src directory to the path to allow importing stardust_sweeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import stardust_sweeper

class TestStardustSweeper(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Control the 'current' time for deterministic tests.
        self.mock_now = datetime.datetime(2024, 1, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)
        self.patcher_now = patch('datetime.datetime', autospec=True)
        self.mock_datetime = self.patcher_now.start()
        self.mock_datetime.now.return_value = self.mock_now
        # Ensure other datetime methods are not mocked out
        self.mock_datetime.fromisoformat = datetime.datetime.fromisoformat
        self.mock_datetime.timedelta = datetime.timedelta
        self.mock_datetime.timezone = datetime.timezone

        # Mock rationale: Simulate the existence of a .git directory for repository validation.
        self.patcher_isdir = patch('os.path.isdir')
        self.mock_isdir = self.patcher_isdir.start()
        self.mock_isdir.return_value = True # Assume .git directory exists by default

    def tearDown(self):
        self.patcher_now.stop()
        self.patcher_isdir.stop()

    @patch('subprocess.run')
    def test_get_all_local_branches(self, mock_run):
        # Mock rationale: Simulate git command output for listing branches.
        mock_run.return_value = MagicMock(
            stdout="main\nfeature/new-thing\nbugfix/old-bug\n",
            stderr="",
            returncode=0
        )
        repo_path = "/mock/repo"
        branches = stardust_sweeper.get_all_local_branches(repo_path)
        self.assertEqual(branches, ["main", "feature/new-thing", "bugfix/old-bug"])
        mock_run.assert_called_once_with(
            ['git', '-C', repo_path, 'branch', '--format=%(refname:short)'],
            capture_output=True, text=True, check=True
        )

    @patch('subprocess.run')
    def test_get_last_commit_date(self, mock_run):
        # Mock rationale: Simulate git command output for a branch's last commit date.
        mock_run.return_value = MagicMock(
            stdout="2023-12-01T10:00:00+00:00\n",
            stderr="",
            returncode=0
        )
        repo_path = "/mock/repo"
        branch_name = "main"
        commit_date = stardust_sweeper.get_last_commit_date(repo_path, branch_name)
        expected_date = datetime.datetime(2023, 12, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
        self.assertEqual(commit_date, expected_date)
        mock_run.assert_called_once_with(
            ['git', '-C', repo_path, 'log', '-1', '--format=%cd', '--date=iso-strict', branch_name],
            capture_output=True, text=True, check=True
        )

    @patch('subprocess.run')
    def test_find_stale_branches_no_stale(self, mock_run):
        # Mock rationale: Simulate git commands where all branches are recent.
        # Mock `get_all_local_branches` and `get_last_commit_date` behavior via side_effect.
        def mock_git_command(cmd_args, **kwargs):
            if 'branch' in cmd_args:
                return MagicMock(stdout="main\nfeature/recent\n", stderr="", returncode=0)
            elif 'log' in cmd_args:
                branch_name = cmd_args[-1]
                if branch_name == "main":
                    return MagicMock(stdout="2024-01-10T10:00:00+00:00\n", stderr="", returncode=0) # 5 days old
                elif branch_name == "feature/recent":
                    return MagicMock(stdout="2024-01-05T10:00:00+00:00\n", stderr="", returncode=0) # 10 days old
            return MagicMock(stdout="", stderr="Unknown command", returncode=1)

        mock_run.side_effect = mock_git_command

        repo_path = "/mock/repo"
        days_threshold = 30 # Current date is Jan 15, 2024. Threshold is Dec 16, 2023.
        stale_branches = stardust_sweeper.find_stale_branches(repo_path, days_threshold)
        self.assertEqual(stale_branches, {})

    @patch('subprocess.run')
    def test_find_stale_branches_with_stale(self, mock_run):
        # Mock rationale: Simulate git commands where some branches are stale.
        def mock_git_command(cmd_args, **kwargs):
            if 'branch' in cmd_args:
                return MagicMock(stdout="main\nfeature/recent\nbugfix/stale-one\nfeature/very-old\n", stderr="", returncode=0)
            elif 'log' in cmd_args:
                branch_name = cmd_args[-1]
                if branch_name == "main":
                    return MagicMock(stdout="2024-01-10T10:00:00+00:00\n", stderr="", returncode=0) # 5 days old
                elif branch_name == "feature/recent":
                    return MagicMock(stdout="2024-01-05T10:00:00+00:00\n", stderr="", returncode=0) # 10 days old
                elif branch_name == "bugfix/stale-one":
                    return MagicMock(stdout="2023-11-01T10:00:00+00:00\n", stderr="", returncode=0) # ~75 days old
                elif branch_name == "feature/very-old":
                    return MagicMock(stdout="2023-08-01T10:00:00+00:00\n", stderr="", returncode=0) # ~167 days old
            return MagicMock(stdout="", stderr="Unknown command", returncode=1)

        mock_run.side_effect = mock_git_command

        repo_path = "/mock/repo"
        days_threshold = 60 # Current date is Jan 15, 2024. Threshold is Nov 16, 2023.
        stale_branches = stardust_sweeper.find_stale_branches(repo_path, days_threshold)

        expected_stale = {
            "bugfix/stale-one": datetime.datetime(2023, 11, 1, 10, 0, 0, tzinfo=datetime.timezone.utc),
            "feature/very-old": datetime.datetime(2023, 8, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
        }
        self.assertEqual(stale_branches, expected_stale)

    @patch('subprocess.run')
    def test_find_stale_branches_git_error(self, mock_run):
        # Mock rationale: Simulate a git command failing due to a CalledProcessError.
        mock_run.side_effect = subprocess.CalledProcessError(128, ['git', 'branch'], stderr="fatal: not a git repository")
        self.mock_isdir.side_effect = [True, True] # First for repo_path, second for .git

        repo_path = "/mock/repo"
        days_threshold = 30
        with self.assertRaises(subprocess.CalledProcessError):
            stardust_sweeper.find_stale_branches(repo_path, days_threshold)

    def test_find_stale_branches_invalid_repo_path(self):
        # Mock rationale: Simulate a non-existent or non-git directory by controlling os.path.isdir.
        self.mock_isdir.side_effect = [False, False] # Simulate repo_path not being a directory

        repo_path = "/not/a/repo"
        days_threshold = 30
        with self.assertRaisesRegex(ValueError, "is not a valid Git repository"):
            stardust_sweeper.find_stale_branches(repo_path, days_threshold)

    @patch('stardust_sweeper.find_stale_branches')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_stale_branches(self, mock_parse_args, mock_print, mock_find_stale_branches):
        # Mock rationale: Simulate the main function's execution path when no stale branches are found.
        mock_parse_args.return_value = MagicMock(repo='.', days=90)
        mock_find_stale_branches.return_value = {}

        stardust_sweeper.main()

        mock_find_stale_branches.assert_called_once_with('.', 90)
        # Check for the "sparkling clean" message
        self.assertTrue(any("sparkling clean" in call.args[0] for call in mock_print.call_args_list))


    @patch('stardust_sweeper.find_stale_branches')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_stale_branches(self, mock_parse_args, mock_print, mock_find_stale_branches):
        # Mock rationale: Simulate the main function's execution path when stale branches are found.
        mock_parse_args.return_value = MagicMock(repo='/mock/repo', days=60)
        stale_date_1 = datetime.datetime(2023, 11, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
        stale_date_2 = datetime.datetime(2023, 8, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
        mock_find_stale_branches.return_value = {
            "bugfix/stale-one": stale_date_1,
            "feature/very-old": stale_date_2
        }

        stardust_sweeper.main()

        mock_find_stale_branches.assert_called_once_with('/mock/repo', 60)
        # Check for the "Stardust Sweeper Report" message and specific branch names
        self.assertTrue(any("Stardust Sweeper Report" in call.args[0] for call in mock_print.call_args_list))
        self.assertTrue(any("bugfix/stale-one" in call.args[0] for call in mock_print.call_args_list))
        self.assertTrue(any("feature/very-old" in call.args[0] for call in mock_print.call_args_list))

    @patch('stardust_sweeper.find_stale_branches')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_value_error(self, mock_exit, mock_parse_args, mock_print, mock_find_stale_branches):
        # Mock rationale: Simulate a ValueError during execution (e.g., invalid repo path).
        mock_parse_args.return_value = MagicMock(repo='/invalid/repo', days=90)
        mock_find_stale_branches.side_effect = ValueError("'/invalid/repo' is not a valid Git repository.")

        stardust_sweeper.main()

        mock_print.assert_any_call("Error: '/invalid/repo' is not a valid Git repository.")
        mock_exit.assert_called_once_with(1)

    @patch('stardust_sweeper.find_stale_branches')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_unexpected_error(self, mock_exit, mock_parse_args, mock_print, mock_find_stale_branches):
        # Mock rationale: Simulate an unexpected error during execution.
        mock_parse_args.return_value = MagicMock(repo='.', days=90)
        mock_find_stale_branches.side_effect = Exception("Something went wrong!")

        stardust_sweeper.main()

        mock_print.assert_any_call("An unexpected error occurred: Something went wrong!")
        mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
