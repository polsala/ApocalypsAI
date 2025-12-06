import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timedelta
from src.tracker import find_stale_files

class TestTemporalTearTracker(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('src.tracker.datetime') # Mock datetime to control 'now'
    def test_find_stale_files_basic(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Control the current time to ensure deterministic age calculation.
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        # Mock rationale: Ensure datetime.fromtimestamp behaves as expected.
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        # Mock rationale: Simulate a valid directory path.
        mock_isdir.return_value = True

        # Mock rationale: Simulate file system structure with one stale and one fresh file.
        mock_walk.return_value = [
            ('/test_dir', [], ['stale_file.txt', 'fresh_file.txt'])
        ]

        # Mock rationale: Control the modification times of the simulated files.
        # stale_file.txt: modified 100 days ago (older than 90 days threshold)
        # fresh_file.txt: modified 10 days ago (newer than 90 days threshold)
        mock_getmtime.side_effect = [
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=100)).timestamp(), # stale_file.txt
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=10)).timestamp()   # fresh_file.txt
        ]

        root_path = '/test_dir'
        age_days = 90
        stale_files = find_stale_files(root_path, age_days)

        self.assertEqual(len(stale_files), 1)
        self.assertEqual(stale_files[0][0], os.path.join(root_path, 'stale_file.txt'))
        self.assertEqual(stale_files[0][1], datetime(2023, 9, 23, 12, 0, 0)) # 100 days before 2024-01-01

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('src.tracker.datetime')
    def test_find_stale_files_no_stale_files(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Control the current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_isdir.return_value = True

        # Mock rationale: Simulate file system with only fresh files.
        mock_walk.return_value = [
            ('/test_dir', [], ['fresh_file1.txt', 'fresh_file2.txt'])
        ]

        # Mock rationale: All files modified within the 90-day threshold.
        mock_getmtime.side_effect = [
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=50)).timestamp(),
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=80)).timestamp()
        ]

        root_path = '/test_dir'
        age_days = 90
        stale_files = find_stale_files(root_path, age_days)

        self.assertEqual(len(stale_files), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('src.tracker.datetime')
    def test_find_stale_files_empty_directory(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Control the current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_isdir.return_value = True

        # Mock rationale: Simulate an empty directory.
        mock_walk.return_value = [
            ('/empty_dir', [], [])
        ]
        # mock_getmtime will not be called as there are no files.

        root_path = '/empty_dir'
        age_days = 30
        stale_files = find_stale_files(root_path, age_days)

        self.assertEqual(len(stale_files), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('src.tracker.datetime')
    def test_find_stale_files_non_existent_directory(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Control the current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        # Mock rationale: Simulate a non-existent directory.
        mock_isdir.return_value = False

        root_path = '/non_existent_dir'
        age_days = 30
        stale_files = find_stale_files(root_path, age_days)

        self.assertEqual(len(stale_files), 0) # Should return empty list and print error
        mock_walk.assert_not_called() # os.walk should not be called if dir doesn't exist

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('src.tracker.datetime')
    def test_find_stale_files_with_subdirectories(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Control the current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory structure with subdirectories and mixed files.
        mock_walk.return_value = [
            ('/root', ['sub1', 'sub2'], ['root_stale.txt', 'root_fresh.txt']),
            ('/root/sub1', [], ['sub1_stale.py']),
            ('/root/sub2', [], ['sub2_fresh.md', 'sub2_stale.json'])
        ]

        # Mock rationale: Control modification times for all simulated files.
        mock_getmtime.side_effect = [
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=120)).timestamp(), # root_stale.txt
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=10)).timestamp(),  # root_fresh.txt
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=150)).timestamp(), # sub1_stale.py
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=5)).timestamp(),   # sub2_fresh.md
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=95)).timestamp()   # sub2_stale.json
        ]

        root_path = '/root'
        age_days = 90
        stale_files = find_stale_files(root_path, age_days)

        expected_stale_files = [
            (os.path.join('/root', 'root_stale.txt'), datetime(2023, 9, 3, 12, 0, 0)),
            (os.path.join('/root/sub1', 'sub1_stale.py'), datetime(2023, 8, 4, 12, 0, 0)),
            (os.path.join('/root/sub2', 'sub2_stale.json'), datetime(2023, 9, 27, 12, 0, 0))
        ]

        # Sort both lists for consistent comparison
        stale_files.sort(key=lambda x: x[0])
        expected_stale_files.sort(key=lambda x: x[0])

        self.assertEqual(len(stale_files), 3)
        self.assertEqual(stale_files, expected_stale_files)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('src.tracker.datetime')
    def test_find_stale_files_os_error_on_getmtime(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Control the current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_isdir.return_value = True

        # Mock rationale: Simulate a file system with one accessible and one inaccessible file.
        mock_walk.return_value = [
            ('/test_dir', [], ['accessible.txt', 'inaccessible.txt'])
        ]

        # Mock rationale: Simulate an OSError for 'inaccessible.txt'.
        mock_getmtime.side_effect = [
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=100)).timestamp(), # accessible.txt (stale)
            OSError("Permission denied") # inaccessible.txt
        ]

        root_path = '/test_dir'
        age_days = 90
        stale_files = find_stale_files(root_path, age_days)

        self.assertEqual(len(stale_files), 1)
        self.assertEqual(stale_files[0][0], os.path.join(root_path, 'accessible.txt'))
        self.assertEqual(stale_files[0][1], datetime(2023, 9, 23, 12, 0, 0))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('src.tracker.datetime')
    def test_find_stale_files_age_zero(self, mock_datetime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Control the current time for deterministic age calculation.
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_isdir.return_value = True

        # Mock rationale: Simulate files with various modification times.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.txt'])
        ]

        # Mock rationale: file1 is 1 day old, file2 is 0.5 days old.
        mock_getmtime.side_effect = [
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(days=1)).timestamp(),
            (datetime(2024, 1, 1, 12, 0, 0) - timedelta(hours=12)).timestamp()
        ]

        root_path = '/test_dir'
        age_days = 0 # All files modified before 'now' are considered stale
        stale_files = find_stale_files(root_path, age_days)

        # With age_days=0, any file not modified *exactly* at 'now' will be considered stale.
        # In this mock setup, both files are older than 'now - 0 days', so both should be found.
        self.assertEqual(len(stale_files), 2)
        self.assertEqual(stale_files[0][0], os.path.join(root_path, 'file1.txt'))
        self.assertEqual(stale_files[1][0], os.path.join(root_path, 'file2.txt'))


if __name__ == '__main__':
    unittest.main()
