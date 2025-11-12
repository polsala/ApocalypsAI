import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import time
from datetime import datetime, timedelta

# Mock rationale: We need to simulate file system interactions (os.walk, os.path.getmtime)
# and the current time (time.time()) without actually touching the disk or relying on
# the system's real clock. This ensures deterministic and fast tests.

# Add src directory to sys.path to allow importing detector.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from detector import find_temporal_anomalies

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic tests
        self.mock_current_time = datetime(2024, 7, 20, 12, 0, 0).timestamp()

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_no_anomalies(self, mock_isdir, mock_walk, mock_getmtime, mock_time):
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        # Mock os.walk to return a directory structure with normal files
        mock_walk.return_value = [
            ('/mock_dir', [], ['file1.txt', 'file2.log']),
            ('/mock_dir/subdir', [], ['subfile.py'])
        ]

        # Mock os.path.getmtime to return times in the past
        mock_getmtime.side_effect = {
            '/mock_dir/file1.txt': (datetime(2024, 7, 19, 10, 0, 0)).timestamp(),
            '/mock_dir/file2.log': (datetime(2024, 7, 18, 15, 30, 0)).timestamp(),
            '/mock_dir/subdir/subfile.py': (datetime(2024, 7, 17, 9, 0, 0)).timestamp(),
        }.get

        anomalies = find_temporal_anomalies('/mock_dir')
        self.assertEqual(len(anomalies), 0)

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_with_future_anomaly(self, mock_isdir, mock_walk, mock_getmtime, mock_time):
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        # Mock os.walk with one future file
        mock_walk.return_value = [
            ('/mock_dir', [], ['normal_file.txt', 'future_file.log'])
        ]

        # Mock os.path.getmtime: one normal, one in the future
        mock_getmtime.side_effect = {
            '/mock_dir/normal_file.txt': (datetime(2024, 7, 19, 10, 0, 0)).timestamp(),
            '/mock_dir/future_file.log': (datetime(2024, 7, 21, 10, 0, 0)).timestamp(), # Future time
        }.get

        anomalies = find_temporal_anomalies('/mock_dir')
        self.assertEqual(len(anomalies), 1)
        self.assertIn('/mock_dir/future_file.log', anomalies)

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_multiple_future_anomalies(self, mock_isdir, mock_walk, mock_getmtime, mock_time):
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        # Mock os.walk with multiple future files across subdirectories
        mock_walk.return_value = [
            ('/mock_dir', [], ['file_a.txt', 'future_b.log']),
            ('/mock_dir/data', [], ['future_c.json', 'file_d.csv'])
        ]

        # Mock os.path.getmtime
        mock_getmtime.side_effect = {
            '/mock_dir/file_a.txt': (datetime(2024, 7, 19, 10, 0, 0)).timestamp(),
            '/mock_dir/future_b.log': (datetime(2024, 7, 22, 10, 0, 0)).timestamp(),
            '/mock_dir/data/future_c.json': (datetime(2024, 7, 23, 10, 0, 0)).timestamp(),
            '/mock_dir/data/file_d.csv': (datetime(2024, 7, 15, 10, 0, 0)).timestamp(),
        }.get

        anomalies = find_temporal_anomalies('/mock_dir')
        self.assertEqual(len(anomalies), 2)
        self.assertIn('/mock_dir/future_b.log', anomalies)
        self.assertIn('/mock_dir/data/future_c.json', anomalies)

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_empty_directory(self, mock_isdir, mock_walk, mock_getmtime, mock_time):
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        # Mock os.walk to return an empty directory structure
        mock_walk.return_value = [
            ('/mock_dir', [], [])
        ]

        anomalies = find_temporal_anomalies('/mock_dir')
        self.assertEqual(len(anomalies), 0)

    @patch('sys.stderr', new_callable=MagicMock)
    @patch('os.path.isdir')
    def test_invalid_directory(self, mock_isdir, mock_stderr):
        mock_isdir.return_value = False

        anomalies = find_temporal_anomalies('/non_existent_dir')
        self.assertEqual(len(anomalies), 0)
        mock_stderr.write.assert_called_with("Error: Directory not found at '/non_existent_dir'\n")

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_os_error_on_getmtime(self, mock_stderr, mock_isdir, mock_walk, mock_getmtime, mock_time):
        mock_isdir.return_value = True
        mock_time.return_value = self.mock_current_time

        mock_walk.return_value = [
            ('/mock_dir', [], ['accessible.txt', 'inaccessible.txt'])
        ]

        def getmtime_side_effect(path):
            if 'inaccessible.txt' in path:
                raise OSError("Permission denied")
            return (datetime(2024, 7, 19, 10, 0, 0)).timestamp()

        mock_getmtime.side_effect = getmtime_side_effect

        anomalies = find_temporal_anomalies('/mock_dir')
        self.assertEqual(len(anomalies), 0) # No future files, inaccessible file is skipped
        mock_stderr.write.assert_called_with("Warning: Could not access '/mock_dir/inaccessible.txt': Permission denied\n")

if __name__ == '__main__':
    unittest.main()
