import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from io import StringIO

# Mock rationale: We need to simulate file system existence without actually creating files.
# os.path.exists and os.path.isdir are critical for this utility, so they must be mocked.
# os.path.join is generally deterministic, but mocking it can ensure paths are handled as expected.
# sys.exit is mocked to prevent the test runner from exiting prematurely when main() is called.
# sys.stdout is mocked to capture print output for verification.

class TestSurvivalKitChecker(unittest.TestCase):

    def setUp(self):
        # Import checker here to ensure mocks are active when it's loaded if needed,
        # or just before calling functions from it.
        # For this structure, it's fine to import at the top.
        pass

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.join', side_effect=os.path.join) # Mock rationale: Use real os.path.join for path construction, but mock existence.
    def test_all_files_present(self, mock_join, mock_isdir, mock_exists):
        from src.checker import check_survival_kit
        mock_isdir.return_value = True # Mock rationale: Assume the directory exists.
        # Mock rationale: Simulate all required files existing.
        mock_exists.side_effect = lambda path: any(f in path for f in ["README.md", "LICENSE", ".gitignore"])

        directory = "/mock/repo"
        required_files = ["README.md", "LICENSE", ".gitignore"]
        result = check_survival_kit(directory, required_files)

        self.assertEqual(result['present'], ["README.md", "LICENSE", ".gitignore"])
        self.assertEqual(result['missing'], [])
        self.assertEqual(result['score'], "3/3")
        self.assertEqual(result['status'], "READY")
        self.assertTrue(mock_isdir.called)
        self.assertEqual(mock_exists.call_count, len(required_files))

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.join', side_effect=os.path.join)
    def test_some_files_missing(self, mock_join, mock_isdir, mock_exists):
        from src.checker import check_survival_kit
        mock_isdir.return_value = True # Mock rationale: Assume the directory exists.
        # Mock rationale: Simulate README.md existing, others missing.
        mock_exists.side_effect = lambda path: "README.md" in path

        directory = "/mock/repo"
        required_files = ["README.md", "LICENSE", ".gitignore"]
        result = check_survival_kit(directory, required_files)

        self.assertEqual(result['present'], ["README.md"])
        self.assertEqual(result['missing'], ["LICENSE", ".gitignore"])
        self.assertEqual(result['score'], "1/3")
        self.assertEqual(result['status'], "NEEDS ATTENTION")
        self.assertTrue(mock_isdir.called)
        self.assertEqual(mock_exists.call_count, len(required_files))

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.join', side_effect=os.path.join)
    def test_all_files_missing(self, mock_join, mock_isdir, mock_exists):
        from src.checker import check_survival_kit
        mock_isdir.return_value = True # Mock rationale: Assume the directory exists.
        mock_exists.return_value = False # Mock rationale: Simulate no required files existing.

        directory = "/mock/repo"
        required_files = ["README.md", "LICENSE", ".gitignore"]
        result = check_survival_kit(directory, required_files)

        self.assertEqual(result['present'], [])
        self.assertEqual(result['missing'], ["README.md", "LICENSE", ".gitignore"])
        self.assertEqual(result['score'], "0/3")
        self.assertEqual(result['status'], "NEEDS ATTENTION")
        self.assertTrue(mock_isdir.called)
        self.assertEqual(mock_exists.call_count, len(required_files))

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.join', side_effect=os.path.join)
    def test_directory_not_found(self, mock_join, mock_isdir, mock_exists):
        from src.checker import check_survival_kit
        mock_isdir.return_value = False # Mock rationale: Simulate the directory not existing.
        mock_exists.return_value = False # Mock rationale: Not relevant if directory doesn't exist, but good to set.

        directory = "/nonexistent/repo"
        required_files = ["README.md", "LICENSE"]
        result = check_survival_kit(directory, required_files)

        self.assertEqual(result['present'], [])
        self.assertEqual(result['missing'], ["README.md", "LICENSE"])
        self.assertEqual(result['score'], "0/2")
        self.assertEqual(result['status'], "DIRECTORY NOT FOUND")
        self.assertTrue(mock_isdir.called)
        self.assertFalse(mock_exists.called) # Should not call exists if dir doesn't exist

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.join', side_effect=os.path.join)
    def test_main_all_present(self, mock_join, mock_isdir, mock_exists, mock_exit, mock_stdout):
        from src.checker import main
        mock_isdir.return_value = True
        mock_exists.return_value = True # All files present

        # Mock rationale: Simulate command line arguments.
        with patch('sys.argv', ['checker.py', '/mock/repo', '--files', 'README.md', 'LICENSE']):
            main()
            mock_exit.assert_called_once_with(0) # Mock rationale: Expect successful exit code.
            output = mock_stdout.getvalue()
            self.assertIn("Status: READY", output)
            self.assertIn("Score: 2/2", output)
            self.assertIn("Present files: README.md, LICENSE", output)
            self.assertNotIn("Missing files", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.join', side_effect=os.path.join)
    def test_main_some_missing(self, mock_join, mock_isdir, mock_exists, mock_exit, mock_stdout):
        from src.checker import main
        mock_isdir.return_value = True
        # Mock rationale: Simulate README.md present, LICENSE missing.
        mock_exists.side_effect = lambda path: "README.md" in path

        with patch('sys.argv', ['checker.py', '/mock/repo', '--files', 'README.md', 'LICENSE']):
            main()
            mock_exit.assert_called_once_with(1) # Mock rationale: Expect failure exit code.
            output = mock_stdout.getvalue()
            self.assertIn("Status: NEEDS ATTENTION", output)
            self.assertIn("Score: 1/2", output)
            self.assertIn("Present files: README.md", output)
            self.assertIn("Missing files: LICENSE", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.join', side_effect=os.path.join)
    def test_main_directory_not_found(self, mock_join, mock_isdir, mock_exists, mock_exit, mock_stdout):
        from src.checker import main
        mock_isdir.return_value = False # Directory does not exist
        mock_exists.return_value = False

        with patch('sys.argv', ['checker.py', '/nonexistent/repo', '--files', 'README.md']):
            main()
            mock_exit.assert_called_once_with(1) # Mock rationale: Expect failure exit code.
            output = mock_stdout.getvalue()
            self.assertIn("Status: DIRECTORY NOT FOUND", output)
            self.assertIn("Score: 0/1", output)
            self.assertIn("Missing files: README.md", output)
            self.assertNotIn("Present files", output)

if __name__ == '__main__':
    unittest.main()
