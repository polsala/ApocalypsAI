import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import the module under test
from utils.git_merged_branch_cleaner.src.cleaner import (
    get_default_branch,
    list_merged_branches,
    delete_branches,
    main,
)

class TestGitMergedBranchCleaner(unittest.TestCase):
    def setUp(self):
        # Ensure the .git directory exists for the duration of the test
        self.git_dir = Path('.git')
        self.git_dir.mkdir(exist_ok=True)

    def tearDown(self):
        # Clean up the dummy .git directory after each test
        if self.git_dir.exists():
            for child in self.git_dir.iterdir():
                child.unlink()
            self.git_dir.rmdir()

    @patch('utils.git_merged_branch_cleaner.src.cleaner._run_git')
    def test_get_default_branch_symbolic_ref(self, mock_run):
        # Mock rationale: Simulate git returning a symbolic ref pointing to 'main'
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = 'refs/remotes/origin/main\n'
        mock_run.return_value = mock_process

        branch = get_default_branch()
        self.assertEqual(branch, 'main')
        mock_run.assert_called_once_with(['symbolic-ref', 'refs/remotes/origin/HEAD'])

    @patch('utils.git_merged_branch_cleaner.src.cleaner._run_git')
    def test_get_default_branch_fallback(self, mock_run):
        # Mock rationale: git symbolic-ref fails, fallback to 'main'
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = 'fatal: ambiguous argument'
        mock_run.return_value = mock_process

        branch = get_default_branch()
        self.assertEqual(branch, 'main')
        mock_run.assert_called_once_with(['symbolic-ref', 'refs/remotes/origin/HEAD'])

    @patch('utils.git_merged_branch_cleaner.src.cleaner._run_git')
    def test_list_merged_branches_parsing(self, mock_run):
        # Mock rationale: Provide deterministic output of `git branch --merged`.
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = '* main\n  feature-1\n  bugfix-2\n'
        mock_run.return_value = mock_process

        branches = list_merged_branches('main')
        self.assertListEqual(branches, ['feature-1', 'bugfix-2'])
        mock_run.assert_called_once_with(['branch', '--merged', 'main'])

    @patch('utils.git_merged_branch_cleaner.src.cleaner._run_git')
    def test_list_merged_branches_error(self, mock_run):
        # Mock rationale: Simulate a git error to ensure RuntimeError is raised.
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = 'not a git repository'
        mock_run.return_value = mock_process

        with self.assertRaises(RuntimeError) as ctx:
            list_merged_branches('main')
        self.assertIn('Git error while listing merged branches', str(ctx.exception))

    @patch('utils.git_merged_branch_cleaner.src.cleaner._run_git')
    def test_delete_branches_success_and_failure(self, mock_run):
        # Mock rationale: First deletion succeeds, second fails.
        def side_effect(args):
            proc = MagicMock()
            if args[-1] == 'good-branch':
                proc.returncode = 0
                proc.stdout = 'Deleted branch good-branch (was abcdefg).\n'
            else:
                proc.returncode = 1
                proc.stderr = 'error: branch "bad-branch" not found.\n'
            return proc
        mock_run.side_effect = side_effect

        # Capture stdout/stderr
        with patch('sys.stdout') as mock_stdout, patch('sys.stderr') as mock_stderr:
            delete_branches(['good-branch', 'bad-branch'])
            # Verify prints
            mock_stdout.write.assert_any_call('Deleted branch good-branch\n')
            mock_stderr.write.assert_any_call('Failed to delete bad-branch: error: branch "bad-branch" not found.')

    @patch('utils.git_merged_branch_cleaner.src.cleaner._run_git')
    def test_main_dry_run(self, mock_run):
        # Mock rationale: Simulate a repository with two merged branches.
        def run_side_effect(args):
            proc = MagicMock()
            if args[0] == 'symbolic-ref':
                proc.returncode = 0
                proc.stdout = 'refs/remotes/origin/main\n'
            elif args[0] == 'branch' and args[1] == '--merged':
                proc.returncode = 0
                proc.stdout = '* main\n  stale-1\n  stale-2\n'
            else:
                proc.returncode = 0
                proc.stdout = ''
            return proc
        mock_run.side_effect = run_side_effect

        with patch('sys.stdout') as mock_stdout:
            exit_code = main([])
            self.assertEqual(exit_code, 0)
            # Ensure the dry‑run hint is printed
            mock_stdout.write.assert_any_call('(dry‑run) Use --delete to remove these branches.')

    @patch('utils.git_merged_branch_cleaner.src.cleaner._run_git')
    def test_main_with_delete(self, mock_run):
        # Mock rationale: Same as dry‑run but also verify delete calls.
        def run_side_effect(args):
            proc = MagicMock()
            if args[0] == 'symbolic-ref':
                proc.returncode = 0
                proc.stdout = 'refs/remotes/origin/main\n'
            elif args[0] == 'branch' and args[1] == '--merged':
                proc.returncode = 0
                proc.stdout = '* main\n  old-branch\n'
            elif args[0] == 'branch' and args[1] == '-d':
                proc.returncode = 0
                proc.stdout = 'Deleted branch old-branch (was abcdefg).\n'
            else:
                proc.returncode = 0
                proc.stdout = ''
            return proc
        mock_run.side_effect = run_side_effect

        with patch('sys.stdout') as mock_stdout:
            exit_code = main(['--delete'])
            self.assertEqual(exit_code, 0)
            # Verify that delete command was invoked
            mock_run.assert_any_call(['branch', '-d', 'old-branch'])
            mock_stdout.write.assert_any_call('Deleted branch old-branch')
