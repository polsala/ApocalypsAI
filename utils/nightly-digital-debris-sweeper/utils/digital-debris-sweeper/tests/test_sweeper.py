import unittest
import os
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Import the function to be tested
# Assuming sweeper.py is in the parent directory relative to tests/
# For self-contained execution, we'll mock os.path.join to ensure paths are consistent
# and directly import the function.
# In a real scenario, sys.path manipulation might be needed, but for a self-contained
# utility, direct import or relative import is fine if structure is fixed.
# Let's assume the test runner is invoked from utils/digital-debris-sweeper/
# so `from src.sweeper import find_digital_debris` works.
try:
    from src.sweeper import find_digital_debris
except ImportError:
    # Fallback for different test runner contexts, e.g., if run from project root
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from src.sweeper import find_digital_debris


class TestDigitalDebrisSweeper(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_empty_directory(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with an empty folder.
        # os.path.isdir is mocked to confirm the base path exists.
        # os.walk is mocked to return tuples representing directory traversal.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', ['empty_dir'], []),
            ('/mock/path/empty_dir', [], []) # This represents an empty directory
        ]
        
        debris = find_digital_debris(['/mock/path'])
        self.assertIn("Empty Directory: /mock/path/empty_dir", debris)
        self.assertEqual(len(debris), 1)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_orphaned_metadata_file(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with a .DS_Store file.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['.DS_Store', 'regular_file.txt'])
        ]
        
        debris = find_digital_debris(['/mock/path'])
        self.assertIn("Orphaned Metadata: /mock/path/.DS_Store", debris)
        self.assertEqual(len(debris), 1)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_cache_directory(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with a __pycache__ folder.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', ['__pycache__'], []),
            ('/mock/path/__pycache__', [], ['file.pyc'])
        ]
        
        debris = find_digital_debris(['/mock/path'])
        self.assertIn("Cache Directory: /mock/path/__pycache__", debris)
        self.assertEqual(len(debris), 1)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_temporary_file(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with a .tmp file.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['report.tmp', 'data.csv'])
        ]
        
        debris = find_digital_debris(['/mock/path'])
        self.assertIn("Temporary File: /mock/path/report.tmp", debris)
        self.assertEqual(len(debris), 1)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_multiple_debris_types(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a complex directory structure with multiple debris types.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/project', ['src', 'build', 'docs', 'empty_logs'], ['.DS_Store', 'config.log']),
            ('/mock/project/src', ['__pycache__'], ['main.py']),
            ('/mock/project/src/__pycache__', [], ['main.pyc']),
            ('/mock/project/build', [], ['app.exe', 'temp.tmp']),
            ('/mock/project/docs', [], ['README.md']),
            ('/mock/project/empty_logs', [], []) # Empty directory
        ]
        
        debris = find_digital_debris(['/mock/project'])
        self.assertIn("Orphaned Metadata: /mock/project/.DS_Store", debris)
        self.assertIn("Temporary File: /mock/project/config.log", debris)
        self.assertIn("Cache Directory: /mock/project/src/__pycache__", debris)
        self.assertIn("Temporary File: /mock/project/build/temp.tmp", debris)
        self.assertIn("Empty Directory: /mock/project/empty_logs", debris)
        self.assertEqual(len(debris), 5)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_no_debris(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a clean directory with no debris.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/clean_project', ['src'], ['README.md']),
            ('/mock/clean_project/src', [], ['main.py'])
        ]
        
        debris = find_digital_debris(['/mock/clean_project'])
        self.assertEqual(len(debris), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('sys.stderr', new_callable=StringIO)
    def test_invalid_path(self, mock_stderr, mock_walk, mock_isdir):
        # Mock rationale: Test behavior when an invalid path is provided.
        # os.path.isdir is mocked to return False for the invalid path.
        # sys.stderr is captured to check warning messages.
        mock_isdir.return_value = False # Simulate path not existing
        
        debris = find_digital_debris(['/mock/nonexistent_path'])
        self.assertEqual(len(debris), 0)
        self.assertIn("Warning: Path '/mock/nonexistent_path' is not a directory or does not exist. Skipping.", mock_stderr.getvalue())

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('sys.argv', ['sweeper.py', '/mock/path'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_args(self, mock_stdout, mock_walk, mock_isdir):
        # Mock rationale: Test the main function's behavior when command-line arguments are provided.
        # sys.argv is mocked to simulate command-line arguments.
        # sys.stdout is captured to check the output.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/path', [], ['.DS_Store'])
        ]
        
        from src.sweeper import main # Re-import main to ensure sys.argv patch is applied
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Scanning /mock/path for digital debris...", output)
        self.assertIn("Orphaned Metadata: /mock/path/.DS_Store", output)
        self.assertIn("Scan complete.", output)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.getcwd', return_value='/mock/current_dir')
    @patch('sys.argv', ['sweeper.py']) # No args, should use getcwd
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_args(self, mock_stdout, mock_getcwd, mock_walk, mock_isdir):
        # Mock rationale: Test the main function's behavior when no command-line arguments are provided.
        # os.getcwd is mocked to control the default scan path.
        # sys.argv is mocked to simulate no command-line arguments.
        # sys.stdout is captured to check the output.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/current_dir', [], ['report.log'])
        ]
        
        from src.sweeper import main # Re-import main to ensure sys.argv patch is applied
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Scanning /mock/current_dir for digital debris...", output)
        self.assertIn("Temporary File: /mock/current_dir/report.log", output)
        self.assertIn("Scan complete.", output)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('sys.argv', ['sweeper.py', '/mock/clean_path'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_debris_found(self, mock_stdout, mock_walk, mock_isdir):
        # Mock rationale: Test the main function's output when no debris is found.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/clean_path', [], ['file.txt'])
        ]
        
        from src.sweeper import main
        main()
        output = mock_stdout.getvalue()
        self.assertIn("No significant digital debris found. Your digital wasteland is surprisingly clean!", output)
        self.assertIn("Scan complete.", output)


if __name__ == '__main__':
    unittest.main()
