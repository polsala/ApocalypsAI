import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import sys
import subprocess

# Add the src directory to the Python path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from prognosticator import _run_git_command, get_last_commit_date, get_stale_branches, get_prognosis

class TestPrognosticator(unittest.TestCase):

    @patch('subprocess.run')
    def test_run_git_command_success(self, mock_subprocess_run):
        # Mock rationale: We need to simulate a successful git command execution without actually running git.
        mock_result = MagicMock()
        mock_result.stdout = "git output\n"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        output = _run_git_command(['git', 'status'])
        self.assertEqual(output, "git output")
        mock_subprocess_run.assert_called_once_with(
            ['git', 'status'], capture_output=True, text=True, check=True, cwd=os.getcwd()
        )

    @patch('subprocess.run')
    def test_run_git_command_failure(self, mock_subprocess_run):
        # Mock rationale: We need to simulate a failed git command execution (e.g., command not found or error output).
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, ['git', 'bad-command'], stderr='fatal: bad command')

        output = _run_git_command(['git', 'bad-command'])
        self.assertIsNone(output)

    @patch('subprocess.run')
    def test_get_last_commit_date(self, mock_subprocess_run):
        # Mock rationale: Simulate the output of `git log -1 --format=%cd` for a specific branch.
        mock_result = MagicMock()
        mock_result.stdout = "Thu Oct 26 10:30:00 2023 +0000\n"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        date = get_last_commit_date('main')
        self.assertEqual(date, "Thu Oct 26 10:30:00 2023 +0000")
        mock_subprocess_run.assert_called_once_with(
            ['git', 'log', 'main', '-1', '--format=%cd'], capture_output=True, text=True, check=True, cwd=os.getcwd()
        )

    @patch('subprocess.run')
    def test_get_stale_branches_no_stale(self, mock_subprocess_run):
        # Mock rationale: Simulate a repository with no stale branches.
        # Mock `git branch -vv` output
        mock_branch_vv = MagicMock()
        mock_branch_vv.stdout = (
            "  feature/active    a1b2c3d [origin/feature/active] Active feature\n"
            "* main              e4f5g6h [origin/main] Latest main commit\n"
        )
        mock_branch_vv.stderr = ""
        mock_branch_vv.returncode = 0

        # Mock `git log` output for branches (all recent)
        mock_log_active = MagicMock()
        mock_log_active.stdout = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=10)).strftime('%a %b %d %H:%M:%S %Y %z') + '\n'
        mock_log_active.stderr = ""
        mock_log_active.returncode = 0

        mock_subprocess_run.side_effect = [
            mock_branch_vv, # For git branch -vv
            mock_log_active # For git log feature/active
        ]

        stale_branches = get_stale_branches(90, 'main')
        self.assertEqual(stale_branches, [])

    @patch('subprocess.run')
    def test_get_stale_branches_with_stale(self, mock_subprocess_run):
        # Mock rationale: Simulate a repository with one stale branch.
        # Mock `git branch -vv` output
        mock_branch_vv = MagicMock()
        mock_branch_vv.stdout = (
            "  feature/stale     a1b2c3d [origin/feature/stale] Old feature\n"
            "* main              e4f5g6h [origin/main] Latest main commit\n"
        )
        mock_branch_vv.stderr = ""
        mock_branch_vv.returncode = 0

        # Mock `git log` output for stale branch (old)
        mock_log_stale = MagicMock()
        stale_date = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=100))
        mock_log_stale.stdout = stale_date.strftime('%a %b %d %H:%M:%S %Y %z') + '\n'
        mock_log_stale.stderr = ""
        mock_log_stale.returncode = 0

        mock_subprocess_run.side_effect = [
            mock_branch_vv, # For git branch -vv
            mock_log_stale  # For git log feature/stale
        ]

        stale_branches = get_stale_branches(90, 'main')
        self.assertEqual(len(stale_branches), 1)
        self.assertEqual(stale_branches[0]['name'], 'feature/stale')
        self.assertEqual(stale_branches[0]['last_commit'], stale_date.strftime('%Y-%m-%d'))

    def test_get_prognosis_healthy(self):
        # Mock rationale: Test prognosis logic with healthy inputs.
        last_commit_date_str = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=5)).strftime('%a %b %d %H:%M:%S %Y %z')
        stale_branches = []
        prognosis = get_prognosis(last_commit_date_str, stale_branches)
        self.assertIn("Cosmic currents are favorable", prognosis)
        self.assertIn("The cosmic forecast is clear", prognosis)

    def test_get_prognosis_stale_branches(self):
        # Mock rationale: Test prognosis logic with stale branches.
        last_commit_date_str = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=5)).strftime('%a %b %d %H:%M:%S %Y %z')
        stale_branches = [
            {'name': 'feature/old', 'last_commit': '2023-01-01'}
        ]
        prognosis = get_prognosis(last_commit_date_str, stale_branches)
        self.assertIn("Minor gravitational anomalies detected", prognosis)

    def test_get_prognosis_many_stale_branches(self):
        # Mock rationale: Test prognosis logic with many stale branches.
        last_commit_date_str = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=5)).strftime('%a %b %d %H:%M:%S %Y %z')
        stale_branches = [
            {'name': f'feature/old-{i}', 'last_commit': '2023-01-01'} for i in range(7)
        ]
        prognosis = get_prognosis(last_commit_date_str, stale_branches)
        self.assertIn("A nebula of forgotten branches is forming", prognosis)

    def test_get_prognosis_inactive_repo(self):
        # Mock rationale: Test prognosis logic with an inactive repository.
        last_commit_date_str = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=200)).strftime('%a %b %d %H:%M:%S %Y %z')
        stale_branches = []
        prognosis = get_prognosis(last_commit_date_str, stale_branches)
        self.assertIn("repository shows signs of cosmic dormancy", prognosis)

    def test_get_prognosis_no_commit_data(self):
        # Mock rationale: Test prognosis logic when no commit data is available.
        last_commit_date_str = "N/A"
        stale_branches = []
        prognosis = get_prognosis(last_commit_date_str, stale_branches)
        self.assertIn("The repository's star has dimmed", prognosis)

if __name__ == '__main__':
    unittest.main()
