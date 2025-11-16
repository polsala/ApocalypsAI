import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timedelta
import io
import sys

# Import the functions to be tested
from src.purifier import get_cache_dirs, clean_directory, main

class TestPurifier(unittest.TestCase):

    @patch('platform.system')
    @patch('os.path.expanduser')
    @patch('os.path.isdir')
    @patch.dict(os.environ, {}, clear=True) # Clear environment variables for consistent testing
    def test_get_cache_dirs_linux(self, mock_isdir, mock_expanduser, mock_platform_system):
        # Mock rationale: Simulate a Linux environment to test path generation.
        mock_platform_system.return_value = "Linux"
        mock_expanduser.return_value = "/home/testuser"
        mock_isdir.side_effect = lambda x: x in ["/home/testuser/.cache", "/tmp"]

        expected_dirs = ["/home/testuser/.cache", "/tmp"]
        self.assertEqual(get_cache_dirs(), expected_dirs)

    @patch('platform.system')
    @patch('os.path.expanduser')
    @patch('os.path.isdir')
    @patch.dict(os.environ, {}, clear=True)
    def test_get_cache_dirs_macos(self, mock_isdir, mock_expanduser, mock_platform_system):
        # Mock rationale: Simulate a macOS environment to test path generation.
        mock_platform_system.return_value = "Darwin"
        mock_expanduser.return_value = "/Users/testuser"
        mock_isdir.side_effect = lambda x: x in ["/Users/testuser/Library/Caches", "/tmp"]

        expected_dirs = ["/Users/testuser/Library/Caches", "/tmp"]
        self.assertEqual(get_cache_dirs(), expected_dirs)

    @patch('platform.system')
    @patch('os.path.isdir')
    @patch.dict(os.environ, {"TEMP": "C:\\Users\\testuser\\AppData\\Local\\Temp", "LOCALAPPDATA": "C:\\Users\\testuser\\AppData\\Local"}, clear=True)
    def test_get_cache_dirs_windows(self, mock_isdir, mock_platform_system):
        # Mock rationale: Simulate a Windows environment and its environment variables.
        mock_platform_system.return_value = "Windows"
        mock_isdir.side_effect = lambda x: x in [
            "C:\\Users\\testuser\\AppData\\Local\\Temp",
            "C:\\Users\\testuser\\AppData\\Local\\Temp" # LOCALAPPDATA\Temp resolves to the same path here
        ]

        expected_dirs = ["C:\\Users\\testuser\\AppData\\Local\\Temp"]
        self.assertEqual(get_cache_dirs(), expected_dirs)
    
    @patch('platform.system')
    @patch('os.path.isdir')
    @patch.dict(os.environ, {}, clear=True)
    def test_get_cache_dirs_windows_no_env_vars(self, mock_isdir, mock_platform_system):
        # Mock rationale: Simulate Windows without TEMP/LOCALAPPDATA env vars.
        mock_platform_system.return_value = "Windows"
        mock_isdir.return_value = False # No dirs exist

        expected_dirs = []
        self.assertEqual(get_cache_dirs(), expected_dirs)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir')
    def test_clean_directory_dry_run(self, mock_listdir, mock_rmdir, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure and file modification times
        # to test the dry-run functionality without actual file system interaction.
        mock_isdir.return_value = True
        
        # Simulate directory structure:
        # /test_dir
        # ├── old_file.txt (modified 10 days ago)
        # ├── new_file.txt (modified 1 day ago)
        # └── empty_subdir/ (becomes empty after old_file_in_subdir.txt is 'deleted')
        #     └── old_file_in_subdir.txt (modified 10 days ago)
        
        mock_walk.return_value = [
            ('/test_dir', ['empty_subdir'], ['old_file.txt', 'new_file.txt']),
            ('/test_dir/empty_subdir', [], ['old_file_in_subdir.txt'])
        ]

        # Mock modification times
        now = datetime.now()
        old_time = (now - timedelta(days=10)).timestamp()
        new_time = (now - timedelta(days=1)).timestamp()

        def mock_getmtime_side_effect(path):
            if "old_file" in path:
                return old_time
            elif "new_file" in path:
                return new_time
            return now.timestamp() # Default for other paths

        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_listdir.return_value = [] # Simulate empty after files are processed

        # Capture print output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        deleted_count = clean_directory("/test_dir", 7, True, now)

        sys.stdout = sys.__stdout__ # Restore stdout

        self.assertEqual(deleted_count, 2) # old_file.txt and old_file_in_subdir.txt
        mock_remove.assert_not_called()
        mock_rmdir.assert_not_called()

        output = captured_output.getvalue()
        self.assertIn("[DRY RUN] Would delete file: /test_dir/old_file.txt", output)
        self.assertIn("[DRY RUN] Would delete file: /test_dir/empty_subdir/old_file_in_subdir.txt", output)
        self.assertIn("[DRY RUN] Would remove empty directory: /test_dir/empty_subdir", output)
        self.assertNotIn("new_file.txt", output)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('os.rmdir')
    @patch('os.listdir')
    def test_clean_directory_actual_run(self, mock_listdir, mock_rmdir, mock_remove, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure and file modification times
        # to test actual deletion functionality without touching the file system.
        mock_isdir.return_value = True
        
        mock_walk.return_value = [
            ('/test_dir', ['empty_subdir'], ['old_file.txt', 'new_file.txt']),
            ('/test_dir/empty_subdir', [], ['old_file_in_subdir.txt'])
        ]

        now = datetime.now()
        old_time = (now - timedelta(days=10)).timestamp()
        new_time = (now - timedelta(days=1)).timestamp()

        def mock_getmtime_side_effect(path):
            if "old_file" in path:
                return old_time
            elif "new_file" in path:
                return new_time
            return now.timestamp()

        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_listdir.return_value = [] # Simulate empty after files are processed

        captured_output = io.StringIO()
        sys.stdout = captured_output

        deleted_count = clean_directory("/test_dir", 7, False, now)

        sys.stdout = sys.__stdout__

        self.assertEqual(deleted_count, 3) # old_file.txt, old_file_in_subdir.txt, and empty_subdir
        mock_remove.assert_any_call("/test_dir/old_file.txt")
        mock_remove.assert_any_call("/test_dir/empty_subdir/old_file_in_subdir.txt")
        mock_rmdir.assert_any_call("/test_dir/empty_subdir")
        self.assertEqual(mock_remove.call_count, 2)
        self.assertEqual(mock_rmdir.call_count, 1)

        output = captured_output.getvalue()
        self.assertIn("Deleted file: /test_dir/old_file.txt", output)
        self.assertIn("Deleted file: /test_dir/empty_subdir/old_file_in_subdir.txt", output)
        self.assertIn("Removed empty directory: /test_dir/empty_subdir", output)
        self.assertNotIn("new_file.txt", output)

    @patch('sys.argv', ['purifier.py', '--dry-run', '--age-days', '5', '--target-dir', '/custom_cache'])
    @patch('src.purifier.datetime') # Mock datetime.now()
    @patch('src.purifier.clean_directory')
    @patch('os.path.isdir') # Mock os.path.isdir for the target_dir check
    def test_main_with_target_dir_dry_run(self, mock_isdir, mock_clean_directory, mock_datetime):
        # Mock rationale: Test the main function's argument parsing and flow
        # when a custom target directory and dry-run are specified.
        mock_now = MagicMock()
        mock_now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now = mock_now

        mock_isdir.return_value = True # Assume /custom_cache exists
        mock_clean_directory.return_value = 5 # Simulate 5 items processed

        captured_output = io.StringIO()
        sys.stdout = captured_output

        main()

        sys.stdout = sys.__stdout__

        mock_clean_directory.assert_called_once_with(
            '/custom_cache', 5, True, datetime(2023, 10, 26, 10, 0, 0)
        )
        self.assertIn("[DRY RUN] Purifier finished. Total items processed for deletion: 5", captured_output.getvalue())
    
    @patch('sys.argv', ['purifier.py', '--age-days', '10'])
    @patch('src.purifier.datetime') # Mock datetime.now()
    @patch('src.purifier.get_cache_dirs')
    @patch('src.purifier.clean_directory')
    def test_main_default_dirs_actual_run(self, mock_clean_directory, mock_get_cache_dirs, mock_datetime):
        # Mock rationale: Test the main function's argument parsing and flow
        # when using default cache directories and actual deletion.
        mock_now = MagicMock()
        mock_now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now = mock_now

        mock_get_cache_dirs.return_value = ['/home/user/.cache', '/tmp']
        mock_clean_directory.side_effect = [2, 3] # Simulate 2 from first dir, 3 from second

        captured_output = io.StringIO()
        sys.stdout = captured_output

        main()

        sys.stdout = sys.__stdout__

        mock_get_cache_dirs.assert_called_once()
        self.assertEqual(mock_clean_directory.call_count, 2)
        mock_clean_directory.assert_any_call(
            '/home/user/.cache', 10, False, datetime(2023, 10, 26, 10, 0, 0)
        )
        mock_clean_directory.assert_any_call(
            '/tmp', 10, False, datetime(2023, 10, 26, 10, 0, 0)
        )
        self.assertIn("Purifier finished. Total items processed for deletion: 5", captured_output.getvalue())

    @patch('sys.argv', ['purifier.py'])
    @patch('src.purifier.datetime')
    @patch('src.purifier.get_cache_dirs')
    @patch('src.purifier.clean_directory')
    def test_main_no_cache_dirs(self, mock_clean_directory, mock_get_cache_dirs, mock_datetime):
        # Mock rationale: Test the scenario where no common cache directories are found.
        mock_now = MagicMock()
        mock_now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now = mock_now

        mock_get_cache_dirs.return_value = [] # Simulate no dirs found

        captured_output = io.StringIO()
        sys.stdout = captured_output

        main()

        sys.stdout = sys.__stdout__

        mock_get_cache_dirs.assert_called_once()
        mock_clean_directory.assert_not_called()
        self.assertIn("No common cache directories found for this OS.", captured_output.getvalue())
        self.assertIn("Purifier finished. Total items processed for deletion: 0", captured_output.getvalue())


if __name__ == '__main__':
    unittest.main()
