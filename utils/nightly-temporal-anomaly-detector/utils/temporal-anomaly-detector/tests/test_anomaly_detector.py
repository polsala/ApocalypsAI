import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the path to allow importing anomaly_detector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from anomaly_detector import detect_anomalies, get_file_timestamps

class TestAnomalyDetector(unittest.TestCase):

    @patch('anomaly_detector.os.stat')
    def test_get_file_timestamps_success(self, mock_stat):
        # Mock rationale: os.stat is a system call that depends on the actual filesystem.
        # We need to control its output for deterministic testing.
        mock_stat_result = MagicMock()
        mock_stat_result.st_ctime = datetime(2023, 1, 1, 10, 0, 0).timestamp()
        mock_stat_result.st_mtime = datetime(2023, 1, 1, 11, 0, 0).timestamp()
        mock_stat.return_value = mock_stat_result

        timestamps = get_file_timestamps("/fake/path/file.txt")
        self.assertEqual(timestamps["ctime"], datetime(2023, 1, 1, 10, 0, 0))
        self.assertEqual(timestamps["mtime"], datetime(2023, 1, 1, 11, 0, 0))

    @patch('anomaly_detector.os.stat')
    def test_get_file_timestamps_os_error(self, mock_stat):
        # Mock rationale: Simulate a file not found or permission error for os.stat.
        mock_stat.side_effect = OSError("File not found")

        timestamps = get_file_timestamps("/nonexistent/file.txt")
        self.assertEqual(timestamps["ctime"], datetime.min)
        self.assertEqual(timestamps["mtime"], datetime.min)

    @patch('anomaly_detector.os.walk')
    @patch('anomaly_detector.os.stat')
    @patch('anomaly_detector.datetime')
    def test_no_anomalies(self, mock_datetime, mock_stat, mock_walk):
        # Mock rationale:
        # - os.walk: Controls the directory structure and files found.
        # - os.stat: Provides specific ctime/mtime for each file.
        # - datetime: Fixes the 'now' time for consistent threshold checks.

        # Setup mock for datetime.now()
        fixed_now = datetime(2024, 7, 20, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp # Allow real conversion
        mock_datetime.min = datetime.min # Ensure datetime.min is available

        # Setup mock for os.walk
        mock_walk.return_value = [
            ("/mock/dir", [], ["file1.txt", "file2.txt"])
        ]

        # Setup mock for os.stat for each file
        def mock_os_stat_side_effect(path):
            mock_stat_result = MagicMock()
            if "file1.txt" in path:
                mock_stat_result.st_ctime = (fixed_now - timedelta(days=5)).timestamp()
                mock_stat_result.st_mtime = (fixed_now - timedelta(days=1)).timestamp()
            elif "file2.txt" in path:
                mock_stat_result.st_ctime = (fixed_now - timedelta(days=10)).timestamp()
                mock_stat_result.st_mtime = (fixed_now - timedelta(days=2)).timestamp()
            return mock_stat_result
        mock_stat.side_effect = mock_os_stat_side_effect

        anomalies = detect_anomalies("/mock/dir")
        self.assertEqual(len(anomalies), 0)

    @patch('anomaly_detector.os.walk')
    @patch('anomaly_detector.os.stat')
    @patch('anomaly_detector.datetime')
    def test_mtime_before_ctime_anomaly(self, mock_datetime, mock_stat, mock_walk):
        # Mock rationale: Simulate a file where modification time is before creation time.
        fixed_now = datetime(2024, 7, 20, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.min = datetime.min

        mock_walk.return_value = [
            ("/mock/dir", [], ["anomalous_file.txt"])
        ]

        def mock_os_stat_side_effect(path):
            mock_stat_result = MagicMock()
            if "anomalous_file.txt" in path:
                mock_stat_result.st_ctime = (fixed_now - timedelta(days=5)).timestamp() # Created 5 days ago
                mock_stat_result.st_mtime = (fixed_now - timedelta(days=10)).timestamp() # Modified 10 days ago (before creation)
            return mock_stat_result
        mock_stat.side_effect = mock_os_stat_side_effect

        anomalies = detect_anomalies("/mock/dir")
        self.assertEqual(len(anomalies), 1)
        self.assertIn("Modification time is before creation time", anomalies[0]["anomalies"])
        self.assertEqual(anomalies[0]["filepath"], os.path.join("/mock/dir", "anomalous_file.txt"))

    @patch('anomaly_detector.os.walk')
    @patch('anomaly_detector.os.stat')
    @patch('anomaly_detector.datetime')
    def test_future_timestamp_anomaly(self, mock_datetime, mock_stat, mock_walk):
        # Mock rationale: Simulate a file with a timestamp far in the future.
        fixed_now = datetime(2024, 7, 20, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.min = datetime.min

        mock_walk.return_value = [
            ("/mock/dir", [], ["future_file.txt"])
        ]

        def mock_os_stat_side_effect(path):
            mock_stat_result = MagicMock()
            if "future_file.txt" in path:
                mock_stat_result.st_ctime = (fixed_now + timedelta(days=2)).timestamp() # Created 2 days in future
                mock_stat_result.st_mtime = (fixed_now + timedelta(days=3)).timestamp() # Modified 3 days in future
            return mock_stat_result
        mock_stat.side_effect = mock_os_stat_side_effect

        # Default future_threshold_hours is 24 (1 day)
        anomalies = detect_anomalies("/mock/dir")
        self.assertEqual(len(anomalies), 1)
        self.assertIn("Creation time is in the future", anomalies[0]["anomalies"])
        self.assertIn("Modification time is in the future", anomalies[0]["anomalies"])

    @patch('anomaly_detector.os.walk')
    @patch('anomaly_detector.os.stat')
    @patch('anomaly_detector.datetime')
    def test_past_timestamp_anomaly(self, mock_datetime, mock_stat, mock_walk):
        # Mock rationale: Simulate a file with a timestamp far in the past.
        fixed_now = datetime(2024, 7, 20, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.min = datetime.min

        mock_walk.return_value = [
            ("/mock/dir", [], ["ancient_file.txt"])
        ]

        def mock_os_stat_side_effect(path):
            mock_stat_result = MagicMock()
            if "ancient_file.txt" in path:
                mock_stat_result.st_ctime = (fixed_now - timedelta(days=365 * 15)).timestamp() # 15 years ago
                mock_stat_result.st_mtime = (fixed_now - timedelta(days=365 * 12)).timestamp() # 12 years ago
            return mock_stat_result
        mock_stat.side_effect = mock_os_stat_side_effect

        # Default past_threshold_years is 10
        anomalies = detect_anomalies("/mock/dir")
        self.assertEqual(len(anomalies), 1)
        self.assertIn("Creation time is significantly in the past", anomalies[0]["anomalies"])
        self.assertIn("Modification time is significantly in the past", anomalies[0]["anomalies"])

    @patch('anomaly_detector.os.walk')
    @patch('anomaly_detector.os.stat')
    @patch('anomaly_detector.datetime')
    def test_multiple_anomalies_and_normal_files(self, mock_datetime, mock_stat, mock_walk):
        # Mock rationale: Test a mix of normal and anomalous files.
        fixed_now = datetime(2024, 7, 20, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.min = datetime.min

        mock_walk.return_value = [
            ("/mock/dir", [], ["normal.txt", "mtime_before_ctime.txt", "future_file.txt", "ancient_file.txt"])
        ]

        def mock_os_stat_side_effect(path):
            mock_stat_result = MagicMock()
            if "normal.txt" in path:
                mock_stat_result.st_ctime = (fixed_now - timedelta(days=5)).timestamp()
                mock_stat_result.st_mtime = (fixed_now - timedelta(days=1)).timestamp()
            elif "mtime_before_ctime.txt" in path:
                mock_stat_result.st_ctime = (fixed_now - timedelta(days=5)).timestamp()
                mock_stat_result.st_mtime = (fixed_now - timedelta(days=10)).timestamp()
            elif "future_file.txt" in path:
                mock_stat_result.st_ctime = (fixed_now + timedelta(days=2)).timestamp()
                mock_stat_result.st_mtime = (fixed_now + timedelta(days=3)).timestamp()
            elif "ancient_file.txt" in path:
                mock_stat_result.st_ctime = (fixed_now - timedelta(days=365 * 15)).timestamp()
                mock_stat_result.st_mtime = (fixed_now - timedelta(days=365 * 12)).timestamp()
            return mock_stat_result
        mock_stat.side_effect = mock_os_stat_side_effect

        anomalies = detect_anomalies("/mock/dir")
        self.assertEqual(len(anomalies), 3)
        filepaths = {a["filepath"] for a in anomalies}
        self.assertIn(os.path.join("/mock/dir", "mtime_before_ctime.txt"), filepaths)
        self.assertIn(os.path.join("/mock/dir", "future_file.txt"), filepaths)
        self.assertIn(os.path.join("/mock/dir", "ancient_file.txt"), filepaths)

    @patch('anomaly_detector.os.walk')
    @patch('anomaly_detector.os.stat')
    @patch('anomaly_detector.datetime')
    def test_threshold_customization(self, mock_datetime, mock_stat, mock_walk):
        # Mock rationale: Verify that custom thresholds are respected.
        fixed_now = datetime(2024, 7, 20, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.min = datetime.min

        mock_walk.return_value = [
            ("/mock/dir", [], ["future_file.txt", "past_file.txt"])
        ]

        def mock_os_stat_side_effect(path):
            mock_stat_result = MagicMock()
            if "future_file.txt" in path:
                mock_stat_result.st_ctime = (fixed_now + timedelta(hours=5)).timestamp() # 5 hours in future
                mock_stat_result.st_mtime = (fixed_now + timedelta(hours=6)).timestamp()
            elif "past_file.txt" in path:
                mock_stat_result.st_ctime = (fixed_now - timedelta(days=365 * 3)).timestamp() # 3 years ago
                mock_stat_result.st_mtime = (fixed_now - timedelta(days=365 * 2)).timestamp()
            return mock_stat_result
        mock_stat.side_effect = mock_os_stat_side_effect

        # With default thresholds (24h future, 10y past), these files should NOT be anomalies
        anomalies_default = detect_anomalies("/mock/dir")
        self.assertEqual(len(anomalies_default), 0)

        # With custom thresholds (1h future, 1y past), these files SHOULD be anomalies
        anomalies_custom = detect_anomalies(
            "/mock/dir",
            future_threshold_hours=1,
            past_threshold_years=1
        )
        self.assertEqual(len(anomalies_custom), 2)
        filepaths = {a["filepath"] for a in anomalies_custom}
        self.assertIn(os.path.join("/mock/dir", "future_file.txt"), filepaths)
        self.assertIn(os.path.join("/mock/dir", "past_file.txt"), filepaths)

if __name__ == '__main__':
    unittest.main()
