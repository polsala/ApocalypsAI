import unittest
import os
import datetime
import time
from unittest.mock import patch, MagicMock

# Ensure the path is correct for importing the module under test
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from detector import scan_directory, DEFAULT_FUTURE_THRESHOLD_DAYS, DEFAULT_PAST_THRESHOLD_DAYS
sys.path.pop(0)

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Define a fixed 'current' time for deterministic tests
        self.current_time_dt = datetime.datetime(2024, 1, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)
        self.current_time_ts = self.current_time_dt.timestamp()

        # Mock datetime.datetime to control its 'now' method
        # Mock rationale: `datetime.datetime.now` is non-deterministic and depends on the system clock. 
        # We need a fixed point in time to reliably test future/past thresholds.
        self.mock_datetime_patch = patch('datetime.datetime')
        self.mock_dt = self.mock_datetime_patch.start()

        # Configure the mock datetime.datetime object
        self.mock_dt.now.return_value = self.current_time_dt
        # Ensure other class methods like fromtimestamp and attributes like timezone work as normal
        self.mock_dt.fromtimestamp = datetime.datetime.fromtimestamp
        self.mock_dt.timezone = datetime.timezone

    def tearDown(self):
        self.mock_datetime_patch.stop()

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_no_anomalies(self, mock_getmtime, mock_walk):
        # Mock rationale: `os.walk` and `os.path.getmtime` interact with the file system, 
        # which is an external dependency and non-deterministic. Mocking them allows 
        # us to simulate various file system states and modification times without 
        # actually creating files or relying on the host system's state.

        # Simulate a directory with normal files
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]
        # All files are within normal range (e.g., 1 day in the past)
        normal_past_ts = (self.current_time_dt - datetime.timedelta(days=1)).timestamp()
        mock_getmtime.side_effect = [normal_past_ts, normal_past_ts]

        anomalies = scan_directory('/test_dir')
        self.assertEqual(len(anomalies), 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_future_anomaly(self, mock_getmtime, mock_walk):
        # Mock rationale: See `test_no_anomalies`.

        # Simulate a directory with one future-dated file
        mock_walk.return_value = [
            ('/test_dir', [], ['future_file.txt', 'normal_file.log'])
        ]
        future_ts = (self.current_time_dt + datetime.timedelta(days=DEFAULT_FUTURE_THRESHOLD_DAYS + 1)).timestamp()
        normal_ts = (self.current_time_dt - datetime.timedelta(days=1)).timestamp()
        mock_getmtime.side_effect = [future_ts, normal_ts]

        anomalies = scan_directory('/test_dir')
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0][0], '/test_dir/future_file.txt')
        self.assertEqual(anomalies[0][2], 'FUTURE ANOMALY')

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_past_anomaly(self, mock_getmtime, mock_walk):
        # Mock rationale: See `test_no_anomalies`.

        # Simulate a directory with one past-dated file
        mock_walk.return_value = [
            ('/test_dir', [], ['past_file.txt', 'normal_file.log'])
        ]
        past_ts = (self.current_time_dt - datetime.timedelta(days=DEFAULT_PAST_THRESHOLD_DAYS + 1)).timestamp()
        normal_ts = (self.current_time_dt - datetime.timedelta(days=1)).timestamp()
        mock_getmtime.side_effect = [past_ts, normal_ts]

        anomalies = scan_directory('/test_dir')
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0][0], '/test_dir/past_file.txt')
        self.assertEqual(anomalies[0][2], 'PAST ANOMALY')

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_custom_thresholds(self, mock_getmtime, mock_walk):
        # Mock rationale: See `test_no_anomalies`.

        # Use custom thresholds: 1 day future, 5 days past
        custom_future_threshold = 1
        custom_past_threshold = 5

        mock_walk.return_value = [
            ('/test_dir', [], ['future_file.txt', 'past_file.txt', 'normal_file.log'])
        ]

        # File 2 days in future (should be flagged)
        future_ts = (self.current_time_dt + datetime.timedelta(days=custom_future_threshold + 1)).timestamp()
        # File 6 days in past (should be flagged)
        past_ts = (self.current_time_dt - datetime.timedelta(days=custom_past_threshold + 1)).timestamp()
        # File 3 days in past (should NOT be flagged)
        normal_ts = (self.current_time_dt - datetime.timedelta(days=3)).timestamp()

        mock_getmtime.side_effect = [future_ts, past_ts, normal_ts]

        anomalies = scan_directory(
            '/test_dir',
            future_threshold_days=custom_future_threshold,
            past_threshold_days=custom_past_threshold
        )

        self.assertEqual(len(anomalies), 2)
        anomaly_types = sorted([a[2] for a in anomalies])
        self.assertEqual(anomaly_types, ['FUTURE ANOMALY', 'PAST ANOMALY'])

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_empty_directory(self, mock_getmtime, mock_walk):
        # Mock rationale: See `test_no_anomalies`.

        mock_walk.return_value = [] # Empty directory
        mock_getmtime.side_effect = [] # No files to get mtime for

        anomalies = scan_directory('/empty_dir')
        self.assertEqual(len(anomalies), 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_os_error_handling(self, mock_getmtime, mock_walk):
        # Mock rationale: See `test_no_anomalies`.

        mock_walk.return_value = [
            ('/test_dir', [], ['unreadable_file.txt', 'normal_file.log'])
        ]
        # Simulate an OSError for one file (e.g., permissions)
        mock_getmtime.side_effect = [OSError("Permission denied"), self.current_time_ts]

        # We expect no anomalies to be reported for the unreadable file, 
        # but the scan should continue for other files.
        anomalies = scan_directory('/test_dir')
        self.assertEqual(len(anomalies), 0) # No *temporal* anomalies, just an error handled internally
