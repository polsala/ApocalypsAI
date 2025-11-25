import unittest
import os
import hashlib
from unittest.mock import patch, mock_open
import sys
from io import StringIO

# Import the functions from the utility
from src.checksum_checker import generate_checksum, save_checksum, verify_checksum, main

class TestChecksumChecker(unittest.TestCase):

    # Mock rationale: We don't want to create actual files on the filesystem during tests.
    # os.path.exists is mocked to simulate file presence.
    # builtins.open is mocked to simulate reading/writing file content.
    # hashlib.sha256 is mocked to provide deterministic checksums without actual hashing.
    # sys.argv is mocked to control command-line arguments for main() function tests.
    # sys.exit is mocked to prevent actual program termination during main() tests.
    # sys.stdout is captured to test print statements.

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data=b'test data')
    @patch('hashlib.sha256')
    def test_generate_checksum_success(self, mock_sha256, mock_file_open, mock_exists):
        mock_hasher_instance = mock_sha256.return_value
        mock_hasher_instance.hexdigest.return_value = 'mock_checksum_123'
        
        checksum = generate_checksum('dummy_file.txt')
        self.assertEqual(checksum, 'mock_checksum_123')
        mock_exists.assert_called_once_with('dummy_file.txt')
        mock_file_open.assert_called_once_with('dummy_file.txt', 'rb')
        mock_hasher_instance.update.assert_called_once_with(b'test data')

    @patch('os.path.exists', return_value=False)
    def test_generate_checksum_file_not_found(self, mock_exists):
        with self.assertRaises(FileNotFoundError):
            generate_checksum('non_existent_file.txt')
        mock_exists.assert_called_once_with('non_existent_file.txt')

    @patch('os.path.exists', return_value=False) # Manifest file doesn't exist initially
    @patch('builtins.open', new_callable=mock_open)
    def test_save_checksum_to_manifest_new(self, mock_file_open, mock_exists):
        filepath = 'test_file.txt'
        checksum = 'mock_checksum_abc'
        manifest_file = 'manifest.sha256'
        
        save_checksum(filepath, checksum, manifest_file)
        
        mock_exists.assert_called_once_with(manifest_file) # Checks if manifest exists
        mock_file_open.assert_called_once_with(manifest_file, 'w') # Opens in write mode
        mock_file_open().write.assert_called_once_with(f"{checksum}  {filepath}\n")
        self.assertIn(f"Checksum for '{filepath}' saved to manifest: '{manifest_file}'", self.mock_stdout.getvalue())

    @patch('os.path.exists', return_value=True) # Manifest file exists
    @patch('builtins.open', new_callable=mock_open)
    def test_save_checksum_to_manifest_append(self, mock_file_open, mock_exists):
        filepath = 'test_file_2.txt'
        checksum = 'mock_checksum_def'
        manifest_file = 'manifest.sha256'
        
        save_checksum(filepath, checksum, manifest_file)
        
        mock_exists.assert_called_once_with(manifest_file) # Checks if manifest exists
        mock_file_open.assert_called_once_with(manifest_file, 'a') # Opens in append mode
        mock_file_open().write.assert_called_once_with(f"{checksum}  {filepath}\n")
        self.assertIn(f"Checksum for '{filepath}' saved to manifest: '{manifest_file}'", self.mock_stdout.getvalue())

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.basename', return_value='test_file.txt')
    def test_save_checksum_to_dot_sha256_file(self, mock_basename, mock_file_open, mock_exists):
        filepath = 'path/to/test_file.txt'
        checksum = 'mock_checksum_xyz'
        
        save_checksum(filepath, checksum)
        
        mock_file_open.assert_called_once_with(f"{filepath}.sha256", 'w')
        mock_file_open().write.assert_called_once_with(f"{checksum}  {mock_basename.return_value}\n")
        self.assertIn(f"Checksum for '{filepath}' saved to: '{filepath}.sha256'", self.mock_stdout.getvalue())

    @patch('src.checksum_checker.generate_checksum', return_value='expected_checksum_123')
    def test_verify_checksum_success(self, mock_generate_checksum):
        filepath = 'verified_file.txt'
        expected = 'expected_checksum_123'
        
        result = verify_checksum(filepath, expected)
        self.assertTrue(result)
        mock_generate_checksum.assert_called_once_with(filepath)
        self.assertIn(f"Verification successful for '{filepath}'. Checksum matches.", self.mock_stdout.getvalue())

    @patch('src.checksum_checker.generate_checksum', return_value='actual_checksum_456')
    def test_verify_checksum_failure(self, mock_generate_checksum):
        filepath = 'failed_file.txt'
        expected = 'expected_checksum_123'
        
        result = verify_checksum(filepath, expected)
        self.assertFalse(result)
        mock_generate_checksum.assert_called_once_with(filepath)
        self.assertIn(f"Verification FAILED for '{filepath}'. Expected: {expected}, Actual: {mock_generate_checksum.return_value}", self.mock_stdout.getvalue())

    @patch('src.checksum_checker.generate_checksum', side_effect=FileNotFoundError("File not found"))
    def test_verify_checksum_file_not_found(self, mock_generate_checksum):
        filepath = 'non_existent.txt'
        expected = 'any_checksum'
        
        result = verify_checksum(filepath, expected)
        self.assertFalse(result)
        mock_generate_checksum.assert_called_once_with(filepath)
        self.assertIn("Error: File not found: File not found", self.mock_stdout.getvalue())

    @patch('sys.argv', ['checksum_checker.py', 'generate', 'test_file.txt'])
    @patch('src.checksum_checker.generate_checksum', return_value='generated_checksum_abc')
    @patch('src.checksum_checker.save_checksum')
    @patch('sys.exit')
    def test_main_generate_no_manifest(self, mock_exit, mock_save_checksum, mock_generate_checksum):
        main()
        mock_generate_checksum.assert_called_once_with('test_file.txt')
        mock_save_checksum.assert_called_once_with('test_file.txt', 'generated_checksum_abc')
        mock_exit.assert_called_once_with(0)
        self.assertIn("Generated SHA256 for 'test_file.txt': generated_checksum_abc", self.mock_stdout.getvalue())

    @patch('sys.argv', ['checksum_checker.py', 'generate', 'test_file.txt', '--manifest', 'my_manifest.sha256'])
    @patch('src.checksum_checker.generate_checksum', return_value='generated_checksum_def')
    @patch('src.checksum_checker.save_checksum')
    @patch('sys.exit')
    def test_main_generate_with_manifest(self, mock_exit, mock_save_checksum, mock_generate_checksum):
        main()
        mock_generate_checksum.assert_called_once_with('test_file.txt')
        mock_save_checksum.assert_called_once_with('test_file.txt', 'generated_checksum_def', 'my_manifest.sha256')
        mock_exit.assert_called_once_with(0)
        self.assertIn("Generated SHA256 for 'test_file.txt': generated_checksum_def", self.mock_stdout.getvalue())

    @patch('sys.argv', ['checksum_checker.py', 'verify', 'test_file.txt', 'expected_checksum_xyz'])
    @patch('src.checksum_checker.verify_checksum', return_value=True)
    @patch('sys.exit')
    def test_main_verify_success(self, mock_exit, mock_verify_checksum):
        main()
        mock_verify_checksum.assert_called_once_with('test_file.txt', 'expected_checksum_xyz')
        mock_exit.assert_called_once_with(0)

    @patch('sys.argv', ['checksum_checker.py', 'verify', 'test_file.txt', 'wrong_checksum_xyz'])
    @patch('src.checksum_checker.verify_checksum', return_value=False)
    @patch('sys.exit')
    def test_main_verify_failure(self, mock_exit, mock_verify_checksum):
        main()
        mock_verify_checksum.assert_called_once_with('test_file.txt', 'wrong_checksum_xyz')
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['checksum_checker.py', 'generate', 'non_existent.txt'])
    @patch('src.checksum_checker.generate_checksum', side_effect=FileNotFoundError("File not found"))
    @patch('sys.exit')
    def test_main_generate_file_not_found_error(self, mock_exit, mock_generate_checksum):
        main()
        mock_generate_checksum.assert_called_once_with('non_existent.txt')
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: File not found: File not found", self.mock_stdout.getvalue())

    @patch('sys.argv', ['checksum_checker.py', 'invalid_command'])
    @patch('sys.exit')
    def test_main_invalid_command(self, mock_exit):
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Unknown command: invalid_command", self.mock_stdout.getvalue())

    @patch('sys.argv', ['checksum_checker.py'])
    @patch('sys.exit')
    def test_main_no_arguments(self, mock_exit):
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Usage:", self.mock_stdout.getvalue())

    @patch('sys.argv', ['checksum_checker.py', 'generate', 'file.txt', '--manifest']) # Missing manifest file path
    @patch('src.checksum_checker.generate_checksum', return_value='dummy_checksum')
    @patch('sys.exit')
    def test_main_generate_manifest_missing_path(self, mock_exit, mock_generate_checksum):
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: --manifest requires a file path.", self.mock_stdout.getvalue())

    @patch('sys.argv', ['checksum_checker.py', 'verify', 'file.txt']) # Missing expected checksum
    @patch('sys.exit')
    def test_main_verify_missing_checksum(self, mock_exit):
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Usage: python checksum_checker.py verify <filepath> <expected_checksum>", self.mock_stdout.getvalue())
