import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Mock rationale: We need to simulate file system interactions (checking if files/dirs exist, listing dir contents)
# without actually touching the disk. This ensures tests are fast, deterministic, and don't rely on external state.

# Adjust sys.path to allow importing from src/ when running tests from the tests/ directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.auditor import scan_repository, main
sys.path.pop(0) # Clean up sys.path after import

class TestApocalypseAssetAuditor(unittest.TestCase):

    def setUp(self):
        # Define a standard set of critical assets for testing
        self.critical_assets = [
            "README.md",
            "LICENSE",
            "CONTRIBUTING.md",
            ".gitignore",
            ".github/workflows/"
        ]
        # Mock sys.argv to control the repo_path argument for main()
        self.original_argv = sys.argv
        sys.argv = [self.original_argv[0], '/mock/repo'] # Default mock path for tests calling main()

    def tearDown(self):
        sys.argv = self.original_argv # Restore original sys.argv

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.listdir')
    def test_all_assets_present(self, mock_listdir, mock_isdir, mock_exists):
        # Mock rationale: Simulate a repository where all critical files and workflows exist.
        mock_exists.side_effect = lambda path: path in [
            '/mock/repo/README.md',
            '/mock/repo/LICENSE',
            '/mock/repo/CONTRIBUTING.md',
            '/mock/repo/.gitignore',
            '/mock/repo/.github/workflows/',
            '/mock/repo/.github/workflows/main.yml',
            '/mock/repo/.github/workflows/test.yml'
        ]
        mock_isdir.side_effect = lambda path: path == '/mock/repo/.github/workflows/'
        mock_listdir.side_effect = lambda path: ['main.yml', 'test.yml'] if path == '/mock/repo/.github/workflows/' else []

        # Test scan_repository function directly
        report = scan_repository('/mock/repo', self.critical_assets)
        self.assertEqual(report['missing_count'], 0)
        self.assertTrue(report['results']['README.md']['present'])
        self.assertTrue(report['results']['LICENSE']['present'])
        self.assertTrue(report['results']['CONTRIBUTING.md']['present'])
        self.assertTrue(report['results']['.gitignore']['present'])
        self.assertTrue(report['results']['.github/workflows/']['present'])
        self.assertEqual(report['results']['.github/workflows/']['count'], 2)

        # Test main function output and exit code
        with patch('sys.stdout', new=MagicMock()) as mock_stdout,
             patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_once_with(0) # Expect success exit code
            output = mock_stdout.getvalue()
            self.assertIn("FULLY STOCKED", output)
            self.assertIn("All critical assets are present", output)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.listdir')
    def test_some_assets_missing(self, mock_listdir, mock_isdir, mock_exists):
        # Mock rationale: Simulate a repository where some critical files are missing.
        mock_exists.side_effect = lambda path: path in [
            '/mock/repo/README.md',
            # '/mock/repo/LICENSE', # Missing
            '/mock/repo/CONTRIBUTING.md',
            '/mock/repo/.gitignore',
            '/mock/repo/.github/workflows/',
            '/mock/repo/.github/workflows/main.yml'
        ]
        mock_isdir.side_effect = lambda path: path == '/mock/repo/.github/workflows/'
        mock_listdir.side_effect = lambda path: ['main.yml'] if path == '/mock/repo/.github/workflows/' else []

        report = scan_repository('/mock/repo', self.critical_assets)
        self.assertEqual(report['missing_count'], 1)
        self.assertTrue(report['results']['README.md']['present'])
        self.assertFalse(report['results']['LICENSE']['present'])
        self.assertTrue(report['results']['CONTRIBUTING.md']['present'])
        self.assertTrue(report['results']['.gitignore']['present'])
        self.assertTrue(report['results']['.github/workflows/']['present'])
        self.assertEqual(report['results']['.github/workflows/']['count'], 1)

        with patch('sys.stdout', new=MagicMock()) as mock_stdout,
             patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_once_with(1) # Expect failure exit code
            output = mock_stdout.getvalue()
            self.assertIn("PARTIALLY STOCKED", output)
            self.assertIn("1 critical asset(s) are missing", output)
            self.assertIn("❌ LICENSE: Missing!", output)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.listdir')
    def test_workflows_directory_missing(self, mock_listdir, mock_isdir, mock_exists):
        # Mock rationale: Simulate a repository where the .github/workflows directory is entirely missing.
        mock_exists.side_effect = lambda path: path in [
            '/mock/repo/README.md',
            '/mock/repo/LICENSE',
            '/mock/repo/CONTRIBUTING.md',
            '/mock/repo/.gitignore'
            # '/mock/repo/.github/workflows/' # Missing
        ]
        mock_isdir.side_effect = lambda path: False # No directories exist
        mock_listdir.side_effect = lambda path: []

        report = scan_repository('/mock/repo', self.critical_assets)
        self.assertEqual(report['missing_count'], 1)
        self.assertFalse(report['results']['.github/workflows/']['present'])
        self.assertEqual(report['results']['.github/workflows/']['reason'], 'Directory not found')

        with patch('sys.stdout', new=MagicMock()) as mock_stdout,
             patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)
            output = mock_stdout.getvalue()
            self.assertIn("PARTIALLY STOCKED", output)
            self.assertIn("❌ .github/workflows/: Missing! Directory not found", output)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.listdir')
    def test_workflows_directory_empty(self, mock_listdir, mock_isdir, mock_exists):
        # Mock rationale: Simulate a repository where .github/workflows exists but contains no .yml files.
        mock_exists.side_effect = lambda path: path in [
            '/mock/repo/README.md',
            '/mock/repo/LICENSE',
            '/mock/repo/CONTRIBUTING.md',
            '/mock/repo/.gitignore',
            '/mock/repo/.github/workflows/' # Dir exists
        ]
        mock_isdir.side_effect = lambda path: path == '/mock/repo/.github/workflows/'
        mock_listdir.side_effect = lambda path: [] # Dir is empty

        report = scan_repository('/mock/repo', self.critical_assets)
        self.assertEqual(report['missing_count'], 1)
        self.assertFalse(report['results']['.github/workflows/']['present'])
        self.assertEqual(report['results']['.github/workflows/']['reason'], 'No workflow files found')

        with patch('sys.stdout', new=MagicMock()) as mock_stdout,
             patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)
            output = mock_stdout.getvalue()
            self.assertIn("PARTIALLY STOCKED", output)
            self.assertIn("❌ .github/workflows/: Missing! No workflow files found", output)

    @patch('os.getcwd', return_value='/mock/repo') # Mock rationale: Control the default repo_path for main()
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.listdir')
    def test_main_with_default_path(self, mock_listdir, mock_isdir, mock_exists, mock_getcwd):
        # Mock rationale: Test main() when no command-line argument is provided, using os.getcwd().
        sys.argv = [self.original_argv[0]] # No path argument

        mock_exists.side_effect = lambda path: path in [
            '/mock/repo/README.md',
            '/mock/repo/LICENSE',
            '/mock/repo/CONTRIBUTING.md',
            '/mock/repo/.gitignore',
            '/mock/repo/.github/workflows/',
            '/mock/repo/.github/workflows/main.yml'
        ]
        mock_isdir.side_effect = lambda path: path == '/mock/repo/.github/workflows/'
        mock_listdir.side_effect = lambda path: ['main.yml'] if path == '/mock/repo/.github/workflows/' else []

        with patch('sys.stdout', new=MagicMock()) as mock_stdout,
             patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)
            output = mock_stdout.getvalue()
            self.assertIn("Scanning repository at: /mock/repo", output)
            self.assertIn("PARTIALLY STOCKED", output)

if __name__ == '__main__':
    unittest.main()
