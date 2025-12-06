import unittest
import os
import hashlib
import datetime
from unittest.mock import patch, mock_open, MagicMock
from src.dust_bunny_detector import find_dust_bunnies, get_file_hash

class TestDustBunnyDetector(unittest.TestCase):

    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_find_dust_bunnies_old_files(self, mock_datetime, mock_getmtime, mock_walk, mock_isfile):
        # Mock rationale: Simulate file system structure and modification times without actual files.
        # This ensures deterministic tests independent of the host system's file state.

        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26)
        # File 1: old (mtime 2023-09-01)
        # File 2: recent (mtime 2023-10-20)
        # File 3: old (mtime 2023-08-15)

        mock_walk.return_value = [
            ('/mock/dir', [], ['file1.txt', 'file2.txt', 'file3.log'])
        ]
        mock_isfile.side_effect = lambda x: x in ['/mock/dir/file1.txt', '/mock/dir/file2.txt', '/mock/dir/file3.log']

        # Mock getmtime to return specific timestamps
        def mock_getmtime_side_effect(path):
            if path == '/mock/dir/file1.txt':
                return datetime.datetime(2023, 9, 1).timestamp() # Older than 30 days
            elif path == '/mock/dir/file2.txt':
                return datetime.datetime(2023, 10, 20).timestamp() # Newer than 30 days
            elif path == '/mock/dir/file3.log':
                return datetime.datetime(2023, 8, 15).timestamp() # Older than 30 days
            return 0

        mock_getmtime.side_effect = mock_getmtime_side_effect

        results = find_dust_bunnies('/mock/dir', age_threshold_days=30, detect_duplicates=False)

        self.assertIn('/mock/dir/file1.txt', results['old_files'])
        self.assertIn('/mock/dir/file3.log', results['old_files'])
        self.assertNotIn('/mock/dir/file2.txt', results['old_files'])
        self.assertEqual(len(results['old_files']), 2)
        self.assertEqual(len(results['duplicate_files']), 0)

    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.md5')
    def test_find_dust_bunnies_duplicate_files(self, mock_md5, mock_builtins_open, mock_datetime, mock_getmtime, mock_walk, mock_isfile):
        # Mock rationale: Simulate file system structure and file content for hashing without actual files.
        # This ensures deterministic tests independent of the host system's file state.

        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26) # Not used for duplicates, but good practice
        mock_getmtime.return_value = datetime.datetime(2023, 10, 25).timestamp() # Not used for duplicates, but good practice

        mock_walk.return_value = [
            ('/mock/dir', [], ['fileA.txt', 'fileB.txt', 'fileC.txt', 'fileD.log'])
        ]
        mock_isfile.side_effect = lambda x: x in [
            '/mock/dir/fileA.txt', '/mock/dir/fileB.txt', '/mock/dir/fileC.txt', '/mock/dir/fileD.log'
        ]

        # Mock hashlib.md5 to return specific hashes for specific file contents
        # fileA.txt and fileC.txt will have the same content/hash
        # fileB.txt and fileD.log will have unique content/hashes
        mock_md5_instance = MagicMock()
        mock_md5.return_value = mock_md5_instance

        def mock_read_side_effect(filepath):
            if filepath == '/mock/dir/fileA.txt':
                mock_md5_instance.hexdigest.return_value = 'hash_A_C'
                return b'content_A'
            elif filepath == '/mock/dir/fileB.txt':
                mock_md5_instance.hexdigest.return_value = 'hash_B'
                return b'content_B'
            elif filepath == '/mock/dir/fileC.txt':
                mock_md5_instance.hexdigest.return_value = 'hash_A_C'
                return b'content_A'
            elif filepath == '/mock/dir/fileD.log':
                mock_md5_instance.hexdigest.return_value = 'hash_D'
                return b'content_D'
            return b''

        mock_builtins_open.side_effect = lambda f, mode: mock_open(read_data=mock_read_side_effect(f)).return_value

        results = find_dust_bunnies('/mock/dir', age_threshold_days=None, detect_duplicates=True)

        self.assertEqual(len(results['old_files']), 0)
        self.assertEqual(len(results['duplicate_files']), 1)
        self.assertIn('hash_A_C', results['duplicate_files'])
        self.assertIn('/mock/dir/fileA.txt', results['duplicate_files']['hash_A_C'])
        self.assertIn('/mock/dir/fileC.txt', results['duplicate_files']['hash_A_C'])
        self.assertEqual(len(results['duplicate_files']['hash_A_C']), 2)

    @patch('os.path.isfile')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.md5')
    def test_find_dust_bunnies_both_old_and_duplicates(self, mock_md5, mock_builtins_open, mock_datetime, mock_getmtime, mock_walk, mock_isfile):
        # Mock rationale: Combine previous mock rationales to test both features simultaneously.

        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26)

        mock_walk.return_value = [
            ('/mock/dir', [], ['old_dup1.txt', 'old_dup2.txt', 'recent_unique.txt', 'old_unique.log'])
        ]
        mock_isfile.side_effect = lambda x: x in [
            '/mock/dir/old_dup1.txt', '/mock/dir/old_dup2.txt', '/mock/dir/recent_unique.txt', '/mock/dir/old_unique.log'
        ]

        # Mock mtime:
        # old_dup1.txt: old (2023-09-01)
        # old_dup2.txt: old (2023-09-01)
        # recent_unique.txt: recent (2023-10-20)
        # old_unique.log: old (2023-08-15)
        def mock_getmtime_side_effect(path):
            if path in ['/mock/dir/old_dup1.txt', '/mock/dir/old_dup2.txt']:
                return datetime.datetime(2023, 9, 1).timestamp() # Older than 30 days
            elif path == '/mock/dir/recent_unique.txt':
                return datetime.datetime(2023, 10, 20).timestamp() # Newer than 30 days
            elif path == '/mock/dir/old_unique.log':
                return datetime.datetime(2023, 8, 15).timestamp() # Older than 30 days
            return 0
        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Mock hashes:
        # old_dup1.txt and old_dup2.txt have same content/hash
        # recent_unique.txt and old_unique.log have unique content/hashes
        mock_md5_instance = MagicMock()
        mock_md5.return_value = mock_md5_instance

        def mock_read_side_effect(filepath):
            if filepath in ['/mock/dir/old_dup1.txt', '/mock/dir/old_dup2.txt']:
                mock_md5_instance.hexdigest.return_value = 'hash_OLD_DUP'
                return b'content_old_dup'
            elif filepath == '/mock/dir/recent_unique.txt':
                mock_md5_instance.hexdigest.return_value = 'hash_RECENT_UNIQUE'
                return b'content_recent_unique'
            elif filepath == '/mock/dir/old_unique.log':
                mock_md5_instance.hexdigest.return_value = 'hash_OLD_UNIQUE'
                return b'content_old_unique'
            return b''
        mock_builtins_open.side_effect = lambda f, mode: mock_open(read_data=mock_read_side_effect(f)).return_value

        results = find_dust_bunnies('/mock/dir', age_threshold_days=30, detect_duplicates=True)

        # Verify old files
        self.assertEqual(len(results['old_files']), 3)
        self.assertIn('/mock/dir/old_dup1.txt', results['old_files'])
        self.assertIn('/mock/dir/old_dup2.txt', results['old_files'])
        self.assertIn('/mock/dir/old_unique.log', results['old_files'])
        self.assertNotIn('/mock/dir/recent_unique.txt', results['old_files'])

        # Verify duplicate files
        self.assertEqual(len(results['duplicate_files']), 1)
        self.assertIn('hash_OLD_DUP', results['duplicate_files'])
        self.assertIn('/mock/dir/old_dup1.txt', results['duplicate_files']['hash_OLD_DUP'])
        self.assertIn('/mock/dir/old_dup2.txt', results['duplicate_files']['hash_OLD_DUP'])
        self.assertEqual(len(results['duplicate_files']['hash_OLD_DUP']), 2)

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.md5')
    def test_get_file_hash(self, mock_md5, mock_builtins_open, mock_isfile):
        # Mock rationale: Simulate file content reading and hashing without actual file I/O.
        # This ensures deterministic tests for the hashing function.

        mock_builtins_open.return_value.__enter__.return_value.read.side_effect = [b'test content', b'']
        mock_md5_instance = MagicMock()
        mock_md5_instance.hexdigest.return_value = 'mock_hash_value'
        mock_md5.return_value = mock_md5_instance

        hash_value = get_file_hash('/mock/file.txt')

        self.assertEqual(hash_value, 'mock_hash_value')
        mock_builtins_open.assert_called_once_with('/mock/file.txt', 'rb')
        mock_md5_instance.update.assert_called_once_with(b'test content')
        mock_md5_instance.hexdigest.assert_called_once()

    @patch('os.path.isfile', return_value=False) # Simulate a non-existent file
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.md5')
    def test_get_file_hash_io_error(self, mock_md5, mock_builtins_open, mock_isfile):
        # Mock rationale: Simulate an IOError during file reading to ensure graceful handling.
        # This tests error paths without requiring actual file system errors.

        mock_builtins_open.side_effect = IOError("Permission denied")

        hash_value = get_file_hash('/mock/unreadable_file.txt')

        self.assertIsNone(hash_value)
        mock_builtins_open.assert_called_once_with('/mock/unreadable_file.txt', 'rb')
        mock_md5.assert_not_called() # Hasher should not be used if open fails

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_find_dust_bunnies_invalid_dir(self, mock_stderr, mock_isdir):
        # Mock rationale: Simulate an invalid directory path to test error handling.
        # This avoids actual file system checks and ensures predictable error output.

        results = find_dust_bunnies('/nonexistent/dir', age_threshold_days=10)
        self.assertEqual(results, {'old_files': [], 'duplicate_files': []})
        mock_stderr.write.assert_called_with("Error: Directory '/nonexistent/dir' not found.\n")


if __name__ == '__main__':
    unittest.main()
