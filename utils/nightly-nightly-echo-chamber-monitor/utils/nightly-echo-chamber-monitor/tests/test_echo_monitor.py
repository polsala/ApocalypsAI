import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import hashlib
import sys

# Import the functions to be tested
from src.echo_monitor import calculate_file_hash, find_duplicate_files, main

class TestEchoMonitor(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.md5')
    def test_calculate_file_hash(self, mock_md5, mock_open_func):
        # Mock rationale: Simulate file content and hash calculation without actual file I/O.
        # This ensures determinism and offline execution.

        mock_file_content = b"test content"
        mock_open_func.return_value.read.side_effect = [mock_file_content, b""] # First read returns content, second returns empty for EOF

        mock_hasher_instance = MagicMock()
        mock_hasher_instance.hexdigest.return_value = "mocked_hash_value"
        mock_md5.return_value = mock_hasher_instance

        filepath = "/mock/path/to/file.txt"
        result_hash = calculate_file_hash(filepath)

        mock_open_func.assert_called_once_with(filepath, 'rb')
        mock_hasher_instance.update.assert_called_once_with(mock_file_content)
        mock_hasher_instance.hexdigest.assert_called_once()
        self.assertEqual(result_hash, "mocked_hash_value")

    @patch('src.echo_monitor.calculate_file_hash') # Mock calculate_file_hash directly
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    def test_find_duplicate_files_no_duplicates(self, mock_os_walk, mock_isfile, mock_calculate_hash):
        # Mock rationale: Simulate a file system with unique files by controlling hash outputs.
        # This isolates the duplicate finding logic from hash calculation details.

        mock_os_walk.return_value = [
            ('/mock/dir1', [], ['fileA.txt', 'fileB.txt'])
        ]

        # Define specific hashes for specific files
        mock_calculate_hash.side_effect = lambda f: {
            '/mock/dir1/fileA.txt': 'hash_A',
            '/mock/dir1/fileB.txt': 'hash_B',
        }.get(f)

        duplicates = find_duplicate_files(['/mock/dir1'])
        self.assertEqual(duplicates, {})
        mock_calculate_hash.assert_any_call('/mock/dir1/fileA.txt')
        mock_calculate_hash.assert_any_call('/mock/dir1/fileB.txt')

    @patch('src.echo_monitor.calculate_file_hash') # Mock calculate_file_hash directly
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    def test_find_duplicate_files_with_duplicates(self, mock_os_walk, mock_isfile, mock_calculate_hash):
        # Mock rationale: Simulate a file system with duplicate files by controlling hash outputs.
        # This isolates the duplicate finding logic from hash calculation details.

        mock_os_walk.return_value = [
            ('/mock/dir1', [], ['file1.txt', 'file2.txt']),
            ('/mock/dir2', [], ['file3.txt', 'unique.txt'])
        ]

        # Define specific hashes for specific files, creating duplicates
        mock_calculate_hash.side_effect = lambda f: {
            '/mock/dir1/file1.txt': 'hash_duplicate',
            '/mock/dir1/file2.txt': 'hash_duplicate',
            '/mock/dir2/file3.txt': 'hash_duplicate',
            '/mock/dir2/unique.txt': 'hash_unique',
        }.get(f)

        duplicates = find_duplicate_files(['/mock/dir1', '/mock/dir2'])
        
        expected_duplicates = {
            "hash_duplicate": [
                '/mock/dir1/file1.txt',
                '/mock/dir1/file2.txt',
                '/mock/dir2/file3.txt'
            ]
        }
        # Sort lists for consistent comparison
        for k in expected_duplicates:
            expected_duplicates[k].sort()
        for k in duplicates:
            duplicates[k].sort()

        self.assertEqual(duplicates, expected_duplicates)
        self.assertNotIn("hash_unique", duplicates) # Ensure unique files are not reported
        mock_calculate_hash.assert_any_call('/mock/dir1/file1.txt')
        mock_calculate_hash.assert_any_call('/mock/dir1/file2.txt')
        mock_calculate_hash.assert_any_call('/mock/dir2/file3.txt')
        mock_calculate_hash.assert_any_call('/mock/dir2/unique.txt')

    @patch('os.path.exists', return_value=False)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_find_duplicate_files_invalid_path(self, mock_stderr, mock_exists):
        # Mock rationale: Test handling of non-existent input paths without actual file system checks.
        # This ensures robustness for invalid user input.
        duplicates = find_duplicate_files(['/nonexistent/path'])
        self.assertEqual(duplicates, {})
        mock_stderr.write.assert_called_with("Warning: Path '/nonexistent/path' does not exist. Skipping.\n")

    @patch('src.echo_monitor.find_duplicate_files')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_with_duplicates(self, mock_exit, mock_stderr, mock_stdout, mock_find_duplicates):
        # Mock rationale: Test the main execution flow when duplicates are found.
        # This verifies correct output formatting and exit code.
        mock_find_duplicates.return_value = {
            "hash123": ["/path/to/fileA.txt", "/path/to/fileB.txt"]
        }
        
        # Mock argparse to simulate command-line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(paths=['/mock/dir'])):
            main()
        
        mock_find_duplicates.assert_called_once_with(['/mock/dir'])
        mock_stdout.write.assert_any_call("Scanning for duplicate files...\n")
        mock_stdout.write.assert_any_call("\n--- Duplicate Files Found ---\n")
        mock_stdout.write.assert_any_call("Hash: hash123\n")
        mock_stdout.write.assert_any_call("  - /path/to/fileA.txt\n")
        mock_stdout.write.assert_any_call("  - /path/to/fileB.txt\n")
        mock_stdout.write.assert_any_call("\n--- End of Duplicates ---\n")
        mock_exit.assert_called_once_with(0)

    @patch('src.echo_monitor.find_duplicate_files')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_no_duplicates(self, mock_exit, mock_stderr, mock_stdout, mock_find_duplicates):
        # Mock rationale: Test the main execution flow when no duplicates are found.
        # This verifies correct output and exit code for the no-op scenario.
        mock_find_duplicates.return_value = {}

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(paths=['/mock/dir'])):
            main()

        mock_find_duplicates.assert_called_once_with(['/mock/dir'])
        mock_stdout.write.assert_any_call("Scanning for duplicate files...\n")
        mock_stdout.write.assert_any_call("\nNo duplicate files found.\n")
        mock_exit.assert_called_once_with(2)

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk', return_value=[('/mock/dir', [], ['file.txt'])])
    @patch('sys.stderr', new_callable=MagicMock)
    def test_calculate_file_hash_io_error(self, mock_stderr, mock_os_walk, mock_isfile, mock_open_func):
        # Mock rationale: Simulate an IOError during file reading.
        # This ensures the utility handles file access errors gracefully without crashing.
        filepath = '/mock/dir/file.txt'
        result = calculate_file_hash(filepath)
        self.assertIsNone(result)
        mock_stderr.write.assert_called_with(f"Error reading file {filepath}: Permission denied\n")
