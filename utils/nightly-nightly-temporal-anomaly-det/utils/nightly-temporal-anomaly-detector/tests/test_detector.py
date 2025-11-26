import unittest
import os
import time
import datetime
from unittest.mock import patch, MagicMock
from src.detector import detect_anomalies, get_file_timestamps

class TestTemporalAnomalyDetector(unittest.TestCase):

    # Mock rationale: os.walk, os.stat, and time.time are system-dependent
    # and non-deterministic. Mocking them allows for controlled test scenarios
    # without actual file system interaction or reliance on current time.

    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    def test_no_anomalies(self, mock_os_walk, mock_os_stat, mock_time_time):
        # Mock rationale: Simulate a clean directory with no anomalies.
        # This ensures the detector correctly identifies a healthy state.
        mock_time_time.return_value = 1678886400.0  # March 15, 2023 00:00:00 UTC

        # Simulate a file with normal timestamps
        mock_os_walk.return_value = [
            ('/test_dir', [], ['normal_file.txt'])
        ]
        mock_stat_info = MagicMock()
        mock_stat_info.st_mtime = 1678886300.0  # 100 seconds before current_time
        mock_stat_info.st_ctime = 1678800000.0  # March 14, 2023
        mock_os_stat.return_value = mock_stat_info

        ref_date = datetime.date(2023, 1, 1)
        anomalies = detect_anomalies(
            target_dir='/test_dir',
            future_threshold_seconds=60,
            stale_threshold_days=365,
            creation_ref_date=ref_date,
            exclude_patterns=[]
        )

        self.assertFalse(any(anomalies.values()))
        self.assertEqual(len(anomalies["future_modified"]), 0)
        self.assertEqual(len(anomalies["ancient_artifacts"]), 0)
        self.assertEqual(len(anomalies["pre_genesis_creations"]), 0)

    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    def test_future_modified_file(self, mock_os_walk, mock_os_stat, mock_time_time):
        # Mock rationale: Simulate a file with a modification time in the future.
        # This tests the 'future_modified' detection logic.
        mock_time_time.return_value = 1678886400.0  # March 15, 2023 00:00:00 UTC

        mock_os_walk.return_value = [
            ('/test_dir', [], ['future_file.txt'])
        ]
        mock_stat_info = MagicMock()
        mock_stat_info.st_mtime = 1678886461.0  # 61 seconds in the future
        mock_stat_info.st_ctime = 1678800000.0
        mock_os_stat.return_value = mock_stat_info

        ref_date = datetime.date(2023, 1, 1)
        anomalies = detect_anomalies(
            target_dir='/test_dir',
            future_threshold_seconds=60, # Threshold is 60s
            stale_threshold_days=365,
            creation_ref_date=ref_date,
            exclude_patterns=[]
        )

        self.assertEqual(len(anomalies["future_modified"]), 1)
        self.assertIn('future_file.txt', anomalies["future_modified"][0])
        self.assertEqual(len(anomalies["ancient_artifacts"]), 0)
        self.assertEqual(len(anomalies["pre_genesis_creations"]), 0)

    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    def test_ancient_artifact_file(self, mock_os_walk, mock_os_stat, mock_time_time):
        # Mock rationale: Simulate a file that hasn't been modified in a long time.
        # This tests the 'ancient_artifacts' detection logic.
        mock_time_time.return_value = 1678886400.0  # March 15, 2023 00:00:00 UTC

        mock_os_walk.return_value = [
            ('/test_dir', [], ['old_file.txt'])
        ]
        mock_stat_info = MagicMock()
        mock_stat_info.st_mtime = 1678886400.0 - (366 * 24 * 60 * 60) # 366 days ago
        mock_stat_info.st_ctime = 1678800000.0
        mock_os_stat.return_value = mock_stat_info

        ref_date = datetime.date(2023, 1, 1)
        anomalies = detect_anomalies(
            target_dir='/test_dir',
            future_threshold_seconds=60,
            stale_threshold_days=365, # Threshold is 365 days
            creation_ref_date=ref_date,
            exclude_patterns=[]
        )

        self.assertEqual(len(anomalies["future_modified"]), 0)
        self.assertEqual(len(anomalies["ancient_artifacts"]), 1)
        self.assertIn('old_file.txt', anomalies["ancient_artifacts"][0])
        self.assertEqual(len(anomalies["pre_genesis_creations"]), 0)

    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    def test_pre_genesis_creation_file(self, mock_os_walk, mock_os_stat, mock_time_time):
        # Mock rationale: Simulate a file created before the reference date.
        # This tests the 'pre_genesis_creations' detection logic.
        mock_time_time.return_value = 1678886400.0  # March 15, 2023 00:00:00 UTC

        mock_os_walk.return_value = [
            ('/test_dir', [], ['ancient_creation.txt'])
        ]
        mock_stat_info = MagicMock()
        mock_stat_info.st_mtime = 1678886300.0
        mock_stat_info.st_ctime = datetime.datetime(2022, 12, 31, tzinfo=datetime.timezone.utc).timestamp() # Dec 31, 2022
        mock_os_stat.return_value = mock_stat_info

        ref_date = datetime.date(2023, 1, 1) # Reference date is Jan 1, 2023
        anomalies = detect_anomalies(
            target_dir='/test_dir',
            future_threshold_seconds=60,
            stale_threshold_days=365,
            creation_ref_date=ref_date,
            exclude_patterns=[]
        )

        self.assertEqual(len(anomalies["future_modified"]), 0)
        self.assertEqual(len(anomalies["ancient_artifacts"]), 0)
        self.assertEqual(len(anomalies["pre_genesis_creations"]), 1)
        self.assertIn('ancient_creation.txt', anomalies["pre_genesis_creations"][0])

    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    def test_multiple_anomalies(self, mock_os_walk, mock_os_stat, mock_time_time):
        # Mock rationale: Simulate a directory with multiple types of anomalies.
        # This ensures the detector can find and report all of them.
        mock_time_time.return_value = 1678886400.0  # March 15, 2023 00:00:00 UTC

        # Define file stats for different anomaly types
        future_mtime = 1678886461.0
        ancient_mtime = 1678886400.0 - (366 * 24 * 60 * 60)
        pre_genesis_ctime = datetime.datetime(2022, 12, 31, tzinfo=datetime.timezone.utc).timestamp()
        normal_mtime = 1678886300.0
        normal_ctime = 1678800000.0

        mock_os_walk.return_value = [
            ('/test_dir', [], ['future.txt', 'old.txt', 'pre_gen.txt', 'normal.txt'])
        ]

        # Mock os.stat to return different values based on the file path
        def mock_stat_side_effect(path):
            stat_info = MagicMock()
            if 'future.txt' in path:
                stat_info.st_mtime = future_mtime
                stat_info.st_ctime = normal_ctime
            elif 'old.txt' in path:
                stat_info.st_mtime = ancient_mtime
                stat_info.st_ctime = normal_ctime
            elif 'pre_gen.txt' in path:
                stat_info.st_mtime = normal_mtime
                stat_info.st_ctime = pre_genesis_ctime
            else: # normal.txt
                stat_info.st_mtime = normal_mtime
                stat_info.st_ctime = normal_ctime
            return stat_info

        mock_os_stat.side_effect = mock_stat_side_effect

        ref_date = datetime.date(2023, 1, 1)
        anomalies = detect_anomalies(
            target_dir='/test_dir',
            future_threshold_seconds=60,
            stale_threshold_days=365,
            creation_ref_date=ref_date,
            exclude_patterns=[]
        )

        self.assertEqual(len(anomalies["future_modified"]), 1)
        self.assertIn('future.txt', anomalies["future_modified"][0])
        self.assertEqual(len(anomalies["ancient_artifacts"]), 1)
        self.assertIn('old.txt', anomalies["ancient_artifacts"][0])
        self.assertEqual(len(anomalies["pre_genesis_creations"]), 1)
        self.assertIn('pre_gen.txt', anomalies["pre_genesis_creations"][0])

    @patch('time.time')
    @patch('os.stat')
    @patch('os.walk')
    def test_exclusion_patterns(self, mock_os_walk, mock_os_stat, mock_time_time):
        # Mock rationale: Test that files matching exclusion patterns are ignored.
        # This verifies the filtering logic.
        mock_time_time.return_value = 1678886400.0  # March 15, 2023 00:00:00 UTC

        # Simulate a future file that should be excluded
        mock_os_walk.return_value = [
            ('/test_dir', ['logs'], ['future_log.txt', 'future_data.bin']),
            ('/test_dir/logs', [], ['log_file.log'])
        ]
        mock_stat_info = MagicMock()
        mock_stat_info.st_mtime = 1678886461.0  # 61 seconds in the future
        mock_stat_info.st_ctime = 1678800000.0
        mock_os_stat.return_value = mock_stat_info

        ref_date = datetime.date(2023, 1, 1)
        anomalies = detect_anomalies(
            target_dir='/test_dir',
            future_threshold_seconds=60,
            stale_threshold_days=365,
            creation_ref_date=ref_date,
            exclude_patterns=['*.log', '*/logs/*', 'future_data.bin']
        )

        self.assertFalse(any(anomalies.values())) # No anomalies should be reported due to exclusion
        self.assertEqual(len(anomalies["future_modified"]), 0)
        self.assertEqual(len(anomalies["ancient_artifacts"]), 0)
        self.assertEqual(len(anomalies["pre_genesis_creations"]), 0)

    @patch('os.stat')
    def test_get_file_timestamps_os_error(self, mock_os_stat):
        # Mock rationale: Test robustness when os.stat fails (e.g., permission denied, file deleted).
        # This ensures the utility handles edge cases gracefully.
        mock_os_stat.side_effect = OSError("Permission denied")
        mtime, ctime = get_file_timestamps("/nonexistent/file.txt")
        self.assertEqual(mtime, 0.0)
        self.assertEqual(ctime, 0.0)

if __name__ == '__main__':
    unittest.main()
