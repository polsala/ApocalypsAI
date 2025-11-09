import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the function to be tested
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_bunny_sweeper import find_dust_bunnies

class TestDustBunnySweeper(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('datetime.datetime')
    def test_no_dust_bunnies_found(self, mock_datetime, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory or files not meeting criteria.
        # This ensures the test is deterministic and doesn't rely on actual file system state.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]

        # Mock rationale: Control the current time for age calculation.
        # This makes the test deterministic regardless of when it's run.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = [
            datetime(2023, 10, 1, 9, 0, 0),  # file1.txt - too recent (25 days old)
            datetime(2023, 1, 1, 8, 0, 0)   # file2.log - old enough (298 days old)
        ]
        # Mock rationale: Control file sizes.
        # This makes the test deterministic and allows testing size criteria.
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_size = 500 * 1024 # 500KB, too small for 1MB default
        mock_stat.return_value = mock_stat_obj

        # Test with default criteria (older than 365 days, larger than 1MB)
        bunnies = find_dust_bunnies('/test_dir')
        self.assertEqual(len(bunnies), 0)

        # Test with custom criteria where files are still too small
        bunnies = find_dust_bunnies('/test_dir', older_than_days=30, larger_than_bytes=100 * 1024 * 1024) # 100MB
        self.assertEqual(len(bunnies), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('datetime.datetime')
    def test_dust_bunnies_found(self, mock_datetime, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with files that meet the criteria.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['old_large_file.zip']),
            ('/test_dir/subdir', [], ['another_old_large.bak', 'recent_small.txt'])
        ]

        # Mock rationale: Control the current time for age calculation.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        # Mock rationale: Control file modification times to simulate age.
        mock_datetime.fromtimestamp.side_effect = [
            datetime(2022, 1, 1, 10, 0, 0), # old_large_file.zip (663 days old)
            datetime(2022, 2, 1, 11, 0, 0), # another_old_large.bak (632 days old)
            datetime(2023, 9, 1, 12, 0, 0)  # recent_small.txt (55 days old)
        ]

        # Mock rationale: Control file sizes to simulate large files.
        mock_stat_obj_large = MagicMock()
        mock_stat_obj_large.st_size = 2 * 1024 * 1024 # 2MB
        mock_stat_obj_small = MagicMock()
        mock_stat_obj_small.st_size = 500 * 1024 # 500KB

        # Ensure stat returns correct size for each file in order of os.walk
        mock_stat.side_effect = [
            mock_stat_obj_large, # old_large_file.zip
            mock_stat_obj_large, # another_old_large.bak
            mock_stat_obj_small  # recent_small.txt
        ]

        # Test with default criteria (older than 365 days, larger than 1MB)
        bunnies = find_dust_bunnies('/test_dir')

        self.assertEqual(len(bunnies), 2)
        self.assertIn({
            "path": os.path.join('/test_dir', 'old_large_file.zip'),
            "age_days": 663,
            "size_bytes": 2 * 1024 * 1024
        }, bunnies)
        self.assertIn({
            "path": os.path.join('/test_dir/subdir', 'another_old_large.bak'),
            "age_days": 632,
            "size_bytes": 2 * 1024 * 1024
        }, bunnies)

        # Test with custom criteria (older than 600 days, larger than 1.5MB)
        bunnies_custom = find_dust_bunnies('/test_dir', older_than_days=600, larger_than_bytes=1.5 * 1024 * 1024)
        self.assertEqual(len(bunnies_custom), 2) # Both still qualify

        # Test with stricter custom criteria (older than 700 days)
        bunnies_stricter = find_dust_bunnies('/test_dir', older_than_days=700, larger_than_bytes=1 * 1024 * 1024)
        self.assertEqual(len(bunnies_stricter), 0) # No files are 700+ days old

    @patch('os.path.isdir')
    def test_invalid_path(self, mock_isdir):
        # Mock rationale: Simulate an invalid directory path.
        mock_isdir.return_value = False
        bunnies = find_dust_bunnies('/non_existent_dir')
        self.assertEqual(len(bunnies), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('datetime.datetime')
    def test_os_error_handling(self, mock_datetime, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulate an OSError during file access (e.g., permissions).
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['accessible_file.txt', 'inaccessible_file.log'])
        ]

        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = [
            datetime(2022, 1, 1, 10, 0, 0), # accessible_file.txt
            datetime(2022, 1, 1, 10, 0, 0)  # inaccessible_file.log
        ]

        mock_stat_obj = MagicMock()
        mock_stat_obj.st_size = 2 * 1024 * 1024 # 2MB

        # Mock rationale: Make os.stat raise an OSError for the second file.
        mock_stat.side_effect = [
            mock_stat_obj,
            OSError("Permission denied")
        ]

        bunnies = find_dust_bunnies('/test_dir')
        self.assertEqual(len(bunnies), 1) # Only the accessible file should be found
        self.assertEqual(bunnies[0]['path'], os.path.join('/test_dir', 'accessible_file.txt'))


if __name__ == '__main__':
    unittest.main()
