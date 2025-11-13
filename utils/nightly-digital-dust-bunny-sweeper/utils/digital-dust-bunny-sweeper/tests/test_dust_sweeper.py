import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime, timedelta

# Adjust sys.path to allow importing the module under test
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_sweeper import find_dust_bunnies, main

class TestDustSweeper(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_empty_directory_detection(self, mock_datetime, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with an empty folder.
        # os.path.isdir: Ensure the root directory is considered valid.
        # os.walk: Provide a specific directory structure where '/root/empty_folder' has no subdirs or files.
        # os.path.getsize, os.path.getmtime, datetime.datetime: Mocked for completeness, but not directly relevant for empty dir logic.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', ['empty_folder'], []), # /root contains empty_folder
            ('/root/empty_folder', [], [])  # /root/empty_folder is empty
        ]
        mock_getsize.return_value = 100 # Default size for any file if checked
        mock_getmtime.return_value = (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=10)).timestamp()
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp # Allow real conversion

        bunnies = find_dust_bunnies('/root')
        self.assertIn('[EMPTY DIRECTORY] /root/empty_folder', bunnies)
        self.assertEqual(len(bunnies), 1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_zero_byte_file_detection(self, mock_datetime, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file system with a zero-byte file.
        # os.path.isdir: Ensure the root directory is considered valid.
        # os.walk: Provide a file structure including a zero-byte file ('zero.txt').
        # os.path.getsize: Return 0 for 'zero.txt' and a normal size for 'normal.txt'.
        # os.path.getmtime, datetime.datetime: Mocked for completeness.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', [], ['zero.txt', 'normal.txt'])
        ]
        # Configure getsize to return 0 for 'zero.txt' and a normal size for 'normal.txt'
        def mock_getsize_side_effect(path):
            if path == '/root/zero.txt':
                return 0
            return 100
        mock_getsize.side_effect = mock_getsize_side_effect

        mock_getmtime.return_value = (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=10)).timestamp()
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp

        bunnies = find_dust_bunnies('/root')
        self.assertIn('[ZERO-BYTE FILE] /root/zero.txt (0 bytes)', bunnies)
        self.assertEqual(len(bunnies), 1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_old_log_file_detection(self, mock_datetime, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file system with an old log file.
        # os.path.isdir: Ensure the root directory is valid.
        # os.walk: Provide a file structure including an old log file ('app.log') and a recent one ('recent.log').
        # os.path.getmtime: Return a timestamp for 'app.log' that is older than the threshold, and 'recent.log' newer.
        # datetime.datetime.now: Control the current time for age comparison to ensure determinism.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root/logs', [], ['app.log', 'recent.log'])
        ]
        mock_getsize.return_value = 100 # Default size

        # Set current time to a known point for deterministic age calculation
        current_time = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = current_time
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp # Allow real conversion from timestamp

        # Simulate modification times: app.log is old (35 days ago), recent.log is new (5 days ago)
        old_log_mtime = (current_time - timedelta(days=35)).timestamp()
        recent_log_mtime = (current_time - timedelta(days=5)).timestamp()

        def mock_getmtime_side_effect(path):
            if path == '/root/logs/app.log':
                return old_log_mtime
            elif path == '/root/logs/recent.log':
                return recent_log_mtime
            return current_time.timestamp() # Default for other files if checked
        mock_getmtime.side_effect = mock_getmtime_side_effect

        bunnies = find_dust_bunnies('/root', age_threshold_days=30)
        expected_mtime_str = datetime.fromtimestamp(old_log_mtime).strftime('%Y-%m-%d %H:%M:%S')
        self.assertIn(f'[OLD LOG FILE] /root/logs/app.log (Last modified: {expected_mtime_str})', bunnies)
        self.assertEqual(len(bunnies), 1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_system_junk_detection(self, mock_datetime, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file system with common system junk files.
        # os.path.isdir: Ensure the root directory is valid.
        # os.walk: Provide a file structure including '.DS_Store', 'Thumbs.db', and 'desktop.ini'.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', [], ['.DS_Store', 'Thumbs.db', 'desktop.ini', 'normal_file.txt'])
        ]
        mock_getsize.return_value = 100 # Default size
        mock_getmtime.return_value = (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=10)).timestamp()
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp

        bunnies = find_dust_bunnies('/root')
        self.assertIn('[SYSTEM JUNK] /root/.DS_Store', bunnies)
        self.assertIn('[SYSTEM JUNK] /root/Thumbs.db', bunnies)
        self.assertIn('[SYSTEM JUNK] /root/desktop.ini', bunnies)
        self.assertEqual(len(bunnies), 3)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_no_dust_bunnies(self, mock_datetime, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a clean directory with no dust bunnies.
        # os.path.isdir: Ensure the root directory is valid.
        # os.walk: Provide a clean file structure (no empty dirs, zero-byte files, old logs, or junk files).

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', ['sub_dir'], ['file1.txt', 'file2.log']),
            ('/root/sub_dir', [], ['another_file.txt'])
        ]
        mock_getsize.return_value = 100 # All files have non-zero size
        # Ensure log file is not old
        current_time = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = current_time
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_getmtime.return_value = (current_time - timedelta(days=5)).timestamp() # Not older than 30 days

        bunnies = find_dust_bunnies('/root')
        self.assertEqual(len(bunnies), 0)

    @patch('os.path.isdir')
    @patch('sys.argv', ['dust_sweeper.py', '/test/path'])
    @patch('builtins.print')
    @patch('dust_sweeper.find_dust_bunnies')
    def test_main_with_bunnies(self, mock_find_bunnies, mock_print, mock_isdir):
        # Mock rationale: Test the main function's output when dust bunnies are found.
        # sys.argv: Simulate command-line arguments to specify a directory.
        # builtins.print: Capture print calls to verify the console output.
        # find_dust_bunnies: Mock the core logic to return known results, isolating main's behavior.
        # os.path.isdir: Ensure the path is valid for main's initial check.

        mock_isdir.return_value = True
        mock_find_bunnies.return_value = [
            '[EMPTY DIRECTORY] /test/path/empty',
            '[ZERO-BYTE FILE] /test/path/zero.txt (0 bytes)'
        ]
        main()
        mock_print.assert_any_call('Scanning /test/path...\n')
        mock_print.assert_any_call('🧹 Digital Dust Bunny Report for /test/path 🧹\n')
        mock_print.assert_any_call('[EMPTY DIRECTORY] /test/path/empty')
        mock_print.assert_any_call('\nFound 2 digital dust bunnies. Time to tidy up!')

    @patch('os.path.isdir')
    @patch('sys.argv', ['dust_sweeper.py', '/test/path'])
    @patch('builtins.print')
    @patch('dust_sweeper.find_dust_bunnies')
    def test_main_no_bunnies(self, mock_find_bunnies, mock_print, mock_isdir):
        # Mock rationale: Test the main function's output when no dust bunnies are found.
        # sys.argv, builtins.print, find_dust_bunnies, os.path.isdir: Same as above.

        mock_isdir.return_value = True
        mock_find_bunnies.return_value = []
        main()
        mock_print.assert_any_call('Scanning /test/path...\n')
        mock_print.assert_any_call('🧹 Digital Dust Bunny Report for /test/path 🧹\n')
        mock_print.assert_any_call('No digital dust bunnies found. Your digital space is sparkling clean!')

    @patch('os.path.isdir')
    @patch('sys.argv', ['dust_sweeper.py']) # No directory argument
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_args(self, mock_exit, mock_print, mock_isdir):
        # Mock rationale: Test main function's error handling for missing command-line arguments.
        # sys.argv: Simulate running the script without a directory argument.
        # builtins.print: Capture print calls to verify the usage message.
        # sys.exit: Capture the exit call to confirm the script terminates with an error code.

        main()
        mock_print.assert_any_call('Usage: python src/dust_sweeper.py <directory_to_scan>', file=sys.stderr)
        mock_exit.assert_called_once_with(1)

    @patch('os.path.isdir')
    @patch('sys.argv', ['dust_sweeper.py', '/non/existent/path'])
    @patch('builtins.print')
    @patch('dust_sweeper.find_dust_bunnies') # This will be called, but isdir will make it return empty
    def test_main_invalid_path(self, mock_find_bunnies, mock_print, mock_isdir):
        # Mock rationale: Test main function's behavior when an invalid path is provided.
        # os.path.isdir: Simulate that the provided path does not exist or is not a directory.
        # find_dust_bunnies: Will be called, but its internal check for isdir will cause it to print an error and return an empty list.

        mock_isdir.return_value = False
        main()
        mock_print.assert_any_call('Error: Directory not found or not a directory: /non/existent/path', file=sys.stderr)
        mock_print.assert_any_call('🧹 Digital Dust Bunny Report for /non/existent/path 🧹\n')
        mock_print.assert_any_call('No digital dust bunnies found. Your digital space is sparkling clean!') # This is because find_dust_bunnies returns empty list on error.

if __name__ == '__main__':
    unittest.main()
