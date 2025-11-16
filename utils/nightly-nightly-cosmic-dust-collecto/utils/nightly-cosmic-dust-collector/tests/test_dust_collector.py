import unittest
from unittest.mock import patch, MagicMock
import os
import datetime
import sys

# Import the functions to be tested
# Assuming dust_collector.py is in src/ and tests/ is in the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_collector import is_dust_file, collect_dust, DEFAULT_MAX_SIZE_KB, DEFAULT_MIN_AGE_DAYS
sys.path.pop(0)

class TestDustCollector(unittest.TestCase):

    def setUp(self):
        # Define a fixed current time for deterministic age calculations
        self.fixed_now = datetime.datetime(2023, 10, 26, 10, 0, 0)
        self.fixed_now_timestamp = self.fixed_now.timestamp()

    @patch('os.stat')
    def test_is_dust_file_empty(self, mock_stat):
        # Mock rationale: os.stat is a system call that provides file metadata. 
        # We mock it to control file size and modification time deterministically 
        # without creating actual files on the filesystem.
        mock_stat.return_value = MagicMock(st_size=0, st_mtime=self.fixed_now_timestamp - (DEFAULT_MIN_AGE_DAYS * 24 * 3600) - 1)
        self.assertTrue(is_dust_file('/path/to/empty.txt', 1024, DEFAULT_MIN_AGE_DAYS * 24 * 3600, self.fixed_now_timestamp))

    @patch('os.stat')
    def test_is_dust_file_small_and_old(self, mock_stat):
        # Mock rationale: Same as above, controlling size and age for a 'small and old' scenario.
        mock_stat.return_value = MagicMock(st_size=500, st_mtime=self.fixed_now_timestamp - (DEFAULT_MIN_AGE_DAYS * 24 * 3600) - 1)
        self.assertTrue(is_dust_file('/path/to/old_small.txt', 1024, DEFAULT_MIN_AGE_DAYS * 24 * 3600, self.fixed_now_timestamp))

    @patch('os.stat')
    def test_is_dust_file_small_but_new(self, mock_stat):
        # Mock rationale: Testing a file that is small but not old enough to be dust.
        mock_stat.return_value = MagicMock(st_size=500, st_mtime=self.fixed_now_timestamp - (DEFAULT_MIN_AGE_DAYS * 24 * 3600) + 1)
        self.assertFalse(is_dust_file('/path/to/new_small.txt', 1024, DEFAULT_MIN_AGE_DAYS * 24 * 3600, self.fixed_now_timestamp))

    @patch('os.stat')
    def test_is_dust_file_large_and_old(self, mock_stat):
        # Mock rationale: Testing a file that is old but too large to be dust.
        mock_stat.return_value = MagicMock(st_size=2000, st_mtime=self.fixed_now_timestamp - (DEFAULT_MIN_AGE_DAYS * 24 * 3600) - 1)
        self.assertFalse(is_dust_file('/path/to/old_large.txt', 1024, DEFAULT_MIN_AGE_DAYS * 24 * 3600, self.fixed_now_timestamp))

    @patch('os.stat', side_effect=FileNotFoundError)
    def test_is_dust_file_not_found(self, mock_stat):
        # Mock rationale: Simulating a file that disappears between os.walk and os.stat.
        self.assertFalse(is_dust_file('/path/to/nonexistent.txt', 1024, DEFAULT_MIN_AGE_DAYS * 24 * 3600, self.fixed_now_timestamp))

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.stat')
    @patch('datetime.datetime')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('builtins.print') # Mock print to suppress output during tests
    def test_collect_dust_moves_files(self, mock_print, mock_move, mock_makedirs, mock_datetime, mock_stat, mock_walk, mock_isdir):
        # Mock rationale:
        # - os.path.isdir: To confirm the scan path is valid without actual directory creation.
        # - os.walk: To simulate the directory traversal and files found within.
        # - os.stat: To provide specific file sizes and modification times for each simulated file.
        # - datetime.datetime: To fix the 'current time' for deterministic age calculations.
        # - os.makedirs: To prevent actual directory creation for the quarantine path.
        # - shutil.move: To prevent actual file movement and verify it was called correctly.
        # - builtins.print: To capture or suppress console output during tests.

        mock_datetime.now.return_value = self.fixed_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts) # Allow real conversion if needed

        # Simulate a directory structure with one dust file and one non-dust file
        mock_walk.return_value = [
            ('/scan/root', [], ['dust_file.txt', 'normal_file.txt'])
        ]

        # Define stat info for dust_file.txt (small and old)
        dust_mtime = self.fixed_now_timestamp - (DEFAULT_MIN_AGE_DAYS * 24 * 3600) - 100 # Older than min_age
        mock_stat.side_effect = [
            MagicMock(st_size=500, st_mtime=dust_mtime), # dust_file.txt
            MagicMock(st_size=5000, st_mtime=self.fixed_now_timestamp - 100) # normal_file.txt (large and new enough)
        ]

        scan_path = '/scan/root'
        quarantine_dir = '/quarantine'

        collected_files = collect_dust(scan_path, quarantine_dir)

        self.assertEqual(len(collected_files), 1)
        self.assertIn('/scan/root/dust_file.txt', collected_files)
        mock_makedirs.assert_called_once_with(quarantine_dir, exist_ok=True)
        mock_move.assert_called_once_with('/scan/root/dust_file.txt', '/quarantine/dust_file.txt')
        mock_print.assert_any_call(f"  Moved: '/scan/root/dust_file.txt' -> '/quarantine/dust_file.txt'")

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.stat')
    @patch('datetime.datetime')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('builtins.print')
    def test_collect_dust_report_only(self, mock_print, mock_move, mock_makedirs, mock_datetime, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Similar to the move test, but verifying that shutil.move is *not* called 
        # when report_only is true, and the output reflects reporting.
        mock_datetime.now.return_value = self.fixed_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)

        mock_walk.return_value = [
            ('/scan/root', [], ['dust_file_1.txt', 'dust_file_2.txt'])
        ]

        dust_mtime = self.fixed_now_timestamp - (DEFAULT_MIN_AGE_DAYS * 24 * 3600) - 100
        mock_stat.side_effect = [
            MagicMock(st_size=10, st_mtime=dust_mtime), # dust_file_1.txt
            MagicMock(st_size=0, st_mtime=dust_mtime)   # dust_file_2.txt (empty)
        ]

        scan_path = '/scan/root'
        quarantine_dir = '/quarantine'

        collected_files = collect_dust(scan_path, quarantine_dir, report_only=True)

        self.assertEqual(len(collected_files), 2)
        self.assertIn('/scan/root/dust_file_1.txt', collected_files)
        self.assertIn('/scan/root/dust_file_2.txt', collected_files)
        mock_makedirs.assert_not_called() # Should not create quarantine dir in report-only mode
        mock_move.assert_not_called()
        mock_print.assert_any_call(f"  Found: '/scan/root/dust_file_1.txt'")
        mock_print.assert_any_call(f"  Found: '/scan/root/dust_file_2.txt'")
        mock_print.assert_any_call(f"\n--- Cosmic Dust Report (2 files) ---")

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/scan/root', [], [])]) # No files found
    @patch('datetime.datetime')
    @patch('builtins.print')
    def test_collect_dust_no_files_found(self, mock_print, mock_datetime, mock_walk, mock_isdir):
        # Mock rationale: Simulating an empty directory scan to ensure correct output.
        mock_datetime.now.return_value = self.fixed_now

        scan_path = '/scan/root'
        collected_files = collect_dust(scan_path)

        self.assertEqual(len(collected_files), 0)
        mock_print.assert_any_call("No cosmic dust found. Your repository is sparkling clean!")

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    def test_collect_dust_invalid_path(self, mock_print, mock_isdir):
        # Mock rationale: Testing the error handling for an invalid scan path.
        scan_path = '/nonexistent/path'
        collected_files = collect_dust(scan_path)

        self.assertIsNone(collected_files) # Should return None on error
        mock_print.assert_any_call(f"Error: Scan path '{scan_path}' is not a valid directory.", file=sys.stderr)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.stat')
    @patch('datetime.datetime')
    @patch('os.makedirs')
    @patch('shutil.move', side_effect=OSError('Permission denied'))
    @patch('builtins.print')
    def test_collect_dust_move_error(self, mock_print, mock_move, mock_makedirs, mock_datetime, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulating a permission error during file movement to ensure error handling.
        mock_datetime.now.return_value = self.fixed_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)

        mock_walk.return_value = [
            ('/scan/root', [], ['dust_file.txt'])
        ]

        dust_mtime = self.fixed_now_timestamp - (DEFAULT_MIN_AGE_DAYS * 24 * 3600) - 100
        mock_stat.return_value = MagicMock(st_size=500, st_mtime=dust_mtime)

        scan_path = '/scan/root'
        quarantine_dir = '/quarantine'

        collected_files = collect_dust(scan_path, quarantine_dir)

        self.assertEqual(len(collected_files), 1) # File was identified as dust
        mock_move.assert_called_once()
        mock_print.assert_any_call(f"  Error moving '/scan/root/dust_file.txt': Permission denied", file=sys.stderr)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.stat')
    @patch('datetime.datetime')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists', side_effect=[False, True, False]) # First move target doesn't exist, second does, third doesn't
    @patch('builtins.print')
    def test_collect_dust_quarantine_collision(self, mock_print, mock_exists, mock_move, mock_makedirs, mock_datetime, mock_stat, mock_walk, mock_isdir):
        # Mock rationale: Simulating a scenario where a file with the same name already exists 
        # in the quarantine directory, requiring the utility to rename the moved file.
        mock_datetime.now.return_value = self.fixed_now
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.datetime.fromtimestamp(ts)

        mock_walk.return_value = [
            ('/scan/root', [], ['duplicate.txt'])
        ]

        dust_mtime = self.fixed_now_timestamp - (DEFAULT_MIN_AGE_DAYS * 24 * 3600) - 100
        mock_stat.return_value = MagicMock(st_size=100, st_mtime=dust_mtime)

        scan_path = '/scan/root'
        quarantine_dir = '/quarantine'

        collected_files = collect_dust(scan_path, quarantine_dir)

        self.assertEqual(len(collected_files), 1)
        # Expect move to be called with the renamed path
        mock_move.assert_called_once_with('/scan/root/duplicate.txt', '/quarantine/duplicate_1.txt')
        mock_print.assert_any_call(f"  Moved: '/scan/root/duplicate.txt' -> '/quarantine/duplicate_1.txt'")


if __name__ == '__main__':
    unittest.main()
