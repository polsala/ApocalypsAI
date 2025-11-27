import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.cleaner import find_stale_files, archive_files

class TestCacheCleaner(unittest.TestCase):

    # Mock rationale: We need a deterministic "current time" for age calculations.
    # This ensures tests don't fail based on when they are run.
    MOCK_CURRENT_TIME = time.mktime(datetime(2023, 10, 26, 10, 0, 0).timetuple())

    @patch('time.time', return_value=MOCK_CURRENT_TIME) # Mock rationale: Fix current time for deterministic age calculations.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume the base directory exists for scanning.
    @patch('os.walk') # Mock rationale: Simulate directory structure and files without actual disk access.
    @patch('os.stat') # Mock rationale: Control file metadata (modification time, size) for deterministic results.
    def test_find_stale_files_by_age(self, mock_stat, mock_walk, mock_isdir, mock_time):
        # Setup mock_walk to simulate a directory with files
        # (root, dirs, files)
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.txt', 'new_file.log', 'medium_file.tmp'])
        ]

        # Setup mock_stat for each file
        # old_file.txt: modified 60 days ago (stale)
        # new_file.log: modified 10 days ago (not stale)
        # medium_file.tmp: modified 40 days ago (stale)
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if 'old_file.txt' in path:
                mock_stat_obj.st_mtime = self.MOCK_CURRENT_TIME - (60 * 24 * 60 * 60) # 60 days old
                mock_stat_obj.st_size = 10 * 1024 # 10 KB
            elif 'new_file.log' in path:
                mock_stat_obj.st_mtime = self.MOCK_CURRENT_TIME - (10 * 24 * 60 * 60) # 10 days old
                mock_stat_obj.st_size = 50 * 1024 # 50 KB
            elif 'medium_file.tmp' in path:
                mock_stat_obj.st_mtime = self.MOCK_CURRENT_TIME - (40 * 24 * 60 * 60) # 40 days old
                mock_stat_obj.st_size = 20 * 1024 # 20 KB
            return mock_stat_obj
        mock_stat.side_effect = mock_stat_side_effect

        # Test with age_days = 30, size_mb = 100 (size is irrelevant here)
        stale_files = find_stale_files('/test_dir', age_days=30, size_mb=100)
        self.assertIn('/test_dir/old_file.txt', stale_files)
        self.assertIn('/test_dir/medium_file.tmp', stale_files)
        self.assertNotIn('/test_dir/new_file.log', stale_files)
        self.assertEqual(len(stale_files), 2)

    @patch('time.time', return_value=MOCK_CURRENT_TIME) # Mock rationale: Fix current time for deterministic age calculations.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume the base directory exists for scanning.
    @patch('os.walk') # Mock rationale: Simulate directory structure and files without actual disk access.
    @patch('os.stat') # Mock rationale: Control file metadata (modification time, size) for deterministic results.
    def test_find_stale_files_by_size(self, mock_stat, mock_walk, mock_isdir, mock_time):
        mock_walk.return_value = [
            ('/test_dir', [], ['small.txt', 'large.bin', 'medium.data'])
        ]

        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            # All files are recent (1 day old) to isolate size check
            mock_stat_obj.st_mtime = self.MOCK_CURRENT_TIME - (1 * 24 * 60 * 60)
            if 'small.txt' in path:
                mock_stat_obj.st_size = 5 * 1024 * 1024 # 5 MB
            elif 'large.bin' in path:
                mock_stat_obj.st_size = 150 * 1024 * 1024 # 150 MB (stale)
            elif 'medium.data' in path:
                mock_stat_obj.st_size = 80 * 1024 * 1024 # 80 MB
            return mock_stat_obj
        mock_stat.side_effect = mock_stat_side_effect

        # Test with age_days = 1 (irrelevant), size_mb = 100
        stale_files = find_stale_files('/test_dir', age_days=1, size_mb=100)
        self.assertIn('/test_dir/large.bin', stale_files)
        self.assertNotIn('/test_dir/small.txt', stale_files)
        self.assertNotIn('/test_dir/medium.data', stale_files)
        self.assertEqual(len(stale_files), 1)

    @patch('time.time', return_value=MOCK_CURRENT_TIME) # Mock rationale: Fix current time for deterministic age calculations.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume the base directory exists for scanning.
    @patch('os.walk') # Mock rationale: Simulate directory structure and files without actual disk access.
    @patch('os.stat') # Mock rationale: Control file metadata (modification time, size) for deterministic results.
    def test_find_stale_files_combined_criteria(self, mock_stat, mock_walk, mock_isdir, mock_time):
        mock_walk.return_value = [
            ('/test_dir', [], ['old_small.txt', 'new_large.bin', 'old_large.data', 'new_small.log'])
        ]

        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if 'old_small.txt' in path: # Old, Small -> Stale by age
                mock_stat_obj.st_mtime = self.MOCK_CURRENT_TIME - (60 * 24 * 60 * 60)
                mock_stat_obj.st_size = 10 * 1024 * 1024 # 10 MB
            elif 'new_large.bin' in path: # New, Large -> Stale by size
                mock_stat_obj.st_mtime = self.MOCK_CURRENT_TIME - (5 * 24 * 60 * 60)
                mock_stat_obj.st_size = 150 * 1024 * 1024 # 150 MB
            elif 'old_large.data' in path: # Old, Large -> Stale by both
                mock_stat_obj.st_mtime = self.MOCK_CURRENT_TIME - (40 * 24 * 60 * 60)
                mock_stat_obj.st_size = 120 * 1024 * 1024 # 120 MB
            elif 'new_small.log' in path: # New, Small -> Not stale
                mock_stat_obj.st_mtime = self.MOCK_CURRENT_TIME - (10 * 24 * 60 * 60)
                mock_stat_obj.st_size = 5 * 1024 * 1024 # 5 MB
            return mock_stat_obj
        mock_stat.side_effect = mock_stat_side_effect

        # Test with age_days = 30, size_mb = 100
        stale_files = find_stale_files('/test_dir', age_days=30, size_mb=100)
        self.assertIn('/test_dir/old_small.txt', stale_files)
        self.assertIn('/test_dir/new_large.bin', stale_files)
        self.assertIn('/test_dir/old_large.data', stale_files)
        self.assertNotIn('/test_dir/new_small.log', stale_files)
        self.assertEqual(len(stale_files), 3)

    @patch('os.path.isdir', return_value=False) # Mock rationale: Simulate a non-existent directory.
    def test_find_stale_files_non_existent_directory(self, mock_isdir):
        stale_files = find_stale_files('/non_existent_dir', age_days=30, size_mb=100)
        self.assertEqual(stale_files, [])

    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume the base directory exists.
    @patch('os.walk', return_value=[('/empty_dir', [], [])]) # Mock rationale: Simulate an empty directory.
    @patch('os.stat') # Mock rationale: Not called if no files, but good to have.
    def test_find_stale_files_empty_directory(self, mock_stat, mock_walk, mock_isdir):
        stale_files = find_stale_files('/empty_dir', age_days=30, size_mb=100)
        self.assertEqual(stale_files, [])

    @patch('os.makedirs') # Mock rationale: Prevent actual directory creation.
    @patch('shutil.move') # Mock rationale: Prevent actual file movement.
    @patch('os.path.exists', side_effect=[False, True, False]) # Mock rationale: Control collision check for destination path.
    @patch('datetime.datetime') # Mock rationale: Fix timestamp for collision handling.
    def test_archive_files(self, mock_datetime, mock_exists, mock_move, mock_makedirs):
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 30, 0) # Mock rationale: Fix timestamp for deterministic collision naming.
        mock_datetime.now().strftime.return_value = "20231026103000" # Mock rationale: Fix timestamp format.

        files_to_archive = ['/src/file1.txt', '/src/file2.log']
        archive_dir = '/archive_dest'

        archived_files = archive_files(files_to_archive, archive_dir)

        mock_makedirs.assert_called_once_with(archive_dir, exist_ok=True)
        self.assertEqual(mock_move.call_count, 2)
        mock_move.assert_any_call('/src/file1.txt', '/archive_dest/file1.txt')
        # The second file will trigger the collision logic due to mock_exists side_effect
        mock_move.assert_any_call('/src/file2.log', '/archive_dest/file2.log_20231026103000.log')
        self.assertEqual(len(archived_files), 2)
        self.assertIn('/archive_dest/file1.txt', archived_files)
        self.assertIn('/archive_dest/file2.log_20231026103000.log', archived_files)

    @patch('os.makedirs') # Mock rationale: Prevent actual directory creation.
    @patch('shutil.move') # Mock rationale: Prevent actual file movement.
    def test_archive_files_empty_list(self, mock_move, mock_makedirs):
        archived_files = archive_files([], '/archive_dest')
        mock_makedirs.assert_not_called()
        mock_move.assert_not_called()
        self.assertEqual(archived_files, [])

    @patch('os.makedirs') # Mock rationale: Prevent actual directory creation.
    @patch('shutil.move', side_effect=Exception("Permission denied")) # Mock rationale: Simulate an error during file movement.
    @patch('os.path.exists', return_value=False) # Mock rationale: No collision for simplicity.
    @patch('datetime.datetime') # Mock rationale: Fix timestamp for collision handling.
    def test_archive_files_with_error(self, mock_datetime, mock_exists, mock_move, mock_makedirs):
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 30, 0)
        mock_datetime.now().strftime.return_value = "20231026103000"

        files_to_archive = ['/src/file1.txt']
        archive_dir = '/archive_dest'

        archived_files = archive_files(files_to_archive, archive_dir)

        mock_makedirs.assert_called_once_with(archive_dir, exist_ok=True)
        mock_move.assert_called_once_with('/src/file1.txt', '/archive_dest/file1.txt')
        self.assertEqual(len(archived_files), 0) # No files successfully archived
