import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import shutil
import hashlib
from datetime import datetime, timedelta
import sys
from io import StringIO

# Import the functions from the duster.py script
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from duster import find_stale_files, find_duplicate_files, quarantine_files, main, get_file_hash

class TestDuster(unittest.TestCase):

    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_stale_files(self, mock_walk, mock_getmtime):
        # Mock rationale: Simulate file system traversal and modification times.
        # This allows deterministic testing without actual file I/O or time-dependent behavior.

        # Simulate current time for consistent stale calculation
        mock_now = datetime(2024, 1, 1, 12, 0, 0)
        with patch('duster.datetime') as mock_dt:
            mock_dt.now.return_value = mock_now
            mock_dt.fromtimestamp = datetime.fromtimestamp # Keep original for conversion
            mock_dt.timedelta = timedelta # Keep original for timedelta

            # Setup mock_walk to return a directory structure
            mock_walk.return_value = [
                ('/test_dir', [], ['file1.txt', 'file2.txt', 'file3.txt'])
            ]

            # Setup mock_getmtime for each file
            # file1.txt: modified 100 days ago (stale for 90 days threshold)
            # file2.txt: modified 50 days ago (not stale for 90 days threshold)
            # file3.txt: modified 10 days ago (not stale for 90 days threshold)
            mock_getmtime.side_effect = [
                (mock_now - timedelta(days=100)).timestamp(), # file1.txt
                (mock_now - timedelta(days=50)).timestamp(),  # file2.txt
                (mock_now - timedelta(days=10)).timestamp()   # file3.txt
            ]

            stale_files = find_stale_files('/test_dir', 90)

            self.assertEqual(len(stale_files), 1)
            self.assertEqual(stale_files[0][0], os.path.join('/test_dir', 'file1.txt'))
            self.assertEqual(stale_files[0][1], (mock_now - timedelta(days=100)).strftime('%Y-%m-%d'))

            # Test with 0 stale_days (should return empty)
            stale_files_disabled = find_stale_files('/test_dir', 0)
            self.assertEqual(len(stale_files_disabled), 0)

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('duster.get_file_hash') # Mock the hash function directly
    def test_find_duplicate_files(self, mock_get_file_hash, mock_walk, mock_getsize):
        # Mock rationale: Simulate file system traversal, file sizes, and file content hashes.
        # This ensures deterministic results for duplicate detection without actual file system or hashing operations.

        # Setup mock_walk to return a directory structure
        mock_walk.return_value = [
            ('/test_dir', [], ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt'])
        ]

        # Setup mock_getsize for each file
        # a.txt: size 100
        # b.txt: size 200
        # c.txt: size 100 (potential duplicate with a.txt)
        # d.txt: size 200 (potential duplicate with b.txt)
        # e.txt: size 300
        mock_getsize.side_effect = [
            100, # a.txt
            200, # b.txt
            100, # c.txt
            200, # d.txt
            300  # e.txt
        ]

        # Setup mock_get_file_hash for each file
        # a.txt: hash 'hash_A'
        # b.txt: hash 'hash_B'
        # c.txt: hash 'hash_A' (actual duplicate of a.txt)
        # d.txt: hash 'hash_C' (not a duplicate of b.txt despite same size)
        # e.txt: hash 'hash_E'
        mock_get_file_hash.side_effect = [
            'hash_A', # a.txt
            'hash_B', # b.txt
            'hash_A', # c.txt
            'hash_C', # d.txt
            'hash_E'  # e.txt
        ]

        duplicate_groups = find_duplicate_files('/test_dir')

        self.assertEqual(len(duplicate_groups), 1)
        self.assertIn('hash_A', duplicate_groups)
        self.assertCountEqual(duplicate_groups['hash_A'], [
            os.path.join('/test_dir', 'a.txt'),
            os.path.join('/test_dir', 'c.txt')
        ])
        self.assertNotIn('hash_B', duplicate_groups) # b.txt and d.txt have different hashes
        self.assertNotIn('hash_C', duplicate_groups)
        self.assertNotIn('hash_E', duplicate_groups)

    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.exists')
    def test_quarantine_files(self, mock_exists, mock_makedirs, mock_move):
        # Mock rationale: Prevent actual file system modifications (moving files, creating directories).
        # This allows testing the logic of file movement and conflict resolution deterministically.

        mock_exists.side_effect = [False, True, False] # First dest_path doesn't exist, second does, then new name doesn't

        files_to_quarantine = [
            os.path.join('/src', 'file1.txt'),
            os.path.join('/src', 'file2.txt')
        ]
        quarantine_dir = '/dustbin'

        quarantined_count = quarantine_files(files_to_quarantine, quarantine_dir)

        mock_makedirs.assert_called_once_with(quarantine_dir, exist_ok=True)
        self.assertEqual(mock_move.call_count, 2)
        mock_move.assert_any_call(os.path.join('/src', 'file1.txt'), os.path.join('/dustbin', 'file1.txt'))
        # For file2.txt, it should try 'file2.txt' first, then 'file2_1.txt'
        mock_move.assert_any_call(os.path.join('/src', 'file2.txt'), os.path.join('/dustbin', 'file2_1.txt'))
        self.assertEqual(quarantined_count, 2)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('duster.find_stale_files')
    @patch('duster.find_duplicate_files')
    @patch('duster.quarantine_files')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_stale_only_report(self, mock_stdout, mock_quarantine, mock_find_duplicates, mock_find_stale, mock_parse_args):
        # Mock rationale: Isolate the main function's logic from its dependencies (CLI args, file system operations).
        # This allows testing argument parsing and report generation without side effects.

        mock_parse_args.return_value = MagicMock(
            directory='/test_dir',
            stale_days=90,
            find_duplicates=False,
            quarantine_dir=None
        )
        mock_find_stale.return_value = [
            (os.path.join('/test_dir', 'old_file.txt'), '2023-01-01')
        ]
        mock_find_duplicates.return_value = {}
        mock_quarantine.return_value = 0

        main()

        output = mock_stdout.getvalue()
        self.assertIn('Scanning /test_dir...', output)
        self.assertIn('--- Stale Files (not modified in 90 days) ---', output)
        self.assertIn('old_file.txt', output)
        self.assertIn('No duplicate files found.', output)
        self.assertIn('Found 1 stale files.', output)
        self.assertIn('Found 0 groups of duplicate files (0 files total).', output)
        self.assertIn('No files were quarantined', output)
        mock_find_stale.assert_called_once_with('/test_dir', 90)
        mock_find_duplicates.assert_not_called()
        mock_quarantine.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('duster.find_stale_files')
    @patch('duster.find_duplicate_files')
    @patch('duster.quarantine_files')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_duplicates_only_report(self, mock_stdout, mock_quarantine, mock_find_duplicates, mock_find_stale, mock_parse_args):
        # Mock rationale: Same as above, focusing on duplicate detection reporting.

        mock_parse_args.return_value = MagicMock(
            directory='/test_dir',
            stale_days=0,
            find_duplicates=True,
            quarantine_dir=None
        )
        mock_find_stale.return_value = []
        mock_find_duplicates.return_value = {
            'hash123': [os.path.join('/test_dir', 'dup1.txt'), os.path.join('/test_dir', 'dup2.txt')]
        }
        mock_quarantine.return_value = 0

        main()

        output = mock_stdout.getvalue()
        self.assertIn('Scanning /test_dir...', output)
        self.assertIn('No stale files found.', output)
        self.assertIn('--- Duplicate Files ---', output)
        self.assertIn('dup1.txt', output)
        self.assertIn('dup2.txt', output)
        self.assertIn('Found 0 stale files.', output)
        self.assertIn('Found 1 groups of duplicate files (2 files total).', output)
        self.assertIn('No files were quarantined', output)
        mock_find_stale.assert_called_once_with('/test_dir', 0)
        mock_find_duplicates.assert_called_once_with('/test_dir')
        mock_quarantine.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('duster.find_stale_files')
    @patch('duster.find_duplicate_files')
    @patch('duster.quarantine_files')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_quarantine(self, mock_stdout, mock_quarantine, mock_find_duplicates, mock_find_stale, mock_parse_args):
        # Mock rationale: Verify that the quarantine function is called correctly when specified.

        mock_parse_args.return_value = MagicMock(
            directory='/test_dir',
            stale_days=1,
            find_duplicates=True,
            quarantine_dir='/dustbin'
        )
        mock_find_stale.return_value = [
            (os.path.join('/test_dir', 'stale.txt'), '2023-01-01')
        ]
        mock_find_duplicates.return_value = {
            'hash123': [os.path.join('/test_dir', 'dup1.txt'), os.path.join('/test_dir', 'dup2.txt')]
        }
        mock_quarantine.return_value = 2 # 1 stale + 1 duplicate (the second one)

        main()

        output = mock_stdout.getvalue()
        self.assertIn('--- Quarantining Files to /dustbin ---', output)
        self.assertIn('Quarantined 2 files.', output)
        # Ensure quarantine_files is called with the correct set of files
        expected_quarantine_list = [
            os.path.join('/test_dir', 'stale.txt'),
            os.path.join('/test_dir', 'dup2.txt') # Only the second duplicate is quarantined by duster logic
        ]
        mock_quarantine.assert_called_once()
        # Check arguments of the call, specifically the list of files
        called_files = mock_quarantine.call_args[0][0]
        self.assertIsInstance(called_files, list)
        self.assertCountEqual(called_files, expected_quarantine_list)
        self.assertEqual(mock_quarantine.call_args[0][1], '/dustbin')

    @patch('builtins.open', new_callable=mock_open, read_data=b'file content')
    @patch('hashlib.md5')
    def test_get_file_hash(self, mock_md5, mock_file_open):
        # Mock rationale: Prevent actual file I/O and cryptographic operations.
        # This ensures the hash calculation logic is tested deterministically.

        mock_hasher = MagicMock()
        mock_hasher.hexdigest.return_value = 'mocked_hash_value'
        mock_md5.return_value = mock_hasher

        test_filepath = '/path/to/dummy.txt'
        result_hash = get_file_hash(test_filepath)

        mock_file_open.assert_called_once_with(test_filepath, 'rb')
        mock_hasher.update.assert_called_once_with(b'file content')
        mock_hasher.hexdigest.assert_called_once()
        self.assertEqual(result_hash, 'mocked_hash_value')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('duster.find_stale_files')
    @patch('duster.find_duplicate_files')
    @patch('duster.quarantine_files')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_issues(self, mock_stdout, mock_quarantine, mock_find_duplicates, mock_find_stale, mock_parse_args):
        # Mock rationale: Test the scenario where no files are found to be stale or duplicate.

        mock_parse_args.return_value = MagicMock(
            directory='/test_dir',
            stale_days=1,
            find_duplicates=True,
            quarantine_dir=None
        )
        mock_find_stale.return_value = []
        mock_find_duplicates.return_value = {}
        mock_quarantine.return_value = 0

        main()

        output = mock_stdout.getvalue()
        self.assertIn('No issues found. Your digital space is sparkling clean!', output)
        self.assertIn('No files were quarantined', output)

if __name__ == '__main__':
    unittest.main()
