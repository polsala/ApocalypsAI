import unittest
from unittest.mock import patch, mock_open
import os
import hashlib
from io import BytesIO

# Import the functions to be tested
from src.checksum_calculator import calculate_file_checksum, calculate_directory_checksums, CHUNK_SIZE

class TestChecksumCalculator(unittest.TestCase):

    def test_calculate_file_checksum_sha256(self):
        # Mock rationale: We need to simulate reading a file without actually creating one.
        # `mock_open` allows us to control the content returned by `open()`.
        file_content = b"This is a test file content for SHA256."
        expected_checksum = hashlib.sha256(file_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=file_content)) as m_open:
            checksum = calculate_file_checksum("dummy_file.txt", 'sha256')
            self.assertEqual(checksum, expected_checksum)
            m_open.assert_called_once_with("dummy_file.txt", 'rb')

    def test_calculate_file_checksum_md5(self):
        # Mock rationale: Similar to SHA256, simulate file content for MD5 calculation.
        file_content = b"Another test content for MD5 hashing."
        expected_checksum = hashlib.md5(file_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=file_content)) as m_open:
            checksum = calculate_file_checksum("another_dummy.bin", 'md5')
            self.assertEqual(checksum, expected_checksum)
            m_open.assert_called_once_with("another_dummy.bin", 'rb')

    def test_calculate_file_checksum_large_file(self):
        # Mock rationale: Test chunked reading for larger files.
        # Create content larger than CHUNK_SIZE.
        file_content = b"a" * (CHUNK_SIZE * 2 + 123) # Two full chunks + some bytes
        expected_checksum = hashlib.sha256(file_content).hexdigest()

        # Use BytesIO to simulate a file object that reads in chunks
        with patch('builtins.open', return_value=BytesIO(file_content)) as m_open:
            checksum = calculate_file_checksum("large_file.dat", 'sha256')
            self.assertEqual(checksum, expected_checksum)
            m_open.assert_called_once_with("large_file.dat", 'rb')

    def test_calculate_file_checksum_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError when trying to open a file.
        with patch('builtins.open', side_effect=FileNotFoundError) as m_open:
            checksum = calculate_file_checksum("non_existent.txt")
            self.assertIn("ERROR: File not found", checksum)
            m_open.assert_called_once_with("non_existent.txt", 'rb')

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.join', side_effect=os.path.join) # Ensure os.path.join works as expected
    @patch('builtins.print') # Mock print to prevent console output during test
    def test_calculate_directory_checksums(self, mock_print, mock_join, mock_isdir):
        # Mock rationale: Simulate a directory structure and file contents.
        # `os.walk` is mocked to control the directory traversal.
        # `builtins.open` is mocked to control file content.

        # Define mock directory structure
        mock_walk_data = [
            ('/mock_dir', ['subdir'], ['file1.txt', 'file2.log']),
            ('/mock_dir/subdir', [], ['subfile.py'])
        ]

        # Define mock file contents and their expected checksums
        file_contents = {
            '/mock_dir/file1.txt': b'content of file1',
            '/mock_dir/file2.log': b'log data here',
            '/mock_dir/subdir/subfile.py': b'import os\nprint("hello")'
        }
        expected_checksums = {
            path: hashlib.sha256(content).hexdigest()
            for path, content in file_contents.items()
        }

        def mock_open_side_effect(filepath, mode):
            if mode == 'rb' and filepath in file_contents:
                return BytesIO(file_contents[filepath])
            raise FileNotFoundError(f"Mock file not found: {filepath}")

        with patch('os.walk', return_value=mock_walk_data),
             patch('builtins.open', side_effect=mock_open_side_effect):

            results = calculate_directory_checksums('/mock_dir', 'sha256')

            self.assertEqual(len(results), 3)
            self.assertDictEqual(results, expected_checksums)
            mock_isdir.assert_called_once_with('/mock_dir')
            # Verify print calls for summary
            mock_print.assert_any_call('Summary: 3 files processed.')

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    def test_calculate_directory_checksums_not_a_directory(self, mock_print, mock_isdir):
        # Mock rationale: Simulate a path that is not a directory.
        results = calculate_directory_checksums('/not_a_dir')
        self.assertIn('/not_a_dir', results)
        self.assertIn('ERROR: Not a directory', results['/not_a_dir'])
        mock_isdir.assert_called_once_with('/not_a_dir')
        mock_print.assert_not_called() # No files processed, so no print output beyond error

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/empty_dir', [], [])])
    @patch('builtins.print')
    def test_calculate_directory_checksums_empty_directory(self, mock_print, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory.
        results = calculate_directory_checksums('/empty_dir')
        self.assertEqual(len(results), 0)
        self.assertDictEqual(results, {})
        mock_isdir.assert_called_once_with('/empty_dir')
        mock_print.assert_any_call('Summary: 0 files processed.')

if __name__ == '__main__':
    unittest.main()
