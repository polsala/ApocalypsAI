import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import sys

# Add the src directory to the path to import detector.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from detector import find_future_files, main

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Define a fixed "current time" for deterministic tests
        self.fixed_current_time = datetime.datetime(2023, 10, 27, 10, 0, 0)
        self.fixed_current_timestamp = self.fixed_current_time.timestamp()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_no_future_files(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure where all files have past modification times.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log']),
            ('/test_dir/subdir', [], ['subfile.txt'])
        ]
        # Mock rationale: All files are older than the fixed current time.
        mock_getmtime.side_effect = [
            (self.fixed_current_time - datetime.timedelta(days=1)).timestamp(), # file1.txt
            (self.fixed_current_time - datetime.timedelta(hours=1)).timestamp(), # file2.log
            (self.fixed_current_time - datetime.timedelta(minutes=1)).timestamp() # subfile.txt
        ]

        anomalies = find_future_files(['/test_dir'], self.fixed_current_time)
        self.assertEqual(anomalies, [])
        mock_isdir.assert_called_with('/test_dir')
        mock_walk.assert_called_with('/test_dir')
        self.assertEqual(mock_getmtime.call_count, 3)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_one_future_file(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with one file having a future modification time.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['past_file.txt', 'future_file.log'])
        ]
        # Mock rationale: 'future_file.log' is newer than the fixed current time.
        mock_getmtime.side_effect = [
            (self.fixed_current_time - datetime.timedelta(days=1)).timestamp(), # past_file.txt
            (self.fixed_current_time + datetime.timedelta(hours=1)).timestamp()  # future_file.log
        ]

        anomalies = find_future_files(['/test_dir'], self.fixed_current_time)
        self.assertEqual(anomalies, ['/test_dir/future_file.log'])
        self.assertEqual(mock_getmtime.call_count, 2)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_multiple_future_files_in_subdirs(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a complex directory structure with multiple future files across subdirectories.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', ['subdir1', 'subdir2'], ['file_past.txt', 'file_future_root.txt']),
            ('/test_dir/subdir1', [], ['file_future_subdir1.log']),
            ('/test_dir/subdir2', [], ['file_past_subdir2.txt', 'file_future_subdir2.dat'])
        ]
        # Mock rationale: Assign specific timestamps to simulate future and past files.
        mock_getmtime.side_effect = [
            (self.fixed_current_time - datetime.timedelta(days=2)).timestamp(), # file_past.txt
            (self.fixed_current_time + datetime.timedelta(hours=2)).timestamp(), # file_future_root.txt
            (self.fixed_current_time + datetime.timedelta(minutes=30)).timestamp(), # file_future_subdir1.log
            (self.fixed_current_time - datetime.timedelta(hours=5)).timestamp(), # file_past_subdir2.txt
            (self.fixed_current_time + datetime.timedelta(days=1)).timestamp()  # file_future_subdir2.dat
        ]

        anomalies = find_future_files(['/test_dir'], self.fixed_current_time)
        expected_anomalies = [
            '/test_dir/file_future_root.txt',
            '/test_dir/subdir1/file_future_subdir1.log',
            '/test_dir/subdir2/file_future_subdir2.dat'
        ]
        self.assertCountEqual(anomalies, expected_anomalies)
        self.assertEqual(mock_getmtime.call_count, 5)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_file_modified_exactly_at_current_time(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test the strict inequality (mtime > current_timestamp).
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['exact_time_file.txt'])
        ]
        # Mock rationale: File modification time is exactly the current time.
        mock_getmtime.return_value = self.fixed_current_timestamp

        anomalies = find_future_files(['/test_dir'], self.fixed_current_time)
        self.assertEqual(anomalies, [])
        self.assertEqual(mock_getmtime.call_count, 1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_non_existent_directory(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a non-existent directory.
        mock_isdir.return_value = False # For '/non_existent_dir'
        mock_walk.return_value = [] # No files to walk if dir doesn't exist

        # Mock rationale: Capture stdout to check warning message.
        with patch('builtins.print') as mock_print:
            anomalies = find_future_files(['/non_existent_dir'], self.fixed_current_time)
            self.assertEqual(anomalies, [])
            mock_isdir.assert_called_with('/non_existent_dir')
            mock_walk.assert_not_called() # os.walk should not be called if isdir is False
            mock_print.assert_called_with("Warning: Directory not found or not a directory: /non_existent_dir")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_os_error_on_file_access(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate an OSError when accessing a file (e.g., permissions).
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file_ok.txt', 'file_error.txt'])
        ]
        # Mock rationale: One file raises an OSError, the other is fine.
        mock_getmtime.side_effect = [
            (self.fixed_current_time - datetime.timedelta(days=1)).timestamp(), # file_ok.txt
            OSError("Permission denied") # file_error.txt
        ]

        with patch('builtins.print') as mock_print:
            anomalies = find_future_files(['/test_dir'], self.fixed_current_time)
            self.assertEqual(anomalies, []) # No future files, just an error
            mock_print.assert_called_with("Error accessing file /test_dir/file_error.txt: Permission denied")
            self.assertEqual(mock_getmtime.call_count, 2)

    @patch('sys.argv', ['detector.py', '/test_dir'])
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('detector.find_future_files')
    def test_main_no_anomalies(self, mock_find_future_files, mock_exit, mock_print):
        # Mock rationale: Simulate `main` execution where no future files are found.
        mock_find_future_files.return_value = []
        mock_exit.side_effect = SystemExit # Prevent actual exit during test

        try:
            main()
        except SystemExit as e:
            self.assertEqual(e.code, 0) # Expect exit code 0 for success
        mock_find_future_files.assert_called_with(['/test_dir'])
        mock_print.assert_any_call("No temporal anomalies detected. All timestamps are in order.")

    @patch('sys.argv', ['detector.py', '/test_dir'])
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('detector.find_future_files')
    def test_main_with_anomalies(self, mock_find_future_files, mock_exit, mock_print):
        # Mock rationale: Simulate `main` execution where future files are found.
        mock_find_future_files.return_value = ['/test_dir/future_file.txt']
        mock_exit.side_effect = SystemExit # Prevent actual exit during test

        try:
            main()
        except SystemExit as e:
            self.assertEqual(e.code, 1) # Expect exit code 1 for failure (anomalies found)
        mock_find_future_files.assert_called_with(['/test_dir'])
        mock_print.assert_any_call("--- Temporal Anomalies Detected! ---")
        mock_print.assert_any_call("- /test_dir/future_file.txt")

    @patch('sys.argv', ['detector.py'])
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('detector.find_future_files')
    def test_main_no_args_defaults_to_current_dir(self, mock_find_future_files, mock_exit, mock_print):
        # Mock rationale: Simulate `main` execution with no directory arguments, expecting it to default to '.'
        mock_find_future_files.return_value = []
        mock_exit.side_effect = SystemExit

        try:
            main()
        except SystemExit as e:
            self.assertEqual(e.code, 0)
        mock_find_future_files.assert_called_with(['.'])
        mock_print.assert_any_call("Scanning directories: .")

if __name__ == '__main__':
    unittest.main()
