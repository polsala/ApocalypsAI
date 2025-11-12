import unittest
import os
import datetime
from unittest.mock import patch, MagicMock
from src.detector import detect_anomalies, get_file_timestamps

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Define a fixed "current time" for deterministic testing
        self.fixed_now = datetime.datetime(2023, 10, 27, 10, 0, 0)
        self.fixed_now_ts = self.fixed_now.timestamp()

        # Mock datetime.datetime.now() for consistent current time
        # Mock rationale: Ensures tests are deterministic and not affected by real-time changes.
        self.patcher_datetime_now = patch('datetime.datetime')
        self.mock_datetime = self.patcher_datetime_now.start()
        self.mock_datetime.now.return_value = self.fixed_now
        self.mock_datetime.fromtimestamp = datetime.datetime.fromtimestamp # Keep original for conversion

        # Mock os.walk and os.stat for file system simulation
        # Mock rationale: Allows simulating various directory structures and file metadata without actual file system interaction.
        self.patcher_os_walk = patch('os.walk')
        self.mock_os_walk = self.patcher_os_walk.start()

        self.patcher_os_stat = patch('os.stat')
        self.mock_os_stat = self.patcher_os_stat.start()

        self.patcher_os_path_isdir = patch('os.path.isdir')
        self.mock_os_path_isdir = self.patcher_os_path_isdir.start()
        self.mock_os_path_isdir.return_value = True # Assume target dir exists for main script execution path

    def tearDown(self):
        self.patcher_datetime_now.stop()
        self.patcher_os_walk.stop()
        self.patcher_os_stat.stop()
        self.patcher_os_path_isdir.stop()

    def _mock_file_stat(self, filepath, mtime_offset_seconds, ctime_offset_seconds):
        """Helper to create a mock stat object with times relative to fixed_now."""
        mock_stat = MagicMock()
        mock_stat.st_mtime = self.fixed_now_ts + mtime_offset_seconds
        mock_stat.st_ctime = self.fixed_now_ts + ctime_offset_seconds
        # Mock rationale: Configures os.stat to return specific timestamp data for mocked files.
        self.mock_os_stat.side_effect = lambda p: mock_stat if p == filepath else FileNotFoundError
        return mock_stat

    def test_no_anomalies(self):
        # Mock rationale: Simulate a directory with normal files, ensuring no anomalies are detected.
        self.mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]
        self._mock_file_stat('/test_dir/file1.txt', -3600, -7200) # mtime 1hr ago, ctime 2hr ago
        self._mock_file_stat('/test_dir/file2.log', -1800, -2700) # mtime 30min ago, ctime 45min ago

        anomalies = detect_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 0)

    def test_future_modification_anomaly(self):
        # Mock rationale: Simulate a file with a modification time in the future to trigger detection.
        self.mock_os_walk.return_value = [
            ('/test_dir', [], ['future_mod.txt'])
        ]
        self._mock_file_stat('/test_dir/future_mod.txt', 3600, -3600) # mtime 1hr in future, ctime 1hr ago

        anomalies = detect_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]["type"], "Future Modification")
        self.assertEqual(anomalies[0]["file"], "/test_dir/future_mod.txt")
        self.assertIn("File modified in the future", anomalies[0]["description"])

    def test_future_creation_anomaly(self):
        # Mock rationale: Simulate a file with a creation time in the future to trigger detection.
        self.mock_os_walk.return_value = [
            ('/test_dir', [], ['future_create.txt'])
        ]
        self._mock_file_stat('/test_dir/future_create.txt', -3600, 3600) # mtime 1hr ago, ctime 1hr in future

        anomalies = detect_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]["type"], "Future Creation")
        self.assertEqual(anomalies[0]["file"], "/test_dir/future_create.txt")
        self.assertIn("File created in the future", anomalies[0]["description"])

    def test_retroactive_modification_anomaly(self):
        # Mock rationale: Simulate a file where modification time is older than creation time to trigger detection.
        self.mock_os_walk.return_value = [
            ('/test_dir', [], ['retro_mod.txt'])
        ]
        self._mock_file_stat('/test_dir/retro_mod.txt', -7200, -3600) # mtime 2hr ago, ctime 1hr ago (mtime < ctime)

        anomalies = detect_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]["type"], "Retroactive Modification")
        self.assertEqual(anomalies[0]["file"], "/test_dir/retro_mod.txt")
        self.assertIn("modification time is older than its creation time", anomalies[0]["description"])

    def test_multiple_anomalies_in_one_file(self):
        # Mock rationale: Simulate multiple files, each exhibiting a different type of anomaly.
        self.mock_os_walk.return_value = [
            ('/test_dir', [], ['file_fm.txt', 'file_fc.txt', 'file_rm.txt'])
        ]
        # Future Modification
        self._mock_file_stat('/test_dir/file_fm.txt', 3600, -3600)
        # Future Creation
        self._mock_file_stat('/test_dir/file_fc.txt', -3600, 3600)
        # Retroactive Modification
        self._mock_file_stat('/test_dir/file_rm.txt', -7200, -3600)

        anomalies = detect_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 3)
        types = sorted([a["type"] for a in anomalies])
        self.assertEqual(types, ["Future Creation", "Future Modification", "Retroactive Modification"])

    def test_file_not_found_graceful_handling(self):
        # Mock rationale: Simulate a scenario where os.stat raises FileNotFoundError for a file, ensuring graceful skipping.
        self.mock_os_walk.return_value = [
            ('/test_dir', [], ['existing.txt', 'non_existing.txt'])
        ]
        mock_stat_existing = MagicMock()
        mock_stat_existing.st_mtime = self.fixed_now_ts - 3600
        mock_stat_existing.st_ctime = self.fixed_now_ts - 7200

        # Configure side_effect for os.stat to raise FileNotFoundError for 'non_existing.txt'
        def stat_side_effect(path):
            if path == '/test_dir/existing.txt':
                return mock_stat_existing
            elif path == '/test_dir/non_existing.txt':
                raise FileNotFoundError
            else:
                raise Exception("Unexpected path in test_file_not_found_graceful_handling")

        self.mock_os_stat.side_effect = stat_side_effect

        anomalies = detect_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 0) # No anomalies from existing.txt, non_existing.txt is skipped.

    def test_get_file_timestamps_error_handling(self):
        # Mock rationale: Directly test get_file_timestamps's error handling when os.stat fails.
        self.mock_os_stat.side_effect = FileNotFoundError
        mtime, ctime = get_file_timestamps('/non_existent_file.txt')
        self.assertIsNone(mtime)
        self.assertIsNone(ctime)
