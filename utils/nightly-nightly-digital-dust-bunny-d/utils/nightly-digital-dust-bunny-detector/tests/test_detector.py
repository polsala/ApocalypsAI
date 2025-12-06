import unittest
import os
import hashlib
from unittest.mock import patch, mock_open
from collections import defaultdict

# Import the functions to be tested
from src.detector import find_empty_directories, calculate_file_hash, find_duplicate_files

class TestDigitalDustBunnyDetector(unittest.TestCase):

    @patch('os.walk')
    def test_find_empty_directories(self, mock_os_walk):
        # Mock rationale: os.walk interacts with the file system, which is non-deterministic
        # and undesirable for unit tests. Mocking it allows us to control the directory
        # structure and test the logic deterministically offline.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'empty_dir', 'dir2'], ['file1.txt']),
            ('/root/dir1', [], ['file2.txt']),
            ('/root/empty_dir', [], []), # This should be found
            ('/root/dir2', ['sub_empty'], ['file3.txt']),
            ('/root/dir2/sub_empty', [], []), # This should be found
            ('/root/dir2/sub_full', [], ['file4.txt']),
        ]
        expected_empty_dirs = [
            '/root/empty_dir',
            '/root/dir2/sub_empty'
        ]
        result = find_empty_directories('/root')
        self.assertCountEqual(result, expected_empty_dirs)
        mock_os_walk.assert_called_once_with('/root')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_calculate_file_hash(self, mock_exists, mock_file_open):
        # Mock rationale: `open` interacts with the file system, making tests non-deterministic.
        # `os.path.exists` also interacts with the file system. Mocking them allows us to
        # simulate file content and existence without actual file I/O, ensuring deterministic
        # and offline testing.
        mock_file_open.return_value.read.side_effect = [b'test content', b'']
        expected_hash = hashlib.sha256(b'test content').hexdigest()
        result = calculate_file_hash('/path/to/file.txt')
        self.assertEqual(result, expected_hash)
        mock_file_open.assert_called_once_with('/path/to/file.txt', 'rb')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.path.islink', return_value=False) # Mock rationale: Avoid actual symlink checks
    @patch('os.walk')
    def test_find_duplicate_files(self, mock_os_walk, mock_islink, mock_exists, mock_file_open):
        # Mock rationale: os.walk, open, os.path.exists, and os.path.islink all interact
        # with the file system. Mocking them allows us to simulate a file system structure
        # and file contents deterministically and offline, ensuring the duplicate detection
        # logic is tested in isolation.

        # Simulate file system structure
        mock_os_walk.return_value = [
            ('/root', [], ['fileA.txt', 'fileB.txt', 'fileC.txt', 'fileD.txt']),
            ('/root/sub', [], ['fileA_copy.txt', 'fileE.txt']),
        ]

        # Simulate file contents for hashing
        # fileA.txt and fileA_copy.txt have same content
        # fileB.txt has different content
        # fileC.txt and fileD.txt have same content
        file_contents = {
            '/root/fileA.txt': b'content_A',
            '/root/fileB.txt': b'content_B',
            '/root/fileC.txt': b'content_C',
            '/root/fileD.txt': b'content_C', # Duplicate of fileC.txt
            '/root/sub/fileA_copy.txt': b'content_A', # Duplicate of fileA.txt
            '/root/sub/fileE.txt': b'content_E',
        }

        def mock_open_side_effect(filepath, mode):
            if mode == 'rb' and filepath in file_contents:
                mock_file_handle = mock_open(read_data=file_contents[filepath]).return_value
                mock_file_handle.read.side_effect = [file_contents[filepath], b'']
                return mock_file_handle
            raise FileNotFoundError(f"File not found: {filepath}")

        mock_file_open.side_effect = mock_open_side_effect

        hash_A = hashlib.sha256(b'content_A').hexdigest()
        hash_C = hashlib.sha256(b'content_C').hexdigest()

        expected_duplicates = {
            hash_A: ['/root/fileA.txt', '/root/sub/fileA_copy.txt'],
            hash_C: ['/root/fileC.txt', '/root/fileD.txt'],
        }

        result = find_duplicate_files('/root')

        # Convert lists to sets for order-independent comparison
        normalized_result = {h: set(paths) for h, paths in result.items()}
        normalized_expected = {h: set(paths) for h, paths in expected_duplicates.items()}

        self.assertEqual(normalized_result, normalized_expected)
        mock_os_walk.assert_called_once_with('/root')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_calculate_file_hash_io_error(self, mock_exists, mock_file_open):
        # Mock rationale: Simulating an IOError during file reading to ensure the
        # function handles such exceptions gracefully and returns None, without
        # actually causing I/O errors in the test environment.
        mock_file_open.side_effect = IOError("Permission denied")
        result = calculate_file_hash('/path/to/unreadable_file.txt')
        self.assertIsNone(result)

    @patch('os.walk')
    @patch('src.detector.calculate_file_hash') # Mock rationale: Isolate find_duplicate_files from hash calculation details
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_no_duplicates(self, mock_islink, mock_calculate_hash, mock_os_walk):
        # Mock rationale: Simulating a scenario with no duplicate files to ensure the
        # function correctly returns an empty dictionary for duplicates.
        mock_os_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt', 'file3.txt']),
        ]
        mock_calculate_hash.side_effect = [
            'hash1', 'hash2', 'hash3' # All unique hashes
        ]
        result = find_duplicate_files('/root')
        self.assertEqual(result, {})

    @patch('os.walk')
    def test_find_empty_directories_no_empty(self, mock_os_walk):
        # Mock rationale: Simulating a scenario with no empty directories to ensure the
        # function correctly returns an empty list.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2'], ['file1.txt']),
            ('/root/dir1', [], ['file2.txt']),
            ('/root/dir2', ['sub_full'], []),
            ('/root/dir2/sub_full', [], ['file3.txt']),
        ]
        result = find_empty_directories('/root')
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
