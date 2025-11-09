import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import sys

# Add the src directory to the path to allow importing detector.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import detector
sys.path.pop(0)

class TestTemporalAnomalyDetector(unittest.TestCase):

    # Mock rationale: Fixes the 'current time' for deterministic testing of future/ancient anomalies.
    @patch('detector.get_current_time')
    def setUp(self, mock_get_current_time):
        # Set a fixed current time for all tests
        self.fixed_current_time = datetime.datetime(2024, 10, 27, 10, 0, 0, tzinfo=datetime.timezone.utc)
        mock_get_current_time.return_value = self.fixed_current_time

        # Define some common mock timestamps (as datetime objects, will be converted to float timestamps for os.path.getmtime)
        self.normal_mtime = datetime.datetime(2024, 9, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)
        self.future_mtime = datetime.datetime(2024, 11, 1, 9, 0, 0, tzinfo=datetime.timezone.utc)
        self.ancient_mtime = datetime.datetime(2018, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        self.very_ancient_mtime = datetime.datetime(2010, 5, 10, 15, 30, 0, tzinfo=datetime.timezone.utc)

    # Mock rationale: Simulates filesystem traversal without needing to create actual files.
    @patch('os.walk')
    # Mock rationale: Controls the modification timestamps of simulated files for deterministic anomaly detection.
    @patch('os.path.getmtime')
    def test_no_anomalies(self, mock_getmtime, mock_walk):
        mock_walk.return_value = [
            ('/mock_dir', [], ['file1.txt', 'file2.py'])
        ]
        # Map file paths to their mock modification timestamps
        mock_getmtime.side_effect = lambda p: {
            '/mock_dir/file1.txt': self.normal_mtime.timestamp(),
            '/mock_dir/file2.py': self.normal_mtime.timestamp()
        }.get(p, self.normal_mtime.timestamp())

        results = detector.detect_anomalies('/mock_dir', ancient_threshold_years=5)

        self.assertEqual(len(results['future_anomalies']), 0)
        self.assertEqual(len(results['ancient_anomalies']), 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_future_anomaly(self, mock_getmtime, mock_walk):
        mock_walk.return_value = [
            ('/mock_dir', [], ['normal.txt', 'future.py'])
        ]
        mock_getmtime.side_effect = lambda p: {
            '/mock_dir/normal.txt': self.normal_mtime.timestamp(),
            '/mock_dir/future.py': self.future_mtime.timestamp()
        }.get(p, self.normal_mtime.timestamp())

        results = detector.detect_anomalies('/mock_dir', ancient_threshold_years=5)

        self.assertEqual(len(results['future_anomalies']), 1)
        self.assertEqual(results['future_anomalies'][0]['filepath'], '/mock_dir/future.py')
        self.assertEqual(len(results['ancient_anomalies']), 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_ancient_anomaly(self, mock_getmtime, mock_walk):
        mock_walk.return_value = [
            ('/mock_dir', [], ['normal.txt', 'ancient.log'])
        ]
        mock_getmtime.side_effect = lambda p: {
            '/mock_dir/normal.txt': self.normal_mtime.timestamp(),
            '/mock_dir/ancient.log': self.ancient_mtime.timestamp()
        }.get(p, self.normal_mtime.timestamp())

        results = detector.detect_anomalies('/mock_dir', ancient_threshold_years=5)

        self.assertEqual(len(results['future_anomalies']), 0)
        self.assertEqual(len(results['ancient_anomalies']), 1)
        self.assertEqual(results['ancient_anomalies'][0]['filepath'], '/mock_dir/ancient.log')

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_mixed_anomalies(self, mock_getmtime, mock_walk):
        mock_walk.return_value = [
            ('/mock_dir', [], ['normal.txt', 'future.py', 'ancient.log'])
        ]
        mock_getmtime.side_effect = lambda p: {
            '/mock_dir/normal.txt': self.normal_mtime.timestamp(),
            '/mock_dir/future.py': self.future_mtime.timestamp(),
            '/mock_dir/ancient.log': self.ancient_mtime.timestamp()
        }.get(p, self.normal_mtime.timestamp())

        results = detector.detect_anomalies('/mock_dir', ancient_threshold_years=5)

        self.assertEqual(len(results['future_anomalies']), 1)
        self.assertEqual(results['future_anomalies'][0]['filepath'], '/mock_dir/future.py')
        self.assertEqual(len(results['ancient_anomalies']), 1)
        self.assertEqual(results['ancient_anomalies'][0]['filepath'], '/mock_dir/ancient.log')

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_empty_directory(self, mock_getmtime, mock_walk):
        mock_walk.return_value = [
            ('/mock_dir', [], [])
        ]
        results = detector.detect_anomalies('/mock_dir', ancient_threshold_years=5)

        self.assertEqual(len(results['future_anomalies']), 0)
        self.assertEqual(len(results['ancient_anomalies']), 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_ancient_threshold_effect(self, mock_getmtime, mock_walk):
        mock_walk.return_value = [
            ('/mock_dir', [], ['old_file.txt', 'very_old_file.dat'])
        ]
        mock_getmtime.side_effect = lambda p: {
            '/mock_dir/old_file.txt': self.ancient_mtime.timestamp(), # 2018-01-01 (6 years old)
            '/mock_dir/very_old_file.dat': self.very_ancient_mtime.timestamp() # 2010-05-10 (14 years old)
        }.get(p, self.normal_mtime.timestamp())

        # Test with threshold 3 years: both should be ancient
        results_3_years = detector.detect_anomalies('/mock_dir', ancient_threshold_years=3)
        self.assertEqual(len(results_3_years['ancient_anomalies']), 2)

        # Test with threshold 7 years: only very_old_file.dat should be ancient
        results_7_years = detector.detect_anomalies('/mock_dir', ancient_threshold_years=7)
        self.assertEqual(len(results_7_years['ancient_anomalies']), 1)
        self.assertEqual(results_7_years['ancient_anomalies'][0]['filepath'], '/mock_dir/very_old_file.dat')

        # Test with threshold 15 years: none should be ancient
        results_15_years = detector.detect_anomalies('/mock_dir', ancient_threshold_years=15)
        self.assertEqual(len(results_15_years['ancient_anomalies']), 0)

    # Mock rationale: Simulates a non-existent directory to test error handling.
    @patch('os.path.isdir')
    def test_non_existent_directory(self, mock_isdir):
        mock_isdir.return_value = False
        # Suppress print output for this test
        with patch('sys.stdout', new=MagicMock()) as mock_stdout, \
             patch('sys.stderr', new=MagicMock()) as mock_stderr:
            results = detector.detect_anomalies('/non_existent_dir')
            self.assertEqual(len(results['future_anomalies']), 0)
            self.assertEqual(len(results['ancient_anomalies']), 0)
            mock_stderr.write.assert_called_with("Error: Directory '/non_existent_dir' not found.\n")


if __name__ == '__main__':
    unittest.main()
