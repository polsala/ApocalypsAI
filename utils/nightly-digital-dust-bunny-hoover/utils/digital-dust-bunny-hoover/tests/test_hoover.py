import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime, timedelta
import io

# Import the function to be tested
# Assuming hoover.py is in src/ relative to the test file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from hoover import hoover_directory, get_file_age_in_days

class TestDigitalDustBunnyHoover(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        self.mock_stdout = io.StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_get_file_age_in_days(self, mock_datetime, mock_getmtime):
        # Mock rationale: get_file_age_in_days depends on current time and file modification time.
        # We mock these to ensure deterministic age calculation.
        
        # Scenario 1: File is 10 days old
        mock_now = datetime(2023, 10, 26)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts) # Keep original behavior for fromtimestamp
        
        # File modified 10 days ago
        file_mtime = (mock_now - timedelta(days=10)).timestamp()
        mock_getmtime.return_value = file_mtime
        
        self.assertEqual(get_file_age_in_days("dummy_path"), 10)

        # Scenario 2: File is 0 days old (today)
        file_mtime_today = mock_now.timestamp()
        mock_getmtime.return_value = file_mtime_today
        self.assertEqual(get_file_age_in_days("dummy_path"), 0)

        # Scenario 3: File does not exist (OSError)
        mock_getmtime.side_effect = OSError
        self.assertEqual(get_file_age_in_days("non_existent_path"), -1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('datetime.datetime')
    def test_hoover_directory_dry_run(self, mock_datetime, mock_remove, mock_getsize, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: This test simulates a file system scan without actually touching files.
        # os.path.isdir: Ensures the target directory is considered valid.
        # os.walk: Provides a predefined directory structure and files.
        # os.path.getmtime: Returns specific modification times for files to control their age.
        # os.path.getsize: Returns specific sizes for files.
        # os.remove: Mocked to ensure it's NOT called in dry run.
        # datetime.datetime: Controls the 'current time' for age calculation.

        mock_isdir.return_value = True
        
        # Set current time for deterministic age calculation
        mock_now = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts) # Keep original behavior for fromtimestamp

        # Define mock file system structure and properties
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.txt', 'new_file.log', 'ancient_report.pdf']),
            ('/test_dir/subdir', [], ['temp.dat'])
        ]

        # Define modification times for files
        file_mtimes = {
            '/test_dir/old_file.txt': (mock_now - timedelta(days=45)).timestamp(), # 45 days old
            '/test_dir/new_file.log': (mock_now - timedelta(days=5)).timestamp(),  # 5 days old
            '/test_dir/ancient_report.pdf': (mock_now - timedelta(days=100)).timestamp(), # 100 days old
            '/test_dir/subdir/temp.dat': (mock_now - timedelta(days=35)).timestamp() # 35 days old
        }
        mock_getmtime.side_effect = lambda p: file_mtimes.get(p, mock_now.timestamp())

        # Define file sizes
        file_sizes = {
            '/test_dir/old_file.txt': 1024 * 1024, # 1MB
            '/test_dir/new_file.log': 500 * 1024,  # 0.5MB
            '/test_dir/ancient_report.pdf': 2 * 1024 * 1024, # 2MB
            '/test_dir/subdir/temp.dat': 0.75 * 1024 * 1024 # 0.75MB
        }
        mock_getsize.side_effect = lambda p: file_sizes.get(p, 0)

        # Run the hoover in dry run mode (default)
        hoover_directory('/test_dir', age_threshold_days=30)

        output = self.mock_stdout.getvalue()
        self.assertIn("Dry Run Mode: No files will be deleted.", output)
        self.assertIn("Digital Dust Bunnies Report (3 found)", output)
        self.assertIn("- '/test_dir/old_file.txt' (Age: 45 days", output)
        self.assertIn("- '/test_dir/ancient_report.pdf' (Age: 100 days", output)
        self.assertIn("- '/test_dir/subdir/temp.dat' (Age: 35 days", output)
        self.assertNotIn("new_file.log", output) # Should not be reported as it's only 5 days old
        self.assertIn("Total potential space to be purified: 3.75 MB", output) # 1MB + 2MB + 0.75MB
        self.assertIn("To proceed with purification, run again with the '--delete' flag.", output)
        mock_remove.assert_not_called() # Crucial for dry run

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('datetime.datetime')
    def test_hoover_directory_delete_mode(self, mock_datetime, mock_remove, mock_getsize, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Similar to dry run, but verifies that os.remove is called for eligible files.
        # os.remove: Mocked to track calls.

        mock_isdir.return_value = True

        mock_now = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)

        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.txt', 'new_file.log'])
        ]

        file_mtimes = {
            '/test_dir/old_file.txt': (mock_now - timedelta(days=45)).timestamp(),
            '/test_dir/new_file.log': (mock_now - timedelta(days=5)).timestamp()
        }
        mock_getmtime.side_effect = lambda p: file_mtimes.get(p, mock_now.timestamp())

        file_sizes = {
            '/test_dir/old_file.txt': 1024 * 1024,
            '/test_dir/new_file.log': 500 * 1024
        }
        mock_getsize.side_effect = lambda p: file_sizes.get(p, 0)

        # Run the hoover in delete mode
        hoover_directory('/test_dir', age_threshold_days=30, delete_mode=True)

        output = self.mock_stdout.getvalue()
        self.assertIn("DELETE MODE ACTIVATED! Files will be permanently removed.", output)
        self.assertIn("Digital Dust Bunnies Report (1 found)", output)
        self.assertIn("- '/test_dir/old_file.txt' (Age: 45 days", output)
        self.assertIn("Purification complete! 1 files removed.", output)
        
        mock_remove.assert_called_once_with('/test_dir/old_file.txt') # Only old_file.txt should be deleted

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('datetime.datetime')
    def test_hoover_directory_no_dust_bunnies(self, mock_datetime, mock_remove, mock_getsize, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test scenario where no files meet the age criteria.
        mock_isdir.return_value = True

        mock_now = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)

        mock_walk.return_value = [
            ('/test_dir', [], ['new_file1.txt', 'new_file2.log'])
        ]

        file_mtimes = {
            '/test_dir/new_file1.txt': (mock_now - timedelta(days=5)).timestamp(),
            '/test_dir/new_file2.log': (mock_now - timedelta(days=10)).timestamp()
        }
        mock_getmtime.side_effect = lambda p: file_mtimes.get(p, mock_now.timestamp())
        mock_getsize.return_value = 100 # Dummy size

        hoover_directory('/test_dir', age_threshold_days=30)

        output = self.mock_stdout.getvalue()
        self.assertIn("No digital dust bunnies found! Your digital realm is pristine.", output)
        mock_remove.assert_not_called()

    @patch('os.path.isdir')
    def test_hoover_directory_invalid_path(self, mock_isdir):
        # Mock rationale: Test behavior when the provided directory path is invalid.
        mock_isdir.return_value = False

        hoover_directory('/non_existent_dir', age_threshold_days=30)

        output = self.mock_stdout.getvalue()
        self.assertIn("Error: Directory '/non_existent_dir' not found or is not a directory.", output)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('datetime.datetime')
    def test_hoover_directory_verbose_mode(self, mock_datetime, mock_remove, mock_getsize, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Verify that verbose output is generated for found files.
        mock_isdir.return_value = True
        
        mock_now = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)

        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.txt'])
        ]

        file_mtimes = {
            '/test_dir/old_file.txt': (mock_now - timedelta(days=45)).timestamp(),
        }
        mock_getmtime.side_effect = lambda p: file_mtimes.get(p, mock_now.timestamp())

        file_sizes = {
            '/test_dir/old_file.txt': 1024 * 1024, # 1MB
        }
        mock_getsize.side_effect = lambda p: file_sizes.get(p, 0)

        hoover_directory('/test_dir', age_threshold_days=30, verbose=True)

        output = self.mock_stdout.getvalue()
        self.assertIn("[FOUND] '/test_dir/old_file.txt' (Age: 45 days, Size: 1.00 MB)", output)
        self.assertIn("Digital Dust Bunnies Report (1 found)", output)


if __name__ == '__main__':
    unittest.main()
