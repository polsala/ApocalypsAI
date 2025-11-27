import unittest
import os
import json
import tempfile
import shutil
import hashlib
from unittest.mock import patch, mock_open
from src.checksum_keeper import (
    calculate_file_checksum,
    calculate_directory_checksums,
    save_manifest,
    load_manifest,
    generate_manifest_cli,
    verify_manifest_cli
)

class TestChecksumKeeper(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.manifest_path = os.path.join(self.test_dir, "test_manifest.json")

        # Create some dummy files
        self.file1_path = os.path.join(self.test_dir, "file1.txt")
        self.file2_path = os.path.join(self.test_dir, "subdir", "file2.log")
        self.file3_path = os.path.join(self.test_dir, "subdir", "subsubdir", "file3.json")

        os.makedirs(os.path.dirname(self.file2_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.file3_path), exist_ok=True)

        with open(self.file1_path, "w") as f:
            f.write("content of file 1")
        with open(self.file2_path, "w") as f:
            f.write("log entry one\nlog entry two")
        with open(self.file3_path, "w") as f:
            f.write('{"key": "value", "number": 123}')

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_calculate_file_checksum_md5(self):
        # Test MD5 checksum calculation
        checksum = calculate_file_checksum(self.file1_path, algorithm='md5')
        self.assertEqual(checksum, hashlib.md5(b"content of file 1").hexdigest())

    def test_calculate_file_checksum_sha256(self):
        # Test SHA256 checksum calculation
        checksum = calculate_file_checksum(self.file1_path, algorithm='sha256')
        self.assertEqual(checksum, hashlib.sha256(b"content of file 1").hexdigest())

    def test_calculate_directory_checksums(self):
        # Test calculating checksums for an entire directory
        checksums = calculate_directory_checksums(self.test_dir, algorithm='md5')
        self.assertIn("file1.txt", checksums)
        self.assertIn(os.path.join("subdir", "file2.log"), checksums)
        self.assertIn(os.path.join("subdir", "subsubdir", "file3.json"), checksums)

        self.assertEqual(checksums["file1.txt"], hashlib.md5(b"content of file 1").hexdigest())
        self.assertEqual(checksums[os.path.join("subdir", "file2.log")], hashlib.md5(b"log entry one\nlog entry two").hexdigest())

    def test_calculate_directory_checksums_non_existent_dir(self):
        # Test error handling for non-existent directory
        with self.assertRaises(FileNotFoundError):
            calculate_directory_checksums("/non/existent/path", algorithm='sha256')

    def test_save_and_load_manifest(self):
        # Test saving and loading a manifest file
        test_data = {
            "generated_at": "2023-10-27T10:00:00",
            "algorithm": "sha256",
            "checksums": {
                "fileA.txt": "abc",
                "fileB.txt": "def"
            }
        }
        save_manifest(test_data, self.manifest_path)
        loaded_data = load_manifest(self.manifest_path)
        self.assertEqual(loaded_data, test_data)

    def test_load_manifest_non_existent_file(self):
        # Test error handling for non-existent manifest file
        with self.assertRaises(FileNotFoundError):
            load_manifest("/non/existent/manifest.json")

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_generate_manifest_cli_success(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.exit is called on success/failure in CLI,
        # so we mock it to prevent the test runner from exiting.
        # sys.stdout/stderr are mocked to capture printed output.
        generate_manifest_cli([self.test_dir, self.manifest_path, '--algorithm', 'md5'])
        mock_exit.assert_not_called() # Should not exit on success
        self.assertIn("Manifest saved to", mock_stdout.getvalue())
        self.assertTrue(os.path.exists(self.manifest_path))
        manifest = load_manifest(self.manifest_path)
        self.assertEqual(manifest['algorithm'], 'md5')
        self.assertIn("file1.txt", manifest['checksums'])

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_generate_manifest_cli_invalid_algorithm(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.exit is called on success/failure in CLI,
        # so we mock it to prevent the test runner from exiting.
        # sys.stdout/stderr are mocked to capture printed output.
        generate_manifest_cli([self.test_dir, self.manifest_path, '--algorithm', 'sha1'])
        mock_exit.assert_called_with(1)
        self.assertIn("Error: Invalid algorithm", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_verify_manifest_cli_success(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.exit is called on success/failure in CLI,
        # so we mock it to prevent the test runner from exiting.
        # sys.stdout/stderr are mocked to capture printed output.
        # First, generate a manifest
        generate_manifest_cli([self.test_dir, self.manifest_path, '--algorithm', 'sha256'])
        mock_exit.reset_mock() # Reset mock_exit for the verify call

        # Then, verify it
        verify_manifest_cli([self.test_dir, self.manifest_path])
        mock_exit.assert_not_called() # Should not exit on success
        self.assertIn("All files verified successfully!", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_verify_manifest_cli_mismatched_file(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.exit is called on success/failure in CLI,
        # so we mock it to prevent the test runner from exiting.
        # sys.stdout/stderr are mocked to capture printed output.
        # Generate manifest
        generate_manifest_cli([self.test_dir, self.manifest_path])
        mock_exit.reset_mock()

        # Modify a file
        with open(self.file1_path, "w") as f:
            f.write("modified content of file 1")

        # Verify
        verify_manifest_cli([self.test_dir, self.manifest_path])
        mock_exit.assert_called_with(1) # Should exit with 1 due to discrepancies
        self.assertIn("files had mismatched checksums (modified)", mock_stdout.getvalue())
        self.assertIn("file1.txt", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_verify_manifest_cli_missing_file(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.exit is called on success/failure in CLI,
        # so we mock it to prevent the test runner from exiting.
        # sys.stdout/stderr are mocked to capture printed output.
        # Generate manifest
        generate_manifest_cli([self.test_dir, self.manifest_path])
        mock_exit.reset_mock()

        # Delete a file
        os.remove(self.file2_path)

        # Verify
        verify_manifest_cli([self.test_dir, self.manifest_path])
        mock_exit.assert_called_with(1)
        self.assertIn("files missing (in manifest but not in directory)", mock_stdout.getvalue())
        self.assertIn(os.path.join("subdir", "file2.log"), mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_verify_manifest_cli_new_file(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.exit is called on success/failure in CLI,
        # so we mock it to prevent the test runner from exiting.
        # sys.stdout/stderr are mocked to capture printed output.
        # Generate manifest
        generate_manifest_cli([self.test_dir, self.manifest_path])
        mock_exit.reset_mock()

        # Add a new file
        new_file_path = os.path.join(self.test_dir, "new_file.txt")
        with open(new_file_path, "w") as f:
            f.write("brand new content")

        # Verify
        verify_manifest_cli([self.test_dir, self.manifest_path])
        mock_exit.assert_called_with(1)
        self.assertIn("new files found (not in manifest)", mock_stdout.getvalue())
        self.assertIn("new_file.txt", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_verify_manifest_cli_non_existent_manifest(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.exit is called on success/failure in CLI,
        # so we mock it to prevent the test runner from exiting.
        # sys.stdout/stderr are mocked to capture printed output.
        verify_manifest_cli([self.test_dir, "/non/existent/manifest.json"])
        mock_exit.assert_called_with(1)
        self.assertIn("Error: Manifest file not found", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_verify_manifest_cli_invalid_json(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.exit is called on success/failure in CLI,
        # so we mock it to prevent the test runner from exiting.
        # sys.stdout/stderr are mocked to capture printed output.
        # Create an invalid JSON manifest
        with open(self.manifest_path, "w") as f:
            f.write("{invalid json")

        verify_manifest_cli([self.test_dir, self.manifest_path])
        mock_exit.assert_called_with(1)
        self.assertIn("Error: Invalid JSON format", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('sys.exit')
    def test_verify_manifest_cli_algorithm_override_warning(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.exit is called on success/failure in CLI,
        # so we mock it to prevent the test runner from exiting.
        # sys.stdout/stderr are mocked to capture printed output.
        # Generate manifest with MD5
        generate_manifest_cli([self.test_dir, self.manifest_path, '--algorithm', 'md5'])
        mock_exit.reset_mock()

        # Verify with SHA256 override (should warn but use manifest's MD5)
        verify_manifest_cli([self.test_dir, self.manifest_path, '--algorithm', 'sha256'])
        mock_exit.assert_not_called()
        self.assertIn("Warning: Manifest was generated with 'md5', but verification requested with 'sha256'. Using manifest's algorithm for verification.", mock_stdout.getvalue())
        self.assertIn("All files verified successfully!", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
