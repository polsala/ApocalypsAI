import unittest
import sys
import os
from unittest.mock import patch, mock_open
from io import StringIO

# Mock rationale: We need to simulate file system operations without actually creating files.
# `mock_open` allows us to control the content read from a file, and `patch('sys.exit')`
# prevents the script from exiting during tests, allowing us to check error messages.

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from checksum_checker import calculate_checksum, verify_checksum, main

class TestChecksumChecker(unittest.TestCase):

    def setUp(self):
        # Capture stdout and stderr for testing CLI output
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        sys.stdout = self.mock_stdout = StringIO()
        sys.stderr = self.mock_stderr = StringIO()

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('builtins.open', new_callable=mock_open, read_data=b'hello world')
    def test_calculate_checksum_basic(self, mock_file):
        # Mock rationale: Simulates reading "hello world" from a file.
        expected_checksum = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938798a0'
        actual_checksum = calculate_checksum('dummy_file.txt')
        self.assertEqual(actual_checksum, expected_checksum)
        mock_file.assert_called_once_with('dummy_file.txt', 'rb')

    @patch('builtins.open', new_callable=mock_open, read_data=b'')
    def test_calculate_checksum_empty_file(self, mock_file):
        # Mock rationale: Simulates reading an empty file.
        expected_checksum = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' # SHA256 for empty string
        actual_checksum = calculate_checksum('empty_file.txt')
        self.assertEqual(actual_checksum, expected_checksum)

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.exit', side_effect=SystemExit)
    def test_calculate_checksum_file_not_found(self, mock_exit, mock_open_error):
        # Mock rationale: Simulates a FileNotFoundError and prevents sys.exit from terminating the test.
        with self.assertRaises(SystemExit) as cm:
            calculate_checksum('non_existent_file.txt')
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: File not found", self.mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data=b'test data')
    def test_verify_checksum_success(self, mock_file):
        # Mock rationale: Simulates reading "test data" from a file.
        test_data_checksum = '93ae1425178a0517926526189196b6680486808796122d716867761048677610' # SHA256 for 'test data'
        result = verify_checksum('test_file.txt', test_data_checksum)
        self.assertTrue(result)

    @patch('builtins.open', new_callable=mock_open, read_data=b'test data')
    def test_verify_checksum_failure(self, mock_file):
        # Mock rationale: Simulates reading "test data" from a file.
        wrong_checksum = 'a' * 64
        result = verify_checksum('test_file.txt', wrong_checksum)
        self.assertFalse(result)

    @patch('sys.argv', ['checksum_checker.py', 'generate', 'test_file.txt'])
    @patch('builtins.open', new_callable=mock_open, read_data=b'hello world')
    def test_main_generate_command(self, mock_file):
        # Mock rationale: Simulates command line arguments for 'generate' and file content.
        with patch('sys.exit') as mock_exit: # Patch sys.exit to prevent actual exit
            main()
            mock_exit.assert_not_called() # Should not exit on success
        expected_checksum = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938798a0'
        self.assertIn(f"{expected_checksum} test_file.txt", self.mock_stdout.getvalue())

    @patch('sys.argv', ['checksum_checker.py', 'verify', 'test_file.txt', '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938798a0'])
    @patch('builtins.open', new_callable=mock_open, read_data=b'hello world')
    def test_main_verify_command_success(self, mock_file):
        # Mock rationale: Simulates command line arguments for 'verify' and correct file content.
        with patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_not_called()
        self.assertIn("Verification successful for test_file.txt", self.mock_stdout.getvalue())

    @patch('sys.argv', ['checksum_checker.py', 'verify', 'test_file.txt', 'wrong_checksum'])
    @patch('builtins.open', new_callable=mock_open, read_data=b'hello world')
    @patch('sys.exit', side_effect=SystemExit)
    def test_main_verify_command_failure(self, mock_exit, mock_file):
        # Mock rationale: Simulates command line arguments for 'verify' with incorrect checksum and file content.
        # `sys.exit` is patched to catch the exit call.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Verification failed for test_file.txt. Expected: wrong_checksum", self.mock_stderr.getvalue())
        self.assertIn("Got: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938798a0", self.mock_stderr.getvalue())

    @patch('sys.argv', ['checksum_checker.py', 'invalid_command', 'file.txt'])
    @patch('sys.exit', side_effect=SystemExit)
    def test_main_invalid_command(self, mock_exit):
        # Mock rationale: Simulates an invalid command line argument.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Unknown command: invalid_command", self.mock_stderr.getvalue())

    @patch('sys.argv', ['checksum_checker.py', 'generate']) # Missing filepath
    @patch('sys.exit', side_effect=SystemExit)
    def test_main_missing_args_generate(self, mock_exit):
        # Mock rationale: Simulates missing arguments for 'generate' command.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Usage:", self.mock_stderr.getvalue())

    @patch('sys.argv', ['checksum_checker.py', 'verify', 'file.txt']) # Missing expected_checksum
    @patch('sys.exit', side_effect=SystemExit)
    def test_main_missing_args_verify(self, mock_exit):
        # Mock rationale: Simulates missing arguments for 'verify' command.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Usage: python src/checksum_checker.py verify <filepath> <expected_checksum>", self.mock_stderr.getvalue())
