import unittest
import os
import hashlib
from unittest.mock import patch, mock_open
from src.resonator import calculate_file_hash, find_duplicate_files

# Mock rationale: We need to simulate file system operations (os.walk, open)
# and file content without actually creating files on disk. This ensures
# the tests are deterministic, fast, and don't leave artifacts.

class TestResonator(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_basic(self, mock_file_open):
        # Mock rationale: Simulate reading a file with known content.
        mock_file_open.return_value.read.side_effect = [b"hello world", b""]
        expected_hash = hashlib.md5(b"hello world").hexdigest()
        self.assertEqual(calculate_file_hash("dummy_path.txt", 'md5'), expected_hash)
        mock_file_open.assert_called_once_with("dummy_path.txt", 'rb')

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_empty_file(self, mock_file_open):
        # Mock rationale: Simulate reading an empty file.
        mock_file_open.return_value.read.side_effect = [b""]
        expected_hash = hashlib.md5(b"").hexdigest()
        self.assertEqual(calculate_file_hash("empty.txt", 'md5'), expected_hash)

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_different_algo(self, mock_file_open):
        # Mock rationale: Simulate reading a file and using a different hash algorithm.
        mock_file_open.return_value.read.side_effect = [b"test content", b""]
        expected_hash = hashlib.sha256(b"test content").hexdigest()
        self.assertEqual(calculate_file_hash("dummy.txt", 'sha256'), expected_hash)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_calculate_file_hash_file_not_found(self, mock_file_open):
        # Mock rationale: Simulate a FileNotFoundError when trying to open a file.
        self.assertIsNone(calculate_file_hash("non_existent.txt", 'md5'))

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicate_files_no_duplicates(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory structure with unique files.
        mock_os_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt']),
        ]
        # Mock rationale: Provide distinct content for each file.
        file_contents = {
            '/root/file1.txt': b"content A",
            '/root/file2.txt': b"content B",
        }
        def mock_open_side_effect(filepath, mode):
            if mode == 'rb':
                m = mock_open(read_data=file_contents.get(filepath, b''))
                return m.return_value
            raise ValueError(f"Unexpected mode: {mode}")
        mock_file_open.side_effect = mock_open_side_effect

        duplicates = find_duplicate_files('/root', 'md5')
        self.assertEqual(duplicates, {})

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicate_files_with_duplicates(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory structure with duplicate files.
        mock_os_walk.return_value = [
            ('/root', ['subdir'], ['fileA.txt', 'fileB.txt']),
            ('/root/subdir', [], ['fileC.txt']),
        ]
        # Mock rationale: Provide content such that fileA and fileC are duplicates.
        file_contents = {
            '/root/fileA.txt': b"duplicate content",
            '/root/fileB.txt': b"unique content",
            '/root/subdir/fileC.txt': b"duplicate content",
        }
        def mock_open_side_effect(filepath, mode):
            if mode == 'rb':
                m = mock_open(read_data=file_contents.get(filepath, b''))
                return m.return_value
            raise ValueError(f"Unexpected mode: {mode}")
        mock_file_open.side_effect = mock_open_side_effect

        expected_hash = hashlib.md5(b"duplicate content").hexdigest()
        duplicates = find_duplicate_files('/root', 'md5')

        self.assertIn(expected_hash, duplicates)
        self.assertCountEqual(duplicates[expected_hash], ['/root/fileA.txt', '/root/subdir/fileC.txt'])
        self.assertEqual(len(duplicates), 1) # Only one set of duplicates

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicate_files_empty_directory(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate an empty directory.
        mock_os_walk.return_value = [
            ('/root', [], []),
        ]
        duplicates = find_duplicate_files('/root', 'md5')
        self.assertEqual(duplicates, {})
        mock_file_open.assert_not_called() # No files to open

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicate_files_with_multiple_duplicate_sets(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate multiple sets of duplicate files.
        mock_os_walk.return_value = [
            ('/root', [], ['f1.txt', 'f2.txt', 'f3.txt', 'f4.txt']),
        ]
        file_contents = {
            '/root/f1.txt': b"content X",
            '/root/f2.txt': b"content Y",
            '/root/f3.txt': b"content X", # Duplicate of f1
            '/root/f4.txt': b"content Y", # Duplicate of f2
        }
        def mock_open_side_effect(filepath, mode):
            if mode == 'rb':
                m = mock_open(read_data=file_contents.get(filepath, b''))
                return m.return_value
            raise ValueError(f"Unexpected mode: {mode}")
        mock_file_open.side_effect = mock_open_side_effect

        hash_x = hashlib.md5(b"content X").hexdigest()
        hash_y = hashlib.md5(b"content Y").hexdigest()

        duplicates = find_duplicate_files('/root', 'md5')

        self.assertEqual(len(duplicates), 2)
        self.assertIn(hash_x, duplicates)
        self.assertIn(hash_y, duplicates)
        self.assertCountEqual(duplicates[hash_x], ['/root/f1.txt', '/root/f3.txt'])
        self.assertCountEqual(duplicates[hash_y], ['/root/f2.txt', '/root/f4.txt'])

if __name__ == '__main__':
    unittest.main()
