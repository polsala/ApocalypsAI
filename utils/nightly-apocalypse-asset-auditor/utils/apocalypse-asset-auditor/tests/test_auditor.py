import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock rationale: We need to simulate file system interactions (checking if paths exist, if they are files/directories)
# without actually touching the disk. This ensures tests are fast, deterministic, and isolated from the host system's file structure.
# `os.path.exists`, `os.path.isdir`, and `os.path.isfile` are the primary functions to mock.

# To make the import work for testing, we'll add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from auditor import audit_repo, main
sys.path.pop(0) # Clean up sys.path after import

class TestApocalypseAssetAuditor(unittest.TestCase):

    def setUp(self):
        self.repo_path = '/mock/repo'
        self.critical_assets = [
            "README.md",
            "LICENSE",
            "AGENTS.md",
            ".github/workflows/", # Directory
            "agents/",            # Directory
            "utils/"              # Directory
        ]

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_all_assets_present(self, mock_isfile, mock_isdir):
        # Mock rationale: Simulate a scenario where all critical assets exist.
        # `os.path.isdir` and `os.path.isfile` are called to distinguish between file and directory checks.
        mock_isdir.side_effect = lambda p: p.endswith('/.github/workflows') or p.endswith('/agents') or p.endswith('/utils') or p == self.repo_path
        mock_isfile.side_effect = lambda p: p.endswith('/README.md') or p.endswith('/LICENSE') or p.endswith('/AGENTS.md')

        results = audit_repo(self.repo_path, self.critical_assets)

        self.assertEqual(len(results['present']), len(self.critical_assets))
        self.assertEqual(len(results['missing']), 0)
        self.assertCountEqual(results['present'], self.critical_assets)

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_some_assets_missing(self, mock_isfile, mock_isdir):
        # Mock rationale: Simulate a scenario where some critical assets are missing.
        # Specifically, README.md and .github/workflows/ will be marked as non-existent.
        mock_isdir.side_effect = lambda p: (p.endswith('/agents') or p.endswith('/utils') or p == self.repo_path) and not p.endswith('/.github/workflows')
        mock_isfile.side_effect = lambda p: (p.endswith('/LICENSE') or p.endswith('/AGENTS.md')) and not p.endswith('/README.md')

        results = audit_repo(self.repo_path, self.critical_assets)

        expected_present = ["LICENSE", "AGENTS.md", "agents/", "utils/"]
        expected_missing = ["README.md", ".github/workflows/"]

        self.assertCountEqual(results['present'], expected_present)
        self.assertCountEqual(results['missing'], expected_missing)
        self.assertEqual(len(results['present']), len(expected_present))
        self.assertEqual(len(results['missing']), len(expected_missing))

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_repo_path_does_not_exist(self, mock_isfile, mock_isdir):
        # Mock rationale: Simulate the case where the provided repository path itself does not exist.
        mock_isdir.return_value = False # The repo_path itself is not a directory
        mock_isfile.return_value = False

        # Capture stderr to check the error message
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            results = audit_repo('/nonexistent/path', self.critical_assets)
            self.assertEqual(results['present'], [])
            self.assertEqual(results['missing'], [])
            mock_stderr.write.assert_called_with("Error: Repository path '/nonexistent/path' does not exist or is not a directory.\n")

    @patch('sys.argv', ['auditor.py', '/mock/repo'])
    @patch('sys.exit')
    @patch('builtins.print')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_main_all_present(self, mock_isfile, mock_isdir, mock_print, mock_exit):
        # Mock rationale: Test the `main` function's execution path when all assets are present.
        # We mock `sys.argv` to provide command-line arguments, `sys.exit` to prevent actual exit,
        # `builtins.print` to capture output, and `os.path.*` to simulate file system.
        mock_isdir.side_effect = lambda p: p.endswith('/.github/workflows') or p.endswith('/agents') or p.endswith('/utils') or p == self.repo_path
        mock_isfile.side_effect = lambda p: p.endswith('/README.md') or p.endswith('/LICENSE') or p.endswith('/AGENTS.md')

        main()

        mock_exit.assert_called_once_with(0)
        # Check for key phrases in print calls
        mock_print.assert_any_call("Repository is apocalypse-ready! All critical assets are present.")
        mock_print.assert_any_call("✅  README.md")

    @patch('sys.argv', ['auditor.py', '/mock/repo'])
    @patch('sys.exit')
    @patch('builtins.print')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_main_some_missing(self, mock_isfile, mock_isdir, mock_print, mock_exit):
        # Mock rationale: Test the `main` function's execution path when some assets are missing.
        # Similar mocking strategy as `test_main_all_present`.
        mock_isdir.side_effect = lambda p: (p.endswith('/agents') or p.endswith('/utils') or p == self.repo_path) and not p.endswith('/.github/workflows')
        mock_isfile.side_effect = lambda p: (p.endswith('/LICENSE') or p.endswith('/AGENTS.md')) and not p.endswith('/README.md')

        main()

        mock_exit.assert_called_once_with(1)
        mock_print.assert_any_call("Repository is NOT apocalypse-ready. Address the missing assets!")
        mock_print.assert_any_call("❌  README.md (Missing)")
        mock_print.assert_any_call("❌  .github/workflows/ (Missing)")
        mock_print.assert_any_call("- README.md")
        mock_print.assert_any_call("- .github/workflows/")

    @patch('sys.argv', ['auditor.py'])
    @patch('sys.exit')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_main_no_args(self, mock_stderr, mock_exit):
        # Mock rationale: Test the `main` function's behavior when no repository path is provided.
        # Expects a usage message to stderr and an exit code of 1.
        main()
        mock_exit.assert_called_once_with(1)
        mock_stderr.write.assert_called_with("Usage: python src/auditor.py <repository_path>\n")

    @patch('sys.argv', ['auditor.py', '/nonexistent/path'])
    @patch('sys.exit')
    @patch('builtins.print')
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_main_invalid_repo_path(self, mock_isfile, mock_isdir, mock_stderr, mock_print, mock_exit):
        # Mock rationale: Test the `main` function's behavior when the provided repository path is invalid.
        mock_isdir.return_value = False
        mock_isfile.return_value = False

        main()

        mock_exit.assert_called_once_with(1)
        mock_stderr.write.assert_called_with("Error: Repository path '/nonexistent/path' does not exist or is not a directory.\n")

if __name__ == '__main__':
    unittest.main()
