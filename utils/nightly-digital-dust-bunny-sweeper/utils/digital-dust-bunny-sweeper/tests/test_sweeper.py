import unittest
from unittest.mock import patch, mock_open
import os
import sys
import time
from datetime import datetime, timedelta

# Add the src directory to the path to import sweeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sweeper

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Define a consistent "current time" for tests
        self.mock_current_time = datetime(2023, 10, 26, 10, 0, 0)
        self.mock_current_timestamp = self.mock_current_time.timestamp()

        # Mock os.path.getmtime and os.path.getsize
        # Mock rationale: These functions interact with the file system and need to return
        # predictable values for deterministic, offline testing.
        self.mock_getmtime_patcher = patch('os.path.getmtime')
        self.mock_getmtime = self.mock_getmtime_patcher.start()
        self.mock_getmtime.side_effect = self._mock_getmtime_impl

        self.mock_getsize_patcher = patch('os.path.getsize')
        self.mock_getsize = self.mock_getsize_patcher.start()
        self.mock_getsize.side_effect = self._mock_getsize_impl

        # Mock os.walk
        # Mock rationale: os.walk traverses the file system. Mocking it allows us to
        # define a virtual file system structure for tests, ensuring determinism.
        self.mock_os_walk_patcher = patch('os.walk')
        self.mock_os_walk = self.mock_os_walk_patcher.start()
        self.mock_os_walk.return_value = self._mock_os_walk_data()

        # Mock get_file_hash
        # Mock rationale: Hashing file content is an I/O operation. Mocking it ensures
        # determinism and avoids actual file reads during tests.
        self.mock_get_file_hash_patcher = patch('sweeper.get_file_hash')
        self.mock_get_file_hash = self.mock_get_file_hash_patcher.start()
        self.mock_get_file_hash.side_effect = self._mock_get_file_hash_impl

        # Mock time.time()
        # Mock rationale: time.time() returns the current timestamp, which is non-deterministic.
        # Mocking it ensures that age calculations are consistent across test runs.
        self.mock_time_time_patcher = patch('time.time', return_value=self.mock_current_timestamp)
        self.mock_time_time = self.mock_time_time_patcher.start()

        # Mock os.path.isdir for main function
        # Mock rationale: Prevents actual file system checks when testing the main function's
        # argument parsing and initial directory validation.
        self.mock_isdir_patcher = patch('os.path.isdir', return_value=True)
        self.mock_isdir = self.mock_isdir_patcher.start()

    def tearDown(self):
        self.mock_getmtime_patcher.stop()
        self.mock_getsize_patcher.stop()
        self.mock_os_walk_patcher.stop()
        self.mock_get_file_hash_patcher.stop()
        self.mock_time_time_patcher.stop()
        self.mock_isdir_patcher.stop()
        sys.path.pop(0) # Clean up sys.path

    # --- Mock Implementations ---
    def _mock_getmtime_impl(self, path):
        # Define specific modification times for test files
        if "giant_old_file.txt" in path:
            return (self.mock_current_time - timedelta(days=400)).timestamp() # Older than 365 days
        if "giant_new_file.txt" in path:
            return (self.mock_current_time - timedelta(days=10)).timestamp() # Newer than 365 days
        if "small_old_file.txt" in path:
            return (self.mock_current_time - timedelta(days=400)).timestamp() # Older than 365 days
        if "small_new_file.txt" in path:
            return (self.mock_current_time - timedelta(days=10)).timestamp() # Newer than 365 days
        if "duplicate_file_a.txt" in path:
            return (self.mock_current_time - timedelta(days=50)).timestamp()
        if "duplicate_file_b.txt" in path:
            return (self.mock_current_time - timedelta(days=60)).timestamp()
        if "unique_file.txt" in path:
            return (self.mock_current_time - timedelta(days=70)).timestamp()
        return self.mock_current_timestamp # Default for other files

    def _mock_getsize_impl(self, path):
        # Define specific sizes for test files
        if "giant_old_file.txt" in path:
            return 200 * 1024 * 1024 # 200 MB
        if "giant_new_file.txt" in path:
            return 150 * 1024 * 1024 # 150 MB
        if "small_old_file.txt" in path:
            return 5 * 1024 * 1024 # 5 MB
        if "small_new_file.txt" in path:
            return 2 * 1024 * 1024 # 2 MB
        if "duplicate_file_a.txt" in path:
            return 10 * 1024 * 1024 # 10 MB
        if "duplicate_file_b.txt" in path:
            return 10 * 1024 * 1024 # 10 MB
        if "unique_file.txt" in path:
            return 12 * 1024 * 1024 # 12 MB
        return 100 # Default small size

    def _mock_os_walk_data(self):
        # Simulate a directory structure
        # root, dirs, files
        return [
            ('/mock/dir', ['subdir'], ['giant_old_file.txt', 'giant_new_file.txt', 'small_old_file.txt']),
            ('/mock/dir/subdir', [], ['small_new_file.txt', 'duplicate_file_a.txt', 'duplicate_file_b.txt', 'unique_file.txt'])
        ]

    def _mock_get_file_hash_impl(self, filepath, block_size=65536):
        # Return predictable hashes based on filename for duplicate detection
        if "duplicate_file_a.txt" in filepath or "duplicate_file_b.txt" in filepath:
            return "mock_hash_duplicate"
        if "unique_file.txt" in filepath:
            return "mock_hash_unique"
        return f"mock_hash_{os.path.basename(filepath)}" # Unique hash for other files

    # --- Test Cases ---

    def test_find_dust_bunnies_giant_files(self):
        # Default max_size_bytes is 100MB (104857600)
        results = sweeper.find_dust_bunnies('/mock/dir', 104857600, 365, False)
        self.assertEqual(len(results['giant_files']), 2)
        self.assertTrue(any("giant_old_file.txt" in f['path'] for f in results['giant_files']))
        self.assertTrue(any("giant_new_file.txt" in f['path'] for f in results['giant_files']))
        self.assertFalse(any("small_old_file.txt" in f['path'] for f in results['giant_files']))

    def test_find_dust_bunnies_ancient_files(self):
        # Default max_age_days is 365
        results = sweeper.find_dust_bunnies('/mock/dir', 1, 365, False) # Set max_size low to not interfere
        self.assertEqual(len(results['ancient_files']), 2)
        self.assertTrue(any("giant_old_file.txt" in f['path'] for f in results['ancient_files']))
        self.assertTrue(any("small_old_file.txt" in f['path'] for f in results['ancient_files']))
        self.assertFalse(any("giant_new_file.txt" in f['path'] for f in results['ancient_files']))

    def test_find_dust_bunnies_duplicates(self):
        results = sweeper.find_dust_bunnies('/mock/dir', 1, 1, True) # Set size/age low to not interfere
        self.assertEqual(len(results['duplicate_files']), 1)
        self.assertIn("mock_hash_duplicate", results['duplicate_files'])
        self.assertEqual(len(results['duplicate_files']['mock_hash_duplicate']), 2)
        self.assertTrue(any("/mock/dir/subdir/duplicate_file_a.txt" in p for p in results['duplicate_files']['mock_hash_duplicate']))
        self.assertTrue(any("/mock/dir/subdir/duplicate_file_b.txt" in p for p in results['duplicate_files']['mock_hash_duplicate']))
        self.assertNotIn("mock_hash_unique", results['duplicate_files']) # Ensure unique files are not reported as duplicates

    def test_find_dust_bunnies_no_duplicates_when_disabled(self):
        results = sweeper.find_dust_bunnies('/mock/dir', 1, 1, False)
        self.assertEqual(len(results['duplicate_files']), 0)

    def test_find_dust_bunnies_all_categories(self):
        # Test with parameters that should catch all types
        results = sweeper.find_dust_bunnies(
            '/mock/dir',
            max_size_bytes=10 * 1024 * 1024, # 10MB threshold
            max_age_days=100, # 100 days threshold
            find_duplicates_enabled=True
        )

        # Giant files: giant_old_file.txt (200MB), giant_new_file.txt (150MB), unique_file.txt (12MB), duplicate_file_a/b.txt (10MB)
        self.assertEqual(len(results['giant_files']), 5)
        self.assertTrue(any("giant_old_file.txt" in f['path'] for f in results['giant_files']))
        self.assertTrue(any("giant_new_file.txt" in f['path'] for f in results['giant_files']))
        self.assertTrue(any("unique_file.txt" in f['path'] for f in results['giant_files']))
        self.assertTrue(any("duplicate_file_a.txt" in f['path'] for f in results['giant_files']))
        self.assertTrue(any("duplicate_file_b.txt" in f['path'] for f in results['giant_files']))

        # Ancient files: giant_old_file.txt (400 days old), small_old_file.txt (400 days old)
        self.assertEqual(len(results['ancient_files']), 2)
        self.assertTrue(any("giant_old_file.txt" in f['path'] for f in results['ancient_files']))
        self.assertTrue(any("small_old_file.txt" in f['path'] for f in results['ancient_files']))

        # Duplicates: duplicate_file_a.txt, duplicate_file_b.txt
        self.assertEqual(len(results['duplicate_files']), 1)
        self.assertIn("mock_hash_duplicate", results['duplicate_files'])

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_output_no_dust_bunnies(self, mock_stdout):
        # Configure mocks to return no dust bunnies
        self.mock_os_walk.return_value = [
            ('/mock/dir', [], ['small_new_file.txt'])
        ]
        self.mock_getsize.side_effect = lambda p: 100 # All files small
        self.mock_getmtime.side_effect = lambda p: (self.mock_current_time - timedelta(days=10)).timestamp() # All files new
        self.mock_get_file_hash.side_effect = lambda p: f"unique_hash_{p}" # All files unique

        # Call main with default args
        sweeper.main()
        output = mock_stdout.getvalue()

        self.assertIn("All clear! No significant digital dust bunnies found.", output)
        self.assertNotIn("Giant Files", output)
        self.assertNotIn("Ancient Files", output)
        self.assertNotIn("Duplicate Files", output)

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_output_with_dust_bunnies(self, mock_stdout):
        # Use default mock setup which has dust bunnies
        sweeper.main()
        output = mock_stdout.getvalue()

        self.assertIn("Sweeping '/mock/dir' for digital dust bunnies...", output)
        self.assertIn("Giant Files", output)
        self.assertIn("Ancient Files", output)
        self.assertNotIn("Duplicate Files", output) # Duplicates are disabled by default in main

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_output_with_duplicates_enabled(self, mock_stdout):
        # Simulate command line args for main
        with patch('sys.argv', ['sweeper.py', '/mock/dir', '--find-duplicates']):
            sweeper.main()
            output = mock_stdout.getvalue()

            self.assertIn("Duplicate Files", output)
            self.assertIn("mock_hash_duplicate", output)
            self.assertIn("/mock/dir/subdir/duplicate_file_a.txt", output)
            self.assertIn("/mock/dir/subdir/duplicate_file_b.txt", output)

    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_main_invalid_directory(self, mock_exit, mock_stderr):
        self.mock_isdir.return_value = False # Simulate invalid directory
        with patch('sys.argv', ['sweeper.py', '/nonexistent/dir']):
            sweeper.main()
            mock_exit.assert_called_once_with(1)
            self.assertIn("Error: Directory '/nonexistent/dir' not found.", mock_stderr.getvalue())

    def test_format_size(self):
        self.assertEqual(sweeper.format_size(100), "100 B")
        self.assertEqual(sweeper.format_size(1024), "1.00 KB")
        self.assertEqual(sweeper.format_size(1024 * 1024), "1.00 MB")
        self.assertEqual(sweeper.format_size(1024 * 1024 * 1024), "1.00 GB")
        self.assertEqual(sweeper.format_size(1500), "1.46 KB")
        self.assertEqual(sweeper.format_size(1500000), "1.43 MB")
        self.assertEqual(sweeper.format_size(1500000000), "1.40 GB")

if __name__ == '__main__':
    unittest.main()
