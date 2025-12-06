import unittest
import os
import tempfile
import shutil
import datetime
from unittest.mock import patch, MagicMock
import time

# Import the functions from the reclaimer script
import sys
# Add the src directory to the path to import reclaimer.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import reclaimer

class TestRubbleRouserResourceReclaimer(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create some test files and directories
        os.makedirs('dir1/subdirA', exist_ok=True)
        os.makedirs('dir1/subdirB', exist_ok=True)
        os.makedirs('dir2', exist_ok=True)
        os.makedirs('empty_dir', exist_ok=True)
        os.makedirs('another_empty_dir', exist_ok=True)

        # Create files with content for hash calculation
        with open('dir1/fileA.txt', 'w') as f: f.write('content1')
        with open('dir1/subdirA/fileB.txt', 'w') as f: f.write('content2')
        with open('dir2/fileC.txt', 'w') as f: f.write('content1') # Duplicate of fileA.txt
        with open('dir2/fileD.txt', 'w') as f: f.write('unique_content')
        with open('dir1/subdirB/fileE.txt', 'w') as f: f.write('content2') # Duplicate of fileB.txt
        with open('old_file.log', 'w') as f: f.write('old logs')
        with open('recent_file.log', 'w') as f: f.write('recent logs')

        # Set modification times for old_file.log and recent_file.log
        # Mock rationale: We need deterministic file modification times for 'old file' detection.
        # We set specific times to ensure 'old_file.log' is older than our test threshold.
        # We use time.mktime to convert datetime objects to epoch seconds.
        old_time = datetime.datetime.now() - datetime.timedelta(days=30)
        os.utime('old_file.log', (old_time.timestamp(), old_time.timestamp()))

        recent_time = datetime.datetime.now() - datetime.timedelta(days=1)
        os.utime('recent_file.log', (recent_time.timestamp(), recent_time.timestamp()))

    def tearDown(self):
        # Clean up the temporary directory
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_find_duplicates(self, mock_print):
        duplicates = reclaimer.find_duplicates(self.test_dir)
        # Expecting fileA.txt and fileC.txt to be duplicates (content1)
        # Expecting fileB.txt and fileE.txt to be duplicates (content2)
        self.assertEqual(len(duplicates), 4) # Two groups of two files
        
        # Check if specific files are in the duplicates list
        self.assertIn(os.path.join(self.test_dir, 'dir1', 'fileA.txt'), duplicates)
        self.assertIn(os.path.join(self.test_dir, 'dir2', 'fileC.txt'), duplicates)
        self.assertIn(os.path.join(self.test_dir, 'dir1', 'subdirA', 'fileB.txt'), duplicates)
        self.assertIn(os.path.join(self.test_dir, 'dir1', 'subdirB', 'fileE.txt'), duplicates)

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_find_empty_dirs(self, mock_print):
        empty_dirs = reclaimer.find_empty_dirs(self.test_dir)
        # Expecting 'empty_dir' and 'another_empty_dir' to be empty
        self.assertEqual(len(empty_dirs), 2)
        self.assertIn(os.path.join(self.test_dir, 'empty_dir'), empty_dirs)
        self.assertIn(os.path.join(self.test_dir, 'another_empty_dir'), empty_dirs)

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_find_old_files(self, mock_print):
        # We set old_file.log to be 30 days old, so it should be found if threshold is < 30
        old_files = reclaimer.find_old_files(self.test_dir, 15) # Find files older than 15 days
        self.assertEqual(len(old_files), 1)
        self.assertIn(os.path.join(self.test_dir, 'old_file.log'), old_files)

        # Test with a higher threshold, should find no files
        old_files_none = reclaimer.find_old_files(self.test_dir, 45) # Find files older than 45 days
        self.assertEqual(len(old_files_none), 0)

    @patch('os.remove') # Mock rationale: Prevent actual file deletion during tests.
    @patch('os.rmdir') # Mock rationale: Prevent actual directory deletion during tests.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_delete_items(self, mock_print, mock_rmdir, mock_remove):
        # Create dummy files/dirs to 'delete'
        file_to_delete = os.path.join(self.test_dir, 'temp_file.txt')
        dir_to_delete = os.path.join(self.test_dir, 'temp_dir')
        with open(file_to_delete, 'w') as f: f.write('temp')
        os.makedirs(dir_to_delete)

        items = [file_to_delete, dir_to_delete]
        reclaimer.delete_items(items, 'test_item')

        mock_remove.assert_called_once_with(file_to_delete)
        mock_rmdir.assert_called_once_with(dir_to_delete)

    @patch('sys.argv', ['reclaimer.py', '--duplicates', '--path', '.'])
    @patch('reclaimer.find_duplicates', return_value=['file1', 'file2']) # Mock rationale: Control the output of find_duplicates for main function test.
    @patch('reclaimer.find_empty_dirs', return_value=[]) # Mock rationale: Ensure other functions don't interfere.
    @patch('reclaimer.find_old_files', return_value=[]) # Mock rationale: Ensure other functions don't interfere.
    @patch('reclaimer.delete_items') # Mock rationale: Prevent actual deletion during main function test.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_main_duplicates_no_delete(self, mock_print, mock_delete_items, mock_find_old_files, mock_find_empty_dirs, mock_find_duplicates):
        reclaimer.main()
        mock_find_duplicates.assert_called_once_with(os.path.abspath('.'))
        mock_delete_items.assert_not_called()

    @patch('sys.argv', ['reclaimer.py', '--empty-dirs', '--path', '.', '--delete'])
    @patch('reclaimer.find_duplicates', return_value=[]) # Mock rationale: Ensure other functions don't interfere.
    @patch('reclaimer.find_empty_dirs', return_value=['empty_dir_path']) # Mock rationale: Control the output of find_empty_dirs for main function test.
    @patch('reclaimer.find_old_files', return_value=[]) # Mock rationale: Ensure other functions don't interfere.
    @patch('reclaimer.delete_items') # Mock rationale: Prevent actual deletion during main function test.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_main_empty_dirs_with_delete(self, mock_print, mock_delete_items, mock_find_old_files, mock_find_empty_dirs, mock_find_duplicates):
        reclaimer.main()
        mock_find_empty_dirs.assert_called_once_with(os.path.abspath('.'))
        mock_delete_items.assert_called_once_with(['empty_dir_path'], 'item')

    @patch('sys.argv', ['reclaimer.py', '--old-files', '10', '--path', '.'])
    @patch('reclaimer.find_duplicates', return_value=[]) # Mock rationale: Ensure other functions don't interfere.
    @patch('reclaimer.find_empty_dirs', return_value=[]) # Mock rationale: Ensure other functions don't interfere.
    @patch('reclaimer.find_old_files', return_value=['old_file_path']) # Mock rationale: Control the output of find_old_files for main function test.
    @patch('reclaimer.delete_items') # Mock rationale: Prevent actual deletion during main function test.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_main_old_files_no_delete(self, mock_print, mock_delete_items, mock_find_old_files, mock_find_empty_dirs, mock_find_duplicates):
        reclaimer.main()
        mock_find_old_files.assert_called_once_with(os.path.abspath('.'), 10)
        mock_delete_items.assert_not_called()

    @patch('sys.argv', ['reclaimer.py'])
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    @patch('argparse.ArgumentParser.print_help') # Mock rationale: Prevent argparse from printing help to stdout during test.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_no_args_exits(self, mock_exit, mock_print_help, mock_print):
        reclaimer.main()
        mock_print_help.assert_called_once()
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['reclaimer.py', '--duplicates', '--path', 'non_existent_dir'])
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_invalid_path_exits(self, mock_exit, mock_print):
        reclaimer.main()
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
