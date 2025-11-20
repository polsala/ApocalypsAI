import unittest
import os
import json
import hashlib
import io
from unittest.mock import patch, mock_open, MagicMock
import sys

# Import the functions from the utility
from src.checksum_calculator import (
    calculate_file_checksum,
    calculate_directory_checksums,
    save_checksums,
    load_checksums,
    verify_checksums,
    main
)

class TestChecksumCalculator(unittest.TestCase):

    def setUp(self):
        self.test_dir = '/mock/test_dir'
        self.manifest_file = os.path.join(self.test_dir, 'checksums.json')
        self.algorithm = 'sha256'

    def _get_checksum(self, content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_checksum(self, mock_file_open):
        # Mock rationale: Simulates reading file content from disk without actual I/O.
        mock_file_open.return_value.read.side_effect = [b'test content', b''] # Read in chunks
        filepath = '/mock/file.txt'
        expected_checksum = hashlib.sha256(b'test content').hexdigest()
        checksum = calculate_file_checksum(filepath, self.algorithm)
        self.assertEqual(checksum, expected_checksum)
        mock_file_open.assert_called_with(filepath, 'rb')

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_checksum_not_found(self, mock_file_open):
        # Mock rationale: Simulates a FileNotFoundError without actual disk I/O.
        mock_file_open.side_effect = FileNotFoundError
        filepath = '/mock/non_existent_file.txt'
        checksum = calculate_file_checksum(filepath, self.algorithm)
        self.assertIsNone(checksum)

    @patch('os.walk')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_directory_checksums(self, mock_file_open, mock_isdir, mock_os_walk):
        # Mock rationale: Simulates a directory structure and file contents for checksum calculation.
        # os.walk provides the directory traversal.
        # os.path.isdir ensures the base directory is seen as valid.
        # builtins.open provides the content for each file.
        mock_os_walk.return_value = [
            (self.test_dir, [], ['file1.txt', 'file2.txt'])
        ]
        file1_content = b'content of file1'
        file2_content = b'content of file2'

        # Configure mock_file_open to return different content for different files
        mock_file_open.side_effect = [
            io.BytesIO(file1_content), # For file1.txt
            io.BytesIO(file2_content)  # For file2.txt
        ]

        expected_checksums = {
            'file1.txt': hashlib.sha256(file1_content).hexdigest(),
            'file2.txt': hashlib.sha256(file2_content).hexdigest()
        }

        checksums = calculate_directory_checksums(self.test_dir, self.algorithm)
        self.assertEqual(checksums, expected_checksums)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_checksums(self, mock_json_dump, mock_file_open):
        # Mock rationale: Simulates writing JSON data to a file without actual disk I/O.
        test_checksums = {'file.txt': 'abc'}
        result = save_checksums(test_checksums, self.manifest_file)
        self.assertTrue(result)
        mock_file_open.assert_called_with(self.manifest_file, 'w')
        mock_json_dump.assert_called_with(test_checksums, mock_file_open(), indent=4)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', return_value={'file.txt': 'abc'})
    def test_load_checksums(self, mock_json_load, mock_file_open):
        # Mock rationale: Simulates reading JSON data from a file without actual disk I/O.
        expected_checksums = {'file.txt': 'abc'}
        checksums = load_checksums(self.manifest_file)
        self.assertEqual(checksums, expected_checksums)
        mock_file_open.assert_called_with(self.manifest_file, 'r')
        mock_json_load.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=FileNotFoundError)
    def test_load_checksums_not_found(self, mock_json_load, mock_file_open):
        # Mock rationale: Simulates a FileNotFoundError when loading a manifest.
        checksums = load_checksums(self.manifest_file)
        self.assertIsNone(checksums)

    @patch('src.checksum_calculator.calculate_directory_checksums')
    @patch('builtins.print') # Mock rationale: Suppress print output during tests.
    def test_verify_checksums_success(self, mock_print, mock_calculate_directory_checksums):
        # Mock rationale: Simulates a scenario where all current checksums match saved ones.
        # calculate_directory_checksums is mocked to provide current state.
        saved_checksums = {
            'file1.txt': self._get_checksum('content1'),
            'file2.txt': self._get_checksum('content2')
        }
        mock_calculate_directory_checksums.return_value = saved_checksums

        result = verify_checksums(self.test_dir, saved_checksums, self.algorithm)
        self.assertTrue(result)
        mock_calculate_directory_checksums.assert_called_with(self.test_dir, self.algorithm)
        self.assertIn('[OK]', mock_print.call_args_list[2][0][0]) # Check for OK message

    @patch('src.checksum_calculator.calculate_directory_checksums')
    @patch('builtins.print')
    def test_verify_checksums_changed_content(self, mock_print, mock_calculate_directory_checksums):
        # Mock rationale: Simulates a scenario where a file's content has changed.
        saved_checksums = {
            'file1.txt': self._get_checksum('content1'),
            'file2.txt': self._get_checksum('content2')
        }
        current_checksums = {
            'file1.txt': self._get_checksum('new content1'), # Changed
            'file2.txt': self._get_checksum('content2')
        }
        mock_calculate_directory_checksums.return_value = current_checksums

        result = verify_checksums(self.test_dir, saved_checksums, self.algorithm)
        self.assertFalse(result)
        self.assertIn('[CHANGED]', mock_print.call_args_list[2][0][0]) # Check for CHANGED message

    @patch('src.checksum_calculator.calculate_directory_checksums')
    @patch('builtins.print')
    def test_verify_checksums_missing_file(self, mock_print, mock_calculate_directory_checksums):
        # Mock rationale: Simulates a scenario where a file from the manifest is now missing.
        saved_checksums = {
            'file1.txt': self._get_checksum('content1'),
            'file2.txt': self._get_checksum('content2')
        }
        current_checksums = {
            'file1.txt': self._get_checksum('content1')
        } # file2.txt is missing
        mock_calculate_directory_checksums.return_value = current_checksums

        result = verify_checksums(self.test_dir, saved_checksums, self.algorithm)
        self.assertFalse(result)
        self.assertIn('[MISSING]', mock_print.call_args_list[3][0][0]) # Check for MISSING message

    @patch('src.checksum_calculator.calculate_directory_checksums')
    @patch('builtins.print')
    def test_verify_checksums_new_file(self, mock_print, mock_calculate_directory_checksums):
        # Mock rationale: Simulates a scenario where a new file has been added to the directory.
        saved_checksums = {
            'file1.txt': self._get_checksum('content1')
        }
        current_checksums = {
            'file1.txt': self._get_checksum('content1'),
            'file3.txt': self._get_checksum('content3') # New file
        }
        mock_calculate_directory_checksums.return_value = current_checksums

        result = verify_checksums(self.test_dir, saved_checksums, self.algorithm)
        self.assertFalse(result)
        self.assertIn('[NEW]', mock_print.call_args_list[3][0][0]) # Check for NEW message

    @patch('sys.argv', ['checksum_calculator.py', 'calculate', '--directory', '/mock/dir', '--output', 'manifest.json'])
    @patch('src.checksum_calculator.calculate_directory_checksums', return_value={'file.txt': 'abc'})
    @patch('src.checksum_calculator.save_checksums', return_value=True)
    @patch('builtins.print')
    def test_main_calculate_command(self, mock_print, mock_save, mock_calculate, mock_argv):
        # Mock rationale: Simulates CLI execution for the 'calculate' command.
        # sys.argv is patched to provide command-line arguments.
        # calculate_directory_checksums and save_checksums are mocked to control their behavior.
        main()
        mock_calculate.assert_called_with('/mock/dir', 'sha256')
        mock_save.assert_called_with({'file.txt': 'abc'}, 'manifest.json')

    @patch('sys.argv', ['checksum_calculator.py', 'verify', '--directory', '/mock/dir', '--manifest', 'manifest.json'])
    @patch('src.checksum_calculator.load_checksums', return_value={'file.txt': 'abc'})
    @patch('src.checksum_calculator.verify_checksums', return_value=True)
    @patch('builtins.print')
    def test_main_verify_command(self, mock_print, mock_verify, mock_load, mock_argv):
        # Mock rationale: Simulates CLI execution for the 'verify' command.
        # sys.argv is patched to provide command-line arguments.
        # load_checksums and verify_checksums are mocked to control their behavior.
        main()
        mock_load.assert_called_with('manifest.json')
        mock_verify.assert_called_with('/mock/dir', {'file.txt': 'abc'}, 'sha256')

    @patch('sys.argv', ['checksum_calculator.py'])
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_command(self, mock_print_help, mock_argv):
        # Mock rationale: Simulates CLI execution with no command, expecting help message.
        main()
        mock_print_help.assert_called_once()

if __name__ == '__main__':
    unittest.main()
