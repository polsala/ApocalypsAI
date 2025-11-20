import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path to allow importing gardener
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import gardener

class TestGardener(unittest.TestCase):

    @patch('gardener.subprocess.run')
    def test_is_git_repo_true(self, mock_run):
        # Mock rationale: Simulate 'git rev-parse --is-inside-work-tree' returning success.
        mock_run.return_value = MagicMock(returncode=0, stdout='true\n', stderr='')
        self.assertTrue(gardener.is_git_repo())
        mock_run.assert_called_once_with(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            check=False, capture_output=True, text=True, cwd=os.getcwd()
        )

    @patch('gardener.subprocess.run')
    def test_is_git_repo_false(self, mock_run):
        # Mock rationale: Simulate 'git rev-parse --is-inside-work-tree' returning failure.
        mock_run.return_value = MagicMock(returncode=128, stdout='', stderr='Not a git repository\n')
        self.assertFalse(gardener.is_git_repo())

    @patch('gardener.subprocess.run')
    def test_get_current_branch(self, mock_run):
        # Mock rationale: Simulate 'git rev-parse --abbrev-ref HEAD' returning a branch name.
        mock_run.return_value = MagicMock(returncode=0, stdout='main\n', stderr='')
        self.assertEqual(gardener.get_current_branch(), 'main')

    @patch('gardener.subprocess.run')
    def test_fetch_remote(self, mock_run):
        # Mock rationale: Simulate 'git fetch --prune' command.
        mock_run.return_value = MagicMock(returncode=0, stdout='Fetched\n', stderr='')
        with patch('builtins.print') as mock_print:
            gardener.fetch_remote()
            mock_run.assert_called_once_with(
                ['git', 'fetch', '--prune'],
                check=False, capture_output=True, text=True, cwd=os.getcwd()
            )
            mock_print.assert_any_call("\nFetching from remote and pruning stale remote-tracking branches...")

    @patch('gardener.get_current_branch', return_value='main')
    @patch('gardener.subprocess.run')
    def test_get_local_branches(self, mock_run, mock_get_current_branch):
        # Mock rationale: Simulate 'git branch --format=%(refname:short)' output.
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='main\nfeature-a\nbugfix-b\n',
            stderr=''
        )
        branches = gardener.get_local_branches()
        self.assertEqual(sorted(branches), sorted(['feature-a', 'bugfix-b']))
        mock_run.assert_called_once_with(
            ['git', 'branch', '--format=%(refname:short)'],
            check=True, capture_output=True, text=True, cwd=os.getcwd()
        )

    @patch('gardener.get_current_branch', return_value='main')
    @patch('gardener.subprocess.run')
    def test_get_merged_branches(self, mock_run, mock_get_current_branch):
        # Mock rationale: Simulate 'git branch --merged main' output.
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='  feature-a\n* main\n  bugfix-b\n',
            stderr=''
        )
        merged = gardener.get_merged_branches('main')
        self.assertEqual(sorted(merged), sorted(['feature-a', 'bugfix-b']))
        mock_run.assert_called_once_with(
            ['git', 'branch', '--merged', 'main', '--format=%(refname:short)'],
            check=True, capture_output=True, text=True, cwd=os.getcwd()
        )

    @patch('gardener.get_local_branches', return_value=['feature-a', 'bugfix-b', 'stale-remote'])
    @patch('gardener.subprocess.run')
    def test_get_remote_deleted_branches(self, mock_run, mock_get_local_branches):
        # Mock rationale: Simulate 'git branch -r' output to identify remote branches.
        # Then compare with local branches to find those without remote counterparts.
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='origin/HEAD -> origin/main\norigin/main\norigin/feature-a\n',
            stderr=''
        )
        deleted = gardener.get_remote_deleted_branches()
        self.assertEqual(sorted(deleted), sorted(['bugfix-b', 'stale-remote']))
        mock_run.assert_called_once_with(
            ['git', 'branch', '-r', '--format=%(refname:short)'],
            check=True, capture_output=True, text=True, cwd=os.getcwd()
        )

    @patch('gardener.subprocess.run')
    @patch('builtins.input', return_value='y')
    @patch('builtins.print')
    def test_delete_branches_confirm(self, mock_print, mock_input, mock_run):
        # Mock rationale: Simulate user confirmation and successful branch deletion.
        mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
        branches = ['feature-a', 'bugfix-b']
        gardener.delete_branches(branches, dry_run=False, force=False)
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(
            ['git', 'branch', '-D', 'feature-a'],
            check=True, capture_output=True, text=True, cwd=os.getcwd()
        )
        mock_run.assert_any_call(
            ['git', 'branch', '-D', 'bugfix-b'],
            check=True, capture_output=True, text=True, cwd=os.getcwd()
        )
        mock_input.assert_called_once()

    @patch('gardener.subprocess.run')
    @patch('builtins.input', return_value='n')
    @patch('builtins.print')
    def test_delete_branches_cancel(self, mock_print, mock_input, mock_run):
        # Mock rationale: Simulate user cancelling branch deletion.
        branches = ['feature-a']
        gardener.delete_branches(branches, dry_run=False, force=False)
        mock_run.assert_not_called()
        mock_input.assert_called_once()
        mock_print.assert_any_call("Deletion cancelled.")

    @patch('gardener.subprocess.run')
    @patch('builtins.print')
    def test_delete_branches_dry_run(self, mock_print, mock_run):
        # Mock rationale: Simulate dry run, ensuring no actual git commands are executed.
        branches = ['feature-a']
        gardener.delete_branches(branches, dry_run=True, force=False)
        mock_run.assert_not_called()
        mock_print.assert_any_call("\n(Dry run) No branches were actually deleted.")

    @patch('gardener.subprocess.run')
    @patch('builtins.print')
    def test_delete_branches_force(self, mock_print, mock_run):
        # Mock rationale: Simulate forced deletion, skipping confirmation.
        mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
        branches = ['feature-a']
        gardener.delete_branches(branches, dry_run=False, force=True)
        mock_run.assert_called_once()
        mock_print.assert_any_call("  Deleting branch: feature-a")

    @patch('gardener.subprocess.run')
    @patch('builtins.print')
    def test_prune_remote_tracking_branches(self, mock_print, mock_run):
        # Mock rationale: Simulate 'git remote prune origin' command.
        mock_run.return_value = MagicMock(returncode=0, stdout='Pruned origin\n', stderr='')
        gardener.prune_remote_tracking_branches(dry_run=False)
        mock_run.assert_called_once_with(
            ['git', 'remote', 'prune', 'origin'],
            check=False, capture_output=True, text=True, cwd=os.getcwd()
        )

    @patch('gardener.subprocess.run')
    @patch('builtins.print')
    def test_prune_remote_tracking_branches_dry_run(self, mock_print, mock_run):
        # Mock rationale: Simulate dry run for remote pruning, ensuring no actual git commands.
        gardener.prune_remote_tracking_branches(dry_run=True)
        mock_run.assert_not_called()
        mock_print.assert_any_call("(Dry run) Remote-tracking branches would have been pruned.")

    @patch('gardener.is_git_repo', return_value=False)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_not_git_repo(self, mock_exit, mock_print, mock_is_git_repo):
        # Mock rationale: Simulate running main outside a git repo, expecting exit.
        gardener.main()
        mock_print.assert_any_call("Error: Not inside a Git repository.", file=sys.stderr)
        mock_exit.assert_called_once_with(1)

    @patch('gardener.is_git_repo', return_value=True)
    @patch('gardener.fetch_remote')
    @patch('gardener.get_current_branch', return_value='main')
    @patch('gardener.get_merged_branches', return_value=['feature-a', 'bugfix-b'])
    @patch('gardener.get_remote_deleted_branches', return_value=['stale-remote'])
    @patch('gardener.delete_branches')
    @patch('gardener.prune_remote_tracking_branches')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(dry_run=False, force=False, no_prune_remote=False))
    def test_main_full_flow(self, mock_parse_args, mock_print, mock_prune_remote, mock_delete_branches, mock_get_remote_deleted, mock_get_merged, mock_get_current, mock_fetch_remote, mock_is_git_repo):
        # Mock rationale: Simulate a full run of the main function, ensuring all sub-functions are called correctly.
        gardener.main()

        mock_is_git_repo.assert_called_once()
        mock_fetch_remote.assert_called_once()
        mock_get_current.assert_called_once()
        mock_get_merged.assert_called_once_with('main')
        mock_get_remote_deleted.assert_called_once()
        
        expected_branches_to_delete = sorted(list(set(['feature-a', 'bugfix-b', 'stale-remote'])))
        mock_delete_branches.assert_called_once_with(expected_branches_to_delete, False, False)
        mock_prune_remote.assert_called_once_with(False)
        mock_print.assert_any_call("\nGit Graveyard Gardening complete! Your repository is now tidier.")

    @patch('gardener.is_git_repo', return_value=True)
    @patch('gardener.fetch_remote')
    @patch('gardener.get_current_branch', return_value='main')
    @patch('gardener.get_merged_branches', return_value=[])
    @patch('gardener.get_remote_deleted_branches', return_value=[])
    @patch('gardener.delete_branches')
    @patch('gardener.prune_remote_tracking_branches')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(dry_run=False, force=False, no_prune_remote=True))
    def test_main_no_branches_no_prune_remote(self, mock_parse_args, mock_print, mock_prune_remote, mock_delete_branches, mock_get_remote_deleted, mock_get_merged, mock_get_current, mock_fetch_remote, mock_is_git_repo):
        # Mock rationale: Simulate a run where no branches need deletion and remote pruning is skipped.
        gardener.main()

        mock_delete_branches.assert_called_once_with([], False, False)
        mock_prune_remote.assert_not_called()
        mock_print.assert_any_call("\nGit Graveyard Gardening complete! Your repository is now tidier.")

if __name__ == '__main__':
    unittest.main()
