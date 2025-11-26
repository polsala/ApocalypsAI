import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the path to allow importing sweeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper

class TestDebrisSweeper(unittest.TestCase):

    def setUp(self):
        # Define a base time for consistent testing of file modification dates
        self.base_time = datetime(2023, 10, 26, 10, 0, 0)
        self.stale_days = 90

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_stale_files_found(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a file system structure and modification times
        # to test stale file detection deterministically without actual file I/O.
        
        # Simulate os.walk output: (dirpath, dirnames, filenames)
        mock_walk.return_value = [
            ('/repo', ['docs', 'src'], ['README.md']),
            ('/repo/docs', [], ['old_doc.txt', 'new_doc.md']),
            ('/repo/src', [], ['script.py']),
        ]

        # Simulate os.path.getmtime output for specific files
        # Files older than (self.base_time - timedelta(days=self.stale_days)) should be stale
        stale_threshold = self.base_time - timedelta(days=self.stale_days) # 2023-07-28
        
        def getmtime_side_effect(path):
            if path == '/repo/README.md':
                return (stale_threshold - timedelta(days=10)).timestamp() # Stale
            elif path == '/repo/docs/old_doc.txt':
                return (stale_threshold - timedelta(days=5)).timestamp() # Stale
            elif path == '/repo/docs/new_doc.md':
                return (self.base_time - timedelta(days=10)).timestamp() # Not stale
            elif path == '/repo/src/script.py':
                return (self.base_time - timedelta(days=50)).timestamp() # Not stale
            return self.base_time.timestamp() # Default for others

        mock_getmtime.side_effect = getmtime_side_effect

        # Mock datetime.now() to ensure consistent stale threshold calculation
        with patch('sweeper.datetime') as mock_dt:
            mock_dt.now.return_value = self.base_time
            mock_dt.fromtimestamp = datetime.fromtimestamp # Keep original fromtimestamp
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime constructor

            stale_files = sweeper.find_stale_files('/repo', self.stale_days)

            self.assertEqual(len(stale_files), 2)
            self.assertIn(('/repo/README.md', datetime.fromtimestamp((stale_threshold - timedelta(days=10)).timestamp())), stale_files)
            self.assertIn(('/repo/docs/old_doc.txt', datetime.fromtimestamp((stale_threshold - timedelta(days=5)).timestamp())), stale_files)

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_stale_files_none(self, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a file system where all files are recently modified,
        # ensuring no stale files are reported.
        mock_walk.return_value = [
            ('/repo', [], ['file1.txt']),
        ]
        mock_getmtime.return_value = (self.base_time - timedelta(days=10)).timestamp() # All recent

        with patch('sweeper.datetime') as mock_dt:
            mock_dt.now.return_value = self.base_time
            mock_dt.fromtimestamp = datetime.fromtimestamp
            mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

            stale_files = sweeper.find_stale_files('/repo', self.stale_days)
            self.assertEqual(len(stale_files), 0)

    @patch('os.listdir')
    @patch('os.walk')
    def test_find_empty_directories_found(self, mock_walk, mock_listdir):
        # Mock rationale: Simulate a file system with empty and non-empty directories
        # to test empty directory detection deterministically.
        
        # os.walk is used to traverse directories, but os.listdir is used to check emptiness.
        mock_walk.return_value = [
            ('/repo', ['empty_dir', 'non_empty_dir', 'another_empty'], []),
            ('/repo/empty_dir', [], []),
            ('/repo/non_empty_dir', [], ['file.txt']),
            ('/repo/another_empty', [], []),
        ]

        def listdir_side_effect(path):
            if path == '/repo/empty_dir':
                return []
            elif path == '/repo/non_empty_dir':
                return ['file.txt']
            elif path == '/repo/another_empty':
                return []
            elif path == '/repo': # Root directory is not empty
                return ['empty_dir', 'non_empty_dir', 'another_empty']
            return []

        mock_listdir.side_effect = listdir_side_effect

        empty_dirs = sweeper.find_empty_directories('/repo')
        self.assertEqual(len(empty_dirs), 2)
        self.assertIn('/repo/empty_dir', empty_dirs)
        self.assertIn('/repo/another_empty', empty_dirs)
        self.assertNotIn('/repo', empty_dirs) # Root should not be reported as empty

    @patch('os.listdir')
    @patch('os.walk')
    def test_find_empty_directories_none(self, mock_walk, mock_listdir):
        # Mock rationale: Simulate a file system where no directories are empty,
        # ensuring no empty directories are reported.
        mock_walk.return_value = [
            ('/repo', ['dir1'], ['file1.txt']),
            ('/repo/dir1', [], ['file2.txt']),
        ]
        
        def listdir_side_effect(path):
            if path == '/repo':
                return ['dir1', 'file1.txt']
            elif path == '/repo/dir1':
                return ['file2.txt']
            return []

        mock_listdir.side_effect = listdir_side_effect

        empty_dirs = sweeper.find_empty_directories('/repo')
        self.assertEqual(len(empty_dirs), 0)

    @patch('os.path.isdir', return_value=True)
    @patch('sweeper.find_stale_files', return_value=[])
    @patch('sweeper.find_empty_directories', return_value=[])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_debris(self, mock_exit, mock_print, mock_find_empty, mock_find_stale, mock_isdir):
        # Mock rationale: Test the main function's behavior when no debris is found,
        # including its output and exit code, without actual file system interaction.
        
        # Simulate command line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/repo', stale_days=90)):
            sweeper.main()
            mock_print.assert_any_call("No stale files found. Your digital archives are fresh!")
            mock_print.assert_any_call("No empty directories found. Your digital landscape is tidy!")
            mock_exit.assert_called_once_with(2) # Exit code 2 for no-op

    @patch('os.path.isdir', return_value=True)
    @patch('sweeper.find_stale_files')
    @patch('sweeper.find_empty_directories')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_with_debris(self, mock_exit, mock_print, mock_find_empty, mock_find_stale, mock_isdir):
        # Mock rationale: Test the main function's behavior when debris is found,
        # including its output and exit code, without actual file system interaction.
        
        mock_find_stale.return_value = [('/repo/old.txt', self.base_time - timedelta(days=100))]
        mock_find_empty.return_value = ['/repo/empty_folder']

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/repo', stale_days=90)):
            sweeper.main()
            mock_print.assert_any_call(f"--- Stale Files (not modified in 90 days) ---")
            mock_print.assert_any_call(f"- /repo/old.txt (Last modified: {(self.base_time - timedelta(days=100)).strftime('%Y-%m-%d')})")
            mock_print.assert_any_call("--- Empty Directories ---")
            mock_print.assert_any_call("- /repo/empty_folder/")
            mock_exit.assert_called_once_with(0) # Exit code 0 for findings

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_print, mock_isdir):
        # Mock rationale: Test the main function's error handling for an invalid path,
        # ensuring it prints an error and exits with code 1.
        
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/nonexistent', stale_days=90)):
            sweeper.main()
            mock_print.assert_any_call("Error: The provided path '/nonexistent' is not a valid directory.")
            mock_exit.assert_called_once_with(1) # Exit code 1 for failure

if __name__ == '__main__':
    unittest.main()
