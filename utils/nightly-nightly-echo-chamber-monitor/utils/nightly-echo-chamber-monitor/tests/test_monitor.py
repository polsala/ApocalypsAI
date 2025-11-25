import unittest
from unittest.mock import patch, mock_open
import os
import hashlib

# Import the functions to be tested
from src.monitor import calculate_file_hash, find_duplicate_files

class TestEchoChamberMonitor(unittest.TestCase):

    def _mock_hash(self, content):
        """Helper to get SHA256 hash for mock content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash(self, mock_file_open):
        # Mock rationale: We need to control the file content to ensure deterministic hash calculation.
        # `mock_open` allows us to simulate reading from a file without actual disk I/O.
        mock_file_open.return_value.read.side_effect = [b'hello', b' world', b'']
        expected_hash = hashlib.sha256(b'hello world').hexdigest()
        self.assertEqual(calculate_file_hash('dummy_path.txt'), expected_hash)

        mock_file_open.return_value.read.side_effect = [b'unique', b' content', b'']
        expected_hash_2 = hashlib.sha256(b'unique content').hexdigest()
        self.assertEqual(calculate_file_hash('another_dummy.txt'), expected_hash_2)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.islink', return_value=False)
    @patch('os.walk')
    @patch('src.monitor.calculate_file_hash') # Mock the hash calculation directly
    def test_find_duplicate_files_no_duplicates(self, mock_calculate_hash, mock_os_walk, mock_islink, mock_isdir):
        # Mock rationale: `os.walk` is mocked to simulate a directory structure without creating real files.
        # `calculate_file_hash` is mocked to return predefined hashes, ensuring deterministic test results
        # without relying on actual file content or I/O.
        mock_os_walk.return_value = [
            ('/root', [], ['fileA.txt', 'fileB.txt']),
            ('/root/subdir', [], ['fileC.txt'])
        ]
        
        # Assign unique hashes to each file
        mock_calculate_hash.side_effect = [
            self._mock_hash('contentA'), # fileA.txt
            self._mock_hash('contentB'), # fileB.txt
            self._mock_hash('contentC')  # fileC.txt
        ]

        duplicates = find_duplicate_files('/root')
        self.assertEqual(duplicates, {})
        self.assertEqual(mock_calculate_hash.call_count, 3)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.islink', return_value=False)
    @patch('os.walk')
    @patch('src.monitor.calculate_file_hash')
    def test_find_duplicate_files_with_duplicates(self, mock_calculate_hash, mock_os_walk, mock_islink, mock_isdir):
        # Mock rationale: Same as above. We simulate a structure with files that should have identical hashes.
        mock_os_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt']),
            ('/root/subdir', [], ['file3.txt', 'unique.txt'])
        ]

        # file1.txt and file3.txt should be duplicates
        hash_dup = self._mock_hash('duplicate content')
        hash_unique = self._mock_hash('unique content')

        mock_calculate_hash.side_effect = [
            hash_dup,      # /root/file1.txt
            hash_unique,   # /root/file2.txt
            hash_dup,      # /root/subdir/file3.txt
            self._mock_hash('another unique') # /root/subdir/unique.txt
        ]

        duplicates = find_duplicate_files('/root')
        
        expected_duplicates = {
            hash_dup: [
                os.path.join('/root', 'file1.txt'),
                os.path.join('/root/subdir', 'file3.txt')
            ]
        }
        self.assertEqual(duplicates, expected_duplicates)
        self.assertEqual(mock_calculate_hash.call_count, 4)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.islink', return_value=False)
    @patch('os.walk')
    @patch('src.monitor.calculate_file_hash')
    def test_find_duplicate_files_empty_directory(self, mock_calculate_hash, mock_os_walk, mock_islink, mock_isdir):
        # Mock rationale: Simulating an empty directory to ensure no duplicates are found.
        mock_os_walk.return_value = [
            ('/root', [], [])
        ]
        duplicates = find_duplicate_files('/root')
        self.assertEqual(duplicates, {})
        self.assertEqual(mock_calculate_hash.call_count, 0)

    @patch('os.path.isdir', return_value=False)
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_invalid_directory(self, mock_islink, mock_isdir):
        # Mock rationale: Testing the error handling for a non-existent directory.
        duplicates = find_duplicate_files('/nonexistent')
        self.assertEqual(duplicates, {})

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.islink', return_value=True) # Mock symlink
    @patch('os.walk')
    @patch('src.monitor.calculate_file_hash')
    def test_find_duplicate_files_skips_symlinks(self, mock_calculate_hash, mock_os_walk, mock_islink, mock_isdir):
        # Mock rationale: Ensure symlinks are skipped to prevent infinite loops or incorrect hash calculations.
        mock_os_walk.return_value = [
            ('/root', [], ['real_file.txt', 'symlink_file.txt'])
        ]
        
        # Only real_file.txt should be hashed
        mock_calculate_hash.side_effect = [
            self._mock_hash('real content') # /root/real_file.txt
        ]

        duplicates = find_duplicate_files('/root')
        self.assertEqual(duplicates, {})
        # calculate_file_hash should only be called for 'real_file.txt'
        self.assertEqual(mock_calculate_hash.call_count, 1)
        self.assertIn(os.path.join('/root', 'real_file.txt'), mock_calculate_hash.call_args[0][0])

if __name__ == '__main__':
    unittest.main()
