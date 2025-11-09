import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the functions to be tested
from src.sweeper import find_dust_bunnies, generate_report

class TestDigitalDustBunnySweeper(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_find_dust_bunnies_empty_directory(self, mock_time_time, mock_getmtime, mock_isfile, mock_getsize, mock_os_walk):
        # Mock rationale: Simulate an empty directory structure.
        mock_os_walk.return_value = [
            ('/test_dir', [], []) # Root directory, no subdirs, no files
        ]
        # Mock rationale: No files exist, so these won't be called for files.
        mock_getsize.return_value = 100
        mock_isfile.return_value = False
        mock_getmtime.return_value = time.time()

        # Mock rationale: Set a consistent current time for age calculations.
        mock_time_time.return_value = datetime(2023, 10, 26).timestamp()

        bunnies = find_dust_bunnies('/test_dir')
        self.assertEqual(bunnies["empty_files"], [])
        self.assertEqual(bunnies["empty_dirs"], ['/test_dir']) # The root itself is empty
        self.assertEqual(bunnies["temp_files"], [])
        self.assertEqual(bunnies["old_files"], [])

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('time.time')
    def test_find_dust_bunnies_with_various_bunnies(self, mock_time_time, mock_getmtime, mock_isfile, mock_getsize, mock_os_walk):
        # Mock rationale: Simulate a directory structure with various types of "dust bunnies".
        # Structure:
        # /test_dir
        #   ├── empty_file.txt (empty)
        #   ├── temp_file.tmp (temp extension)
        #   ├── old_file.log (temp extension, also old)
        #   ├── regular_file.txt (not empty, not temp, not old)
        #   ├── old_but_not_temp.txt (not empty, not temp, but old)
        #   ├── subdir_empty/ (empty directory)
        #   └── subdir_with_files/
        #       └── another_empty.txt (empty)

        current_timestamp = datetime(2023, 10, 26).timestamp()
        old_timestamp = (datetime(2023, 10, 26) - timedelta(days=100)).timestamp() # Older than 90 days

        mock_time_time.return_value = current_timestamp

        mock_os_walk.return_value = [
            ('/test_dir', ['subdir_empty', 'subdir_with_files'], ['empty_file.txt', 'temp_file.tmp', 'old_file.log', 'regular_file.txt', 'old_but_not_temp.txt']),
            ('/test_dir/subdir_empty', [], []),
            ('/test_dir/subdir_with_files', [], ['another_empty.txt'])
        ]

        # Mock rationale: Control file sizes and types.
        def mock_getsize_side_effect(path):
            if 'empty_file.txt' in path or 'another_empty.txt' in path:
                return 0
            return 100 # All other files have content
        mock_getsize.side_effect = mock_getsize_side_effect

        def mock_isfile_side_effect(path):
            return 'file' in path or '.txt' in path or '.tmp' in path or '.log' in path
        mock_isfile.side_effect = mock_isfile_side_effect

        # Mock rationale: Control modification times for age-based checks.
        def mock_getmtime_side_effect(path):
            if 'old_but_not_temp.txt' in path:
                return old_timestamp
            return current_timestamp # All other files are "recent"
        mock_getmtime.side_effect = mock_getmtime_side_effect

        bunnies = find_dust_bunnies('/test_dir', age_threshold_days=90)

        self.assertIn('/test_dir/empty_file.txt', bunnies["empty_files"])
        self.assertIn('/test_dir/subdir_with_files/another_empty.txt', bunnies["empty_files"])
        self.assertEqual(len(bunnies["empty_files"]), 2)

        self.assertIn('/test_dir/subdir_empty', bunnies["empty_dirs"])
        # The root dir itself is not empty because it contains files/subdirs
        # subdir_with_files is not empty because it contains another_empty.txt
        self.assertEqual(len(bunnies["empty_dirs"]), 1)

        self.assertIn('/test_dir/temp_file.tmp', bunnies["temp_files"])
        self.assertIn('/test_dir/old_file.log', bunnies["temp_files"]) # .log is a temp extension
        self.assertEqual(len(bunnies["temp_files"]), 2)

        self.assertIn('/test_dir/old_but_not_temp.txt', bunnies["old_files"])
        self.assertEqual(len(bunnies["old_files"]), 1)

        # Ensure regular_file.txt is not caught
        self.assertNotIn('/test_dir/regular_file.txt', bunnies["empty_files"])
        self.assertNotIn('/test_dir/regular_file.txt', bunnies["temp_files"])
        self.assertNotIn('/test_dir/regular_file.txt', bunnies["old_files"])


    def test_generate_report_no_bunnies(self):
        # Mock rationale: Simulate a scenario where no dust bunnies are found.
        bunnies = {
            "empty_files": [],
            "empty_dirs": [],
            "temp_files": [],
            "old_files": []
        }
        report = generate_report(bunnies, '/clean_dir')
        self.assertIn("sparkling clean! No dust bunnies found.", report)
        self.assertNotIn("Empty Files", report)
        self.assertNotIn("Empty Directories", report)
        self.assertNotIn("Temporary & Backup Files", report)
        self.assertNotIn("Ancient Files", report)
        self.assertIn("Total Digital Dust Bunnies Found: 0", report)

    def test_generate_report_with_bunnies(self):
        # Mock rationale: Simulate a scenario where various dust bunnies are found.
        bunnies = {
            "empty_files": ['/path/to/empty.txt'],
            "empty_dirs": ['/path/to/empty_folder'],
            "temp_files": ['/path/to/temp.tmp', '/path/to/backup.bak'],
            "old_files": ['/path/to/old_document.pdf']
        }
        report = generate_report(bunnies, '/messy_dir')
        self.assertIn("--- Digital Dust Bunny Sweeper Report for '/messy_dir' ---", report)
        self.assertIn("Empty Files (1):", report)
        self.assertIn("  - /path/to/empty.txt", report)
        self.assertIn("Empty Directories (1):", report)
        self.assertIn("  - /path/to/empty_folder", report)
        self.assertIn("Temporary & Backup Files (2):", report)
        self.assertIn("  - /path/to/temp.tmp", report)
        self.assertIn("  - /path/to/backup.bak", report)
        self.assertIn("Ancient Files (1):", report)
        self.assertIn("  - /path/to/old_document.pdf", report)
        self.assertIn("Total Digital Dust Bunnies Found: 5", report)
        self.assertIn("Consider giving them a good sweep!", report)

if __name__ == '__main__':
    unittest.main()
