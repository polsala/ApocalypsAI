import unittest
import os
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.detector import find_stale_files

class TestTemporalAnomalyDetector(unittest.TestCase):

    # Mock rationale: We need to control the current time for deterministic
    # staleness calculations, as `datetime.now()` would otherwise vary.
    @patch('src.detector.datetime')
    # Mock rationale: We need to simulate a file system structure and file
    # modification times without actually touching the disk. `os.walk` and
    # `os.path.getmtime` are key for this.
    @patch('src.detector.os')
    def test_no_stale_files(self, mock_os, mock_datetime):
        # Mock rationale: Set a fixed "current time" for the test.
        mock_datetime.now.return_value = datetime(2024, 7, 15, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta # Ensure timedelta works as expected

        # Mock rationale: Simulate a directory with files, all recently modified.
        mock_os.path.isdir.return_value = True
        mock_os.walk.return_value = [
            ('/project', [], ['file1.txt', 'file2.log']),
            ('/project/sub', [], ['sub_file.py'])
        ]
        # Mock rationale: Provide modification times for simulated files.
        # All files are within the 90-day threshold (e.g., modified yesterday).
        mock_os.path.getmtime.side_effect = lambda p: (mock_datetime.now.return_value - timedelta(days=1)).timestamp()
        mock_os.path.join.side_effect = os.path.join # Use real join for paths

        root_dir = '/project'
        stale_days = 90
        stale_files = find_stale_files(root_dir, stale_days)
        self.assertEqual(len(stale_files), 0)

    @patch('src.detector.datetime')
    @patch('src.detector.os')
    def test_some_stale_files(self, mock_os, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 7, 15, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta

        mock_os.path.isdir.return_value = True
        mock_os.walk.return_value = [
            ('/project', [], ['recent.txt', 'stale_old.log']),
            ('/project/sub', [], ['recent_sub.py', 'stale_very_old.json'])
        ]

        # Mock rationale: Define specific modification times for each file.
        # 'recent.txt' and 'recent_sub.py' are fresh.
        # 'stale_old.log' and 'stale_very_old.json' are older than 90 days.
        mod_times = {
            '/project/recent.txt': (mock_datetime.now.return_value - timedelta(days=10)).timestamp(),
            '/project/stale_old.log': (mock_datetime.now.return_value - timedelta(days=100)).timestamp(),
            '/project/sub/recent_sub.py': (mock_datetime.now.return_value - timedelta(days=50)).timestamp(),
            '/project/sub/stale_very_old.json': (mock_datetime.now.return_value - timedelta(days=200)).timestamp(),
        }
        mock_os.path.getmtime.side_effect = lambda p: mod_times.get(p, 0)
        mock_os.path.join.side_effect = os.path.join

        root_dir = '/project'
        stale_days = 90
        stale_files = find_stale_files(root_dir, stale_days)

        self.assertEqual(len(stale_files), 2)
        self.assertIn(('/project/stale_old.log', datetime(2024, 4, 6, 12, 0, 0)), stale_files)
        self.assertIn(('/project/sub/stale_very_old.json', datetime(2023, 12, 28, 12, 0, 0)), stale_files)

    @patch('src.detector.datetime')
    @patch('src.detector.os')
    def test_empty_directory(self, mock_os, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 7, 15, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta

        mock_os.path.isdir.return_value = True
        # Mock rationale: Simulate an empty directory.
        mock_os.walk.return_value = [
            ('/empty_project', [], [])
        ]
        mock_os.path.getmtime.return_value = 0 # Should not be called
        mock_os.path.join.side_effect = os.path.join

        root_dir = '/empty_project'
        stale_days = 90
        stale_files = find_stale_files(root_dir, stale_days)
        self.assertEqual(len(stale_files), 0)

    @patch('src.detector.datetime')
    @patch('src.detector.os')
    def test_non_existent_directory(self, mock_os, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 7, 15, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta

        # Mock rationale: Simulate a directory that does not exist.
        mock_os.path.isdir.return_value = False
        mock_os.walk.return_value = [] # Should not be called
        mock_os.path.getmtime.return_value = 0 # Should not be called
        mock_os.path.join.side_effect = os.path.join

        root_dir = '/non_existent'
        stale_days = 90
        stale_files = find_stale_files(root_dir, stale_days)
        self.assertEqual(len(stale_files), 0) # Expect empty list and an error message printed

    @patch('src.detector.datetime')
    @patch('src.detector.os')
    def test_file_just_under_threshold(self, mock_os, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 7, 15, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta

        mock_os.path.isdir.return_value = True
        mock_os.walk.return_value = [
            ('/project', [], ['file.txt'])
        ]
        # Mock rationale: File modified exactly 89 days ago, so it's NOT stale.
        mod_time = mock_datetime.now.return_value - timedelta(days=89)
        mock_os.path.getmtime.return_value = mod_time.timestamp()
        mock_os.path.join.side_effect = os.path.join

        root_dir = '/project'
        stale_days = 90
        stale_files = find_stale_files(root_dir, stale_days)
        self.assertEqual(len(stale_files), 0)

    @patch('src.detector.datetime')
    @patch('src.detector.os')
    def test_file_just_over_threshold(self, mock_os, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 7, 15, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta

        mock_os.path.isdir.return_value = True
        mock_os.walk.return_value = [
            ('/project', [], ['file.txt'])
        ]
        # Mock rationale: File modified exactly 91 days ago, so it IS stale.
        mod_time = mock_datetime.now.return_value - timedelta(days=91)
        mock_os.path.getmtime.return_value = mod_time.timestamp()
        mock_os.path.join.side_effect = os.path.join

        root_dir = '/project'
        stale_days = 90
        stale_files = find_stale_files(root_dir, stale_days)
        self.assertEqual(len(stale_files), 1)
        self.assertIn(('/project/file.txt', datetime(2024, 4, 15, 12, 0, 0)), stale_files)

    @patch('src.detector.datetime')
    @patch('src.detector.os')
    def test_os_error_handling(self, mock_os, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 7, 15, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta

        mock_os.path.isdir.return_value = True
        mock_os.walk.return_value = [
            ('/project', [], ['accessible.txt', 'inaccessible.txt'])
        ]
        # Mock rationale: Simulate an OSError for 'inaccessible.txt'.
        def getmtime_side_effect(path):
            if 'inaccessible.txt' in path:
                raise OSError("Permission denied")
            return (mock_datetime.now.return_value - timedelta(days=100)).timestamp() # Stale
        mock_os.path.getmtime.side_effect = getmtime_side_effect
        mock_os.path.join.side_effect = os.path.join

        root_dir = '/project'
        stale_days = 90
        stale_files = find_stale_files(root_dir, stale_days)

        # Only 'accessible.txt' should be reported as stale, 'inaccessible.txt' should be skipped.
        self.assertEqual(len(stale_files), 1)
        self.assertIn(('/project/accessible.txt', datetime(2024, 4, 6, 12, 0, 0)), stale_files)
