import unittest
import os
import hashlib
from unittest.mock import patch, mock_open, MagicMock
from collections import defaultdict

# Import the functions to be tested
from src.resonator import calculate_file_hash, find_duplicate_files, report_duplicates

class TestResonator(unittest.TestCase):

    def test_calculate_file_hash_success(self):
        # Mock rationale: Simulate file reading without actual disk I/O.
        # This ensures deterministic tests independent of the file system.
        mock_file_content = b"test content"
        expected_hash = hashlib.sha256(mock_file_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=mock_file_content)) as mock_file:
            # Ensure read is called with a buffer size
            mock_file.return_value.__iter__.return_value = [mock_file_content]
            mock_file.return_value.read.side_effect = [mock_file_content, b'']
            
            result_hash = calculate_file_hash("dummy_path.txt")
            self.assertEqual(result_hash, expected_hash)
            mock_file.assert_called_once_with("dummy_path.txt", 'rb')

    def test_calculate_file_hash_io_error(self):
        # Mock rationale: Simulate a file not found or permission error.
        # This tests error handling without needing to create problematic files.
        with patch('builtins.open', side_effect=IOError("File not found")):
            result_hash = calculate_file_hash("non_existent.txt")
            self.assertIsNone(result_hash)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('src.resonator.calculate_file_hash')
    @patch('os.path.islink', return_value=False) # Mock rationale: Ensure symbolic links are not followed by default.
    def test_find_duplicate_files_no_duplicates(self, mock_islink, mock_calculate_hash, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure and file hashes.
        # This allows testing the logic of finding duplicates without actual files.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt']),
            ('/root/subdir', [], ['file3.txt'])
        ]
        mock_calculate_hash.side_effect = [
            'hash1', 'hash2', 'hash3'
        ]

        expected_result = defaultdict(list)
        expected_result['hash1'].append(os.path.join('/root', 'file1.txt'))
        expected_result['hash2'].append(os.path.join('/root', 'file2.txt'))
        expected_result['hash3'].append(os.path.join('/root/subdir', 'file3.txt'))

        with patch('builtins.print'): # Mock rationale: Suppress print statements during test.
            result = find_duplicate_files('/root')
            self.assertEqual(result, expected_result)
            mock_calculate_hash.assert_called_with(os.path.join('/root/subdir', 'file3.txt')) # Check last call

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('src.resonator.calculate_file_hash')
    @patch('os.path.islink', return_value=False)
    def test_find_duplicate_files_with_duplicates(self, mock_islink, mock_calculate_hash, mock_walk, mock_isdir):
        # Mock rationale: Simulate files with identical hashes to test duplicate detection.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/root', [], ['fileA.txt', 'fileB.txt']),
            ('/root/subdir', [], ['fileC.txt'])
        ]
        mock_calculate_hash.side_effect = [
            'duplicate_hash', 'unique_hash', 'duplicate_hash'
        ]

        expected_result = defaultdict(list)
        expected_result['duplicate_hash'].append(os.path.join('/root', 'fileA.txt'))
        expected_result['unique_hash'].append(os.path.join('/root', 'fileB.txt'))
        expected_result['duplicate_hash'].append(os.path.join('/root/subdir', 'fileC.txt'))

        with patch('builtins.print'):
            result = find_duplicate_files('/root')
            self.assertEqual(result, expected_result)
            self.assertEqual(len(result['duplicate_hash']), 2) # Explicitly check duplicate count

    @patch('os.path.isdir')
    @patch('builtins.print')
    def test_find_duplicate_files_invalid_directory(self, mock_print, mock_isdir):
        # Mock rationale: Simulate an invalid directory path.
        mock_isdir.return_value = False
        result = find_duplicate_files('/nonexistent')
        self.assertEqual(result, {})
        mock_print.assert_called_with("Error: Directory '/nonexistent' not found.")

    @patch('builtins.print')
    def test_report_duplicates_no_duplicates(self, mock_print):
        # Mock rationale: Test reporting when no duplicates are found.
        hash_to_paths = defaultdict(list)
        hash_to_paths['hash1'].append('/path/to/file1.txt')
        hash_to_paths['hash2'].append('/path/to/file2.txt')

        report_duplicates(hash_to_paths)
        mock_print.assert_any_call("\nNo echoing files found. Your chamber is uniquely resonant!")
        # Ensure no group reports are printed
        self.assertNotIn("Found 0 groups of echoing files:", [call.args[0] for call in mock_print.call_args_list])


    @patch('builtins.print')
    def test_report_duplicates_with_duplicates(self, mock_print):
        # Mock rationale: Test the formatting and content of the duplicate report.
        hash_to_paths = defaultdict(list)
        hash_to_paths['hash_dup_A'].extend(['/path/to/fileA1.txt', '/path/to/fileA2.txt'])
        hash_to_paths['hash_dup_B'].extend(['/path/to/fileB1.txt', '/path/to/fileB2.txt', '/path/to/fileB3.txt'])
        hash_to_paths['hash_unique'].append('/path/to/fileU.txt')

        report_duplicates(hash_to_paths);

        # Check for overall summary
        mock_print.assert_any_call("\nFound 2 groups of echoing files:")

        # Check for group A details
        mock_print.assert_any_call(unittest.mock.ANY) # Consume the first print call
        mock_print.assert_any_call(f"\n--- Group 1 (SHA256: {'hash_dup_A'[:12]}...) ---")
        mock_print.assert_any_call("  - /path/to/fileA1.txt")
        mock_print.assert_any_call("  - /path/to/fileA2.txt")

        # Check for group B details
        mock_print.assert_any_call(f"\n--- Group 2 (SHA256: {'hash_dup_B'[:12]}...) ---")
        mock_print.assert_any_call("  - /path/to/fileB1.txt")
        mock_print.assert_any_call("  - /path/to/fileB2.txt")
        mock_print.assert_any_call("  - /path/to/fileB3.txt")

        # Check for final message
        mock_print.assert_any_call("\n🎶 Echo Chamber Resonation complete. Uniqueness amplified! 🎶")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.resonator.find_duplicate_files')
    @patch('src.resonator.report_duplicates')
    def test_main_function(self, mock_report_duplicates, mock_find_duplicate_files, mock_parse_args):
        # Mock rationale: Test the main entry point's argument parsing and function calls.
        # This ensures the CLI interface works as expected without running the full logic.
        mock_args = MagicMock()
        mock_args.path = '/test/path'
        mock_parse_args.return_value = mock_args

        mock_found_duplicates = {'hash': ['file1', 'file2']}
        mock_find_duplicate_files.return_value = mock_found_duplicates

        # Call main directly
        from src.resonator import main
        main()

        mock_parse_args.assert_called_once()
        mock_find_duplicate_files.assert_called_once_with('/test/path')
        mock_report_duplicates.assert_called_once_with(mock_found_duplicates)

if __name__ == '__main__':
    unittest.main()
