import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import hashlib

# Add src directory to path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import monitor

class TestMonitor(unittest.TestCase):

    @patch('monitor.calculate_file_hash')
    @patch('os.walk')
    def test_no_duplicates(self, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Simulate a directory structure without actually creating files.
        # This makes tests deterministic and offline.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['fileA.txt', 'fileB.txt']),
            ('/test_dir/subdir', [], ['fileC.txt'])
        ]

        # Mock rationale: Provide deterministic hash values for mocked files.
        # This avoids actual file I/O and ensures consistent test results.
        mock_calculate_file_hash.side_effect = {
            '/test_dir/fileA.txt': 'hashA',
            '/test_dir/fileB.txt': 'hashB',
            '/test_dir/subdir/fileC.txt': 'hashC',
        }.get

        duplicates = monitor.find_duplicate_files('/test_dir')
        self.assertEqual(duplicates, {})
        mock_os_walk.assert_called_once_with('/test_dir')
        self.assertEqual(mock_calculate_file_hash.call_count, 3)

    @patch('monitor.calculate_file_hash')
    @patch('os.walk')
    def test_with_duplicates(self, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Simulate a directory structure with duplicate files.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.txt', 'file3.txt']),
            ('/test_dir/subdir', [], ['file4.txt'])
        ]

        # Mock rationale: Assign identical hash values to simulate duplicates.
        mock_calculate_file_hash.side_effect = {
            '/test_dir/file1.txt': 'hash_duplicate',
            '/test_dir/file2.txt': 'hash_unique',
            '/test_dir/file3.txt': 'hash_duplicate',
            '/test_dir/subdir/file4.txt': 'hash_another_unique',
        }.get

        duplicates = monitor.find_duplicate_files('/test_dir')
        expected_duplicates = {
            'hash_duplicate': ['/test_dir/file1.txt', '/test_dir/file3.txt']
        }
        self.assertEqual(duplicates, expected_duplicates)
        mock_os_walk.assert_called_once_with('/test_dir')
        self.assertEqual(mock_calculate_file_hash.call_count, 4)

    @patch('monitor.calculate_file_hash')
    @patch('os.walk')
    def test_empty_directory(self, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Simulate an empty directory.
        mock_os_walk.return_value = [
            ('/empty_dir', [], [])
        ]

        duplicates = monitor.find_duplicate_files('/empty_dir')
        self.assertEqual(duplicates, {})
        mock_os_walk.assert_called_once_with('/empty_dir')
        mock_calculate_file_hash.assert_not_called()

    @patch('monitor.calculate_file_hash')
    @patch('os.walk')
    def test_nested_duplicates(self, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Simulate duplicates across different subdirectories.
        mock_os_walk.return_value = [
            ('/test_dir', ['subdir1', 'subdir2'], ['root_file.txt']),
            ('/test_dir/subdir1', [], ['fileA.txt', 'fileB.txt']),
            ('/test_dir/subdir2', [], ['fileC.txt'])
        ]

        mock_calculate_file_hash.side_effect = {
            '/test_dir/root_file.txt': 'hash_unique_root',
            '/test_dir/subdir1/fileA.txt': 'hash_common',
            '/test_dir/subdir1/fileB.txt': 'hash_unique_B',
            '/test_dir/subdir2/fileC.txt': 'hash_common',
        }.get

        duplicates = monitor.find_duplicate_files('/test_dir')
        expected_duplicates = {
            'hash_common': ['/test_dir/subdir1/fileA.txt', '/test_dir/subdir2/fileC.txt']
        }
        self.assertEqual(duplicates, expected_duplicates)
        self.assertEqual(mock_calculate_file_hash.call_count, 4)

    @patch('monitor.calculate_file_hash')
    @patch('os.walk')
    def test_single_file_directory(self, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Simulate a directory with only one file.
        mock_os_walk.return_value = [
            ('/single_file_dir', [], ['only_file.txt'])
        ]

        mock_calculate_file_hash.side_effect = {
            '/single_file_dir/only_file.txt': 'hash_single',
        }.get

        duplicates = monitor.find_duplicate_files('/single_file_dir')
        self.assertEqual(duplicates, {})
        self.assertEqual(mock_calculate_file_hash.call_count, 1)

    @patch('monitor.calculate_file_hash')
    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate a non-existent directory.
    @patch('os.walk')
    def test_non_existent_directory(self, mock_os_walk, mock_os_path_exists, mock_calculate_file_hash):
        # Mock rationale: Ensure the utility handles non-existent directories gracefully.
        with self.assertRaises(FileNotFoundError):
            monitor.find_duplicate_files('/non_existent_dir')
        mock_os_path_exists.assert_called_once_with('/non_existent_dir')
        mock_os_walk.assert_not_called()
        mock_calculate_file_hash.assert_not_called()

    @patch('monitor.calculate_file_hash')
    @patch('os.path.isdir', return_value=False) # Mock rationale: Simulate a path that is not a directory.
    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate path existence.
    @patch('os.walk')
    def test_path_is_not_directory(self, mock_os_walk, mock_os_path_exists, mock_os_path_isdir, mock_calculate_file_hash):
        # Mock rationale: Ensure NotADirectoryError is raised for non-directory paths.
        with self.assertRaises(NotADirectoryError):
            monitor.find_duplicate_files('/not_a_dir')
        mock_os_path_exists.assert_called_once_with('/not_a_dir')
        mock_os_path_isdir.assert_called_once_with('/not_a_dir')
        mock_os_walk.assert_not_called()
        mock_calculate_file_hash.assert_not_called()

    @patch('monitor.calculate_file_hash')
    @patch('os.walk')
    @patch('builtins.print') # Mock rationale: Capture print output for CLI testing.
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/test_dir'))
    def test_main_with_duplicates_cli(self, mock_parse_args, mock_print, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Test the main function's output when duplicates are found.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.txt', 'file3.txt']),
        ]
        mock_calculate_file_hash.side_effect = {
            '/test_dir/file1.txt': 'hash_duplicate',
            '/test_dir/file2.txt': 'hash_unique',
            '/test_dir/file3.txt': 'hash_duplicate',
        }.get

        monitor.main()

        mock_print.assert_any_call("Found duplicate files:")
        mock_print.assert_any_call("  Hash: hash_duplicate")
        mock_print.assert_any_call("    - /test_dir/file1.txt")
        mock_print.assert_any_call("    - /test_dir/file3.txt")
        # Check that print was called exactly 4 times (header, hash, 2 files)
        self.assertEqual(mock_print.call_count, 4)

    @patch('monitor.calculate_file_hash')
    @patch('os.walk')
    @patch('builtins.print') # Mock rationale: Capture print output for CLI testing.
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/test_dir'))
    def test_main_no_duplicates_cli(self, mock_parse_args, mock_print, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Test the main function's output when no duplicates are found.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.txt']),
        ]
        mock_calculate_file_hash.side_effect = {
            '/test_dir/file1.txt': 'hash_unique1',
            '/test_dir/file2.txt': 'hash_unique2',
        }.get

        monitor.main()

        mock_print.assert_called_once_with("No duplicate files found.")

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('os.path.exists', return_value=True) # Mock rationale: Simulate file existence.
    def test_calculate_file_hash_function(self, mock_os_path_exists, mock_open):
        # Mock rationale: Simulate file content without actual disk I/O.
        # This ensures deterministic hashing for testing.
        mock_file_content = b"This is some test content for hashing." * 10 # Make it longer to test chunking
        # Simulate reading in chunks of 10 bytes
        mock_open.return_value.read.side_effect = [mock_file_content[i:i+10] for i in range(0, len(mock_file_content), 10)] + [b'']

        expected_hash = hashlib.sha256(mock_file_content).hexdigest()
        actual_hash = monitor.calculate_file_hash('/mock/path/to/file.txt', block_size=10)

        self.assertEqual(actual_hash, expected_hash)
        mock_open.assert_called_once_with('/mock/path/to/file.txt', 'rb')
        self.assertTrue(mock_open.return_value.read.called)

    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate a non-existent file.
    def test_calculate_file_hash_non_existent_file(self, mock_os_path_exists):
        # Mock rationale: Ensure FileNotFoundError is raised for non-existent files.
        with self.assertRaises(FileNotFoundError):
            monitor.calculate_file_hash('/mock/non_existent_file.txt')
        mock_os_path_exists.assert_called_once_with('/mock/non_existent_file.txt')

    @patch('monitor.calculate_file_hash', side_effect=FileNotFoundError('File disappeared'))
    @patch('os.walk')
    @patch('builtins.print') # Mock rationale: Capture stderr output for warnings.
    def test_file_disappears_during_scan(self, mock_print, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Simulate a file being deleted between os.walk and hash calculation.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['fileA.txt'])
        ]

        duplicates = monitor.find_duplicate_files('/test_dir')
        self.assertEqual(duplicates, {})
        mock_print.assert_called_once_with("Warning: File disappeared during scan: /test_dir/fileA.txt", file=sys.stderr)

    @patch('monitor.calculate_file_hash', side_effect=Exception('Permission denied'))
    @patch('os.walk')
    @patch('builtins.print') # Mock rationale: Capture stderr output for errors.
    def test_file_processing_error(self, mock_print, mock_os_walk, mock_calculate_file_hash):
        # Mock rationale: Simulate an unexpected error during file processing (e.g., permission issue).
        mock_os_walk.return_value = [
            ('/test_dir', [], ['fileA.txt'])
        ]

        duplicates = monitor.find_duplicate_files('/test_dir')
        self.assertEqual(duplicates, {})
        mock_print.assert_called_once_with("Error processing file /test_dir/fileA.txt: Permission denied", file=sys.stderr)
