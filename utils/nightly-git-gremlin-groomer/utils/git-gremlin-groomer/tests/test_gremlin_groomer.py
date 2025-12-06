import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import subprocess

# Mock rationale: We need to simulate Git command outputs without actually running Git
# or modifying the file system. This ensures tests are fast, deterministic, and isolated.

# Add src directory to path for import
sys.path.insert(0, 'utils/git-gremlin-groomer/src')
import gremlin_groomer
sys.path.pop(0)

class TestGitGremlinGroomer(unittest.TestCase):

    @patch('gremlin_groomer.subprocess.run')
    def test_get_current_branch(self, mock_run):
        # Mock rationale: Simulate 'git rev-parse --abbrev-ref HEAD' output.
        mock_run.return_value = MagicMock(
            stdout="main\n", stderr="", returncode=0
        )
        self.assertEqual(gremlin_groomer.get_current_branch(), "main")
        mock_run.assert_called_once_with(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            check=True, capture_output=True, text=True, cwd=None
        )

    @patch('gremlin_groomer.subprocess.run')
    def test_get_merged_branches(self, mock_run):
        # Mock rationale: Simulate 'git branch --merged <branch>' output.
        mock_run.return_value = MagicMock(
            stdout="  feature/old-feature\n* main\n  bugfix/fix-typo\n",
            stderr="", returncode=0
        )
        merged = gremlin_groomer.get_merged_branches("main")
        self.assertIn("feature/old-feature", merged)
        self.assertIn("bugfix/fix-typo", merged)
        self.assertNotIn("main", merged) # Current branch should be excluded
        mock_run.assert_called_once_with(
            ['git', 'branch', '--merged', 'main'],
            check=True, capture_output=True, text=True, cwd=None
        )

    @patch('gremlin_groomer.subprocess.run')
    def test_get_gone_remote_branches(self, mock_run):
        # Mock rationale: Simulate 'git remote prune origin --dry-run' and 'git branch -vv' outputs.
        # We need to mock two calls to subprocess.run
        mock_run.side_effect = [
            # First call: git remote prune origin --dry-run
            MagicMock(stdout="", stderr="", returncode=0),
            # Second call: git branch -vv
            MagicMock(
                stdout=(
                    "  feature/active-feature 1234567 [origin/feature/active-feature] Commit message\n"
                    "  bugfix/old-bugfix    abcdef0 [origin/bugfix/old-bugfix: gone] Old bugfix commit\n"
                    "* main                 fedcba9 [origin/main] Latest main commit\n"
                    "  feature/another-gone 9876543 [origin/feature/another-gone: gone] Another gone feature\n"
                ),
                stderr="", returncode=0
            )
        ]
        gone = gremlin_groomer.get_gone_remote_branches()
        self.assertIn("bugfix/old-bugfix", gone)
        self.assertIn("feature/another-gone", gone)
        self.assertNotIn("main", gone)
        self.assertNotIn("feature/active-feature", gone)
        self.assertEqual(mock_run.call_count, 2)

    @patch('gremlin_groomer.get_current_branch', return_value='main')
    @patch('gremlin_groomer.get_merged_branches', return_value=['merged-feature', 'merged-bugfix'])
    @patch('gremlin_groomer.get_gone_remote_branches', return_value=['gone-feature', 'gone-bugfix'])
    def test_identify_stale_branches(self, mock_gone, mock_merged, mock_current):
        # Mock rationale: Isolate the identification logic from Git commands.
        stale = gremlin_groomer.identify_stale_branches()
        self.assertEqual(sorted(stale), sorted(['merged-feature', 'merged-bugfix', 'gone-feature', 'gone-bugfix']))
        mock_current.assert_called_once()
        mock_merged.assert_called_once_with('main', cwd=None)
        mock_gone.assert_called_once_with(cwd=None)

    @patch('builtins.input', return_value='y')
    @patch('gremlin_groomer.subprocess.run')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_branches_confirmed(self, mock_stdout, mock_run, mock_input):
        # Mock rationale: Simulate user input 'y' and successful branch deletion via Git.
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        branches_to_delete = ['old-feature', 'old-bugfix']
        gremlin_groomer.delete_branches(branches_to_delete, dry_run=False)

        self.assertIn("Confirm deletion? (y/N):", mock_stdout.getvalue())
        self.assertIn("Successfully deleted old-feature", mock_stdout.getvalue())
        self.assertIn("Successfully deleted old-bugfix", mock_stdout.getvalue())
        self.assertEqual(mock_run.call_count, 2) # Two calls for '-D'
        mock_run.assert_any_call(['git', 'branch', '-D', 'old-feature'], check=False, cwd=None)
        mock_run.assert_any_call(['git', 'branch', '-D', 'old-bugfix'], check=False, cwd=None)

    @patch('builtins.input', return_value='n')
    @patch('gremlin_groomer.subprocess.run')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_branches_cancelled(self, mock_stdout, mock_run, mock_input):
        # Mock rationale: Simulate user input 'n' to cancel deletion.
        branches_to_delete = ['old-feature']
        gremlin_groomer.delete_branches(branches_to_delete, dry_run=False)

        self.assertIn("Deletion cancelled.", mock_stdout.getvalue())
        mock_run.assert_not_called()

    @patch('gremlin_groomer.subprocess.run')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_branches_dry_run(self, mock_stdout, mock_run):
        # Mock rationale: Test dry-run behavior, ensuring no actual Git commands are run for deletion.
        branches_to_delete = ['old-feature']
        gremlin_groomer.delete_branches(branches_to_delete, dry_run=True)

        self.assertIn("[DRY RUN] Attempting to delete the following branches:", mock_stdout.getvalue())
        self.assertIn("(Dry run complete. No changes were made.)", mock_stdout.getvalue())
        mock_run.assert_not_called() # No git branch -D should be called

    @patch('gremlin_groomer.identify_stale_branches', return_value=['stale-1', 'stale-2'])
    @patch('gremlin_groomer.delete_branches')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['gremlin_groomer.py', '--delete'])
    def test_main_delete_mode(self, mock_stdout, mock_delete_branches, mock_identify_stale_branches):
        # Mock rationale: Simulate running the script with --delete argument.
        gremlin_groomer.main()
        mock_identify_stale_branches.assert_called_once()
        mock_delete_branches.assert_called_once_with(['stale-1', 'stale-2'], dry_run=False)

    @patch('gremlin_groomer.identify_stale_branches', return_value=['stale-1', 'stale-2'])
    @patch('gremlin_groomer.delete_branches')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['gremlin_groomer.py', '--list', '--dry-run'])
    def test_main_list_dry_run_mode(self, mock_stdout, mock_delete_branches, mock_identify_stale_branches):
        # Mock rationale: Simulate running the script with --list and --dry-run arguments.
        gremlin_groomer.main()
        mock_identify_stale_branches.assert_called_once()
        mock_delete_branches.assert_not_called()
        self.assertIn("Found the following stale branches:", mock_stdout.getvalue())
        self.assertIn("  - stale-1", mock_stdout.getvalue())
        self.assertIn("  - stale-2", mock_stdout.getvalue())
        self.assertIn("(Dry run complete. No changes were made.)", mock_stdout.getvalue())

    @patch('gremlin_groomer.identify_stale_branches', return_value=[])
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['gremlin_groomer.py'])
    def test_main_no_stale_branches(self, mock_exit, mock_stdout, mock_identify_stale_branches):
        # Mock rationale: Simulate a repository with no stale branches.
        gremlin_groomer.main()
        mock_identify_stale_branches.assert_called_once()
        self.assertIn("No stale branches found. Your repository is pristine! ✨", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(0)

    @patch('gremlin_groomer.subprocess.run', side_effect=subprocess.CalledProcessError(1, ['git', 'command'], stderr='fatal: not a git repository'))
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['gremlin_groomer.py'])
    def test_main_git_error(self, mock_exit, mock_stderr, mock_stdout, mock_run):
        # Mock rationale: Simulate a Git command failing (e.g., not in a Git repo).
        gremlin_groomer.main()
        self.assertIn("Error running git command:", mock_stderr.getvalue())
        self.assertIn("Stderr: fatal: not a git repository", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('gremlin_groomer.subprocess.run', side_effect=FileNotFoundError)
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['gremlin_groomer.py'])
    def test_main_git_not_found(self, mock_exit, mock_stderr, mock_stdout, mock_run):
        # Mock rationale: Simulate Git executable not being found.
        gremlin_groomer.main()
        self.assertIn("Error: Git is not installed or not in your PATH.", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)
