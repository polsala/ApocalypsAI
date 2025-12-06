import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import hashlib
import sys

# Import the functions to be tested
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from duster import calculate_file_hash, find_duplicate_files, main

class TestDuster(unittest.TestCase):

    def setUp(self):
        # Reset sys.argv for each test
        self._original_argv = sys.argv
        sys.argv = [self._original_argv[0]] # Keep script name

    def tearDown(self):
        sys.argv = self._original_argv

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_success(self, mock_file_open):
        # Mock rationale: Simulate reading a file's content to ensure hash calculation is correct.
        # This avoids actual file I/O, making the test deterministic and offline.
        mock_file_open.return_value.read.side_effect = [b"hello", b" world", b""]
        expected_hash = hashlib.sha256(b"hello world").hexdigest()
        self.assertEqual(calculate_file_hash("dummy_path.txt"), expected_hash)
        mock_file_open.assert_called_once_with("dummy_path.txt", 'rb')

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_calculate_file_hash_io_error(self, mock_file_open):
        # Mock rationale: Simulate an IOError during file reading to test error handling.
        # Ensures the utility gracefully handles inaccessible files without crashing.
        self.assertIsNone(calculate_file_hash("inaccessible.txt"))
        mock_file_open.assert_called_once_with("inaccessible.txt", 'rb')

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('duster.calculate_file_hash') # Mock the hash calculation to control output
    def test_find_duplicate_files_no_duplicates(self, mock_calculate_hash, mock_getsize, mock_walk):
        # Mock rationale: Simulate a directory structure with unique files.
        # `os.walk` is mocked to return specific file paths.
        # `os.path.getsize` is mocked to return distinct sizes.
        # `calculate_file_hash` is mocked to return distinct hashes.
        # This ensures the test is deterministic and doesn't rely on actual file system state.

        mock_walk.return_value = [
            ('/dir1', [], ['fileA.txt', 'fileB.txt']),
        ]
        mock_getsize.side_effect = [100, 200] # Different sizes
        mock_calculate_hash.side_effect = ['hashA', 'hashB'] # Different hashes

        duplicates = find_duplicate_files(['/dir1'])
        self.assertEqual(duplicates, {})
        mock_walk.assert_called_once_with('/dir1')
        self.assertEqual(mock_getsize.call_count, 2)
        self.assertEqual(mock_calculate_hash.call_count, 2)

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('duster.calculate_file_hash')
    def test_find_duplicate_files_with_duplicates(self, mock_calculate_hash, mock_getsize, mock_walk):
        # Mock rationale: Simulate a directory structure with duplicate files.
        # `os.walk` returns paths. `os.path.getsize` returns same sizes for duplicates.
        # `calculate_file_hash` returns same hashes for duplicates.
        # This setup allows testing the core logic of duplicate detection without real files.

        mock_walk.side_effect = [
            ('/dir1', [], ['file1.txt', 'file2.txt']),
            ('/dir2', [], ['file3.txt']),
        ]
        # file1.txt (100 bytes, hashX)
        # file2.txt (100 bytes, hashX) -> duplicate of file1.txt
        # file3.txt (200 bytes, hashY)
        mock_getsize.side_effect = [100, 100, 200]
        mock_calculate_hash.side_effect = ['hashX', 'hashX', 'hashY']

        duplicates = find_duplicate_files(['/dir1', '/dir2'])
        expected_duplicates = {
            'hashX': ['/dir1/file1.txt', '/dir1/file2.txt']
        }
        self.assertEqual(duplicates, expected_duplicates)
        self.assertEqual(mock_walk.call_count, 2)
        self.assertEqual(mock_getsize.call_count, 3)
        self.assertEqual(mock_calculate_hash.call_count, 3)

    @patch('os.walk')
    @patch('os.path.getsize', side_effect=OSError("File not found"))
    @patch('duster.calculate_file_hash')
    def test_find_duplicate_files_getsize_error(self, mock_calculate_hash, mock_getsize, mock_walk):
        # Mock rationale: Simulate an OSError when calling `os.path.getsize`.
        # This tests that the utility skips inaccessible files gracefully without crashing.
        mock_walk.return_value = [
            ('/dir1', [], ['fileA.txt']),
        ]
        duplicates = find_duplicate_files(['/dir1'])
        self.assertEqual(duplicates, {})
        mock_getsize.assert_called_once_with('/dir1/fileA.txt')
        mock_calculate_hash.assert_not_called() # Should not try to hash if size fails

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_find_duplicate_files_invalid_directory(self, mock_stderr, mock_isdir):
        # Mock rationale: Simulate an invalid directory path.
        # `os.path.isdir` is mocked to return False.
        # `sys.stderr` is mocked to capture warning messages.
        # This ensures the utility handles invalid input gracefully.
        duplicates = find_duplicate_files(['/nonexistent_dir'])
        self.assertEqual(duplicates, {})
        mock_isdir.assert_called_once_with('/nonexistent_dir')
        mock_stderr.write.assert_called_with("Warning: Directory not found or not accessible: /nonexistent_dir\n")

    @patch('duster.find_duplicate_files', return_value={})
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_main_no_duplicates_found(self, mock_stderr, mock_stdout, mock_find_duplicates):
        # Mock rationale: Test the main function's output when no duplicates are found.
        # `find_duplicate_files` is mocked to return an empty dict.
        # `sys.stdout` and `sys.stderr` are mocked to capture printed output.
        # This verifies the correct message is displayed.
        sys.argv.extend(['/test_dir'])
        main()
        mock_find_duplicates.assert_called_once_with(['/test_dir'], dry_run=True)
        mock_stdout.write.assert_any_call("\nNo duplicate files found. Your digital realm is pristine!\n")
        self.assertEqual(sys.exit.called, False) # Should not exit with error

    @patch('duster.find_duplicate_files')
    @patch('os.path.getsize', side_effect=[100, 100]) # For calculating total space saved
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_main_duplicates_found(self, mock_stderr, mock_stdout, mock_find_duplicates, mock_getsize):
        # Mock rationale: Test the main function's output when duplicates are found.
        # `find_duplicate_files` is mocked to return a dict with duplicates.
        # `os.path.getsize` is mocked to provide file sizes for space calculation.
        # `sys.stdout` and `sys.stderr` are mocked to capture printed output.
        # This verifies the correct report format and space calculation.
        mock_find_duplicates.return_value = {
            'hashX': ['/dir1/file1.txt', '/dir1/file2.txt']
        }
        sys.argv.extend(['/test_dir'])
        main()
        mock_find_duplicates.assert_called_once_with(['/test_dir'], dry_run=True)
        mock_stdout.write.assert_any_call("\n--- Duplicate Files Found ---\n")
        mock_stdout.write.assert_any_call(f"Total potential space reclaimable: {100 / (1024*1024):.2f} MB\n")
        self.assertEqual(sys.exit.called, False)

    @patch('sys.exit')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_main_no_args(self, mock_stderr, mock_exit):
        # Mock rationale: Test the main function's behavior with no command-line arguments.
        # `sys.exit` is mocked to prevent actual program termination.
        # `sys.stderr` is mocked to capture usage messages.
        # This ensures the utility prints correct usage and exits with an error code.
        mock_exit.side_effect = SystemExit # Allow testing exit code
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        mock_stderr.write.assert_any_call("Usage: python src/duster.py <directory1> [directory2 ...] [--dry-run]\n")

    @patch('sys.exit')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_main_only_dry_run_arg(self, mock_stderr, mock_exit):
        # Mock rationale: Test the main function's behavior when only `--dry-run` is provided.
        # `sys.exit` is mocked to prevent actual program termination.
        # `sys.stderr` is mocked to capture error messages.
        # This ensures the utility correctly identifies missing directories and exits.
        mock_exit.side_effect = SystemExit
        sys.argv.extend(['--dry-run'])
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        mock_stderr.write.assert_any_call("Error: No directories specified for scanning.\n")

if __name__ == '__main__':
    unittest.main()
