import unittest
import os
import hashlib
from unittest.mock import patch, mock_open
from src.purifier import find_duplicates, calculate_file_hash

class TestPurifier(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize', return_value=100) # Mock getsize for calculate_file_hash
    def test_calculate_file_hash(self, mock_getsize, mock_open_func):
        # Mock rationale: We don't want to read actual files during unit tests.
        # mock_open simulates file content, and mock_getsize prevents errors if size is checked.
        mock_open_func.return_value.read.side_effect = [b'test content', b'']
        
        expected_hash = hashlib.md5(b'test content').hexdigest()
        self.assertEqual(calculate_file_hash('dummy_path.txt', 'md5'), expected_hash)

        mock_open_func.return_value.read.side_effect = [b'another test', b'']
        expected_hash_sha256 = hashlib.sha256(b'another test').hexdigest()
        self.assertEqual(calculate_file_hash('dummy_path.txt', 'sha256'), expected_hash_sha256)

    @patch('src.purifier.calculate_file_hash')
    @patch('os.walk')
    def test_find_duplicates_no_duplicates(self, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: We simulate a file system structure and file hashes
        # without touching the actual disk or performing real hash calculations.
        mock_os_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt']),
            ('/root/subdir', [], ['file3.txt'])
        ]
        mock_calculate_file_hash.side_effect = {
            '/root/file1.txt': 'hash_a',
            '/root/file2.txt': 'hash_b',
            '/root/subdir/file3.txt': 'hash_c'
        }.get

        duplicates = find_duplicates('/root')
        self.assertEqual(duplicates, {})
        mock_calculate_file_hash.assert_any_call('/root/file1.txt', 'md5')
        mock_calculate_file_hash.assert_any_call('/root/file2.txt', 'md5')
        mock_calculate_file_hash.assert_any_call('/root/subdir/file3.txt', 'md5')

    @patch('src.purifier.calculate_file_hash')
    @patch('os.walk')
    def test_find_duplicates_with_duplicates(self, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Simulates a scenario where some files have identical content hashes.
        mock_os_walk.return_value = [
            ('/root', [], ['a.txt', 'b.txt', 'c.txt']),
            ('/root/subdir', [], ['d.txt'])
        ]
        mock_calculate_file_hash.side_effect = {
            '/root/a.txt': 'hash_x',
            '/root/b.txt': 'hash_y',
            '/root/c.txt': 'hash_x', # Duplicate of a.txt
            '/root/subdir/d.txt': 'hash_z'
        }.get

        duplicates = find_duplicates('/root')
        expected_duplicates = {
            'hash_x': ['/root/a.txt', '/root/c.txt']
        }
        # Sort paths in expected_duplicates for deterministic comparison
        for h, paths in expected_duplicates.items():
            expected_duplicates[h] = sorted(paths)
        
        # Sort paths in actual duplicates for deterministic comparison
        actual_duplicates_sorted = {}
        for h, paths in duplicates.items():
            actual_duplicates_sorted[h] = sorted(paths)

        self.assertEqual(actual_duplicates_sorted, expected_duplicates)

    @patch('src.purifier.calculate_file_hash')
    @patch('os.walk')
    def test_find_duplicates_multiple_groups(self, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Tests the scenario with multiple distinct groups of duplicate files.
        mock_os_walk.return_value = [
            ('/root', [], ['f1.txt', 'f2.txt', 'f3.txt']),
            ('/root/sub1', [], ['f4.txt']),
            ('/root/sub2', [], ['f5.txt', 'f6.txt'])
        ]
        mock_calculate_file_hash.side_effect = {
            '/root/f1.txt': 'hash_alpha',
            '/root/f2.txt': 'hash_beta',
            '/root/f3.txt': 'hash_alpha', # Duplicate of f1
            '/root/sub1/f4.txt': 'hash_gamma',
            '/root/sub2/f5.txt': 'hash_beta', # Duplicate of f2
            '/root/sub2/f6.txt': 'hash_delta'
        }.get

        duplicates = find_duplicates('/root')
        expected_duplicates = {
            'hash_alpha': ['/root/f1.txt', '/root/f3.txt'],
            'hash_beta': ['/root/f2.txt', '/root/sub2/f5.txt']
        }
        
        actual_duplicates_sorted = {}
        for h, paths in duplicates.items():
            actual_duplicates_sorted[h] = sorted(paths)

        for h, paths in expected_duplicates.items():
            expected_duplicates[h] = sorted(paths)

        self.assertEqual(actual_duplicates_sorted, expected_duplicates)

    @patch('src.purifier.calculate_file_hash')
    @patch('os.walk')
    @patch('builtins.print') # Mock print to suppress output during test
    def test_find_duplicates_io_error(self, mock_print, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Ensures the utility handles file access errors gracefully without crashing.
        mock_os_walk.return_value = [
            ('/root', [], ['unreadable.txt', 'readable.txt'])
        ]
        # Simulate one file being unreadable and another being readable and unique.
        def mock_hash_side_effect(filepath, *args, **kwargs):
            if 'unreadable.txt' in filepath:
                raise IOError("Permission denied")
            return 'unique_hash_for_readable'

        mock_calculate_file_hash.side_effect = mock_hash_side_effect

        duplicates = find_duplicates('/root')
        self.assertEqual(duplicates, {}) # No duplicates should be found if one fails and the other is unique.
        mock_print.assert_called_with(unittest.mock.ANY) # Check if warning was printed
        self.assertIn("Warning: Could not read file", mock_print.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
