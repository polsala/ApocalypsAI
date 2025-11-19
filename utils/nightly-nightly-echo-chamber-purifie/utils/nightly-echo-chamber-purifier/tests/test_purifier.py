import unittest
from unittest.mock import patch, mock_open
import os
import hashlib
from src.purifier import calculate_file_hash, find_duplicates

class TestPurifier(unittest.TestCase):

    def test_calculate_file_hash_basic(self):
        # Mock rationale: Simulate file content without creating actual files.
        # This ensures determinism and isolation from the file system.
        mock_file_content = b"This is some test content."
        expected_hash = hashlib.sha256(mock_file_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            hash_result = calculate_file_hash("dummy_path.txt")
            self.assertEqual(hash_result, expected_hash)
            m_open.assert_called_once_with("dummy_path.txt", 'rb')

    def test_calculate_file_hash_empty_file(self):
        # Mock rationale: Test edge case of an empty file.
        mock_file_content = b""
        expected_hash = hashlib.sha256(mock_file_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            hash_result = calculate_file_hash("empty.txt")
            self.assertEqual(hash_result, expected_hash)

    def test_calculate_file_hash_io_error(self):
        # Mock rationale: Simulate a file read error.
        with patch('builtins.open', side_effect=IOError("Permission denied")) as m_open:
            hash_result = calculate_file_hash("unreadable.txt")
            self.assertIsNone(hash_result)
            m_open.assert_called_once_with("unreadable.txt", 'rb')

    @patch('os.path.islink', return_value=False)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    def test_find_duplicates_no_duplicates(self, mock_os_walk, mock_isdir, mock_islink):
        # Mock rationale: Simulate a directory structure with unique files.
        # os.walk is mocked to control the file system traversal without actual disk access.
        # builtins.open is mocked to provide specific content for each file path.
        mock_os_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt']),
            ('/root/subdir', [], ['file3.txt'])
        ]

        file_contents = {
            '/root/file1.txt': b'content1',
            '/root/file2.txt': b'content2',
            '/root/subdir/file3.txt': b'content3'
        }

        def mock_open_side_effect(filepath, mode):
            if mode == 'rb' and filepath in file_contents:
                return mock_open(read_data=file_contents[filepath]).return_value
            raise FileNotFoundError(f"File not found: {filepath}")

        with patch('builtins.open', side_effect=mock_open_side_effect):
            duplicates = find_duplicates('/root')
            self.assertEqual(duplicates, {})

    @patch('os.path.islink', return_value=False)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    def test_find_duplicates_with_duplicates(self, mock_os_walk, mock_isdir, mock_islink):
        # Mock rationale: Simulate a directory structure with duplicate files.
        # This allows testing the core logic of identifying and grouping duplicates.
        mock_os_walk.return_value = [
            ('/root', [], ['a.txt', 'b.txt']),
            ('/root/subdir', [], ['c.txt', 'd.txt'])
        ]

        file_contents = {
            '/root/a.txt': b'duplicate_content_1',
            '/root/b.txt': b'unique_content',
            '/root/subdir/c.txt': b'duplicate_content_1',
            '/root/subdir/d.txt': b'duplicate_content_2'
        }

        def mock_open_side_effect(filepath, mode):
            if mode == 'rb' and filepath in file_contents:
                return mock_open(read_data=file_contents[filepath]).return_value
            raise FileNotFoundError(f"File not found: {filepath}")

        with patch('builtins.open', side_effect=mock_open_side_effect):
            duplicates = find_duplicates('/root')

            hash1 = hashlib.sha256(b'duplicate_content_1').hexdigest()
            hash2 = hashlib.sha256(b'duplicate_content_2').hexdigest()

            expected_duplicates = {
                hash1: ['/root/a.txt', '/root/subdir/c.txt'],
                hash2: ['/root/subdir/d.txt'] # This should not be a duplicate group as it only has one file
            }
            # Filter out groups with only one file, as find_duplicates should do this implicitly
            expected_duplicates = {h: paths for h, paths in expected_duplicates.items() if len(paths) > 1}

            self.assertIn(hash1, duplicates)
            self.assertCountEqual(duplicates[hash1], ['/root/a.txt', '/root/subdir/c.txt'])
            self.assertNotIn(hash2, duplicates) # Should not be in duplicates as it's a single file
            self.assertEqual(len(duplicates), 1)

    @patch('os.path.islink', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    def test_find_duplicates_skips_symlinks(self, mock_os_walk, mock_isdir, mock_islink):
        # Mock rationale: Ensure symbolic links are skipped to prevent infinite loops or incorrect hashing.
        mock_os_walk.return_value = [
            ('/root', [], ['link_to_file.txt'])
        ]
        with patch('builtins.open') as m_open:
            duplicates = find_duplicates('/root')
            self.assertEqual(duplicates, {})
            m_open.assert_not_called() # open should not be called for a symlink

    @patch('os.path.isdir', return_value=False)
    def test_find_duplicates_invalid_directory(self, mock_isdir):
        # Mock rationale: Test behavior when the provided directory does not exist.
        duplicates = find_duplicates('/nonexistent')
        self.assertEqual(duplicates, {})

if __name__ == '__main__':
    unittest.main()
