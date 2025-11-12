import unittest
import os
import hashlib
import time
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
from src.sweeper import DigitalDustBunnySweeper

# Mock rationale:
# - os.walk: Simulates directory structure and files without actual file system access.
# - os.path.getsize: Provides predefined file sizes for testing empty files.
# - os.path.getmtime: Provides predefined modification times for testing old files.
# - hashlib.sha256: Mocks file content hashing to control duplicate detection.
# - open: Mocks file reading for hash calculation.
# - time.time: Fixes the current time for deterministic age calculations.

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Fix the current time for deterministic age calculations
        self.mock_now = 1672531200.0  # Jan 1, 2023, 00:00:00 UTC
        self.mock_age_threshold_days = 365
        self.mock_age_threshold_timestamp = self.mock_now - (self.mock_age_threshold_days * 24 * 3600) # Jan 1, 2022

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.islink', return_value=False) # Assume no symlinks for simplicity
    def test_empty_files_detection(self, mock_islink, mock_isdir, mock_walk, mock_getsize, mock_getmtime, mock_time):
        mock_time.return_value = self.mock_now
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/root', [], ['file1.txt', 'empty.txt', 'file2.txt'])
        ]
        mock_getsize.side_effect = lambda x: {
            '/mock/root/file1.txt': 100,
            '/mock/root/empty.txt': 0,
            '/mock/root/file2.txt': 50,
        }.get(x, 0)
        mock_getmtime.return_value = self.mock_now # Not relevant for empty file test, but needed by patch

        sweeper = DigitalDustBunnySweeper('/mock/root')
        sweeper.scan()

        self.assertIn('/mock/root/empty.txt', sweeper.empty_files)
        self.assertEqual(len(sweeper.empty_files), 1)

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.islink', return_value=False)
    @patch('builtins.open', new_callable=mock_open) # Mock open for file content
    @patch('hashlib.sha256') # Mock hashlib.sha256
    def test_duplicate_files_detection(self, mock_sha256, mock_open_file, mock_islink, mock_isdir, mock_walk, mock_getsize, mock_getmtime, mock_time):
        mock_time.return_value = self.mock_now
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/root', [], ['fileA.txt', 'fileB.txt', 'fileC.txt', 'unique.txt'])
        ]
        mock_getsize.side_effect = lambda x: {
            '/mock/root/fileA.txt': 100,
            '/mock/root/fileB.txt': 100,
            '/mock/root/fileC.txt': 100,
            '/mock/root/unique.txt': 50,
        }.get(x, 0)
        mock_getmtime.return_value = self.mock_now

        # Mock hashlib.sha256 to return specific hashes
        mock_hasher_a = unittest.mock.Mock()
        mock_hasher_a.hexdigest.return_value = 'hash_duplicate_1'
        mock_hasher_b = unittest.mock.Mock()
        mock_hasher_b.hexdigest.return_value = 'hash_duplicate_1' # Same hash as A
        mock_hasher_c = unittest.mock.Mock()
        mock_hasher_c.hexdigest.return_value = 'hash_duplicate_2' # Different hash
        mock_hasher_unique = unittest.mock.Mock()
        mock_hasher_unique.hexdigest.return_value = 'hash_unique'

        # Control which mock hasher is returned based on call order
        mock_sha256.side_effect = [mock_hasher_a, mock_hasher_b, mock_hasher_c, mock_hasher_unique]

        sweeper = DigitalDustBunnySweeper('/mock/root')
        sweeper.scan()

        self.assertIn('hash_duplicate_1', sweeper.duplicate_files)
        self.assertIn('/mock/root/fileA.txt', sweeper.duplicate_files['hash_duplicate_1'])
        self.assertIn('/mock/root/fileB.txt', sweeper.duplicate_files['hash_duplicate_1'])
        self.assertEqual(len(sweeper.duplicate_files['hash_duplicate_1']), 2)

        self.assertIn('hash_duplicate_2', sweeper.duplicate_files)
        self.assertIn('/mock/root/fileC.txt', sweeper.duplicate_files['hash_duplicate_2'])
        self.assertEqual(len(sweeper.duplicate_files['hash_duplicate_2']), 1) # Not a duplicate

        self.assertIn('hash_unique', sweeper.duplicate_files)
        self.assertIn('/mock/root/unique.txt', sweeper.duplicate_files['hash_unique'])
        self.assertEqual(len(sweeper.duplicate_files['hash_unique']), 1) # Not a duplicate

        # Check total duplicates reported (redundant ones)
        duplicates_found = {h: paths for h, paths in sweeper.duplicate_files.items() if len(paths) > 1}
        total_redundant = sum(len(paths) - 1 for paths in duplicates_found.values())
        self.assertEqual(total_redundant, 1) # fileB is redundant to fileA

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.islink', return_value=False)
    def test_old_files_detection(self, mock_islink, mock_isdir, mock_walk, mock_getsize, mock_getmtime, mock_time):
        mock_time.return_value = self.mock_now # Jan 1, 2023
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/root', [], ['new_file.txt', 'old_file.txt', 'very_old_file.txt'])
        ]
        mock_getsize.return_value = 100 # Not relevant for old file test, but needed by patch

        # Define modification times:
        # new_file: Dec 1, 2022 (within 365 days of Jan 1, 2023)
        # old_file: Feb 1, 2022 (within 365 days of Jan 1, 2023, but older than Jan 1, 2022)
        # very_old_file: Jan 1, 2021 (older than Jan 1, 2022)
        mock_getmtime.side_effect = lambda x: {
            '/mock/root/new_file.txt': datetime(2022, 12, 1).timestamp(),
            '/mock/root/old_file.txt': datetime(2022, 2, 1).timestamp(), # This should be flagged as old
            '/mock/root/very_old_file.txt': datetime(2021, 1, 1).timestamp(), # This should be flagged as old
        }.get(x, self.mock_now)

        sweeper = DigitalDustBunnySweeper('/mock/root', age_threshold_days=365) # Threshold is Jan 1, 2022
        sweeper.scan()

        self.assertNotIn('/mock/root/new_file.txt', sweeper.old_files)
        self.assertIn('/mock/root/old_file.txt', sweeper.old_files)
        self.assertIn('/mock/root/very_old_file.txt', sweeper.old_files)
        self.assertEqual(len(sweeper.old_files), 2)

    @patch('time.time')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.islink', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    def test_combined_detection_and_report(self, mock_sha256, mock_open_file, mock_islink, mock_isdir, mock_walk, mock_getsize, mock_getmtime, mock_time):
        mock_time.return_value = self.mock_now # Jan 1, 2023
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/root', [], ['empty.txt', 'old_unique.txt', 'duplicate_1.txt', 'duplicate_2.txt', 'new_unique.txt'])
        ]
        mock_getsize.side_effect = lambda x: {
            '/mock/root/empty.txt': 0,
            '/mock/root/old_unique.txt': 100,
            '/mock/root/duplicate_1.txt': 200,
            '/mock/root/duplicate_2.txt': 200,
            '/mock/root/new_unique.txt': 50,
        }.get(x, 0)
        mock_getmtime.side_effect = lambda x: {
            '/mock/root/empty.txt': self.mock_now, # Not old
            '/mock/root/old_unique.txt': datetime(2021, 6, 1).timestamp(), # Old
            '/mock/root/duplicate_1.txt': self.mock_now, # Not old
            '/mock/root/duplicate_2.txt': self.mock_now, # Not old
            '/mock/root/new_unique.txt': datetime(2022, 10, 1).timestamp(), # Not old
        }.get(x, self.mock_now)

        mock_hasher_dup1 = unittest.mock.Mock()
        mock_hasher_dup1.hexdigest.return_value = 'hash_dup'
        mock_hasher_dup2 = unittest.mock.Mock()
        mock_hasher_dup2.hexdigest.return_value = 'hash_dup'
        mock_hasher_old_unique = unittest.mock.Mock()
        mock_hasher_old_unique.hexdigest.return_value = 'hash_old_unique'
        mock_hasher_new_unique = unittest.mock.Mock()
        mock_hasher_new_unique.hexdigest.return_value = 'hash_new_unique'

        mock_sha256.side_effect = [
            mock_hasher_old_unique, # for old_unique.txt
            mock_hasher_dup1,       # for duplicate_1.txt
            mock_hasher_dup2,       # for duplicate_2.txt
            mock_hasher_new_unique  # for new_unique.txt
        ]

        sweeper = DigitalDustBunnySweeper('/mock/root', age_threshold_days=365)
        sweeper.scan()

        self.assertIn('/mock/root/empty.txt', sweeper.empty_files)
        self.assertIn('/mock/root/old_unique.txt', sweeper.old_files)
        self.assertIn('hash_dup', sweeper.duplicate_files)
        self.assertIn('/mock/root/duplicate_1.txt', sweeper.duplicate_files['hash_dup'])
        self.assertIn('/mock/root/duplicate_2.txt', sweeper.duplicate_files['hash_dup'])

        # Test report output (just check if it runs without error and contains key phrases)
        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout:
            sweeper.report(dry_run=True)
            output = mock_stdout.getvalue()

            self.assertIn("--- Digital Dust Bunny Report ---", output)
            self.assertIn("### Empty Files (0 bytes) ###", output)
            self.assertIn("- /mock/root/empty.txt", output)
            self.assertIn("Found 1 empty files.", output)

            self.assertIn("### Duplicate Files (identical content) ###", output)
            self.assertIn("Hash: hash_dup", output)
            self.assertIn("- /mock/root/duplicate_1.txt", output)
            self.assertIn("- /mock/root/duplicate_2.txt", output)
            self.assertIn("Found 1 redundant duplicate files.", output) # Only one is redundant

            self.assertIn("### Old Files (modified before 2022-01-01) ###", output)
            self.assertIn("- /mock/root/old_unique.txt", output)
            self.assertIn("Found 1 old files.", output)

            self.assertIn("Total potential digital dust bunnies to clean: 3", output) # 1 empty + 1 redundant duplicate + 1 old
            self.assertIn("This was a DRY RUN. No files were deleted.", output)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_invalid_directory(self, mock_stdout, mock_isdir):
        sweeper = DigitalDustBunnySweeper('/nonexistent/path')
        sweeper.scan()
        self.assertIn("Error: Directory '/nonexistent/path' not found.", mock_stdout.getvalue())
        self.assertEqual(len(sweeper.empty_files), 0)
        self.assertEqual(len(sweeper.duplicate_files), 0)
        self.assertEqual(len(sweeper.old_files), 0)
