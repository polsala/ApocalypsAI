import unittest
import os
import shutil
import tempfile
import time
from unittest.mock import patch, call
from datetime import datetime, timedelta

# Import the functions from the collector script
from src.collector import find_empty_dirs, find_old_files, clean_up

class TestCosmicDustBunnyCollector(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing to ensure isolation and clean state
        self.test_dir = tempfile.mkdtemp()
        # Store a consistent 'current time' for tests involving file ages
        self.current_time = time.time()

    def tearDown(self):
        # Clean up the temporary directory and its contents after each test
        shutil.rmtree(self.test_dir)

    def _create_file(self, path, age_days=0):
        """Helper to create a file within the test directory with a specific modification time."""
        full_path = os.path.join(self.test_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write('test content')
        # Set modification time relative to self.current_time
        mod_time = self.current_time - (age_days * 24 * 60 * 60)
        os.utime(full_path, (mod_time, mod_time))
        return full_path

    def _create_dir(self, path):
        """Helper to create a directory within the test directory."""
        full_path = os.path.join(self.test_dir, path)
        os.makedirs(full_path, exist_ok=True)
        return full_path

    def test_find_empty_dirs_no_empty(self):
        # Test case: Directory with files and subdirectories, no truly empty ones
        self._create_file('dir1/file1.txt')
        self._create_dir('dir2/subdir1') # Not empty, contains subdir
        empty_dirs = find_empty_dirs(self.test_dir)
        self.assertEqual(len(empty_dirs), 0)

    def test_find_empty_dirs_simple_empty(self):
        # Test case: A single empty directory
        empty_path = self._create_dir('empty_dir')
        empty_dirs = find_empty_dirs(self.test_dir)
        self.assertIn(empty_path, empty_dirs)
        self.assertEqual(len(empty_dirs), 1)

    def test_find_empty_dirs_nested_empty(self):
        # Test case: Nested empty directories, ensuring correct order for deletion
        self._create_dir('parent/child/grandchild')
        empty_dirs = find_empty_dirs(self.test_dir)
        # Should find grandchild, child, and parent if they are truly empty
        # The function sorts by length descending, so deepest first
        expected_dirs = [
            os.path.join(self.test_dir, 'parent/child/grandchild'),
            os.path.join(self.test_dir, 'parent/child'),
            os.path.join(self.test_dir, 'parent')
        ]
        self.assertEqual(empty_dirs, expected_dirs)
        self.assertEqual(len(empty_dirs), 3)

    def test_find_empty_dirs_mixed(self):
        # Test case: Mix of empty and non-empty directories
        self._create_file('dir_with_file/file.txt')
        empty_path1 = self._create_dir('empty_dir1')
        self._create_dir('parent_empty/child_empty')
        # The order depends on os.walk and then the sort key
        empty_dirs = find_empty_dirs(self.test_dir)
        self.assertIn(empty_path1, empty_dirs)
        self.assertIn(os.path.join(self.test_dir, 'parent_empty/child_empty'), empty_dirs)
        self.assertIn(os.path.join(self.test_dir, 'parent_empty'), empty_dirs)
        self.assertEqual(len(empty_dirs), 3)

    @patch('time.time') # Mock rationale: To control the 'current time' for deterministic age calculations.
    def test_find_old_files_no_old_files(self, mock_time):
        mock_time.return_value = self.current_time
        # Create files that are not older than the threshold
        self._create_file('recent_file.txt', age_days=1)
        self._create_file('another_recent.log', age_days=5)
        old_files = find_old_files(self.test_dir, days_old=10)
        self.assertEqual(len(old_files), 0)

    @patch('time.time') # Mock rationale: To control the 'current time' for deterministic age calculations.
    def test_find_old_files_some_old_files(self, mock_time):
        mock_time.return_value = self.current_time
        # Create some old files and some recent ones
        old_file1 = self._create_file('old_file1.txt', age_days=15)
        self._create_file('recent_file.txt', age_days=5)
        old_file2 = self._create_file('subdir/old_file2.log', age_days=12)
        old_files = find_old_files(self.test_dir, days_old=10)
        self.assertIn(old_file1, old_files)
        self.assertIn(old_file2, old_files)
        self.assertEqual(len(old_files), 2)

    @patch('time.time') # Mock rationale: To control the 'current time' for deterministic age calculations.
    def test_find_old_files_edge_case_exact_age(self, mock_time):
        mock_time.return_value = self.current_time
        # File exactly 10 days old should be considered old if days_old is 10
        exact_old_file = self._create_file('exact_old.txt', age_days=10)
        # File slightly less than 10 days old should not be considered old
        less_old_file = self._create_file('less_old.txt', age_days=9.9)

        old_files = find_old_files(self.test_dir, days_old=10)
        self.assertIn(exact_old_file, old_files)
        self.assertNotIn(less_old_file, old_files)
        self.assertEqual(len(old_files), 1)

    def test_clean_up_dry_run_files(self):
        # Test dry-run for files: should print but not delete
        file_to_delete = self._create_file('temp_file.txt')
        self.assertTrue(os.path.exists(file_to_delete))
        with patch('builtins.print') as mock_print:
            clean_up([file_to_delete], dry_run=True, item_type="file")
            mock_print.assert_any_call(f"[DRY RUN] Would remove: {file_to_delete}")
        self.assertTrue(os.path.exists(file_to_delete)) # Should still exist in dry run

    def test_clean_up_actual_deletion_files(self):
        # Test actual deletion for files
        file_to_delete = self._create_file('temp_file.txt')
        self.assertTrue(os.path.exists(file_to_delete))
        with patch('builtins.print'): # Suppress print output for cleaner test logs
            clean_up([file_to_delete], dry_run=False, item_type="file")
        self.assertFalse(os.path.exists(file_to_delete)) # Should be deleted

    def test_clean_up_dry_run_dirs(self):
        # Test dry-run for directories: should print but not delete
        dir_to_delete = self._create_dir('temp_dir/subdir')
        self.assertTrue(os.path.isdir(dir_to_delete))
        with patch('builtins.print') as mock_print:
            clean_up([dir_to_delete], dry_run=True, item_type="directory")
            mock_print.assert_any_call(f"[DRY RUN] Would remove: {dir_to_delete}")
        self.assertTrue(os.path.isdir(dir_to_delete)) # Should still exist in dry run

    def test_clean_up_actual_deletion_dirs(self):
        # Test actual deletion for directories
        dir_to_delete = self._create_dir('temp_dir/subdir')
        self.assertTrue(os.path.isdir(dir_to_delete))
        with patch('builtins.print'): # Suppress print output
            clean_up([dir_to_delete], dry_run=False, item_type="directory")
        self.assertFalse(os.path.isdir(dir_to_delete)) # Should be deleted
        # Verify that parent directory is also gone if it became empty after child deletion
        self.assertFalse(os.path.isdir(os.path.join(self.test_dir, 'temp_dir')))

    def test_clean_up_with_non_existent_item(self):
        # Test that the cleanup function handles non-existent items gracefully without crashing
        non_existent_path = os.path.join(self.test_dir, 'non_existent_file.txt')
        with patch('builtins.print') as mock_print:
            clean_up([non_existent_path], dry_run=False, item_type="file")
            # Check if an error message was printed for the non-existent file
            mock_print.assert_any_call(unittest.mock.ANY)
            self.assertIn("Error removing file", mock_print.call_args_list[0].args[0])

    def test_clean_up_no_items(self):
        # Test when no items are passed to clean_up
        with patch('builtins.print') as mock_print:
            clean_up([], dry_run=False, item_type="nothing")
            mock_print.assert_called_once_with("No nothings found to clean up.")

if __name__ == '__main__':
    unittest.main()
