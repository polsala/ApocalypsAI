import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Mock current time for deterministic tests
MOCK_CURRENT_TIME = 1678886400.0  # March 15, 2023, 12:00:00 PM UTC

class TestAnomalyDetector(unittest.TestCase):

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print') # Mock print to capture output
    def test_scan_directory_no_anomalies(self, mock_print, mock_isdir, mock_time):
        # Mock rationale: Simulate a directory with files that have consistent timestamps.
        # This ensures the detector correctly identifies a 'clean' state.
        mock_os_walk_return = [
            ('/root', ['dir_a'], ['file1.txt']),
            ('/root/dir_a', [], ['file2.txt'])
        ]
        mock_os_stat_map = {
            '/root': MagicMock(st_mtime=MOCK_CURRENT_TIME - 3600*24*10, st_ctime=MOCK_CURRENT_TIME - 3600*24*10),
            '/root/file1.txt': MagicMock(st_mtime=MOCK_CURRENT_TIME - 3600*24*10, st_ctime=MOCK_CURRENT_TIME - 3600*24*10),
            '/root/dir_a': MagicMock(st_mtime=MOCK_CURRENT_TIME - 3600*24*5, st_ctime=MOCK_CURRENT_TIME - 3600*24*5),
            '/root/dir_a/file2.txt': MagicMock(st_mtime=MOCK_CURRENT_TIME - 3600*24*5, st_ctime=MOCK_CURRENT_TIME - 3600*24*5)
        }

        with patch('os.walk', return_value=mock_os_walk_return),
             patch('os.stat', side_effect=lambda p: mock_os_stat_map.get(p, MagicMock(st_mtime=0, st_ctime=0))):
            from src.detector import AnomalyDetector
            detector = AnomalyDetector(threshold_days=30)
            detector.scan_directory('/root')

            self.assertEqual(len(detector.anomalies), 0)
            mock_print.assert_any_call("No chrono-sync anomalies detected. Your filesystem is temporally sound!")

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_scan_directory_future_dated_file(self, mock_print, mock_isdir, mock_time):
        # Mock rationale: Simulate a file with a modification time in the future.
        # This tests the 'Future-Dated File' anomaly detection.
        future_time = MOCK_CURRENT_TIME + 3600 * 24 * 5 # 5 days in the future
        mock_os_walk_return = [
            ('/root', [], ['future_file.txt'])
        ]
        mock_os_stat_map = {
            '/root': MagicMock(st_mtime=MOCK_CURRENT_TIME - 3600, st_ctime=MOCK_CURRENT_TIME - 3600),
            '/root/future_file.txt': MagicMock(st_mtime=future_time, st_ctime=future_time)
        }

        with patch('os.walk', return_value=mock_os_walk_return),
             patch('os.stat', side_effect=lambda p: mock_os_stat_map.get(p, MagicMock(st_mtime=0, st_ctime=0))):
            from src.detector import AnomalyDetector
            detector = AnomalyDetector(threshold_days=30)
            detector.scan_directory('/root')

            self.assertEqual(len(detector.anomalies), 1)
            self.assertEqual(detector.anomalies[0]['type'], "Future-Dated File")
            self.assertEqual(detector.anomalies[0]['path'], "/root/future_file.txt")
            mock_print.assert_any_call(unittest.mock.ANY) # Check if print was called

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_scan_directory_file_much_older_than_parent(self, mock_print, mock_isdir, mock_time):
        # Mock rationale: Simulate a file whose modification time is significantly older
        # than its parent directory's modification time. This tests the 'File Much Older Than Parent' anomaly.
        parent_mtime = MOCK_CURRENT_TIME - 3600 * 24 * 10 # 10 days ago
        file_mtime = MOCK_CURRENT_TIME - 3600 * 24 * 60 # 60 days ago (more than 30-day threshold)
        mock_os_walk_return = [
            ('/root', [], ['old_file.txt'])
        ]
        mock_os_stat_map = {
            '/root': MagicMock(st_mtime=parent_mtime, st_ctime=parent_mtime),
            '/root/old_file.txt': MagicMock(st_mtime=file_mtime, st_ctime=file_mtime)
        }

        with patch('os.walk', return_value=mock_os_walk_return),
             patch('os.stat', side_effect=lambda p: mock_os_stat_map.get(p, MagicMock(st_mtime=0, st_ctime=0))):
            from src.detector import AnomalyDetector
            detector = AnomalyDetector(threshold_days=30)
            detector.scan_directory('/root')

            self.assertEqual(len(detector.anomalies), 1)
            self.assertEqual(detector.anomalies[0]['type'], "File Much Older Than Parent")
            self.assertEqual(detector.anomalies[0]['path'], "/root/old_file.txt")

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_scan_directory_file_much_newer_than_parent(self, mock_print, mock_isdir, mock_time):
        # Mock rationale: Simulate a file whose modification time is significantly newer
        # than its parent directory's modification time. This tests the 'File Much Newer Than Parent' anomaly.
        parent_mtime = MOCK_CURRENT_TIME - 3600 * 24 * 60 # 60 days ago
        file_mtime = MOCK_CURRENT_TIME - 3600 * 24 * 10 # 10 days ago (more than 30-day threshold newer)
        mock_os_walk_return = [
            ('/root', [], ['new_file.txt'])
        ]
        mock_os_stat_map = {
            '/root': MagicMock(st_mtime=parent_mtime, st_ctime=parent_mtime),
            '/root/new_file.txt': MagicMock(st_mtime=file_mtime, st_ctime=file_mtime)
        }

        with patch('os.walk', return_value=mock_os_walk_return),
             patch('os.stat', side_effect=lambda p: mock_os_stat_map.get(p, MagicMock(st_mtime=0, st_ctime=0))):
            from src.detector import AnomalyDetector
            detector = AnomalyDetector(threshold_days=30)
            detector.scan_directory('/root')

            self.assertEqual(len(detector.anomalies), 1)
            self.assertEqual(detector.anomalies[0]['type'], "File Much Newer Than Parent")
            self.assertEqual(detector.anomalies[0]['path'], "/root/new_file.txt")

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_scan_directory_multiple_anomalies(self, mock_print, mock_isdir, mock_time):
        # Mock rationale: Simulate a scenario with multiple types of anomalies
        # to ensure all are detected and reported correctly.
        future_time = MOCK_CURRENT_TIME + 3600 * 24 * 5
        parent_mtime_old = MOCK_CURRENT_TIME - 3600 * 24 * 10
        file_mtime_very_old = MOCK_CURRENT_TIME - 3600 * 24 * 60
        parent_mtime_new = MOCK_CURRENT_TIME - 3600 * 24 * 60
        file_mtime_very_new = MOCK_CURRENT_TIME - 3600 * 24 * 10

        mock_os_walk_return = [
            ('/root', [], ['future.txt', 'old.txt', 'new.txt'])
        ]
        mock_os_stat_map = {
            '/root': MagicMock(st_mtime=MOCK_CURRENT_TIME - 3600, st_ctime=MOCK_CURRENT_TIME - 3600),
            '/root/future.txt': MagicMock(st_mtime=future_time, st_ctime=future_time),
            '/root/old.txt': MagicMock(st_mtime=file_mtime_very_old, st_ctime=file_mtime_very_old),
            '/root/new.txt': MagicMock(st_mtime=file_mtime_very_new, st_ctime=file_mtime_very_new)
        }
        # Adjust parent mtime for specific files to trigger anomalies
        mock_os_stat_map['/root'].st_mtime = parent_mtime_old # For old.txt
        # For new.txt, we need a parent that is older than new.txt by threshold
        # Let's make /root's mtime suitable for new.txt, and old.txt will still be older than this root.
        mock_os_stat_map['/root'].st_mtime = MOCK_CURRENT_TIME - 3600 * 24 * 40 # 40 days ago

        with patch('os.walk', return_value=mock_os_walk_return),
             patch('os.stat', side_effect=lambda p: mock_os_stat_map.get(p, MagicMock(st_mtime=0, st_ctime=0))):
            from src.detector import AnomalyDetector
            detector = AnomalyDetector(threshold_days=30)
            detector.scan_directory('/root')

            self.assertEqual(len(detector.anomalies), 3)
            anomaly_types = sorted([a['type'] for a in detector.anomalies])
            self.assertEqual(anomaly_types, [
                "File Much Newer Than Parent",
                "File Much Older Than Parent",
                "Future-Dated File"
            ])

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    def test_scan_directory_invalid_path(self, mock_print, mock_isdir, mock_time):
        # Mock rationale: Test the behavior when an invalid path is provided.
        # This ensures the utility handles non-directory inputs gracefully.
        from src.detector import AnomalyDetector
        detector = AnomalyDetector()
        detector.scan_directory('/nonexistent')

        mock_print.assert_any_call("Error: Path '/nonexistent' is not a valid directory.")
        self.assertEqual(len(detector.anomalies), 0)

    @patch('time.time', return_value=MOCK_CURRENT_TIME)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_scan_directory_future_dated_directory(self, mock_print, mock_isdir, mock_time):
        # Mock rationale: Simulate a directory with a modification time in the future.
        # This tests the 'Future-Dated Directory' anomaly detection.
        future_time = MOCK_CURRENT_TIME + 3600 * 24 * 5 # 5 days in the future
        mock_os_walk_return = [
            ('/root', ['future_dir'], []),
            ('/root/future_dir', [], [])
        ]
        mock_os_stat_map = {
            '/root': MagicMock(st_mtime=MOCK_CURRENT_TIME - 3600, st_ctime=MOCK_CURRENT_TIME - 3600),
            '/root/future_dir': MagicMock(st_mtime=future_time, st_ctime=future_time)
        }

        with patch('os.walk', return_value=mock_os_walk_return),
             patch('os.stat', side_effect=lambda p: mock_os_stat_map.get(p, MagicMock(st_mtime=0, st_ctime=0))):
            from src.detector import AnomalyDetector
            detector = AnomalyDetector(threshold_days=30)
            detector.scan_directory('/root')

            self.assertEqual(len(detector.anomalies), 1)
            self.assertEqual(detector.anomalies[0]['type'], "Future-Dated Directory")
            self.assertEqual(detector.anomalies[0]['path'], "/root/future_dir")


if __name__ == '__main__':
    unittest.main()
