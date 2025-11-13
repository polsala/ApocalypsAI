import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested, assuming tests are run from the utility's root directory
from src.sweeper import find_empty_directories, find_old_files, main

class TestSweeper(unittest.TestCase):

    @patch('os.walk')
    # Mock rationale: os.walk is a generator that traverses the file system. Mocking it allows us to define a virtual file system structure for testing without touching actual files.
    def test_find_empty_directories(self, mock_os_walk):
        # Scenario 1: No empty directories
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['fileA.txt']),
            ('/root/dir1', [], ['fileB.txt']),
            ('/root/dir2', ['subdir'], []),
            ('/root/dir2/subdir', [], ['fileC.txt'])
        ]
        self.assertEqual(find_empty_directories('/root'), [])

        # Scenario 2: With empty directories
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'empty_dir1', 'dir2'], ['fileA.txt']),
            ('/root/dir1', [], ['fileB.txt']),
            ('/root/empty_dir1', [], []),
            ('/root/dir2', ['subdir', 'empty_dir2'], []),
            ('/root/dir2/subdir', [], ['fileC.txt']),
            ('/root/dir2/empty_dir2', [], [])
        ]
        expected_empty = [
            '/root/empty_dir1',
            '/root/dir2/empty_dir2'
        ]
        self.assertCountEqual(find_empty_directories('/root'), expected_empty)

        # Scenario 3: Nested empty directories
        mock_os_walk.return_value = [
            ('/root', ['parent_empty'], []),
            ('/root/parent_empty', ['child_empty'], []),
            ('/root/parent_empty/child_empty', [], [])
        ]
        expected_empty_nested = [
            '/root/parent_empty/child_empty',
            '/root/parent_empty'
        ]
        self.assertCountEqual(find_empty_directories('/root'), expected_empty_nested)

    @patch('os.walk')
    # Mock rationale: os.walk is used to traverse the directory structure.
    @patch('os.path.isfile')
    # Mock rationale: os.path.isfile is used to confirm if a path points to a file, preventing errors if a directory or broken symlink is encountered.
    @patch('os.path.getmtime')
    # Mock rationale: os.path.getmtime retrieves the last modification time of a file. Mocking it allows us to control file ages for deterministic testing.
    def test_find_old_files(self, mock_getmtime, mock_isfile, mock_os_walk):
        current_time = time.time()
        # Define timestamps for files relative to current_time
        recent_file_time = current_time - timedelta(days=10).total_seconds()
        old_file_time = current_time - timedelta(days=100).total_seconds()
        very_old_file_time = current_time - timedelta(days=200).total_seconds()

        # Mock os.walk to return a specific file structure
        mock_os_walk.return_value = [
            ('/root', [], ['recent.txt', 'old.log', 'very_old.bak']),
            ('/root/subdir', [], ['another_recent.py', 'another_old.csv'])
        ]

        # Mock os.path.isfile for all paths that are files
        mock_isfile.side_effect = lambda p: p in [
            '/root/recent.txt', '/root/old.log', '/root/very_old.bak',
            '/root/subdir/another_recent.py', '/root/subdir/another_old.csv'
        ]

        # Mock os.path.getmtime for each file
        def getmtime_side_effect(path):
            if path == '/root/recent.txt': return recent_file_time
            if path == '/root/old.log': return old_file_time
            if path == '/root/very_old.bak': return very_old_file_time
            if path == '/root/subdir/another_recent.py': return recent_file_time
            if path == '/root/subdir/another_old.csv': return old_file_time
            return current_time # Default for unexpected paths

        mock_getmtime.side_effect = getmtime_side_effect

        # Test with a threshold of 90 days
        # Expected: old.log, very_old.bak, another_old.csv
        old_files = find_old_files('/root', 90)
        expected_files = [
            ('/root/old.log', datetime.fromtimestamp(old_file_time).strftime('%Y-%m-%d')),
            ('/root/very_old.bak', datetime.fromtimestamp(very_old_file_time).strftime('%Y-%m-%d')),
            ('/root/subdir/another_old.csv', datetime.fromtimestamp(old_file_time).strftime('%Y-%m-%d'))
        ]
        self.assertCountEqual(old_files, expected_files)

        # Test with a threshold of 150 days
        # Expected: very_old.bak
        old_files_150 = find_old_files('/root', 150)
        expected_files_150 = [
            ('/root/very_old.bak', datetime.fromtimestamp(very_old_file_time).strftime('%Y-%m-%d'))
        ]
        self.assertCountEqual(old_files_150, expected_files_150)

        # Test with a threshold of 5 days (all files should be old)
        old_files_5 = find_old_files('/root', 5)
        expected_files_5 = [
            ('/root/recent.txt', datetime.fromtimestamp(recent_file_time).strftime('%Y-%m-%d')),
            ('/root/old.log', datetime.fromtimestamp(old_file_time).strftime('%Y-%m-%d')),
            ('/root/very_old.bak', datetime.fromtimestamp(very_old_file_time).strftime('%Y-%m-%d')),
            ('/root/subdir/another_recent.py', datetime.fromtimestamp(recent_file_time).strftime('%Y-%m-%d')),
            ('/root/subdir/another_old.csv', datetime.fromtimestamp(old_file_time).strftime('%Y-%m-%d'))
        ]
        self.assertCountEqual(old_files_5, expected_files_5)

    @patch('os.path.isdir')
    # Mock rationale: os.path.isdir checks if a given path is a directory. Mocking it allows us to simulate valid/invalid input paths for the main function.
    @patch('src.sweeper.find_empty_directories')
    # Mock rationale: We want to test the main function's orchestration, not re-test the internal logic of find_empty_directories. Mocking it isolates the test.
    @patch('src.sweeper.find_old_files')
    # Mock rationale: Similar to find_empty_directories, we mock this to isolate the main function's behavior.
    @patch('builtins.print')
    # Mock rationale: The main function prints output to stdout. Mocking print allows us to capture and assert on the printed messages without affecting the console.
    @patch('argparse.ArgumentParser.parse_args')
    # Mock rationale: argparse.ArgumentParser.parse_args parses command-line arguments. Mocking it allows us to programmatically set arguments for testing the main function's different execution paths.
    def test_main_function(self, mock_parse_args, mock_print, mock_find_old_files, mock_find_empty_directories, mock_isdir):
        # Scenario 1: No dust bunnies found
        mock_parse_args.return_value = MagicMock(path='/test/path', age_threshold=90)
        mock_isdir.return_value = True
        mock_find_empty_directories.return_value = []
        mock_find_old_files.return_value = []

        main()
        mock_print.assert_any_call("Your workspace is sparkling clean! No digital dust bunnies found.")

        # Scenario 2: Empty directories found
        mock_find_empty_directories.return_value = ['/test/path/empty1', '/test/path/empty2']
        mock_find_old_files.return_value = []

        main()
        mock_print.assert_any_call("🧹 /test/path/empty1/")
        mock_print.assert_any_call("🧹 /test/path/empty2/")
        mock_print.assert_any_call("No ancient files found. Your files are spry!")
        mock_print.assert_any_call("Time to consider some tidying up! (Remember, I only report, I don't delete!)")

        # Scenario 3: Old files found
        mock_find_empty_directories.return_value = []
        mock_find_old_files.return_value = [
            ('/test/path/old_file.txt', '2023-01-01'),
            ('/test/path/another_old.log', '2022-11-15')
        ]

        main()
        mock_print.assert_any_call("No empty directories found. Good job!")
        mock_print.assert_any_call("⏳ /test/path/old_file.txt (Last modified: 2023-01-01)")
        mock_print.assert_any_call("⏳ /test/path/another_old.log (Last modified: 2022-11-15)")
        mock_print.assert_any_call("Time to consider some tidying up! (Remember, I only report, I don't delete!)")

        # Scenario 4: Both empty dirs and old files found
        mock_find_empty_directories.return_value = ['/test/path/empty_combo']
        mock_find_old_files.return_value = [('/test/path/old_combo.txt', '2023-03-01')]

        main()
        mock_print.assert_any_call("🧹 /test/path/empty_combo/")
        mock_print.assert_any_call("⏳ /test/path/old_combo.txt (Last modified: 2023-03-01)")
        mock_print.assert_any_call("Time to consider some tidying up! (Remember, I only report, I don't delete!)")

        # Scenario 5: Invalid path
        mock_isdir.return_value = False
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Error: The path '/test/path' does not exist or is not a directory.")

if __name__ == '__main__':
    unittest.main()
