import unittest
from unittest.mock import patch, MagicMock
import datetime
import sys
import io
import subprocess

# Add src directory to Python path for importing the module under test
sys.path.append('utils/nightly-git-gremlin-branch-purger/src')
import gremlin

class TestGitGremlin(unittest.TestCase):

    def setUp(self):
        # Capture stdout/stderr for testing print statements
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        self.new_stdout = io.StringIO()
        self.new_stderr = io.StringIO()
        sys.stdout = self.new_stdout
        sys.stderr = self.new_stderr

    def tearDown(self):
        # Restore stdout/stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('gremlin.subprocess.run')
    def test_run_git_command_success(self, mock_subprocess_run):
        # Mock rationale: Simulate a successful git command execution.
        mock_result = MagicMock()
        mock_result.stdout = "success output\n"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        output = gremlin.run_git_command(['git', 'status'])
        self.assertEqual(output, "success output")
        mock_subprocess_run.assert_called_once_with(
            ['git', 'status'], cwd=None, capture_output=True, text=True, check=True, encoding='utf-8'
        )

    @patch('gremlin.subprocess.run')
    def test_run_git_command_failure(self, mock_subprocess_run):
        # Mock rationale: Simulate a failed git command execution.
        mock_error = subprocess.CalledProcessError(1, ['git', 'fail'], stderr="error output")
        mock_subprocess_run.side_effect = mock_error

        with self.assertRaises(SystemExit) as cm:
            gremlin.run_git_command(['git', 'fail'])
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error running git command: git fail", self.new_stderr.getvalue())
        self.assertIn("Stderr: error output", self.new_stderr.getvalue())

    @patch('gremlin.subprocess.run')
    def test_run_git_command_not_found(self, mock_subprocess_run):
        # Mock rationale: Simulate 'git' command not being found in PATH.
        mock_subprocess_run.side_effect = FileNotFoundError()

        with self.assertRaises(SystemExit) as cm:
            gremlin.run_git_command(['git', 'status'])
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: 'git' command not found", self.new_stderr.getvalue())

    @patch('gremlin.run_git_command')
    def test_get_local_branches(self, mock_run_git_command):
        # Mock rationale: Provide a predefined list of branches as if returned by 'git branch'.
        mock_run_git_command.return_value = "main\nfeature/new-thing\nbugfix/old-bug"
        branches = gremlin.get_local_branches()
        self.assertEqual(branches, ['main', 'feature/new-thing', 'bugfix/old-bug'])
        mock_run_git_command.assert_called_once_with(['git', 'branch', '--format=%(refname:short)'], cwd=None)

    @patch('gremlin.run_git_command')
    def test_get_last_commit_date(self, mock_run_git_command):
        # Mock rationale: Provide a specific ISO-strict date string for a commit.
        mock_run_git_command.return_value = "2023-01-15T10:00:00+01:00"
        date = gremlin.get_last_commit_date('main')
        self.assertEqual(date, datetime.datetime(2023, 1, 15, 10, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=3600))))
        mock_run_git_command.assert_called_once_with(['git', 'log', '-1', '--format=%cd', '--date=iso-strict', 'main'], cwd=None)

    @patch('gremlin.get_last_commit_date')
    def test_find_stale_branches(self, mock_get_last_commit_date):
        # Mock rationale: Control the last commit dates for various branches to test staleness logic.
        # Mock datetime.datetime.now() to ensure deterministic 'current_date' for comparison.
        current_date = datetime.datetime(2023, 2, 20, 12, 0, 0) # Feb 20, 2023 (naive datetime)

        # Branch 'fresh' is 5 days old (Feb 15)
        # Branch 'stale_35' is 35 days old (Jan 16)
        # Branch 'stale_40' is 40 days old (Jan 11)
        # Branch 'very_fresh' is 1 day old (Feb 19)

        mock_get_last_commit_date.side_effect = [
            datetime.datetime(2023, 2, 15, 10, 0, tzinfo=datetime.timezone.utc), # fresh
            datetime.datetime(2023, 1, 16, 10, 0, tzinfo=datetime.timezone.utc), # stale_35
            datetime.datetime(2023, 1, 11, 10, 0, tzinfo=datetime.timezone.utc), # stale_40
            datetime.datetime(2023, 2, 19, 10, 0, tzinfo=datetime.timezone.utc), # very_fresh
        ]

        branches = ['fresh', 'stale_35', 'stale_40', 'very_fresh']
        days_stale = 30

        stale = gremlin.find_stale_branches(branches, days_stale, current_date)

        # Expected stale branches: stale_35 (35 days old), stale_40 (40 days old)
        expected_stale = [
            ('stale_35', datetime.date(2023, 1, 16)),
            ('stale_40', datetime.date(2023, 1, 11))
        ]
        self.assertEqual(stale, expected_stale)

    @patch('gremlin.datetime')
    @patch('gremlin.get_local_branches')
    @patch('gremlin.find_stale_branches')
    @patch('gremlin.run_git_command')
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_stale_branches(self, mock_parse_args, mock_sys_exit, mock_run_git_command, mock_find_stale_branches, mock_get_local_branches, mock_datetime):
        # Mock rationale: Simulate a scenario where no stale branches are found.
        mock_parse_args.return_value = MagicMock(days=30, suggest_delete=False, delete=False, cwd=None)
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 3, 1)
        mock_get_local_branches.return_value = ['main', 'dev']
        mock_find_stale_branches.return_value = []
        mock_sys_exit.side_effect = SystemExit # Allow sys.exit to be caught

        with self.assertRaises(SystemExit) as cm:
            gremlin.main()
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("No stale branches found", self.new_stdout.getvalue())
        mock_run_git_command.assert_not_called()

    @patch('gremlin.datetime')
    @patch('gremlin.get_local_branches')
    @patch('gremlin.find_stale_branches')
    @patch('gremlin.run_git_command')
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_list_stale_branches(self, mock_parse_args, mock_sys_exit, mock_run_git_command, mock_find_stale_branches, mock_get_local_branches, mock_datetime):
        # Mock rationale: Simulate finding stale branches and listing them without deletion.
        mock_parse_args.return_value = MagicMock(days=30, suggest_delete=False, delete=False, cwd=None)
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 3, 1)
        mock_get_local_branches.return_value = ['main', 'feature/old', 'bugfix/ancient']
        mock_find_stale_branches.return_value = [
            ('feature/old', datetime.date(2023, 1, 15)),
            ('bugfix/ancient', datetime.date(2023, 1, 1))
        ]
        mock_sys_exit.side_effect = SystemExit

        with self.assertRaises(SystemExit) as cm:
            gremlin.main()
        self.assertEqual(cm.exception.code, 0)
        output = self.new_stdout.getvalue()
        self.assertIn("Found 2 stale branch(es):", output)
        self.assertIn("  - feature/old (last commit: 2023-01-15)", output)
        self.assertIn("  - bugfix/ancient (last commit: 2023-01-01)", output)
        self.assertIn("To delete these branches, run with '--delete' or '--suggest-delete'.", output)
        mock_run_git_command.assert_not_called()

    @patch('gremlin.datetime')
    @patch('gremlin.get_local_branches')
    @patch('gremlin.find_stale_branches')
    @patch('gremlin.run_git_command')
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_suggest_delete(self, mock_parse_args, mock_sys_exit, mock_run_git_command, mock_find_stale_branches, mock_get_local_branches, mock_datetime):
        # Mock rationale: Simulate finding stale branches and suggesting deletion commands.
        mock_parse_args.return_value = MagicMock(days=30, suggest_delete=True, delete=False, cwd=None)
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 3, 1)
        mock_get_local_branches.return_value = ['main', 'feature/old']
        mock_find_stale_branches.return_value = [('feature/old', datetime.date(2023, 1, 15))]
        mock_sys_exit.side_effect = SystemExit

        with self.assertRaises(SystemExit) as cm:
            gremlin.main()
        self.assertEqual(cm.exception.code, 0)
        output = self.new_stdout.getvalue()
        self.assertIn("To delete these branches, run the following commands", output)
        self.assertIn("  git branch -d feature/old", output)
        mock_run_git_command.assert_not_called()

    @patch('gremlin.datetime')
    @patch('gremlin.get_local_branches')
    @patch('gremlin.find_stale_branches')
    @patch('gremlin.run_git_command')
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_delete_branches_success(self, mock_parse_args, mock_sys_exit, mock_run_git_command, mock_find_stale_branches, mock_get_local_branches, mock_datetime):
        # Mock rationale: Simulate finding stale branches and successfully deleting them.
        mock_parse_args.return_value = MagicMock(days=30, suggest_delete=False, delete=True, cwd=None)
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 3, 1)
        mock_get_local_branches.return_value = ['main', 'feature/old']
        mock_find_stale_branches.return_value = [('feature/old', datetime.date(2023, 1, 15))]
        mock_sys_exit.side_effect = SystemExit

        # Mock run_git_command for the deletion step
        mock_run_git_command.return_value = ""

        with self.assertRaises(SystemExit) as cm:
            gremlin.main()
        self.assertEqual(cm.exception.code, 0)
        output = self.new_stdout.getvalue()
        self.assertIn("Attempting to delete stale branches...", output)
        self.assertIn("  Deleting branch: feature/old", output)
        self.assertIn("    Successfully deleted feature/old", output)
        mock_run_git_command.assert_called_once_with(['git', 'branch', '-d', 'feature/old'], cwd=None)

    @patch('gremlin.datetime')
    @patch('gremlin.get_local_branches')
    @patch('gremlin.find_stale_branches')
    @patch('gremlin.run_git_command')
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_delete_branches_failure(self, mock_parse_args, mock_sys_exit, mock_run_git_command, mock_find_stale_branches, mock_get_local_branches, mock_datetime):
        # Mock rationale: Simulate finding stale branches but failing to delete one.
        mock_parse_args.return_value = MagicMock(days=30, suggest_delete=False, delete=True, cwd=None)
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 3, 1)
        mock_get_local_branches.return_value = ['main', 'feature/old']
        mock_find_stale_branches.return_value = [('feature/old', datetime.date(2023, 1, 15))]
        mock_sys_exit.side_effect = SystemExit

        # Mock run_git_command to raise an exception during deletion
        mock_run_git_command.side_effect = Exception("Branch not merged")

        with self.assertRaises(SystemExit) as cm:
            gremlin.main()
        self.assertEqual(cm.exception.code, 0)
        output = self.new_stdout.getvalue()
        error_output = self.new_stderr.getvalue()
        self.assertIn("Attempting to delete stale branches...", output)
        self.assertIn("  Deleting branch: feature/old", output)
        self.assertIn("    Failed to delete feature/old: Branch not merged", error_output)
        mock_run_git_command.assert_called_once_with(['git', 'branch', '-d', 'feature/old'], cwd=None)

    @patch('gremlin.datetime')
    @patch('gremlin.get_local_branches')
    @patch('gremlin.find_stale_branches')
    @patch('gremlin.run_git_command')
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_branches(self, mock_parse_args, mock_sys_exit, mock_run_git_command, mock_find_stale_branches, mock_get_local_branches, mock_datetime):
        # Mock rationale: Simulate a repository with no local branches.
        mock_parse_args.return_value = MagicMock(days=30, suggest_delete=False, delete=False, cwd=None)
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 3, 1)
        mock_get_local_branches.return_value = []
        mock_sys_exit.side_effect = SystemExit

        with self.assertRaises(SystemExit) as cm:
            gremlin.main()
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("No local Git branches found.", self.new_stdout.getvalue())
        mock_find_stale_branches.assert_not_called()
        mock_run_git_command.assert_not_called()

if __name__ == '__main__':
    unittest.main()
