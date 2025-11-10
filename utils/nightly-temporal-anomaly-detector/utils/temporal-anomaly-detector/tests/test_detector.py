import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
from src.detector import find_temporal_anomalies, main

class TestTemporalAnomalyDetector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_no_anomalies(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with files, none of which have future mtimes.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]
        
        # Set current time to a specific point
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        
        # Set mtimes to be in the past
        mock_getmtime.side_effect = [
            datetime.datetime(2023, 10, 25, 9, 0, 0).timestamp(), # file1.txt
            datetime.datetime(2023, 10, 25, 11, 0, 0).timestamp() # file2.log
        ]

        anomalies = list(find_temporal_anomalies('/test_dir'))
        self.assertEqual(len(anomalies), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_single_anomaly(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with one file having a future mtime.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['future_file.txt', 'past_file.log'])
        ]
        
        # Set current time
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        
        # Set mtimes: one in future, one in past
        mock_getmtime.side_effect = [
            datetime.datetime(2023, 10, 27, 9, 0, 0).timestamp(),  # future_file.txt
            datetime.datetime(2023, 10, 25, 11, 0, 0).timestamp() # past_file.log
        ]

        anomalies = list(find_temporal_anomalies('/test_dir'))
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0][0], os.path.join('/test_dir', 'future_file.txt'))
        self.assertEqual(anomalies[0][1], datetime.datetime(2023, 10, 27, 9, 0, 0))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_multiple_anomalies_in_subdirs(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with multiple future mtimes across subdirectories.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', ['subdir1', 'subdir2'], ['file0.txt']),
            ('/test_dir/subdir1', [], ['file1.txt']),
            ('/test_dir/subdir2', [], ['file2.txt', 'file3.txt'])
        ]
        
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        
        mock_getmtime.side_effect = [
            datetime.datetime(2023, 10, 25, 9, 0, 0).timestamp(),  # file0.txt (past)
            datetime.datetime(2023, 10, 27, 9, 0, 0).timestamp(),  # file1.txt (future)
            datetime.datetime(2023, 10, 28, 10, 0, 0).timestamp(), # file2.txt (future)
            datetime.datetime(2023, 10, 25, 11, 0, 0).timestamp() # file3.txt (past)
        ]

        anomalies = list(find_temporal_anomalies('/test_dir'))
        self.assertEqual(len(anomalies), 2)
        self.assertIn((os.path.join('/test_dir', 'subdir1', 'file1.txt'), datetime.datetime(2023, 10, 27, 9, 0, 0)), anomalies)
        self.assertIn((os.path.join('/test_dir', 'subdir2', 'file2.txt'), datetime.datetime(2023, 10, 28, 10, 0, 0)), anomalies)

    @patch('os.path.isdir')
    def test_directory_not_found(self, mock_isdir):
        # Mock rationale: Simulate the scenario where the target directory does not exist.
        mock_isdir.return_value = False
        with self.assertRaises(FileNotFoundError):
            list(find_temporal_anomalies('/non_existent_dir'))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=MagicMock) # Capture stdout for main function tests
    @patch('sys.stderr', new_callable=MagicMock) # Capture stderr for main function tests
    def test_main_no_anomalies(self, mock_stderr, mock_stdout, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test the main function's output when no anomalies are found.
        mock_isdir.return_value = True
        mock_walk.return_value = [('/test_dir', [], ['file1.txt'])]
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_getmtime.return_value = datetime.datetime(2023, 10, 25, 9, 0, 0).timestamp()

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/test_dir')):
            main()
            mock_stdout.assert_any_call("Scanning '/test_dir' for temporal anomalies...")
            mock_stdout.assert_any_call("No temporal anomalies detected. All clear!")
            self.assertEqual(mock_stderr.call_count, 0) # No errors should be printed to stderr

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_main_with_anomalies(self, mock_stderr, mock_stdout, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test the main function's output when anomalies are found.
        mock_isdir.return_value = True
        mock_walk.return_value = [('/test_dir', [], ['future_file.txt'])]
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_getmtime.return_value = datetime.datetime(2023, 10, 27, 9, 0, 0).timestamp()

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/test_dir')):
            main()
            mock_stdout.assert_any_call("Scanning '/test_dir' for temporal anomalies...")
            mock_stdout.assert_any_call(f"ANOMALY DETECTED: '{os.path.join('/test_dir', 'future_file.txt')}' has future modification time: {datetime.datetime(2023, 10, 27, 9, 0, 0)}")
            self.assertEqual(mock_stderr.call_count, 0)

    @patch('os.path.isdir')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    def test_main_directory_not_found_error(self, mock_exit, mock_stderr, mock_stdout, mock_isdir):
        # Mock rationale: Test the main function's error handling for a non-existent directory.
        mock_isdir.return_value = False
        
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/non_existent_dir')):
            main()
            mock_stderr.assert_any_call("Error: Directory not found: /non_existent_dir")
            mock_exit.assert_called_once_with(1)
            self.assertEqual(mock_stdout.call_count, 1) # Only the scanning message

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime', side_effect=OSError("Permission denied"))
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_os_error_handling(self, mock_stderr, mock_stdout, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate an OSError (e.g., permission denied) when accessing a file.
        mock_isdir.return_value = True
        mock_walk.return_value = [('/test_dir', [], ['unreadable_file.txt'])]
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)

        anomalies = list(find_temporal_anomalies('/test_dir'))
        self.assertEqual(len(anomalies), 0)
        mock_stderr.assert_any_call(f"Warning: Could not access {os.path.join('/test_dir', 'unreadable_file.txt')}: Permission denied")
