import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import hashlib

# Import functions from the duster module
from src.duster import find_duplicate_files, remove_duplicate_files, calculate_file_hash

class TestDataDustbinDuster(unittest.TestCase):

    # Mock rationale: We need to simulate file system traversal and file content
    # without actually creating files or performing disk I/O for deterministic,
    # offline testing. `os.walk` is mocked to control the directory structure,
    # and `open` is mocked to provide specific file contents for hash calculation.

    @patch('src.duster.open', new_callable=mock_open)
    @patch('src.duster.os.walk')
    def test_find_duplicate_files_no_duplicates(self, mock_os_walk, mock_file_open):
        # Mock rationale: Simulate a directory with unique files.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.txt']),
        ]
        # Mock rationale: Provide distinct content for each file to ensure unique hashes.
        mock_file_open.side_effect = [
            mock_open(read_data=b"content1").return_value, # file1.txt
            mock_open(read_data=b"content2").return_value, # file2.txt
        ]

        duplicates = find_duplicate_files('/test_dir')
        self.assertEqual(duplicates, {})
        self.assertEqual(mock_file_open.call_count, 2) # Ensure files were "opened"

    @patch('src.duster.open', new_callable=mock_open)
    @patch('src.duster.os.walk')
    def test_find_duplicate_files_with_duplicates(self, mock_os_walk, mock_file_open):
        # Mock rationale: Simulate a directory with duplicate files.
        mock_os_walk.return_value = [
            ('/test_dir', ['subdir'], ['fileA.txt', 'fileB.txt']),
            ('/test_dir/subdir', [], ['fileC.txt']),
        ]
        
        # Mock rationale: fileA.txt and fileC.txt have the same content, fileB.txt is unique.
        # We need to mock the 'read' method of the file handle returned by mock_open.
        mock_file_open.side_effect = [
            mock_open(read_data=b"duplicate_content").return_value, # fileA.txt
            mock_open(read_data=b"unique_content").return_value,    # fileB.txt
            mock_open(read_data=b"duplicate_content").return_value, # fileC.txt
        ]

        duplicates = find_duplicate_files('/test_dir')

        # Calculate expected hash for "duplicate_content" directly using hashlib for test determinism
        expected_hash_duplicate = hashlib.sha256(b"duplicate_content").hexdigest()
        
        expected_duplicates = {
            expected_hash_duplicate: [
                os.path.join('/test_dir', 'fileA.txt'),
                os.path.join('/test_dir/subdir', 'fileC.txt'),
            ]
        }
        self.assertEqual(duplicates, expected_duplicates)
        self.assertEqual(mock_file_open.call_count, 3)

    @patch('src.duster.os.remove')
    def test_remove_duplicate_files_dry_run(self, mock_os_remove):
        # Mock rationale: Test the dry_run functionality without actual file deletion.
        duplicates_map = {
            "hash123": ["/path/to/file1.txt", "/path/to/file1_copy.txt", "/path/to/another/file1.txt"],
            "hash456": ["/path/to/file2.txt", "/path/to/file2_copy.txt"],
        }
        
        removed = remove_duplicate_files(duplicates_map, dry_run=True)
        
        expected_removed = [
            "/path/to/file1_copy.txt",
            "/path/to/another/file1.txt",
            "/path/to/file2_copy.txt",
        ]
        self.assertCountEqual(removed, expected_removed)
        mock_os_remove.assert_not_called() # Ensure no deletion happened

    @patch('src.duster.os.remove')
    def test_remove_duplicate_files_actual_removal(self, mock_os_remove):
        # Mock rationale: Test actual file deletion by ensuring `os.remove` is called.
        duplicates_map = {
            "hash123": ["/path/to/file1.txt", "/path/to/file1_copy.txt", "/path/to/another/file1.txt"],
            "hash456": ["/path/to/file2.txt", "/path/to/file2_copy.txt"],
        }
        
        removed = remove_duplicate_files(duplicates_map, dry_run=False)
        
        expected_removed = [
            "/path/to/file1_copy.txt",
            "/path/to/another/file1.txt",
            "/path/to/file2_copy.txt",
        ]
        self.assertCountEqual(removed, expected_removed)
        
        # Verify os.remove was called for each duplicate
        self.assertEqual(mock_os_remove.call_count, len(expected_removed))
        mock_os_remove.assert_any_call("/path/to/file1_copy.txt")
        mock_os_remove.assert_any_call("/path/to/another/file1.txt")
        mock_os_remove.assert_any_call("/path/to/file2_copy.txt")

    @patch('src.duster.open', new_callable=mock_open)
    def test_calculate_file_hash(self, mock_file_open):
        # Mock rationale: Provide specific content to `open` to get a predictable hash.
        mock_file_open.return_value.read.side_effect = [b"test content", b""]
        
        # Calculate expected hash manually for verification
        expected_hash = hashlib.sha256(b"test content").hexdigest()
        
        actual_hash = calculate_file_hash("dummy_path.txt")
        self.assertEqual(actual_hash, expected_hash)
        mock_file_open.assert_called_once_with("dummy_path.txt", 'rb')

    @patch('src.duster.open', new_callable=mock_open)
    @patch('src.duster.os.walk')
    def test_find_duplicate_files_io_error(self, mock_os_walk, mock_file_open):
        # Mock rationale: Simulate a file that cannot be opened (e.g., permissions issue).
        mock_os_walk.return_value = [
            ('/test_dir', [], ['accessible.txt', 'inaccessible.txt']),
        ]
        # First file is accessible, second raises IOError
        mock_file_open.side_effect = [
            mock_open(read_data=b"accessible content").return_value, # accessible.txt
            MagicMock(side_effect=IOError("Permission denied")),     # inaccessible.txt
        ]

        duplicates = find_duplicate_files('/test_dir')
        self.assertEqual(duplicates, {}) # No duplicates, and inaccessible file is skipped
        self.assertEqual(mock_file_open.call_count, 2) # Both files were attempted to be opened

if __name__ == '__main__':
    unittest.main()
