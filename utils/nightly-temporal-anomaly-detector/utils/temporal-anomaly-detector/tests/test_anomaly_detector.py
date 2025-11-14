import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import os

# Import the function to be tested
from src.anomaly_detector import find_temporal_anomalies

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Define a fixed 'now' for deterministic testing
        self.fixed_now = datetime(2024, 7, 20, 12, 0, 0) # Mock rationale: Ensures datetime.now() is consistent across test runs.

        # Define thresholds based on fixed_now and default parameters
        self.default_max_age_days = 30
        self.default_min_age_seconds = 60
        self.old_threshold = self.fixed_now - timedelta(days=self.default_max_age_days)
        self.new_threshold = self.fixed_now - timedelta(seconds=self.default_min_age_seconds)

    @patch('datetime.datetime')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    def test_no_anomalies(self, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        # Mock rationale: datetime.datetime is mocked to control the 'current time'.
        # Mock rationale: os.walk is mocked to simulate file system structure without actual disk access.
        # Mock rationale: os.path.getmtime is mocked to control file modification times.
        # Mock rationale: os.path.isdir is mocked to confirm the directory exists.

        mock_datetime.now.return_value = self.fixed_now
        mock_isdir.return_value = True

        # Simulate a file within the normal temporal window
        mock_walk.return_value = [
            ('/test_dir', [], ['normal_file.txt'])
        ]
        # File modified 15 days ago (within 30 days max, not within 60 seconds min)
        mock_getmtime.return_value = (self.fixed_now - timedelta(days=15)).timestamp()

        anomalies = find_temporal_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 0)

    @patch('datetime.datetime')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    def test_too_old_anomaly(self, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        mock_datetime.now.return_value = self.fixed_now
        mock_isdir.return_value = True

        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.log'])
        ]
        # File modified 31 days ago (older than 30 days default)
        mock_getmtime.return_value = (self.fixed_now - timedelta(days=31)).timestamp()

        anomalies = find_temporal_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['path'], os.path.join('/test_dir', 'old_file.log'))
        self.assertEqual(anomalies[0]['type'], 'TOO_OLD')

    @patch('datetime.datetime')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    def test_too_new_anomaly(self, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        mock_datetime.now.return_value = self.fixed_now
        mock_isdir.return_value = True

        mock_walk.return_value = [
            ('/test_dir', [], ['new_report.csv'])
        ]
        # File modified 10 seconds ago (newer than 60 seconds default)
        mock_getmtime.return_value = (self.fixed_now - timedelta(seconds=10)).timestamp()

        anomalies = find_temporal_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['path'], os.path.join('/test_dir', 'new_report.csv'))
        self.assertEqual(anomalies[0]['type'], 'TOO_NEW')

    @patch('datetime.datetime')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    def test_custom_thresholds(self, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        mock_datetime.now.return_value = self.fixed_now
        mock_isdir.return_value = True

        mock_walk.return_value = [
            ('/test_dir', [], ['custom_old.txt', 'custom_new.json'])
        ]

        # Custom thresholds: max_age_days=7, min_age_seconds=300 (5 minutes)
        custom_old_threshold = self.fixed_now - timedelta(days=7)
        custom_new_threshold = self.fixed_now - timedelta(seconds=300)

        # File 'custom_old.txt' modified 8 days ago (older than 7 days)
        # File 'custom_new.json' modified 100 seconds ago (newer than 300 seconds)
        def mock_getmtime_side_effect(path):
            if 'custom_old.txt' in path:
                return (self.fixed_now - timedelta(days=8)).timestamp()
            elif 'custom_new.json' in path:
                return (self.fixed_now - timedelta(seconds=100)).timestamp()
            return self.fixed_now.timestamp() # Fallback, though not expected here

        mock_getmtime.side_effect = mock_getmtime_side_effect

        anomalies = find_temporal_anomalies('/test_dir', max_age_days=7, min_age_seconds=300)
        self.assertEqual(len(anomalies), 2)

        # Check 'TOO_OLD' anomaly
        old_anomaly = next(a for a in anomalies if a['type'] == 'TOO_OLD')
        self.assertEqual(old_anomaly['path'], os.path.join('/test_dir', 'custom_old.txt'))

        # Check 'TOO_NEW' anomaly
        new_anomaly = next(a for a in anomalies if a['type'] == 'TOO_NEW')
        self.assertEqual(new_anomaly['path'], os.path.join('/test_dir', 'custom_new.json'))

    @patch('datetime.datetime')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    def test_directory_not_found(self, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        mock_datetime.now.return_value = self.fixed_now
        mock_isdir.return_value = False # Mock rationale: Simulates a non-existent directory.

        anomalies = find_temporal_anomalies('/non_existent_dir')
        self.assertEqual(len(anomalies), 0)
        # We expect a print statement for error, but the function should return empty list

    @patch('datetime.datetime')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.isdir')
    def test_os_error_on_getmtime(self, mock_isdir, mock_getmtime, mock_walk, mock_datetime):
        mock_datetime.now.return_value = self.fixed_now
        mock_isdir.return_value = True

        mock_walk.return_value = [
            ('/test_dir', [], ['unreadable_file.txt'])
        ]
        mock_getmtime.side_effect = OSError("Permission denied") # Mock rationale: Simulates a file that cannot be accessed.

        anomalies = find_temporal_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 0)
        # We expect a print statement for warning, but the function should return empty list

if __name__ == '__main__':
    unittest.main()
