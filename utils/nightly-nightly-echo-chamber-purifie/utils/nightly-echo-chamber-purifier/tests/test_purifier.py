import unittest
import os
import hashlib
from unittest.mock import patch, mock_open
from collections import defaultdict

# Import the functions to be tested
from src.purifier import calculate_file_hash, find_duplicate_files

class TestPurifier(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_success(self, mock_file_open):
        # Mock rationale: Simulate file content without actual disk I/O.
        # This ensures deterministic tests and avoids side effects.
        mock_file_open.return_value.read.side_effect = [b"hello", b" world", b""]
        expected_hash = hashlib.sha256(b"hello world").hexdigest()
        self.assertEqual(calculate_file_hash("dummy_path.txt"), expected_hash)
        mock_file_open.assert_called_with("dummy_path.txt", 'rb')

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_calculate_file_hash_io_error(self, mock_file_open):
        # Mock rationale: Simulate a file that cannot be read due to permissions or other I/O errors.
        # This tests error handling without needing to create unreadable files.
        self.assertIsNone(calculate_file_hash("unreadable_path.txt"))
        mock_file_open.assert_called_with("unreadable_path.txt", 'rb')

    @patch('os.path.isfile', return_value=True)
    @patch('os.path.isdir', return_value=False)
    @patch('src.purifier.calculate_file_hash')
    def test_find_duplicate_files_single_file(self, mock_calculate_hash, mock_isdir, mock_isfile):
        # Mock rationale: Simulate a single file path.
        # `os.path.isfile` and `os.path.isdir` are mocked to control path type.
        # `calculate_file_hash` is mocked to provide predictable hash values.
        mock_calculate_hash.return_value = "hash1"
        result = find_duplicate_files(["/path/to/file1.txt"])
        self.assertEqual(result, {}) # No duplicates if only one file
        mock_calculate_hash.assert_called_with("/path/to/file1.txt")

    @patch('os.path.isfile', side_effect=[True, True])
    @patch('os.path.isdir', return_value=False)
    @patch('src.purifier.calculate_file_hash', side_effect=["hash1", "hash1"])
    def test_find_duplicate_files_two_identical_files(self, mock_calculate_hash, mock_isdir, mock_isfile):
        # Mock rationale: Simulate two distinct file paths that resolve to the same hash.
        # This tests the core duplicate detection logic.
        paths = ["/path/to/file1.txt", "/path/to/file2.txt"]
        result = find_duplicate_files(paths)
        expected = {"hash1": ["/path/to/file1.txt", "/path/to/file2.txt"]}
        self.assertEqual(result, expected)
        mock_calculate_hash.assert_any_call("/path/to/file1.txt")
        mock_calculate_hash.assert_any_call("/path/to/file2.txt")

    @patch('os.path.isfile', side_effect=[True, True])
    @patch('os.path.isdir', return_value=False)
    @patch('src.purifier.calculate_file_hash', side_effect=["hash1", "hash2"])
    def test_find_duplicate_files_two_different_files(self, mock_calculate_hash, mock_isdir, mock_isfile):
        # Mock rationale: Simulate two distinct file paths with different hashes.
        # Ensures that non-duplicates are correctly ignored.
        paths = ["/path/to/file1.txt", "/path/to/file2.txt"]
        result = find_duplicate_files(paths)
        self.assertEqual(result, {})
        mock_calculate_hash.assert_any_call("/path/to/file1.txt")
        mock_calculate_hash.assert_any_call("/path/to/file2.txt")

    @patch('os.path.isfile', return_value=False)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('src.purifier.calculate_file_hash', side_effect=["hashA", "hashB", "hashA", "hashC"])
    @patch('os.path.exists', return_value=True) # Assume files exist
    @patch('os.path.islink', return_value=False) # Assume not symlinks
    def test_find_duplicate_files_directory_scan(self, mock_islink, mock_exists, mock_calculate_hash, mock_walk, mock_isdir, mock_isfile):
        # Mock rationale: Simulate a directory structure using `os.walk`.
        # This allows testing recursive scanning without creating a real directory tree.
        mock_walk.return_value = [
            ('/dir1', [], ['file1.txt', 'file2.txt']),
            ('/dir1/subdir', [], ['file3.txt', 'file4.txt'])
        ]
        paths = ["/dir1"]
        result = find_duplicate_files(paths)
        expected = {"hashA": ["/dir1/file1.txt", "/dir1/subdir/file3.txt"]}
        self.assertEqual(result, expected)
        mock_calculate_hash.assert_any_call("/dir1/file1.txt")
        mock_calculate_hash.assert_any_call("/dir1/file2.txt")
        mock_calculate_hash.assert_any_call("/dir1/subdir/file3.txt")
        mock_calculate_hash.assert_any_call("/dir1/subdir/file4.txt")

    @patch('os.path.isfile', return_value=False)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('src.purifier.calculate_file_hash', side_effect=["hashA", None, "hashA"]) # One file unreadable
    @patch('os.path.exists', return_value=True)
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_directory_with_unreadable_file(self, mock_islink, mock_exists, mock_calculate_hash, mock_walk, mock_isdir, mock_isfile):
        # Mock rationale: Simulate a directory containing an unreadable file.
        # Ensures that unreadable files (where hash calculation returns None) are skipped.
        mock_walk.return_value = [
            ('/dir1', [], ['file1.txt', 'unreadable.txt', 'file2.txt'])
        ]
        paths = ["/dir1"]
        result = find_duplicate_files(paths)
        expected = {"hashA": ["/dir1/file1.txt", "/dir1/file2.txt"]}
        self.assertEqual(result, expected)
        mock_calculate_hash.assert_any_call("/dir1/file1.txt")
        mock_calculate_hash.assert_any_call("/dir1/unreadable.txt")
        mock_calculate_hash.assert_any_call("/dir1/file2.txt")

    @patch('os.path.isfile', return_value=False)
    @patch('os.path.isdir', return_value=False) # Neither file nor dir
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_find_duplicate_files_invalid_path(self, mock_stderr, mock_isdir, mock_isfile):
        # Mock rationale: Simulate an invalid path (neither file nor directory).
        # Checks if the warning message is printed to stderr.
        paths = ["/invalid/path"]
        result = find_duplicate_files(paths)
        self.assertEqual(result, {})
        self.assertIn("Warning: Path '/invalid/path' is not a valid file or directory. Skipping.", mock_stderr.getvalue())

    @patch('sys.argv', ['src/purifier.py', '/path/to/dir1', '/path/to/dir2'])
    @patch('src.purifier.find_duplicate_files', return_value={
        "hash1": ["/path/to/dir1/fileA.txt", "/path/to/dir2/fileA_copy.txt"],
        "hash2": ["/path/to/dir1/fileB.txt", "/path/to/dir1/subdir/fileB.txt"]
    })
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_with_duplicates(self, mock_exit, mock_print, mock_find_duplicates):
        # Mock rationale: Test the main execution flow when duplicates are found.
        # `sys.argv` is mocked to provide command-line arguments.
        # `find_duplicate_files` is mocked to return a predefined set of duplicates.
        # `print` and `sys.exit` are mocked to capture output and prevent actual exit.
        from src.purifier import main
        main()
        mock_find_duplicates.assert_called_with(['/path/to/dir1', '/path/to/dir2'])
        mock_print.assert_any_call("--- Duplicate Files Found ---")
        mock_print.assert_any_call("\nDuplicate Group (SHA256: hash1)")
        mock_print.assert_any_call("  - /path/to/dir1/fileA.txt")
        mock_print.assert_any_call("  - /path/to/dir2/fileA_copy.txt")
        mock_print.assert_any_call("\nDuplicate Group (SHA256: hash2)")
        mock_print.assert_any_call("  - /path/to/dir1/fileB.txt")
        mock_print.assert_any_call("  - /path/to/dir1/subdir/fileB.txt")
        mock_exit.assert_called_with(0)

    @patch('sys.argv', ['src/purifier.py', '/path/to/dir'])
    @patch('src.purifier.find_duplicate_files', return_value={})
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_duplicates(self, mock_exit, mock_print, mock_find_duplicates):
        # Mock rationale: Test the main execution flow when no duplicates are found.
        from src.purifier import main
        main()
        mock_find_duplicates.assert_called_with(['/path/to/dir'])
        mock_print.assert_called_with("No duplicate files found. Your digital echo chamber is pristine!")
        mock_exit.assert_called_with(0)

    @patch('sys.argv', ['src/purifier.py'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_arguments(self, mock_exit, mock_print):
        # Mock rationale: Test the main execution flow when no arguments are provided.
        from src.purifier import main
        main()
        mock_print.assert_called_with("Usage: python src/purifier.py <directory1> [directory2 ...]")
        mock_exit.assert_called_with(1)
