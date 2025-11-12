import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timedelta
import shutil

# Mock rationale: We need to simulate file system interactions (creating files, getting stats, moving/deleting) 
# without actually touching the disk. This ensures tests are fast, deterministic, and don't leave artifacts.
# We also mock datetime.now() to control the 'current time' for age calculations.

# Import the functions to be tested
from src.dust_collector import find_dust_bunnies, quarantine_dust_bunnies, delete_dust_bunnies

class TestCosmicDustBunnyCollector(unittest.TestCase):

    @patch('src.dust_collector.datetime')
    @patch('src.dust_collector.os.walk')
    @patch('src.dust_collector.os.stat')
    def test_find_dust_bunnies_basic(self, mock_os_stat, mock_os_walk, mock_datetime):
        # Mock rationale: Simulate the current time for age comparison.
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp # Allow actual timestamp conversion
        mock_datetime.timedelta = timedelta # Allow timedelta to work normally

        # Mock rationale: Simulate a directory structure with files of different ages and sizes.
        # os.walk returns (root, dirs, files)
        mock_os_walk.return_value = [
            ('/test_dir', [], ['old_small.txt', 'new_small.txt', 'old_large.txt', 'new_large.txt'])
        ]

        # Mock rationale: Simulate os.stat results for each file.
        # st_mtime is last modified time, st_size is file size.
        # old_small.txt: old, small -> should be a dust bunny
        # new_small.txt: new, small -> not a dust bunny
        # old_large.txt: old, large -> not a dust bunny
        # new_large.txt: new, large -> not a dust bunny
        
        # Define mock stat objects
        mock_stat_old_small = MagicMock()
        mock_stat_old_small.st_mtime = (datetime(2022, 9, 1) - datetime(1970, 1, 1)).total_seconds() # Older than 90 days
        mock_stat_old_small.st_size = 500 # 0.5 KB, smaller than 1KB

        mock_stat_new_small = MagicMock()
        mock_stat_new_small.st_mtime = (datetime(2022, 11, 15) - datetime(1970, 1, 1)).total_seconds() # Newer than 90 days
        mock_stat_new_small.st_size = 500 # 0.5 KB, smaller than 1KB

        mock_stat_old_large = MagicMock()
        mock_stat_old_large.st_mtime = (datetime(2022, 9, 1) - datetime(1970, 1, 1)).total_seconds() # Older than 90 days
        mock_stat_old_large.st_size = 2000 # 2 KB, larger than 1KB

        mock_stat_new_large = MagicMock()
        mock_stat_new_large.st_mtime = (datetime(2022, 11, 15) - datetime(1970, 1, 1)).total_seconds() # Newer than 90 days
        mock_stat_new_large.st_size = 2000 # 2 KB, larger than 1KB

        # Map file paths to their mock stat objects
        def mock_stat_side_effect(path):
            if 'old_small.txt' in path: return mock_stat_old_small
            if 'new_small.txt' in path: return mock_stat_new_small
            if 'old_large.txt' in path: return mock_stat_old_large
            if 'new_large.txt' in path: return mock_stat_new_large
            raise FileNotFoundError # Should not happen with current mock_os_walk

        mock_os_stat.side_effect = mock_stat_side_effect

        # Run the function with default parameters (age_days=90, max_size_kb=1)
        dust_bunnies = find_dust_bunnies('/test_dir', 90, 1)

        self.assertEqual(len(dust_bunnies), 1)
        self.assertIn('old_small.txt', dust_bunnies[0]['path'])
        self.assertEqual(dust_bunnies[0]['size'], 500)

    @patch('src.dust_collector.datetime')
    @patch('src.dust_collector.os.walk')
    @patch('src.dust_collector.os.stat')
    def test_find_dust_bunnies_no_matches(self, mock_os_stat, mock_os_walk, mock_datetime):
        # Mock rationale: Simulate the current time for age comparison.
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta

        # Mock rationale: Simulate files that don't meet the criteria.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['new_small.txt', 'old_large.txt'])
        ]

        mock_stat_new_small = MagicMock()
        mock_stat_new_small.st_mtime = (datetime(2022, 11, 15) - datetime(1970, 1, 1)).total_seconds()
        mock_stat_new_small.st_size = 500

        mock_stat_old_large = MagicMock()
        mock_stat_old_large.st_mtime = (datetime(2022, 9, 1) - datetime(1970, 1, 1)).total_seconds()
        mock_stat_old_large.st_size = 2000

        def mock_stat_side_effect(path):
            if 'new_small.txt' in path: return mock_stat_new_small
            if 'old_large.txt' in path: return mock_stat_old_large
            raise FileNotFoundError

        mock_os_stat.side_effect = mock_stat_side_effect

        dust_bunnies = find_dust_bunnies('/test_dir', 90, 1)
        self.assertEqual(len(dust_bunnies), 0)

    @patch('src.dust_collector.datetime')
    @patch('src.dust_collector.os.walk')
    @patch('src.dust_collector.os.stat')
    def test_find_dust_bunnies_empty_dir(self, mock_os_stat, mock_os_walk, mock_datetime):
        # Mock rationale: Simulate an empty directory.
        mock_os_walk.return_value = [
            ('/empty_dir', [], [])
        ]
        dust_bunnies = find_dust_bunnies('/empty_dir', 90, 1)
        self.assertEqual(len(dust_bunnies), 0)
        mock_os_stat.assert_not_called() # No files to stat

    @patch('src.dust_collector.os.makedirs')
    @patch('src.dust_collector.shutil.move')
    @patch('builtins.print') # Mock rationale: Capture print output for verification
    def test_quarantine_dust_bunnies(self, mock_print, mock_shutil_move, mock_os_makedirs):
        # Mock rationale: Simulate a list of files to be quarantined.
        dust_bunnies = [
            {'path': '/src/file1.txt', 'size': 100, 'last_modified': datetime.now()},
            {'path': '/src/nested/file2.txt', 'size': 200, 'last_modified': datetime.now()}
        ]
        quarantine_dir = '/quarantine_zone'

        quarantine_dust_bunnies(dust_bunnies, quarantine_dir)

        mock_os_makedirs.assert_called_once_with(quarantine_dir, exist_ok=True)
        mock_shutil_move.assert_any_call('/src/file1.txt', '/quarantine_zone/file1.txt')
        mock_shutil_move.assert_any_call('/src/nested/file2.txt', '/quarantine_zone/file2.txt')
        self.assertEqual(mock_shutil_move.call_count, 2)
        mock_print.assert_any_call(f"Moving 2 dust bunnies to quarantine zone: '{quarantine_dir}'")

    @patch('src.dust_collector.os.remove')
    @patch('builtins.input', return_value='DELETE') # Mock rationale: Simulate user confirmation for deletion.
    @patch('builtins.print') # Mock rationale: Capture print output for verification
    def test_delete_dust_bunnies_confirmed(self, mock_print, mock_input, mock_os_remove):
        # Mock rationale: Simulate a list of files to be deleted.
        dust_bunnies = [
            {'path': '/src/file1.txt', 'size': 100, 'last_modified': datetime.now()},
            {'path': '/src/file2.txt', 'size': 200, 'last_modified': datetime.now()}
        ]

        delete_dust_bunnies(dust_bunnies)

        mock_input.assert_called_once_with("Type 'DELETE' to confirm: ")
        mock_os_remove.assert_any_call('/src/file1.txt')
        mock_os_remove.assert_any_call('/src/file2.txt')
        self.assertEqual(mock_os_remove.call_count, 2)
        mock_print.assert_any_call("Permanently deleting 2 dust bunnies. This action is irreversible!")

    @patch('src.dust_collector.os.remove')
    @patch('builtins.input', return_value='NO') # Mock rationale: Simulate user cancelling deletion.
    @patch('builtins.print') # Mock rationale: Capture print output for verification
    def test_delete_dust_bunnies_cancelled(self, mock_print, mock_input, mock_os_remove):
        dust_bunnies = [
            {'path': '/src/file1.txt', 'size': 100, 'last_modified': datetime.now()}
        ]

        delete_dust_bunnies(dust_bunnies)

        mock_input.assert_called_once_with("Type 'DELETE' to confirm: ")
        mock_os_remove.assert_not_called()
        mock_print.assert_any_call("Deletion cancelled.")

    @patch('src.dust_collector.os.walk')
    @patch('src.dust_collector.os.stat')
    @patch('src.dust_collector.datetime')
    @patch('builtins.print')
    def test_find_dust_bunnies_os_error(self, mock_print, mock_datetime, mock_os_stat, mock_os_walk):
        # Mock rationale: Simulate an OSError when trying to stat a file.
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta

        mock_os_walk.return_value = [
            ('/test_dir', [], ['unreadable.txt'])
        ]

        mock_os_stat.side_effect = OSError("Permission denied")

        dust_bunnies = find_dust_bunnies('/test_dir', 90, 1, verbose=True)
        self.assertEqual(len(dust_bunnies), 0)
        mock_print.assert_any_call("  Warning: Could not access /test_dir/unreadable.txt: Permission denied")


if __name__ == '__main__':
    unittest.main()
