import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, mock_open
import sys

# Add the src directory to the path to import checksum_checker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import checksum_checker

class TestChecksumChecker(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.manifest_file = os.path.join(self.test_dir, "test_manifest.json")

        # Define some file contents and their expected SHA256 checksums
        self.file_contents = {
            "file1.txt": "The quick brown fox jumps over the lazy dog.",
            "subdir/file2.log": "Error: Something went wrong.\nWarning: Disk space low.",
            "empty.txt": ""
        }
        self.expected_checksums = {
            "empty.txt": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" # Actual SHA256 for empty string
        }

        # Populate the temporary directory with files
        for rel_path, content in self.file_contents.items():
            full_path = os.path.join(self.test_dir, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)
            # Calculate actual checksums for non-empty files and store them
            if rel_path != "empty.txt":
                self.expected_checksums[rel_path] = checksum_checker.calculate_sha256(full_path)

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_calculate_sha256(self):
        # Test with a known file and content
        filepath = os.path.join(self.test_dir, "file1.txt")
        self.assertEqual(checksum_checker.calculate_sha256(filepath), self.expected_checksums["file1.txt"])

        # Test with an empty file
        filepath = os.path.join(self.test_dir, "empty.txt")
        self.assertEqual(checksum_checker.calculate_sha256(filepath), self.expected_checksums["empty.txt"])

        # Test with a non-existent file
        self.assertIsNone(checksum_checker.calculate_sha256(os.path.join(self.test_dir, "non_existent.txt")))

    def test_generate_checksums(self):
        # Run the generate command
        return_code = checksum_checker.generate_checksums(self.test_dir, self.manifest_file)
        self.assertEqual(return_code, 0)

        # Check if the manifest file was created and contains correct data
        self.assertTrue(os.path.exists(self.manifest_file))
        with open(self.manifest_file, "r") as f:
            manifest = json.load(f)

        # Adjust expected checksums for relative paths
        expected_manifest = {
            "file1.txt": self.expected_checksums["file1.txt"],
            "subdir/file2.log": self.expected_checksums["subdir/file2.log"],
            "empty.txt": self.expected_checksums["empty.txt"]
        }
        self.assertDictEqual(manifest, expected_manifest)

    def test_verify_checksums_ok(self):
        # First, generate a manifest
        checksum_checker.generate_checksums(self.test_dir, self.manifest_file)

        # Then, verify without changes
        return_code = checksum_checker.verify_checksums(self.test_dir, self.manifest_file)
        self.assertEqual(return_code, 0) # Expect 0 for no issues

    def test_verify_checksums_modified_file(self):
        # Generate initial manifest
        checksum_checker.generate_checksums(self.test_dir, self.manifest_file)

        # Modify a file
        modified_filepath = os.path.join(self.test_dir, "file1.txt")
        with open(modified_filepath, "a") as f:
            f.write(" Appended new content.")
        
        # Verify and expect a non-zero return code (issues found)
        return_code = checksum_checker.verify_checksums(self.test_dir, self.manifest_file)
        self.assertEqual(return_code, 1)

    def test_verify_checksums_missing_file(self):
        # Generate initial manifest
        checksum_checker.generate_checksums(self.test_dir, self.manifest_file)

        # Remove a file
        os.remove(os.path.join(self.test_dir, "subdir", "file2.log"))

        # Verify and expect a non-zero return code (issues found)
        return_code = checksum_checker.verify_checksums(self.test_dir, self.manifest_file)
        self.assertEqual(return_code, 1)

    def test_verify_checksums_new_file(self):
        # Generate initial manifest
        checksum_checker.generate_checksums(self.test_dir, self.manifest_file)

        # Add a new file
        new_filepath = os.path.join(self.test_dir, "new_file.txt")
        with open(new_filepath, "w") as f:
            f.write("This is a brand new file.")
        
        # Verify and expect a zero return code (new files are not integrity issues)
        return_code = checksum_checker.verify_checksums(self.test_dir, self.manifest_file)
        self.assertEqual(return_code, 0)

    def test_verify_checksums_missing_directory(self):
        # Mock os.path.isdir to simulate missing directory
        # Mock rationale: Avoid actual file system interaction for negative case,
        # ensuring test determinism and speed without creating/deleting directories.
        with patch('os.path.isdir', return_value=False):
            return_code = checksum_checker.verify_checksums("/non/existent/dir", self.manifest_file)
            self.assertEqual(return_code, 1)

    def test_verify_checksums_missing_manifest(self):
        # Mock os.path.isfile to simulate missing manifest
        # Mock rationale: Avoid actual file system interaction for negative case,
        # ensuring test determinism and speed without creating/deleting files.
        with patch('os.path.isfile', return_value=False):
            return_code = checksum_checker.verify_checksums(self.test_dir, "/non/existent/manifest.json")
            self.assertEqual(return_code, 1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_verify_checksums_invalid_manifest_json(self, mock_json_load, mock_file_open):
        # Mock json.load to raise an error
        # Mock rationale: Simulate a corrupted or malformed JSON manifest file
        # without needing to create an actual invalid JSON file, ensuring test
        # determinism and focusing on the error handling logic.
        mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)
        
        # Ensure the manifest file is reported as existing for this test
        with patch('os.path.isfile', return_value=True):
            return_code = checksum_checker.verify_checksums(self.test_dir, self.manifest_file)
            self.assertEqual(return_code, 1)
            mock_file_open.assert_called_with(self.manifest_file, "r")
            mock_json_load.assert_called_once()

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_calculate_sha256_io_error(self, mock_file_open):
        # Mock open to raise an IOError
        # Mock rationale: Simulate a file that cannot be read due to permissions
        # or other I/O issues, ensuring test determinism and focusing on error handling.
        filepath = os.path.join(self.test_dir, "file1.txt")
        self.assertIsNone(checksum_checker.calculate_sha256(filepath))
        mock_file_open.assert_called_with(filepath, "rb")

    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_generate_command(self, mock_parse_args, mock_sys_exit):
        # Mock argparse to simulate 'generate' command arguments
        # Mock rationale: Test the main function's command dispatch without
        # actually running the full CLI, ensuring determinism and isolation.
        mock_parse_args.return_value = argparse.Namespace(
            command='generate',
            directory=self.test_dir,
            output=self.manifest_file
        )
        checksum_checker.main()
        mock_sys_exit.assert_called_with(0) # Expect success

    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_verify_command(self, mock_parse_args, mock_sys_exit):
        # Generate a manifest first for the verify command to have something to work with
        checksum_checker.generate_checksums(self.test_dir, self.manifest_file)

        # Mock argparse to simulate 'verify' command arguments
        # Mock rationale: Test the main function's command dispatch without
        # actually running the full CLI, ensuring determinism and isolation.
        mock_parse_args.return_value = argparse.Namespace(
            command='verify',
            directory=self.test_dir,
            manifest=self.manifest_file
        )
        checksum_checker.main()
        mock_sys_exit.assert_called_with(0) # Expect success

if __name__ == '__main__':
    unittest.main()
