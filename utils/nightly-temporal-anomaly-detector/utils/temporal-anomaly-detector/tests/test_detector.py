import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.detector import scan_directory_for_anomalies, get_current_time_utc, get_file_mtime_utc

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Define a fixed 'current time' for deterministic tests
        self.fixed_current_time_dt = datetime(2024, 10, 27, 12, 0, 0) # UTC
        self.fixed_current_time_ts = self.fixed_current_time_dt.timestamp()

    @patch('src.detector.time.time')
    def test_get_current_time_utc(self, mock_time):
        # Mock rationale: Ensure get_current_time_utc returns a deterministic time for testing.
        mock_time.return_value = self.fixed_current_time_ts
        self.assertEqual(get_current_time_utc(), self.fixed_current_time_dt)

    @patch('src.detector.os.path.getmtime')
    def test_get_file_mtime_utc(self, mock_getmtime):
        # Mock rationale: Ensure get_file_mtime_utc returns a deterministic time for testing.
        test_filepath = '/fake/path/file.txt'
        test_mtime_dt = datetime(2023, 1, 1, 0, 0, 0) # UTC
        test_mtime_ts = test_mtime_dt.timestamp()
        mock_getmtime.return_value = test_mtime_ts

        self.assertEqual(get_file_mtime_utc(test_filepath), test_mtime_dt)

    @patch('src.detector.os.path.getmtime')
    @patch('src.detector.os.walk')
    @patch('src.detector.os.path.isdir')
    @patch('src.detector.time.time')
    def test_no_anomalies(self, mock_time, mock_isdir, mock_walk, mock_getmtime):
        # Mock rationale: Simulate a directory with files having normal modification times.
        mock_time.return_value = self.fixed_current_time_ts
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]

        # Files modified slightly in the past, well within thresholds
        normal_mtime_ts = (self.fixed_current_time_dt - timedelta(days=30)).timestamp()
        mock_getmtime.side_effect = [normal_mtime_ts, normal_mtime_ts]

        anomalies = scan_directory_for_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 0)

    @patch('src.detector.os.path.getmtime')
    @patch('src.detector.os.walk')
    @patch('src.detector.os.path.isdir')
    @patch('src.detector.time.time')
    def test_future_modification_anomaly(self, mock_time, mock_isdir, mock_walk, mock_getmtime):
        # Mock rationale: Simulate a file with a modification time in the future.
        mock_time.return_value = self.fixed_current_time_ts
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['future_file.txt'])
        ]

        future_mtime_ts = (self.fixed_current_time_dt + timedelta(seconds=100)).timestamp()
        mock_getmtime.return_value = future_mtime_ts

        anomalies = scan_directory_for_anomalies('/test_dir', future_threshold_seconds=0)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'Future Modification')
        self.assertIn('future_file.txt', anomalies[0]['path'])
        self.assertIn('100 seconds in the future', anomalies[0]['message'])

    @patch('src.detector.os.path.getmtime')
    @patch('src.detector.os.walk')
    @patch('src.detector.os.path.isdir')
    @patch('src.detector.time.time')
    def test_old_modification_anomaly(self, mock_time, mock_isdir, mock_walk, mock_getmtime):
        # Mock rationale: Simulate a file with an excessively old modification time.
        mock_time.return_value = self.fixed_current_time_ts
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.txt'])
        ]

        old_mtime_ts = (self.fixed_current_time_dt - timedelta(days=400)).timestamp()
        mock_getmtime.return_value = old_mtime_ts

        anomalies = scan_directory_for_anomalies('/test_dir', old_threshold_days=365)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'Excessively Old Modification')
        self.assertIn('old_file.txt', anomalies[0]['path'])
        self.assertIn('400 days ago', anomalies[0]['message'])

    @patch('src.detector.os.path.isdir')
    def test_non_existent_directory(self, mock_isdir):
        # Mock rationale: Simulate a scenario where the target directory does not exist.
        mock_isdir.return_value = False

        anomalies = scan_directory_for_anomalies('/non_existent_dir')
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'Path Error')
        self.assertIn('Directory does not exist', anomalies[0]['message'])

    @patch('src.detector.os.path.getmtime')
    @patch('src.detector.os.walk')
    @patch('src.detector.os.path.isdir')
    @patch('src.detector.time.time')
    def test_file_access_error(self, mock_time, mock_isdir, mock_walk, mock_getmtime):
        # Mock rationale: Simulate a file that cannot be stat'd (e.g., deleted mid-scan).
        mock_time.return_value = self.fixed_current_time_ts
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['unreadable_file.txt'])
        ]

        mock_getmtime.side_effect = OSError # Simulate file access error

        anomalies = scan_directory_for_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'File Access Error')
        self.assertIn('unreadable_file.txt', anomalies[0]['path'])
        self.assertIn('Could not retrieve modification time', anomalies[0]['message'])

    @patch('src.detector.os.path.getmtime')
    @patch('src.detector.os.walk')
    @patch('src.detector.os.path.isdir')
    @patch('src.detector.time.time')
    def test_multiple_anomalies(self, mock_time, mock_isdir, mock_walk, mock_getmtime):
        # Mock rationale: Simulate a directory with multiple types of anomalies.
        mock_time.return_value = self.fixed_current_time_ts
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['future.txt', 'old.txt', 'normal.txt'])
        ]

        future_mtime_ts = (self.fixed_current_time_dt + timedelta(seconds=50)).timestamp()
        old_mtime_ts = (self.fixed_current_time_dt - timedelta(days=500)).timestamp()
        normal_mtime_ts = (self.fixed_current_time_dt - timedelta(days=10)).timestamp()

        # Order matters for side_effect
        mock_getmtime.side_effect = [
            future_mtime_ts, # future.txt
            old_mtime_ts,    # old.txt
            normal_mtime_ts  # normal.txt
        ]

        anomalies = scan_directory_for_anomalies('/test_dir', future_threshold_seconds=0, old_threshold_days=365)
        self.assertEqual(len(anomalies), 2)

        anomaly_types = [a['type'] for a in anomalies]
        self.assertIn('Future Modification', anomaly_types)
        self.assertIn('Excessively Old Modification', anomaly_types)

if __name__ == '__main__':
    unittest.main()
