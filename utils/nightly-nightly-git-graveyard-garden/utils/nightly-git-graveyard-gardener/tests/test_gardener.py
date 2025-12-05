import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import sys
import io

# Import the functions to be tested
from src.gardener import (
    run_git_command,
    get_local_branches,
    get_merged_branches,
    get_current_branch,
    get_last_commit_date,
    delete_branch,
    main
)

class TestGardener(unittest.TestCase):

    @patch('subprocess.run')
    def test_run_git_command_success(self, mock_subprocess_run):
        # Mock rationale: We don't want to actually run git commands during tests.
        # We simulate a successful git command execution.
        mock_subprocess_run.return_value = MagicMock(
            stdout="success output", stderr="", returncode=0
        )
        self.assertEqual(run_git_command(['git', 'status']), "success output")
        mock_subprocess_run.assert_called_once()

    @patch('subprocess.run')
    def test_run_git_command_failure(self, mock_subprocess_run):
        # Mock rationale: Simulate a failed git command to test error handling.
        mock_subprocess_run.return_value = MagicMock(
            stdout="", stderr="error output", returncode=1
        )
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=['git', 'fail'], stderr="error output"
        )
        with self.assertRaises(SystemExit) as cm:
            run_git_command(['git', 'fail'])
        self.assertEqual(cm.exception.code, 1)
        mock_subprocess_run.assert_called_once()

    @patch('src.gardener.run_git_command')
    def test_get_local_branches(self, mock_run_git_command):
        # Mock rationale: Simulate the output of 'git branch --format=%(refname:short)'.
        mock_run_git_command.return_value = "main\nfeature/a\nbugfix/b"
        branches = get_local_branches()
        self.assertEqual(branches, ["main", "feature/a", "bugfix/b"])
        mock_run_git_command.assert_called_once_with(['git', 'branch', '--format=%(refname:short)'], cwd=None)

    @patch('src.gardener.run_git_command')
    def test_get_merged_branches(self, mock_run_git_command):
        # Mock rationale: Simulate the output of 'git branch --merged'.
        mock_run_git_command.return_value = "  main\n  feature/merged-a\n* current-branch"
        merged = get_merged_branches("current-branch")
        self.assertEqual(merged, ["main", "feature/merged-a"])
        mock_run_git_command.assert_called_once_with(['git', 'branch', '--merged', '--format=%(refname:short)'], cwd=None)

    @patch('src.gardener.run_git_command')
    def test_get_current_branch(self, mock_run_git_command):
        # Mock rationale: Simulate the output of 'git rev-parse --abbrev-ref HEAD'.
        mock_run_git_command.return_value = "main"
        self.assertEqual(get_current_branch(), "main")
        mock_run_git_command.assert_called_once_with(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=None)

    @patch('src.gardener.run_git_command')
    def test_get_current_branch_detached_head(self, mock_run_git_command):
        # Mock rationale: Simulate a detached HEAD state where git rev-parse fails.
        mock_run_git_command.side_effect = SystemExit(1)
        self.assertEqual(get_current_branch(), "HEAD")
        mock_run_git_command.assert_called_once_with(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=None)

    @patch('src.gardener.run_git_command')
    def test_get_last_commit_date(self, mock_run_git_command):
        # Mock rationale: Simulate the output of 'git log -1 --format=%at'.
        # Use a fixed timestamp for deterministic testing.
        fixed_timestamp = 1678886400 # March 15, 2023 12:00:00 PM UTC
        mock_run_git_command.return_value = str(fixed_timestamp)
        
        expected_date = datetime.fromtimestamp(fixed_timestamp)
        self.assertEqual(get_last_commit_date("some-branch"), expected_date)
        mock_run_git_command.assert_called_once_with(['git', 'log', 'some-branch', '-1', '--format=%at'], cwd=None)

    @patch('src.gardener.run_git_command')
    def test_delete_branch(self, mock_run_git_command):
        # Mock rationale: Simulate successful branch deletion.
        mock_run_git_command.return_value = ""
        delete_branch("old-branch")
        mock_run_git_command.assert_called_once_with(['git', 'branch', '-d', 'old-branch'], cwd=None)

        mock_run_git_command.reset_mock()
        delete_branch("stale-branch", force=True)
        mock_run_git_command.assert_called_once_with(['git', 'branch', '-D', 'stale-branch'], cwd=None)

    @patch('src.gardener.get_current_branch')
    @patch('src.gardener.get_local_branches')
    @patch('src.gardener.get_merged_branches')
    @patch('src.gardener.get_last_commit_date')
    @patch('src.gardener.delete_branch')
    @patch('builtins.input', return_value='y') # Mock rationale: Simulate user confirming deletion
    @patch('sys.stdout', new_callable=io.StringIO) # Mock rationale: Capture stdout for assertions
    @patch('sys.stderr', new_callable=io.StringIO) # Mock rationale: Capture stderr for assertions
    def test_main_merged_and_stale_deletion(self, mock_stderr, mock_stdout, mock_input, mock_delete_branch, mock_get_last_commit_date, mock_get_merged_branches, mock_get_local_branches, mock_get_current_branch):
        # Mock rationale: Simulate a full scenario with merged and stale branches.
        # We control all external interactions (git commands, user input, time).
        
        mock_get_current_branch.return_value = "main"
        mock_get_local_branches.return_value = [
            "main", "feature/merged-old", "feature/stale-new", "feature/active", "feature/merged-recent"
        ]
        mock_get_merged_branches.return_value = [
            "feature/merged-old", "feature/merged-recent"
        ]

        # Define fixed dates for deterministic testing
        now = datetime(2023, 10, 27, 10, 0, 0)
        old_date = now - timedelta(days=40) # Older than 30 days
        recent_date = now - timedelta(days=5) # Newer than 30 days

        # Mock get_last_commit_date for specific branches
        def mock_date_side_effect(branch_name, cwd=None):
            if branch_name == "feature/merged-old":
                return old_date
            elif branch_name == "feature/stale-new":
                return old_date # This branch is stale but not merged
            elif branch_name == "feature/active":
                return recent_date
            elif branch_name == "feature/merged-recent":
                return recent_date
            raise ValueError(f"Unexpected branch: {branch_name}")

        mock_get_last_commit_date.side_effect = mock_date_side_effect

        # Simulate command line arguments
        sys.argv = ['gardener.py', '--merged', '--days', '30']

        with patch('src.gardener.datetime') as mock_dt:
            mock_dt.now.return_value = now
            mock_dt.fromtimestamp = datetime.fromtimestamp # Keep original fromtimestamp
            mock_dt.timedelta = timedelta # Keep original timedelta
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime.datetime() calls

            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0) # Expect successful exit

        output = mock_stdout.getvalue()
        self.assertIn("feature/merged-old", output) # Merged and old
        self.assertIn("feature/stale-new", output) # Stale (old)
        self.assertNotIn("feature/active", output) # Not old, not merged
        self.assertNotIn("feature/merged-recent", output) # Merged but not old enough

        # Assert deletion calls
        mock_delete_branch.assert_any_call("feature/merged-old", force=False, cwd='.')
        mock_delete_branch.assert_any_call("feature/stale-new", force=False, cwd='.')
        self.assertEqual(mock_delete_branch.call_count, 2)

    @patch('src.gardener.get_current_branch')
    @patch('src.gardener.get_local_branches')
    @patch('src.gardener.get_merged_branches')
    @patch('src.gardener.get_last_commit_date')
    @patch('src.gardener.delete_branch')
    @patch('builtins.input', return_value='n') # Mock rationale: Simulate user declining deletion
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_deletion_cancelled(self, mock_stderr, mock_stdout, mock_input, mock_delete_branch, mock_get_last_commit_date, mock_get_merged_branches, mock_get_local_branches, mock_get_current_branch):
        # Mock rationale: Test the scenario where the user cancels the deletion.
        mock_get_current_branch.return_value = "main"
        mock_get_local_branches.return_value = ["main", "feature/old"]
        mock_get_merged_branches.return_value = []
        mock_get_last_commit_date.return_value = datetime.now() - timedelta(days=40)

        sys.argv = ['gardener.py', '--days', '30']

        with patch('src.gardener.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2023, 10, 27, 10, 0, 0)
            mock_dt.fromtimestamp = datetime.fromtimestamp
            mock_dt.timedelta = timedelta
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0) # Exit code 0 for cancellation is fine

        output = mock_stdout.getvalue()
        self.assertIn("Deletion cancelled.", output)
        mock_delete_branch.assert_not_called()

    @patch('src.gardener.get_current_branch')
    @patch('src.gardener.get_local_branches')
    @patch('src.gardener.get_merged_branches')
    @patch('src.gardener.get_last_commit_date')
    @patch('src.gardener.delete_branch')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_dry_run(self, mock_stderr, mock_stdout, mock_delete_branch, mock_get_last_commit_date, mock_get_merged_branches, mock_get_local_branches, mock_get_current_branch):
        # Mock rationale: Test the dry-run functionality, ensuring no deletions occur.
        mock_get_current_branch.return_value = "main"
        mock_get_local_branches.return_value = ["main", "feature/old"]
        mock_get_merged_branches.return_value = []
        mock_get_last_commit_date.return_value = datetime.now() - timedelta(days=40)

        sys.argv = ['gardener.py', '--days', '30', '--dry-run']

        with patch('src.gardener.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2023, 10, 27, 10, 0, 0)
            mock_dt.fromtimestamp = datetime.fromtimestamp
            mock_dt.timedelta = timedelta
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)

        output = mock_stdout.getvalue()
        self.assertIn("Dry run complete. No branches were deleted.", output)
        mock_delete_branch.assert_not_called()

    @patch('src.gardener.get_current_branch')
    @patch('src.gardener.get_local_branches')
    @patch('src.gardener.get_merged_branches')
    @patch('src.gardener.get_last_commit_date')
    @patch('src.gardener.delete_branch')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_no_deletable_branches(self, mock_stderr, mock_stdout, mock_delete_branch, mock_get_last_commit_date, mock_get_merged_branches, mock_get_local_branches, mock_get_current_branch):
        # Mock rationale: Test the scenario where no branches match the deletion criteria.
        mock_get_current_branch.return_value = "main"
        mock_get_local_branches.return_value = ["main", "feature/active"]
        mock_get_merged_branches.return_value = []
        mock_get_last_commit_date.return_value = datetime.now() - timedelta(days=5) # Not old enough

        sys.argv = ['gardener.py', '--days', '30']

        with patch('src.gardener.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2023, 10, 27, 10, 0, 0)
            mock_dt.fromtimestamp = datetime.fromtimestamp
            mock_dt.timedelta = timedelta
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)

        output = mock_stdout.getvalue()
        self.assertIn("No deletable branches found based on the criteria.", output)
        mock_delete_branch.assert_not_called()

    @patch('src.gardener.get_current_branch')
    @patch('src.gardener.get_local_branches')
    @patch('src.gardener.get_merged_branches')
    @patch('src.gardener.get_last_commit_date')
    @patch('src.gardener.delete_branch')
    @patch('builtins.input', return_value='y')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_force_deletion(self, mock_stderr, mock_stdout, mock_input, mock_delete_branch, mock_get_last_commit_date, mock_get_merged_branches, mock_get_local_branches, mock_get_current_branch):
        # Mock rationale: Test the --force flag, ensuring no confirmation prompt.
        mock_get_current_branch.return_value = "main"
        mock_get_local_branches.return_value = ["main", "feature/old"]
        mock_get_merged_branches.return_value = []
        mock_get_last_commit_date.return_value = datetime.now() - timedelta(days=40)

        sys.argv = ['gardener.py', '--days', '30', '--force']

        with patch('src.gardener.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2023, 10, 27, 10, 0, 0)
            mock_dt.fromtimestamp = datetime.fromtimestamp
            mock_dt.timedelta = timedelta
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)

        output = mock_stdout.getvalue()
        self.assertIn("Deleting branch: feature/old", output)
        mock_delete_branch.assert_called_once_with("feature/old", force=True, cwd='.')
        mock_input.assert_not_called() # No confirmation prompt

if __name__ == '__main__':
    unittest.main()
