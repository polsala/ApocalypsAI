import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from datetime import datetime, timedelta
import hashlib
import sys
from io import StringIO

# Add the src directory to the path for importing defragmenter
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import defragmenter

class TestDefragmenter(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.md5')
    def test_get_file_info_success(self, mock_md5, mock_open_file, mock_getmtime, mock_getsize):
        # Mock rationale: os.path.getsize, os.path.getmtime, and file reading are external system calls.
        # We mock them to provide deterministic values for testing file info retrieval without actual file system interaction.
        # hashlib.md5 is mocked to control the hash output directly.
        
        mock_getsize.return_value = 1024
        mock_getmtime.return_value = datetime(2023, 1, 1).timestamp()
        
        mock_hasher = MagicMock()
        mock_hasher.hexdigest.return_value = "mockhash123"
        mock_md5.return_value = mock_hasher
        
        mock_open_file.return_value.__enter__.return_value.read.side_effect = [b'chunk1', b'chunk2', b'']

        info = defragmenter.get_file_info("/path/to/file.txt")
        
        self.assertIsNotNone(info)
        self.assertEqual(info['path'], "/path/to/file.txt")
        self.assertEqual(info['size'], 1024)
        self.assertEqual(info['mod_time'], datetime(2023, 1, 1))
        self.assertEqual(info['hash'], "mockhash123")
        mock_open_file.assert_called_once_with("/path/to/file.txt", 'rb')
        mock_hasher.update.assert_any_call(b'chunk1')
        mock_hasher.update.assert_any_call(b'chunk2')

    @patch('os.path.getsize', side_effect=OSError("Permission denied"))
    @patch('os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.md5')
    def test_get_file_info_os_error(self, mock_md5, mock_open_file, mock_getmtime, mock_getsize):
        # Mock rationale: Simulating an OSError during file access to ensure error handling is robust.
        info = defragmenter.get_file_info("/path/to/unreadable.txt")
        self.assertIsNone(info)
        self.assertIn("Warning: Could not get info for /path/to/unreadable.txt: Permission denied", self.mock_stdout.getvalue())

    def test_find_old_files(self):
        # Mock rationale: Testing the logic of date comparison, which is internal to the function.
        # No external mocks needed for this specific function as it operates on pre-processed data.
        now = datetime.now()
        files_info = [
            {'path': 'file1.txt', 'mod_time': now - timedelta(days=10)},
            {'path': 'file2.txt', 'mod_time': now - timedelta(days=60)},
            {'path': 'file3.txt', 'mod_time': now - timedelta(days=1)},
        ]
        
        old_files = defragmenter.find_old_files(files_info, 7) # Older than 7 days
        self.assertEqual(len(old_files), 2)
        self.assertIn('file1.txt', [f['path'] for f in old_files])
        self.assertIn('file2.txt', [f['path'] for f in old_files])
        self.assertNotIn('file3.txt', [f['path'] for f in old_files])

        self.assertEqual(defragmenter.find_old_files(files_info, None), []) # No days_old specified

    def test_find_large_files(self):
        # Mock rationale: Testing the logic of size comparison, which is internal to the function.
        # No external mocks needed for this specific function as it operates on pre-processed data.
        files_info = [
            {'path': 'small.txt', 'size': 500 * 1024}, # 0.5 MB
            {'path': 'medium.txt', 'size': 10 * 1024 * 1024}, # 10 MB
            {'path': 'large.txt', 'size': 100 * 1024 * 1024}, # 100 MB
        ]
        
        large_files = defragmenter.find_large_files(files_info, 50) # Larger than 50 MB
        self.assertEqual(len(large_files), 1)
        self.assertIn('large.txt', [f['path'] for f in large_files])
        
        large_files_2 = defragmenter.find_large_files(files_info, 5) # Larger than 5 MB
        self.assertEqual(len(large_files_2), 2)
        self.assertIn('medium.txt', [f['path'] for f in large_files_2])
        self.assertIn('large.txt', [f['path'] for f in large_files_2])

        self.assertEqual(defragmenter.find_large_files(files_info, None), []) # No min_size_mb specified

    def test_find_duplicate_files(self):
        # Mock rationale: Testing the logic of hash comparison, which is internal to the function.
        # No external mocks needed for this specific function as it operates on pre-processed data.
        files_info = [
            {'path': 'fileA.txt', 'hash': 'hash1', 'size': 100},
            {'path': 'fileB.txt', 'hash': 'hash2', 'size': 200},
            {'path': 'fileC.txt', 'hash': 'hash1', 'size': 100}, # Duplicate of fileA
            {'path': 'fileD.txt', 'hash': 'hash3', 'size': 300},
            {'path': 'fileE.txt', 'hash': 'hash2', 'size': 200}, # Duplicate of fileB
        ]
        
        duplicate_groups = defragmenter.find_duplicate_files(files_info)
        self.assertEqual(len(duplicate_groups), 2)
        self.assertIn('hash1', duplicate_groups)
        self.assertIn('hash2', duplicate_groups)
        self.assertEqual(len(duplicate_groups['hash1']), 2)
        self.assertEqual(len(duplicate_groups['hash2']), 2)
        self.assertIn('fileA.txt', [f['path'] for f in duplicate_groups['hash1']])
        self.assertIn('fileC.txt', [f['path'] for f in duplicate_groups['hash1']])
        self.assertIn('fileB.txt', [f['path'] for f in duplicate_groups['hash2']])
        self.assertIn('fileE.txt', [f['path'] for f in duplicate_groups['hash2']])

        # Test with no duplicates
        no_duplicates_info = [
            {'path': 'file1.txt', 'hash': 'hashA', 'size': 100},
            {'path': 'file2.txt', 'hash': 'hashB', 'size': 200},
        ]
        self.assertEqual(defragmenter.find_duplicate_files(no_duplicates_info), {})

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('defragmenter.get_file_info')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_all_criteria(self, mock_parse_args, mock_get_file_info, mock_os_walk, mock_isdir):
        # Mock rationale: os.path.isdir and os.walk are external system calls for directory traversal.
        # get_file_info is a helper function that itself involves external calls.
        # argparse.ArgumentParser.parse_args is mocked to control command-line arguments programmatically.
        # This allows testing the main orchestration logic without actual file system interaction or command line parsing.

        mock_parse_args.return_value = MagicMock(
            path="/mock/path",
            old_days=30,
            min_size_mb=1,
            find_duplicates=True
        )

        now = datetime.now()
        mock_os_walk.return_value = [
            ('/mock/path', [], ['old_large_dup.txt', 'new_small.txt', 'old_small_dup.txt']),
            ('/mock/path/subdir', [], ['another_dup.txt'])
        ]
        
        # Mock get_file_info to return specific data for each file
        mock_get_file_info.side_effect = [
            # old_large_dup.txt
            {'path': '/mock/path/old_large_dup.txt', 'size': 2 * 1024 * 1024, 'mod_time': now - timedelta(days=45), 'hash': 'hash_A'},
            # new_small.txt
            {'path': '/mock/path/new_small.txt', 'size': 0.5 * 1024 * 1024, 'mod_time': now - timedelta(days=10), 'hash': 'hash_B'},
            # old_small_dup.txt
            {'path': '/mock/path/old_small_dup.txt', 'size': 0.5 * 1024 * 1024, 'mod_time': now - timedelta(days=40), 'hash': 'hash_A'},
            # another_dup.txt
            {'path': '/mock/path/subdir/another_dup.txt', 'size': 2 * 1024 * 1024, 'mod_time': now - timedelta(days=5), 'hash': 'hash_C'},
        ]

        defragmenter.main()
        output = self.mock_stdout.getvalue()
        
        self.assertIn("Scanning '/mock/path' for data dust...", output)
        self.assertIn("Found 2 files older than 30 days:", output)
        self.assertIn("old_large_dup.txt", output)
        self.assertIn("old_small_dup.txt", output)
        
        self.assertIn("Found 1 files larger than 1 MB:", output)
        self.assertIn("old_large_dup.txt", output) # Only this one is > 1MB
        
        self.assertIn("Found 1 groups of duplicate files:", output)
        self.assertIn("Hash: hash_A", output)
        self.assertIn("old_large_dup.txt", output)
        self.assertIn("old_small_dup.txt", output)


    @patch('os.path.isdir', return_value=False)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_path(self, mock_parse_args, mock_isdir):
        # Mock rationale: os.path.isdir is an external system call.
        # argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # This tests the error handling for an invalid directory path.
        mock_parse_args.return_value = MagicMock(
            path="/non/existent/path",
            old_days=None,
            min_size_mb=None,
            find_duplicates=False
        )
        
        defragmenter.main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Error: Directory not found at '/non/existent/path'", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[]) # No files found
    @patch('defragmenter.get_file_info', return_value=None) # No files found
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_files_found(self, mock_parse_args, mock_get_file_info, mock_os_walk, mock_isdir):
        # Mock rationale: os.path.isdir and os.walk are external system calls.
        # get_file_info is mocked to simulate no valid files being found.
        # argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # This tests the scenario where the directory is empty or no files match criteria.
        mock_parse_args.return_value = MagicMock(
            path="/mock/empty/path",
            old_days=30,
            min_size_mb=1,
            find_duplicates=True
        )
        
        defragmenter.main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Scanning '/mock/empty/path' for data dust...", output)
        self.assertIn("No files found older than 30 days.", output)
        self.assertIn("No files found larger than 1 MB.", output)
        self.assertIn("No duplicate files found.", output)
        self.assertIn("All clear! Your digital landscape is free of significant data dust.", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[])
    @patch('defragmenter.get_file_info', return_value=None)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_criteria_specified(self, mock_parse_args, mock_get_file_info, mock_os_walk, mock_isdir):
        # Mock rationale: os.path.isdir, os.walk, get_file_info are mocked to control external interactions.
        # argparse.ArgumentParser.parse_args is mocked to simulate running the script without any criteria.
        # This tests the warning message when no analysis criteria are provided.
        mock_parse_args.return_value = MagicMock(
            path="/mock/path",
            old_days=None,
            min_size_mb=None,
            find_duplicates=False
        )
        
        defragmenter.main()
        output = self.mock_stdout.getvalue()
        self.assertIn("No criteria specified. Use --old-days, --min-size-mb, or --find-duplicates.", output)

if __name__ == '__main__':
    unittest.main()
