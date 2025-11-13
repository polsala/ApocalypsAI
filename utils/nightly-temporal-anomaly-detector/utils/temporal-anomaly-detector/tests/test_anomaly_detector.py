import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import os
import sys

# Add the src directory to the path to allow importing anomaly_detector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from anomaly_detector import detect_anomalies, get_threshold_datetime

class TestTemporalAnomalyDetector(unittest.TestCase):

    @patch('anomaly_detector.datetime')
    def test_get_threshold_datetime_older_days(self, mock_datetime):
        # Mock rationale: Ensure deterministic 'now' for threshold calculation.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow actual datetime object creation

        threshold = get_threshold_datetime('older-than', 5, 'days')
        expected_threshold = datetime(2023, 10, 21, 10, 0, 0)
        self.assertEqual(threshold, expected_threshold)

    @patch('anomaly_detector.datetime')
    def test_get_threshold_datetime_newer_hours(self, mock_datetime):
        # Mock rationale: Ensure deterministic 'now' for threshold calculation.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        threshold = get_threshold_datetime('newer-than', 2, 'hours')
        expected_threshold = datetime(2023, 10, 26, 8, 0, 0)
        self.assertEqual(threshold, expected_threshold)

    @patch('anomaly_detector.os.path.isfile')
    @patch('anomaly_detector.os.path.getmtime')
    @patch('anomaly_detector.os.listdir')
    @patch('anomaly_detector.datetime')
    def test_detect_anomalies_older_than(self, mock_datetime, mock_listdir, mock_getmtime, mock_isfile):
        # Mock rationale: Control file system state and current time for deterministic testing.
        # mock_datetime: Fixes 'now' for threshold calculation.
        # mock_listdir: Simulates directory contents.
        # mock_getmtime: Provides specific modification times for simulated files.
        # mock_isfile: Confirms paths are files.

        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp # Allow actual conversion
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        mock_listdir.return_value = ['old_file.txt', 'recent_file.log', 'future_file.dat']
        mock_isfile.return_value = True # Assume all listed items are files

        # Define specific modification times (timestamps)
        # old_file: Oct 1, 2023 (older than 20 days ago from Oct 26)
        # recent_file: Oct 20, 2023 (not older than 20 days ago)
        # future_file: Oct 27, 2023 (not older than 20 days ago)
        file_mtimes = {
            '/test_dir/old_file.txt': datetime(2023, 10, 1, 10, 0, 0).timestamp(),
            '/test_dir/recent_file.log': datetime(2023, 10, 20, 10, 0, 0).timestamp(),
            '/test_dir/future_file.dat': datetime(2023, 10, 27, 10, 0, 0).timestamp()
        }
        mock_getmtime.side_effect = lambda p: file_mtimes[p]

        anomalies = detect_anomalies('/test_dir', 'older-than', 20, 'days')
        self.assertEqual(anomalies, ['/test_dir/old_file.txt'])

    @patch('anomaly_detector.os.path.isfile')
    @patch('anomaly_detector.os.path.getmtime')
    @patch('anomaly_detector.os.listdir')
    @patch('anomaly_detector.datetime')
    def test_detect_anomalies_newer_than(self, mock_datetime, mock_listdir, mock_getmtime, mock_isfile):
        # Mock rationale: Control file system state and current time for deterministic testing.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        mock_listdir.return_value = ['old_file.txt', 'recent_file.log', 'very_new_file.json']
        mock_isfile.return_value = True

        # Define specific modification times (timestamps)
        # old_file: Oct 1, 2023 (not newer than 5 hours ago from Oct 26 10:00)
        # recent_file: Oct 26, 09:00 (not newer than 5 hours ago, i.e., before 05:00)
        # very_new_file: Oct 26, 09:30 (newer than 5 hours ago, i.e., after 05:00)
        file_mtimes = {
            '/test_dir/old_file.txt': datetime(2023, 10, 1, 10, 0, 0).timestamp(),
            '/test_dir/recent_file.log': datetime(2023, 10, 26, 9, 0, 0).timestamp(),
            '/test_dir/very_new_file.json': datetime(2023, 10, 26, 9, 30, 0).timestamp()
        }
        mock_getmtime.side_effect = lambda p: file_mtimes[p]

        anomalies = detect_anomalies('/test_dir', 'newer-than', 5, 'hours')
        self.assertEqual(anomalies, ['/test_dir/very_new_file.json'])

    @patch('anomaly_detector.os.path.isfile')
    @patch('anomaly_detector.os.path.getmtime')
    @patch('anomaly_detector.os.listdir')
    @patch('anomaly_detector.datetime')
    def test_detect_anomalies_no_anomalies(self, mock_datetime, mock_listdir, mock_getmtime, mock_isfile):
        # Mock rationale: Control file system state and current time to ensure no anomalies are detected.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        mock_listdir.return_value = ['normal_file_1.txt', 'normal_file_2.log']
        mock_isfile.return_value = True

        # All files are within the 'normal' range (not older than 10 days, not newer than 1 hour)
        file_mtimes = {
            '/test_dir/normal_file_1.txt': datetime(2023, 10, 20, 10, 0, 0).timestamp(), # 6 days old
            '/test_dir/normal_file_2.log': datetime(2023, 10, 26, 9, 30, 0).timestamp()  # 30 mins old
        }
        mock_getmtime.side_effect = lambda p: file_mtimes[p]

        anomalies_older = detect_anomalies('/test_dir', 'older-than', 10, 'days')
        self.assertEqual(anomalies_older, [])

        anomalies_newer = detect_anomalies('/test_dir', 'newer-than', 1, 'hours')
        self.assertEqual(anomalies_newer, [])

    @patch('anomaly_detector.os.listdir')
    def test_detect_anomalies_empty_directory(self, mock_listdir):
        # Mock rationale: Simulate an empty directory to ensure no files are processed.
        mock_listdir.return_value = []
        anomalies = detect_anomalies('/empty_dir', 'older-than', 10, 'days')
        self.assertEqual(anomalies, [])

    @patch('anomaly_detector.os.listdir')
    def test_detect_anomalies_directory_not_found(self, mock_listdir):
        # Mock rationale: Simulate a FileNotFoundError when listing directory contents.
        mock_listdir.side_effect = FileNotFoundError
        anomalies = detect_anomalies('/non_existent_dir', 'older-than', 10, 'days')
        self.assertEqual(anomalies, [])

    @patch('anomaly_detector.os.path.isfile')
    @patch('anomaly_detector.os.path.getmtime')
    @patch('anomaly_detector.os.listdir')
    @patch('anomaly_detector.datetime')
    def test_detect_anomalies_with_subdirectories(self, mock_datetime, mock_listdir, mock_getmtime, mock_isfile):
        # Mock rationale: Ensure only files are processed, not subdirectories.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        mock_listdir.return_value = ['file.txt', 'subdir']
        
        # Mock isfile to return True for 'file.txt' and False for 'subdir'
        def isfile_side_effect(path):
            return path == '/test_dir/file.txt'
        mock_isfile.side_effect = isfile_side_effect

        file_mtimes = {
            '/test_dir/file.txt': datetime(2023, 10, 1, 10, 0, 0).timestamp()
        }
        mock_getmtime.side_effect = lambda p: file_mtimes[p] if p in file_mtimes else 0

        anomalies = detect_anomalies('/test_dir', 'older-than', 20, 'days')
        self.assertEqual(anomalies, ['/test_dir/file.txt'])

if __name__ == '__main__':
    unittest.main()
