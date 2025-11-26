import unittest
import os
import shutil
import time
from unittest.mock import patch, MagicMock

# Import the functions from the module under test
from src.dust_collector import collect_dust, is_older_than, matches_patterns, get_current_time

class TestCosmicDustCollector(unittest.TestCase):

    # Mock rationale: We need to control the 'current time' for age calculations
    # to make tests deterministic and independent of the actual system time.
    @patch('src.dust_collector.get_current_time')
    def test_is_older_than(self, mock_get_current_time):
        mock_get_current_time.return_value = time.time() # Current time for the test
        current_time = mock_get_current_time.return_value

        # File modified 10 days ago
        mtime_10_days_ago = current_time - (10 * 24 * 60 * 60) - 1 # Ensure strictly older
        # File modified 5 days ago
        mtime_5_days_ago = current_time - (5 * 24 * 60 * 60)
        # File modified exactly 7 days ago
        mtime_7_days_ago = current_time - (7 * 24 * 60 * 60)

        # Mock rationale: os.path.getmtime is a system call that depends on actual file metadata.
        # We mock it to provide controlled modification times for our test files.
        with patch('os.path.getmtime', side_effect=[
            mtime_10_days_ago, # for file1
            mtime_5_days_ago,  # for file2
            mtime_7_days_ago,  # for file3
            mtime_10_days_ago  # for file4 (error test)
        ]):
            # Test with age_days = 7
            self.assertTrue(is_older_than('/path/to/file1', 7, current_time), "File 10 days old should be older than 7 days")
            self.assertFalse(is_older_than('/path/to/file2', 7, current_time), "File 5 days old should not be older than 7 days")

            # Test with age_days = 7 (boundary condition: exactly 7 days old is not 'older than 7 days')
            self.assertFalse(is_older_than('/path/to/file3', 7, current_time), "File exactly 7 days old should not be strictly older than 7 days")

        # Mock rationale: Test error handling for os.path.getmtime.
        with patch('os.path.getmtime', side_effect=OSError("Permission denied")):
            self.assertFalse(is_older_than('/path/to/unreadable_file', 7, current_time), "Should return False if mtime cannot be retrieved")

    def test_matches_patterns(self):
        self.assertTrue(matches_patterns('test.log', ['*.log']), "Should match single pattern")
        self.assertTrue(matches_patterns('temp_file.txt', ['temp_*', '*.tmp']), "Should match one of multiple patterns")
        self.assertFalse(matches_patterns('image.jpg', ['*.log', '*.txt']), "Should not match any pattern")
        self.assertTrue(matches_patterns('any_file.txt', []), "Should match all if no patterns provided")
        self.assertTrue(matches_patterns('another_dir', []), "Should match all if no patterns provided for directories")
        self.assertFalse(matches_patterns('test.log', ['*.txt']), "Should not match if pattern is different")

    # Mock rationale: We need to simulate a file system without actually creating files.
    # os.path.exists, os.path.isdir, os.path.isfile, os.walk, os.remove, shutil.rmtree
    # are all system calls that interact with the real file system. Mocking them
    # allows for deterministic, isolated, and fast tests.
    @patch('src.dust_collector.get_current_time')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('os.walk')
    def test_collect_dust_dry_run(self, mock_walk, mock_isfile, mock_isdir, mock_exists, mock_rmtree, mock_remove, mock_getmtime, mock_get_current_time):
        test_path = '/mock/root'
        mock_exists.return_value = True
        # Simulate directories and files based on path names
        mock_isdir.side_effect = lambda p: 'dir' in p and not 'file' in p
        mock_isfile.side_effect = lambda p: 'file' in p

        # Set current time to a fixed point
        fixed_current_time = time.time()
        mock_get_current_time.return_value = fixed_current_time

        # Define modification times for mock files/dirs
        # Older than 7 days (e.g., 10 days old)
        mtime_old = fixed_current_time - (10 * 24 * 60 * 60) - 1
        # Newer than 7 days (e.g., 5 days old)
        mtime_new = fixed_current_time - (5 * 24 * 60 * 60)

        # Mock os.walk to simulate a directory structure
        # (root, dirs, files)
        mock_walk.return_value = [
            (test_path, ['dir_old', 'dir_new'], ['file_old.log', 'file_new.txt', 'keep_me_old.txt']),
            (os.path.join(test_path, 'dir_old'), [], ['sub_file_old.tmp']),
            (os.path.join(test_path, 'dir_new'), [], ['sub_file_new.log']),
        ]

        # Mock os.path.getmtime for each file/dir
        def mock_getmtime_side_effect(path):
            if 'old' in path:
                return mtime_old
            elif 'new' in path:
                return mtime_new
            return fixed_current_time # Default for others

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Test 1: Dry run, age 7 days, patterns ['*.log', '*.tmp', 'dir_old']
        expected_deleted = [
            os.path.join(test_path, 'file_old.log'),
            os.path.join(test_path, 'dir_old', 'sub_file_old.tmp'),
            os.path.join(test_path, 'dir_old'),
        ]
        deleted_items = collect_dust(test_path, 7, ['*.log', '*.tmp', 'dir_old'], dry_run=True, verbose=False)

        self.assertCountEqual(deleted_items, expected_deleted)
        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()

        # Test 2: Dry run, no patterns (should list all old files/dirs)
        # Reset mock_walk for the new test case
        mock_walk.return_value = [
            (test_path, ['dir_old', 'dir_new'], ['file_old.log', 'file_new.txt', 'keep_me_old.txt']),
            (os.path.join(test_path, 'dir_old'), [], ['sub_file_old.tmp']),
            (os.path.join(test_path, 'dir_new'), [], ['sub_file_new.log']),
        ]
        expected_deleted_no_patterns = [
            os.path.join(test_path, 'file_old.log'),
            os.path.join(test_path, 'keep_me_old.txt'), # This one is old, no pattern filter
            os.path.join(test_path, 'dir_old', 'sub_file_old.tmp'),
            os.path.join(test_path, 'dir_old'),
        ]
        deleted_items_no_patterns = collect_dust(test_path, 7, [], dry_run=True, verbose=False)
        self.assertCountEqual(deleted_items_no_patterns, expected_deleted_no_patterns)

    @patch('src.dust_collector.get_current_time')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    @patch('os.walk')
    def test_collect_dust_actual_run(self, mock_walk, mock_isfile, mock_isdir, mock_exists, mock_rmtree, mock_remove, mock_getmtime, mock_get_current_time):
        test_path = '/mock/root'
        mock_exists.return_value = True
        mock_isdir.side_effect = lambda p: 'dir' in p and not 'file' in p
        mock_isfile.side_effect = lambda p: 'file' in p

        fixed_current_time = time.time()
        mock_get_current_time.return_value = fixed_current_time
        mtime_old = fixed_current_time - (10 * 24 * 60 * 60) - 1
        mtime_new = fixed_current_time - (5 * 24 * 60 * 60)

        def mock_getmtime_side_effect(path):
            if 'old' in path:
                return mtime_old
            elif 'new' in path:
                return mtime_new
            return fixed_current_time

        mock_getmtime.side_effect = mock_getmtime_side_effect

        mock_walk.return_value = [
            (test_path, ['dir_old', 'dir_new'], ['file_old.log', 'file_new.txt', 'keep_me_old.txt']),
            (os.path.join(test_path, 'dir_old'), [], ['sub_file_old.tmp']),
            (os.path.join(test_path, 'dir_new'), [], ['sub_file_new.log']),
        ]

        expected_deleted = [
            os.path.join(test_path, 'file_old.log'),
            os.path.join(test_path, 'dir_old', 'sub_file_old.tmp'),
            os.path.join(test_path, 'dir_old'),
        ]
        deleted_items = collect_dust(test_path, 7, ['*.log', '*.tmp', 'dir_old'], dry_run=False, verbose=False)

        self.assertCountEqual(deleted_items, expected_deleted)
        # Assert that os.remove and shutil.rmtree were called for the correct items
        mock_remove.assert_any_call(os.path.join(test_path, 'file_old.log'))
        mock_remove.assert_any_call(os.path.join(test_path, 'dir_old', 'sub_file_old.tmp'))
        mock_rmtree.assert_any_call(os.path.join(test_path, 'dir_old'))
        self.assertEqual(mock_remove.call_count, 2)
        self.assertEqual(mock_rmtree.call_count, 1)

    # Mock rationale: os.path.exists is a system call. Mocking it allows simulating
    # scenarios where the target path does not exist without actual file system interaction.
    @patch('os.path.exists', return_value=False)
    def test_collect_dust_path_not_exists(self, mock_exists):
        deleted_items = collect_dust('/non/existent/path', 7, [], dry_run=True)
        self.assertEqual(deleted_items, [])
        mock_exists.assert_called_once_with('/non/existent/path')

    # Mock rationale: os.remove and shutil.rmtree are system calls. Mocking them
    # with side_effect=OSError allows testing error handling during deletion
    # without actual file system interaction or needing specific permissions.
    @patch('src.dust_collector.get_current_time')
    @patch('os.path.getmtime')
    @patch('os.remove', side_effect=OSError("Permission denied"))
    @patch('shutil.rmtree', side_effect=OSError("Permission denied"))
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    def test_collect_dust_deletion_error(self, mock_walk, mock_isfile, mock_isdir, mock_exists, mock_rmtree, mock_remove, mock_getmtime, mock_get_current_time):
        test_path = '/mock/root'
        fixed_current_time = time.time()
        mock_get_current_time.return_value = fixed_current_time
        mtime_old = fixed_current_time - (10 * 24 * 60 * 60) - 1
        mock_getmtime.return_value = mtime_old

        mock_walk.return_value = [
            (test_path, [], ['file_old.log']),
        ]

        # Even with deletion errors, the item is still 'considered' for deletion and added to the list
        # because the function reports what *would* be deleted or attempted to be deleted.
        deleted_items = collect_dust(test_path, 7, ['*.log'], dry_run=False, verbose=False)
        self.assertCountEqual(deleted_items, [os.path.join(test_path, 'file_old.log')])
        mock_remove.assert_called_once_with(os.path.join(test_path, 'file_old.log'))


if __name__ == '__main__':
    unittest.main()
