import unittest
import os
import tempfile
import hashlib
from unittest.mock import patch, mock_open
from io import StringIO
import sys

# Add the src directory to the path to allow importing checksum_checker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import checksum_checker

class TestChecksumChecker(unittest.TestCase):

    def setUp(self):
        # Capture stdout and stderr
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        sys.stdout = self.mock_stdout = StringIO()
        sys.stderr = self.mock_stderr = StringIO()

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    def test_calculate_checksum_success(self):
        # Mock rationale: Avoids actual file system interaction for a pure function.
        # Ensures deterministic output for known input.
        mock_file_content = b"This is a test file content."
        expected_checksum = hashlib.sha256(mock_file_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=mock_file_content), create=True) as m_open:
            # Ensure read method returns chunks
            m_open().read.side_effect = [mock_file_content[i:i+8192] for i in range(0, len(mock_file_content), 8192)] + [b'']
            
            checksum = checksum_checker.calculate_checksum("dummy_path.txt")
            self.assertEqual(checksum, expected_checksum)
            m_open.assert_called_once_with("dummy_path.txt", 'rb')

    def test_calculate_checksum_file_not_found(self):
        # Mock rationale: Simulates a FileNotFoundError without needing to create/delete files.
        # Allows testing error handling paths deterministically.
        with patch('builtins.open', side_effect=FileNotFoundError), \
             self.assertRaises(SystemExit) as cm: # Expect sys.exit(1)
            checksum_checker.calculate_checksum("non_existent_file.txt")
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: File not found", self.mock_stderr.getvalue())

    def test_calculate_checksum_io_error(self):
        # Mock rationale: Simulates an IOError during file reading without actual file system interaction.
        # Allows testing error handling paths deterministically.
        with patch('builtins.open', side_effect=IOError("Permission denied")), \
             self.assertRaises(SystemExit) as cm: # Expect sys.exit(1)
            checksum_checker.calculate_checksum("unreadable_file.txt")
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error reading file 'unreadable_file.txt': Permission denied", self.mock_stderr.getvalue())

    def test_generate_checksum_file_success(self):
        # Mock rationale: Uses temp files for actual file creation to test the full flow
        # without polluting the test directory. Mocks calculate_checksum to ensure
        # its output is controlled and deterministic.
        mock_filepath = "test_file.txt"
        mock_checksum = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file_path = os.path.join(tmpdir, mock_filepath)
            checksum_file_path = f"{test_file_path}.sha256"

            # Create a dummy file
            with open(test_file_path, 'w') as f:
                f.write("some content")

            with patch('checksum_checker.calculate_checksum', return_value=mock_checksum), \
                 patch('sys.stdout', new=self.mock_stdout): # Capture print output
                checksum_checker.generate_checksum_file(test_file_path)

            self.assertTrue(os.path.exists(checksum_file_path))
            with open(checksum_file_path, 'r') as f:
                content = f.read().strip()
            self.assertEqual(content, f"{mock_checksum}  {mock_filepath}")
            self.assertIn(f"Checksum generated for '{test_file_path}'", self.mock_stdout.getvalue())

    def test_generate_checksum_file_io_error(self):
        # Mock rationale: Simulates an IOError during checksum file writing.
        # Tests error handling and sys.exit.
        mock_filepath = "test_file.txt"
        mock_checksum = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
        
        with patch('checksum_checker.calculate_checksum', return_value=mock_checksum), \
             patch('builtins.open', side_effect=IOError("Disk full")), \
             self.assertRaises(SystemExit) as cm: # Expect sys.exit(1)
            checksum_checker.generate_checksum_file(mock_filepath)
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error writing checksum file", self.mock_stderr.getvalue())
        self.assertIn("Disk full", self.mock_stderr.getvalue())

    def test_verify_checksum_file_success(self):
        # Mock rationale: Uses temp files to simulate real file system interaction for verification.
        # Mocks calculate_checksum to provide a controlled "actual" checksum.
        mock_filepath = "verified_file.txt"
        mock_checksum = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file_path = os.path.join(tmpdir, mock_filepath)
            checksum_file_path = f"{test_file_path}.sha256"

            # Create dummy files
            with open(test_file_path, 'w') as f:
                f.write("some content")
            with open(checksum_file_path, 'w') as f:
                f.write(f"{mock_checksum}  {mock_filepath}\n")

            with patch('checksum_checker.calculate_checksum', return_value=mock_checksum), \
                 patch('sys.stdout', new=self.mock_stdout): # Capture print output
                result = checksum_checker.verify_checksum_file(test_file_path)
            
            self.assertTrue(result)
            self.assertIn("Integrity check PASSED", self.mock_stdout.getvalue())

    def test_verify_checksum_file_failure(self):
        # Mock rationale: Uses temp files and mocks calculate_checksum to simulate a mismatch.
        mock_filepath = "corrupted_file.txt"
        expected_checksum = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
        actual_checksum = "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3" # Mismatched
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file_path = os.path.join(tmpdir, mock_filepath)
            checksum_file_path = f"{test_file_path}.sha256"

            # Create dummy files
            with open(test_file_path, 'w') as f:
                f.write("some content")
            with open(checksum_file_path, 'w') as f:
                f.write(f"{expected_checksum}  {mock_filepath}\n")

            with patch('checksum_checker.calculate_checksum', return_value=actual_checksum), \
                 patch('sys.stdout', new=self.mock_stdout): # Capture print output
                result = checksum_checker.verify_checksum_file(test_file_path)
            
            self.assertFalse(result)
            self.assertIn("Integrity check FAILED", self.mock_stdout.getvalue())
            self.assertIn(f"Expected: {expected_checksum}", self.mock_stdout.getvalue())
            self.assertIn(f"Actual:   {actual_checksum}", self.mock_stdout.getvalue())

    def test_verify_checksum_file_not_found(self):
        # Mock rationale: Simulates a missing checksum file without actual file system interaction.
        # Tests error handling and sys.exit.
        with patch('os.path.exists', return_value=False), \
             self.assertRaises(SystemExit) as cm:
            checksum_checker.verify_checksum_file("some_file.txt")
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Checksum file not found", self.mock_stderr.getvalue())

    def test_verify_checksum_file_malformed_empty(self):
        # Mock rationale: Uses temp files to create an empty checksum file.
        # Tests robust parsing and error handling.
        mock_filepath = "malformed_empty_file.txt"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file_path = os.path.join(tmpdir, mock_filepath)
            checksum_file_path = f"{test_file_path}.sha256"

            # Create dummy files
            with open(test_file_path, 'w') as f:
                f.write("some content")
            with open(checksum_file_path, 'w') as f:
                f.write("\n") # Empty content

            with patch('checksum_checker.calculate_checksum', return_value="dummy_hash"), \
                 patch('sys.stderr', new=self.mock_stderr), \
                 self.assertRaises(SystemExit) as cm:
                checksum_checker.verify_checksum_file(test_file_path)
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Checksum file", self.mock_stderr.getvalue())
            self.assertIn("is empty or malformed", self.mock_stderr.getvalue())

    def test_verify_checksum_file_malformed_invalid_format(self):
        # Mock rationale: Uses temp files to create a malformed checksum file.
        # Tests robust parsing and error handling.
        mock_filepath = "malformed_file.txt"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file_path = os.path.join(tmpdir, mock_filepath)
            checksum_file_path = f"{test_file_path}.sha256"

            # Create dummy files
            with open(test_file_path, 'w') as f:
                f.write("some content")
            with open(checksum_file_path, 'w') as f:
                f.write("justahashnofilename\n") # Malformed content

            with patch('checksum_checker.calculate_checksum', return_value="dummy_hash"), \
                 patch('sys.stderr', new=self.mock_stderr), \
                 self.assertRaises(SystemExit) as cm:
                checksum_checker.verify_checksum_file(test_file_path)
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Checksum file", self.mock_stderr.getvalue())
            self.assertIn("has an invalid format", self.mock_stderr.getvalue())

    def test_verify_checksum_file_io_error_reading_checksum_file(self):
        # Mock rationale: Simulates an IOError during checksum file reading.
        # Tests error handling and sys.exit.
        mock_filepath = "test_file.txt"
        checksum_filepath = f"{mock_filepath}.sha256"

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', side_effect=IOError("Checksum file locked")), \
             self.assertRaises(SystemExit) as cm: # Expect sys.exit(1)
            checksum_checker.verify_checksum_file(mock_filepath)
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error reading checksum file", self.mock_stderr.getvalue())
        self.assertIn("Checksum file locked", self.mock_stderr.getvalue())

    def test_main_generate_command(self):
        # Mock rationale: Mocks argparse and the core function to test CLI dispatch.
        # Ensures the correct function is called with the correct arguments.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args, \
             patch('checksum_checker.generate_checksum_file') as mock_generate:
            
            mock_parse_args.return_value = argparse.Namespace(command='generate', filepath='test.txt')
            checksum_checker.main()
            mock_generate.assert_called_once_with('test.txt')

    def test_main_verify_command_success(self):
        # Mock rationale: Mocks argparse and the core function to test CLI dispatch.
        # Ensures the correct function is called and success path is handled.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args, \
             patch('checksum_checker.verify_checksum_file', return_value=True) as mock_verify:
            
            mock_parse_args.return_value = argparse.Namespace(command='verify', filepath='test.txt')
            checksum_checker.main()
            mock_verify.assert_called_once_with('test.txt')

    def test_main_verify_command_failure(self):
        # Mock rationale: Mocks argparse and the core function to test CLI dispatch.
        # Ensures the correct function is called and failure path (sys.exit(1)) is handled.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args, \
             patch('checksum_checker.verify_checksum_file', return_value=False) as mock_verify, \
             self.assertRaises(SystemExit) as cm:
            
            mock_parse_args.return_value = argparse.Namespace(command='verify', filepath='test.txt')
            checksum_checker.main()
            mock_verify.assert_called_once_with('test.txt')
            self.assertEqual(cm.exception.code, 1)

    def test_verify_checksum_file_filename_mismatch_warning(self):
        # Mock rationale: Uses temp files to simulate a scenario where the filename in the checksum
        # file doesn't match the provided filename, but the hash itself is correct.
        mock_filepath = "actual_file.txt"
        checksum_filename_in_file = "different_name.txt"
        mock_checksum = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file_path = os.path.join(tmpdir, mock_filepath)
            checksum_file_path = f"{test_file_path}.sha256"

            # Create dummy files
            with open(test_file_path, 'w') as f:
                f.write("some content")
            with open(checksum_file_path, 'w') as f:
                f.write(f"{mock_checksum}  {checksum_filename_in_file}\n")

            with patch('checksum_checker.calculate_checksum', return_value=mock_checksum), \
                 patch('sys.stdout', new=self.mock_stdout), \
                 patch('sys.stderr', new=self.mock_stderr): # Capture stderr for warning
                result = checksum_checker.verify_checksum_file(test_file_path)
            
            self.assertTrue(result) # Should still pass if checksum matches
            self.assertIn("Integrity check PASSED", self.mock_stdout.getvalue())
            self.assertIn("Warning: Filename in checksum file", self.mock_stderr.getvalue())
            self.assertIn(f"'{checksum_filename_in_file}' does not match provided file ('{mock_filepath}')", self.mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
