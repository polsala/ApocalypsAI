import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import time
import sys

# Add the src directory to the path to allow importing dust_bunny_sweeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_bunny_sweeper import find_digital_dust_bunnies, get_file_hash
sys.path.pop(0)

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        self.test_dir = '/mock/test/dir'
        self.current_time = time.time()

    @patch('os.walk')
    @patch('os.stat')
    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('dust_bunny_sweeper.get_file_hash') # Mock the hash function directly
    @patch('builtins.print') # Mock print to capture output
    def test_find_old_files(self, mock_print, mock_get_file_hash, mock_isfile, mock_islink, mock_stat, mock_walk):
        # Mock rationale: os.walk simulates directory structure.
        # os.stat simulates file metadata (size, mtime).
        # os.path.islink and os.path.isfile ensure we process regular files.
        # get_file_hash is mocked to return consistent hashes without actual file I/O.
        # builtins.print is mocked to prevent console output during tests and allow inspection.

        # Simulate files:
        # - file_old: older than 365 days
        # - file_recent: newer than 365 days
        # - file_tiny: smaller than min_size_bytes
        mock_walk.return_value = [
            (self.test_dir, [], ['file_old.txt', 'file_recent.txt', 'file_tiny.log'])
        ]

        # Mock os.stat for each file
        mock_stat.side_effect = [
            # file_old.txt
            MagicMock(st_size=1000, st_mtime=self.current_time - (366 * 24 * 3600)),
            # file_recent.txt
            MagicMock(st_size=2000, st_mtime=self.current_time - (100 * 24 * 3600)),
            # file_tiny.log (smaller than default min_size=0, but let's test with a custom min_size)
            MagicMock(st_size=50, st_mtime=self.current_time - (500 * 24 * 3600))
        ]

        # Mock get_file_hash for each file
        mock_get_file_hash.side_effect = ['hash_old', 'hash_recent', 'hash_tiny']

        old_files, duplicate_groups = find_digital_dust_bunnies(self.test_dir, age_threshold_days=365, min_size_bytes=0)

        self.assertEqual(len(old_files), 2) # file_old.txt and file_tiny.log should be old
        self.assertIn(os.path.join(self.test_dir, 'file_old.txt'), [f[0] for f in old_files])
        self.assertIn(os.path.join(self.test_dir, 'file_tiny.log'), [f[0] for f in old_files])
        self.assertEqual(len(duplicate_groups), 0)

        # Verify print calls for old files
        mock_print.assert_any_call(self.assertRegex('### Fluffy Dust Bunnies', '### Fluffy Dust Bunnies'))
        mock_print.assert_any_call(self.assertRegex(f'  - {os.path.join(self.test_dir, 'file_old.txt')}', 'file_old.txt'))
        mock_print.assert_any_call(self.assertRegex(f'  - {os.path.join(self.test_dir, 'file_tiny.log')}', 'file_tiny.log'))

    @patch('os.walk')
    @patch('os.stat')
    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('dust_bunny_sweeper.get_file_hash')
    @patch('builtins.print')
    def test_find_duplicate_files(self, mock_print, mock_get_file_hash, mock_isfile, mock_islink, mock_stat, mock_walk):
        # Mock rationale: Same as above, focusing on duplicate detection.

        mock_walk.return_value = [
            (self.test_dir, [], ['fileA.txt', 'fileB.txt', 'fileC.txt'])
        ]

        # All files are recent enough not to be old, and have a size.
        mock_stat.side_effect = [
            MagicMock(st_size=100, st_mtime=self.current_time - (10 * 24 * 3600)),
            MagicMock(st_size=100, st_mtime=self.current_time - (20 * 24 * 3600)),
            MagicMock(st_size=200, st_mtime=self.current_time - (30 * 24 * 3600))
        ]

        # fileA.txt and fileB.txt have the same hash
        mock_get_file_hash.side_effect = ['hash_duplicate', 'hash_duplicate', 'hash_unique']

        old_files, duplicate_groups = find_digital_dust_bunnies(self.test_dir, age_threshold_days=365, min_size_bytes=0)

        self.assertEqual(len(old_files), 0)
        self.assertEqual(len(duplicate_groups), 1)
        self.assertIn('hash_duplicate', duplicate_groups)
        self.assertEqual(len(duplicate_groups['hash_duplicate']), 2)
        self.assertIn((os.path.join(self.test_dir, 'fileA.txt'), 100), duplicate_groups['hash_duplicate'])
        self.assertIn((os.path.join(self.test_dir, 'fileB.txt'), 100), duplicate_groups['hash_duplicate'])

        # Verify print calls for duplicate files
        mock_print.assert_any_call(self.assertRegex('### Tangled Dust Clumps', '### Tangled Dust Clumps'))
        mock_print.assert_any_call(self.assertRegex(f'  - {os.path.join(self.test_dir, 'fileA.txt')}', 'fileA.txt'))
        mock_print.assert_any_call(self.assertRegex(f'  - {os.path.join(self.test_dir, 'fileB.txt')}', 'fileB.txt'))

    @patch('os.walk')
    @patch('os.stat')
    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('dust_bunny_sweeper.get_file_hash')
    @patch('builtins.print')
    def test_no_dust_bunnies(self, mock_print, mock_get_file_hash, mock_isfile, mock_islink, mock_stat, mock_walk):
        # Mock rationale: Simulates a clean directory with no old or duplicate files.

        mock_walk.return_value = [
            (self.test_dir, [], ['clean_file1.txt', 'clean_file2.txt'])
        ]

        mock_stat.side_effect = [
            MagicMock(st_size=100, st_mtime=self.current_time - (10 * 24 * 3600)),
            MagicMock(st_size=200, st_mtime=self.current_time - (20 * 24 * 3600))
        ]

        mock_get_file_hash.side_effect = ['hash_clean1', 'hash_clean2']

        old_files, duplicate_groups = find_digital_dust_bunnies(self.test_dir, age_threshold_days=365, min_size_bytes=0)

        self.assertEqual(len(old_files), 0)
        self.assertEqual(len(duplicate_groups), 0)
        mock_print.assert_any_call('✨ Your digital space is sparkling clean! No dust bunnies found. ✨\n')

    @patch('os.walk')
    @patch('os.stat')
    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('dust_bunny_sweeper.get_file_hash')
    @patch('builtins.print')
    def test_min_size_filter(self, mock_print, mock_get_file_hash, mock_isfile, mock_islink, mock_stat, mock_walk):
        # Mock rationale: Tests the min_size_bytes argument to ensure small files are ignored.

        mock_walk.return_value = [
            (self.test_dir, [], ['small.txt', 'medium.txt', 'large.txt'])
        ]

        mock_stat.side_effect = [
            MagicMock(st_size=50, st_mtime=self.current_time - (10 * 24 * 3600)),   # small
            MagicMock(st_size=500, st_mtime=self.current_time - (20 * 24 * 3600)),  # medium
            MagicMock(st_size=1500, st_mtime=self.current_time - (30 * 24 * 3600)) # large
        ]

        mock_get_file_hash.side_effect = ['hash_small', 'hash_medium', 'hash_large']

        # Set min_size_bytes to 100 bytes
        old_files, duplicate_groups = find_digital_dust_bunnies(self.test_dir, age_threshold_days=365, min_size_bytes=100)

        # Only medium.txt and large.txt should have been processed for old/duplicates
        # In this specific test, none are old and none are duplicates, but the key is that 'small.txt' was skipped.
        self.assertEqual(len(old_files), 0)
        self.assertEqual(len(duplicate_groups), 0)
        # Ensure get_file_hash was called only for medium and large files
        self.assertEqual(mock_get_file_hash.call_count, 2)
        mock_get_file_hash.assert_any_call(os.path.join(self.test_dir, 'medium.txt'))
        mock_get_file_hash.assert_any_call(os.path.join(self.test_dir, 'large.txt'))
        mock_get_file_hash.assert_called_with(os.path.join(self.test_dir, 'large.txt')) # Last call was large.txt

    @patch('builtins.open', new_callable=mock_open)
    def test_get_file_hash(self, mock_file):
        # Mock rationale: builtins.open is mocked to simulate reading file content.
        # This allows testing the hashing logic without actual file I/O.

        mock_file.return_value.read.side_effect = [b'chunk1', b'chunk2', b'']
        expected_hash = hashlib.sha256(b'chunk1chunk2').hexdigest()
        self.assertEqual(get_file_hash('/mock/path/file.txt'), expected_hash)
        mock_file.assert_called_with('/mock/path/file.txt', 'rb')

    @patch('os.walk')
    @patch('os.stat')
    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('dust_bunny_sweeper.get_file_hash')
    @patch('builtins.print')
    def test_os_error_handling(self, mock_print, mock_get_file_hash, mock_isfile, mock_islink, mock_stat, mock_walk):
        # Mock rationale: Simulates an OSError during os.stat to ensure graceful error handling.

        mock_walk.return_value = [
            (self.test_dir, [], ['good_file.txt', 'bad_file.txt'])
        ]

        mock_stat.side_effect = [
            MagicMock(st_size=100, st_mtime=self.current_time - (10 * 24 * 3600)),
            OSError("Permission denied") # Simulate an error for bad_file.txt
        ]

        mock_get_file_hash.side_effect = ['hash_good'] # Only good_file will be hashed

        old_files, duplicate_groups = find_digital_dust_bunnies(self.test_dir, age_threshold_days=365, min_size_bytes=0)

        # Only good_file.txt should have been processed
        self.assertEqual(len(old_files), 0)
        self.assertEqual(len(duplicate_groups), 0)
        mock_print.assert_any_call(self.assertRegex('Warning: Could not access', 'Warning: Could not access'))
        mock_print.assert_any_call(self.assertRegex(f"Warning: Could not access '{os.path.join(self.test_dir, 'bad_file.txt')}'", 'bad_file.txt'))
        self.assertEqual(mock_get_file_hash.call_count, 1)
        mock_get_file_hash.assert_called_with(os.path.join(self.test_dir, 'good_file.txt'))


if __name__ == '__main__':
    unittest.main()
