import unittest
import os
import hashlib
from unittest.mock import patch, mock_open, MagicMock
from collections import defaultdict
import sys

# Add the src directory to the path to allow importing echo_locator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from echo_locator import calculate_file_hash, find_duplicate_files, main

class TestEchoLocator(unittest.TestCase):

    def setUp(self):
        # Reset sys.argv for each test
        self._original_argv = sys.argv
        sys.argv = [self._original_argv[0]] # Keep script name

    def tearDown(self):
        sys.argv = self._original_argv

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_success(self, mock_file_open):
        # Mock rationale: We need to simulate reading file content to calculate its hash
        # without actually touching the filesystem.
        mock_file_open.return_value.read.side_effect = [b"test content", b""]
        expected_hash = hashlib.sha256(b"test content").hexdigest()
        self.assertEqual(calculate_file_hash("dummy_path.txt"), expected_hash)
        mock_file_open.assert_called_once_with("dummy_path.txt", 'rb')

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_calculate_file_hash_io_error(self, mock_file_open):
        # Mock rationale: Simulate a file that cannot be opened or read due to permissions
        # or other I/O issues, ensuring the function handles it gracefully.
        self.assertIsNone(calculate_file_hash("unreadable_path.txt"))
        mock_file_open.assert_called_once_with("unreadable_path.txt", 'rb')

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', side_effect=lambda p: p in ['/path/to/fileA.txt', '/path/to/fileB.txt'])
    @patch('os.walk')
    @patch('os.path.getsize', side_effect=lambda p: 100 if 'fileA' in p or 'file1' in p or 'file3' in p else 200)
    @patch('echo_locator.calculate_file_hash', side_effect=[
        'hash1', # /path/to/dir1/file1.txt
        'hash2', # /path/to/dir1/file2.txt
        'hash1', # /path/to/dir2/file3.txt (duplicate of file1)
        'hash3', # /path/to/dir2/file4.txt
        'hash4', # /path/to/fileA.txt
        'hash4', # /path/to/fileB.txt (duplicate of fileA)
    ])
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_multiple_paths(self, mock_islink, mock_calculate_hash, mock_getsize, mock_walk, mock_isfile, mock_exists):
        # Mock rationale: Simulate a file system structure with multiple directories and files,
        # including some duplicates, without creating actual files.
        # os.walk: Simulates directory traversal.
        # os.path.getsize: Provides file sizes for reporting.
        # calculate_file_hash: Provides pre-determined hashes to control duplicate detection.
        # os.path.exists: Ensures paths are considered valid.
        # os.path.isfile: Distinguishes between files and directories.
        # os.path.islink: Prevents symlink traversal issues.

        mock_walk.side_effect = [
            [
                ('/path/to/dir1', [], ['file1.txt', 'file2.txt']),
            ],
            [
                ('/path/to/dir2', [], ['file3.txt', 'file4.txt']),
            ]
        ]

        paths = ['/path/to/dir1', '/path/to/dir2', '/path/to/fileA.txt', '/path/to/fileB.txt']
        duplicates = find_duplicate_files(paths)

        expected_duplicates = {
            'hash1': {'size': 100, 'files': ['/path/to/dir1/file1.txt', '/path/to/dir2/file3.txt']},
            'hash4': {'size': 100, 'files': ['/path/to/fileA.txt', '/path/to/fileB.txt']}
        }

        self.assertEqual(len(duplicates), 2)
        self.assertIn('hash1', duplicates)
        self.assertIn('hash4', duplicates)

        # Sort files lists for consistent comparison
        self.assertEqual(sorted(duplicates['hash1']['files']), sorted(expected_duplicates['hash1']['files']))
        self.assertEqual(duplicates['hash1']['size'], expected_duplicates['hash1']['size'])
        self.assertEqual(sorted(duplicates['hash4']['files']), sorted(expected_duplicates['hash4']['files']))
        self.assertEqual(duplicates['hash4']['size'], expected_duplicates['hash4']['size'])

    @patch('os.path.exists', return_value=False)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_find_duplicate_files_path_not_found(self, mock_stderr, mock_exists):
        # Mock rationale: Simulate a non-existent path being passed to the function
        # and verify that a warning is printed to stderr.
        paths = ['/nonexistent/path']
        duplicates = find_duplicate_files(paths)
        self.assertEqual(duplicates, {})
        mock_stderr.write.assert_called_with("Warning: Path not found - /nonexistent/path\n")

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=False) # All paths are directories
    @patch('os.walk', return_value=[]) # No files found
    def test_find_duplicate_files_no_files(self, mock_walk, mock_isfile, mock_exists):
        # Mock rationale: Simulate a scenario where the given paths exist but contain no files,
        # ensuring the function correctly reports no duplicates.
        paths = ['/empty/dir']
        duplicates = find_duplicate_files(paths)
        self.assertEqual(duplicates, {})

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=False)
    @patch('os.walk', side_effect=[
        [('/path/to/dir', [], ['file1.txt', 'file2.txt'])],
    ])
    @patch('os.path.getsize', return_value=100)
    @patch('echo_locator.calculate_file_hash', side_effect=['hash_unique_1', 'hash_unique_2'])
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_no_duplicates(self, mock_islink, mock_calculate_hash, mock_getsize, mock_walk, mock_isfile, mock_exists):
        # Mock rationale: Simulate a directory with unique files, verifying no duplicates are reported.
        paths = ['/path/to/dir']
        duplicates = find_duplicate_files(paths)
        self.assertEqual(duplicates, {})

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('echo_locator.find_duplicate_files', return_value={
        'hash1': {'size': 123, 'files': ['/a/file1.txt', '/b/file2.txt']},
        'hash2': {'size': 456, 'files': ['/c/file3.txt', '/d/file4.txt', '/e/file5.txt']}
    })
    def test_main_duplicates_found(self, mock_find_duplicates, mock_stderr, mock_stdout):
        # Mock rationale: Test the main function's output when duplicates are found.
        # find_duplicate_files: Provides a controlled set of duplicate data.
        # sys.stdout: Captures printed output to verify the report format.
        sys.argv.extend(['/test/path'])
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0) # Should exit with 0 on success
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)

        self.assertIn("--- Duplicate Files Report ---", output)
        self.assertIn("--- Duplicate Group (SHA256: hash1) ---", output)
        self.assertIn("  Size: 123 bytes", output)
        self.assertIn("  - /a/file1.txt", output)
        self.assertIn("  - /b/file2.txt", output)
        self.assertIn("--- Duplicate Group (SHA256: hash2) ---", output)
        self.assertIn("  Size: 456 bytes", output)
        self.assertIn("  - /c/file3.txt", output)
        self.assertIn("  - /d/file4.txt", output)
        self.assertIn("  - /e/file5.txt", output)
        self.assertIn("--- End of Report ---", output)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('echo_locator.find_duplicate_files', return_value={})
    def test_main_no_duplicates_found(self, mock_find_duplicates, mock_stderr, mock_stdout):
        # Mock rationale: Test the main function's output when no duplicates are found.
        # find_duplicate_files: Provides an empty set of duplicate data.
        # sys.stdout: Captures printed output to verify the "no duplicates" message.
        sys.argv.extend(['/test/path'])
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0) # Should exit with 0 on success
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        self.assertIn("No duplicate files found. Your digital wasteland is pristine!", output)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('echo_locator.find_duplicate_files', return_value={}) # Not strictly needed but good practice
    def test_main_no_args(self, mock_find_duplicates, mock_stderr, mock_stdout):
        # Mock rationale: Test the main function's behavior when no command-line arguments are provided.
        # sys.stdout/stderr: Captures output to verify the usage message.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1) # Should exit with 1 on error
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        self.assertIn("Usage: python src/echo_locator.py <path1> [path2 ...]", output)

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=False)
    @patch('os.walk', side_effect=[
        [('/path/to/dir', [], ['file1.txt'])],
    ])
    @patch('os.path.getsize', return_value=100)
    @patch('echo_locator.calculate_file_hash', side_effect=OSError("Disk full"))
    @patch('os.path.islink', return_value=False)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_find_duplicate_files_os_error_accessing_file(self, mock_stderr, mock_islink, mock_calculate_hash, mock_getsize, mock_walk, mock_isfile, mock_exists):
        # Mock rationale: Simulate an OSError during file access (e.g., permissions, disk error)
        # and ensure it's caught and reported to stderr without crashing.
        paths = ['/path/to/dir']
        duplicates = find_duplicate_files(paths)
        self.assertEqual(duplicates, {})
        mock_stderr.write.assert_called_with("Error accessing file /path/to/dir/file1.txt: Disk full\n")


if __name__ == '__main__':
    unittest.main()
