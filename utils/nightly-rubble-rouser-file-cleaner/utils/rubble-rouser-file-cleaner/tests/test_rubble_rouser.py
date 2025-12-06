import unittest
import os
import hashlib
from unittest.mock import patch, mock_open, MagicMock
from collections import defaultdict

# Import the functions to be tested
from src.rubble_rouser import find_empty_dirs, find_duplicate_files, _hash_file

class TestRubbleRouser(unittest.TestCase):

    @patch('os.walk')
    def test_find_empty_dirs(self, mock_os_walk):
        # Mock rationale: os.walk is a file system traversal function.
        # We need to control the directory structure for deterministic testing
        # without actually creating files on disk.
        mock_os_walk.return_value = [
            ('/root', ['dir1', 'dir2', 'empty_dir'], ['file1.txt']),
            ('/root/dir1', ['subdir1'], ['file2.txt']),
            ('/root/dir1/subdir1', [], ['file3.txt']),
            ('/root/dir2', [], []), # This is an empty directory
            ('/root/empty_dir', [], []), # This is another empty directory
            ('/root/dir_with_only_sub', ['sub_only'], []),
            ('/root/dir_with_only_sub/sub_only', [], []), # Not empty itself, but its parent is not empty
        ]

        expected_empty_dirs = [
            '/root/dir2',
            '/root/empty_dir',
        ]
        
        result = find_empty_dirs('/root')
        self.assertCountEqual(result, expected_empty_dirs)
        mock_os_walk.assert_called_once_with('/root')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.islink', return_value=False) # Mock rationale: Assume no symlinks for simplicity
    def test_find_duplicate_files(self, mock_islink, mock_file_open, mock_os_walk):
        # Mock rationale: os.walk is for directory traversal.
        # builtins.open is for reading file content to hash.
        # We need to simulate a file system with specific content for hashing.

        # Define a mock file system structure
        mock_os_walk.return_value = [
            ('/root', ['dirA', 'dirB'], ['file_unique.txt']),
            ('/root/dirA', [], ['file_dup1.txt', 'file_dup2.txt']),
            ('/root/dirB', [], ['file_dup3.txt', 'file_another_unique.txt']),
        ]

        # Define mock file contents and their hashes
        file_contents = {
            '/root/file_unique.txt': b'unique content',
            '/root/dirA/file_dup1.txt': b'duplicate content',
            '/root/dirA/file_dup2.txt': b'duplicate content', # Same content as file_dup1.txt
            '/root/dirB/file_dup3.txt': b'duplicate content', # Same content as file_dup1.txt
            '/root/dirB/file_another_unique.txt': b'another unique content',
        }

        # Helper to get hash for mock content
        def get_hash(content):
            return hashlib.md5(content).hexdigest()

        # Configure mock_file_open to return specific content based on path
        def mock_open_side_effect(filepath, mode='r', **kwargs):
            if filepath in file_contents:
                mock_file = MagicMock()
                mock_file.__enter__.return_value = mock_file
                mock_file.read.side_effect = [file_contents[filepath], b''] # Read once, then EOF
                return mock_file
            raise FileNotFoundError(f"Mock file not found: {filepath}")

        mock_file_open.side_effect = mock_open_side_effect

        # Expected duplicates based on content
        duplicate_hash = get_hash(b'duplicate content')
        expected_duplicates = {
            duplicate_hash: [
                '/root/dirA/file_dup1.txt',
                '/root/dirA/file_dup2.txt',
                '/root/dirB/file_dup3.txt',
            ]
        }

        result = find_duplicate_files('/root')
        
        # Sort lists for consistent comparison
        for h in expected_duplicates:
            expected_duplicates[h].sort()
        for h in result:
            result[h].sort()

        self.assertDictEqual(result, expected_duplicates)
        mock_os_walk.assert_called_once_with('/root')
        # Verify open was called for each file
        self.assertEqual(mock_file_open.call_count, len(file_contents))
        
    def test_hash_file(self):
        # Mock rationale: Test the internal _hash_file function directly
        # by mocking file content.
        mock_content = b"This is some test content for hashing."
        expected_hash = hashlib.md5(mock_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=mock_content)) as m_open:
            filepath = "/fake/path/to/file.txt"
            result_hash = _hash_file(filepath)
            self.assertEqual(result_hash, expected_hash)
            m_open.assert_called_once_with(filepath, 'rb')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_with_io_error(self, mock_islink, mock_file_open, mock_os_walk):
        # Mock rationale: Ensure the utility handles files that cannot be read
        # gracefully without crashing, and logs a warning if verbose.

        mock_os_walk.return_value = [
            ('/root', [], ['good_file.txt', 'bad_file.txt']),
        ]

        file_contents = {
            '/root/good_file.txt': b'good content',
        }

        def mock_open_side_effect(filepath, mode='r', **kwargs):
            if filepath == '/root/good_file.txt':
                mock_file = MagicMock()
                mock_file.__enter__.return_value = mock_file
                mock_file.read.side_effect = [file_contents[filepath], b'']
                return mock_file
            elif filepath == '/root/bad_file.txt':
                raise IOError("Permission denied")
            raise FileNotFoundError(f"Mock file not found: {filepath}")

        mock_file_open.side_effect = mock_open_side_effect

        # Expect no duplicates, as only one file is readable
        expected_duplicates = {}
        
        # Test with verbose=False (default)
        result = find_duplicate_files('/root')
        self.assertDictEqual(result, expected_duplicates)

        # Test with verbose=True to ensure warning is printed (can't assert print directly here,
        # but the code path for the warning should be covered).
        # For a real test, one might capture stdout/stderr.
        # Here, we just ensure it doesn't crash.
        result_verbose = find_duplicate_files('/root', verbose=True)
        self.assertDictEqual(result_verbose, expected_duplicates)


if __name__ == '__main__':
    unittest.main()
