import unittest
import os
import json
import tempfile
import shutil
import hashlib
from pathlib import Path
from unittest.mock import patch, mock_open
from src.checksum_checker import calculate_sha256, generate_manifest, verify_manifest

class TestChecksumChecker(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = Path(tempfile.mkdtemp())
        self.manifest_path = self.test_dir / "test_manifest.json"

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def _create_file(self, relative_path: str, content: str):
        """Helper to create a file within the test directory."""
        filepath = self.test_dir / relative_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
        return filepath

    def test_calculate_sha256(self):
        # Test with a simple string
        filepath = self._create_file("test_file.txt", "hello world")
        expected_checksum = hashlib.sha256(b"hello world").hexdigest()
        self.assertEqual(calculate_sha256(filepath), expected_checksum)

        # Test with an empty file
        filepath_empty = self._create_file("empty_file.txt", "")
        expected_checksum_empty = hashlib.sha256(b"").hexdigest()
        self.assertEqual(calculate_sha256(filepath_empty), expected_checksum_empty)

        # Test with different content
        filepath_diff = self._create_file("diff_file.txt", "different content")
        expected_checksum_diff = hashlib.sha256(b"different content").hexdigest()
        self.assertEqual(calculate_sha256(filepath_diff), expected_checksum_diff)

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_generate_manifest_success(self, mock_print):
        # Create a directory structure
        self._create_file("file1.txt", "content1")
        self._create_file("subdir/file2.txt", "content2")
        self._create_file("subdir/subsubdir/file3.txt", "content3")

        # Expected checksums
        checksum1 = hashlib.sha256(b"content1").hexdigest()
        checksum2 = hashlib.sha256(b"content2").hexdigest()
        checksum3 = hashlib.sha256(b"content3").hexdigest()

        # Generate manifest
        exit_code = generate_manifest(self.test_dir, self.manifest_path)
        self.assertEqual(exit_code, 0)

        # Verify manifest content
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)

        expected_manifest = {
            "file1.txt": checksum1,
            "subdir/file2.txt": checksum2,
            "subdir/subsubdir/file3.txt": checksum3,
        }
        self.assertDictEqual(manifest, expected_manifest)

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_generate_manifest_empty_dir(self, mock_print):
        # Generate manifest for an empty directory
        exit_code = generate_manifest(self.test_dir, self.manifest_path)
        self.assertEqual(exit_code, 0)

        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
        self.assertDictEqual(manifest, {})

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_generate_manifest_non_existent_dir(self, mock_print):
        non_existent_dir = self.test_dir / "non_existent"
        exit_code = generate_manifest(non_existent_dir, self.manifest_path)
        self.assertEqual(exit_code, 1)
        self.assertFalse(self.manifest_path.exists())

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_verify_manifest_success(self, mock_print):
        # Create files and generate initial manifest
        self._create_file("fileA.txt", "alpha")
        self._create_file("dirB/fileC.txt", "beta")
        generate_manifest(self.test_dir, self.manifest_path)

        # Verify against the same state
        exit_code = verify_manifest(self.test_dir, self.manifest_path)
        self.assertEqual(exit_code, 0)
        mock_print.assert_any_call(f"\nVerification successful. All 2 files match the manifest.")

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_verify_manifest_file_changed(self, mock_print):
        # Create files and generate initial manifest
        self._create_file("fileA.txt", "alpha")
        generate_manifest(self.test_dir, self.manifest_path)

        # Modify a file
        self._create_file("fileA.txt", "gamma") # Changed content

        # Verify
        exit_code = verify_manifest(self.test_dir, self.manifest_path)
        self.assertEqual(exit_code, 1)
        mock_print.assert_any_call("\nVerification found discrepancies:")
        # Check that the message contains "CHANGED" and the file name
        self.assertTrue(any("CHANGED: fileA.txt" in call.args[0] for call in mock_print.call_args_list if call.args))


    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_verify_manifest_file_missing(self, mock_print):
        # Create files and generate initial manifest
        file_to_delete = self._create_file("fileB.txt", "beta")
        self._create_file("fileA.txt", "alpha")
        generate_manifest(self.test_dir, self.manifest_path)

        # Delete a file
        os.remove(file_to_delete)

        # Verify
        exit_code = verify_manifest(self.test_dir, self.manifest_path)
        self.assertEqual(exit_code, 1)
        mock_print.assert_any_call("\nVerification found discrepancies:")
        mock_print.assert_any_call("- MISSING: fileB.txt")

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_verify_manifest_new_file(self, mock_print):
        # Create files and generate initial manifest
        self._create_file("fileA.txt", "alpha")
        generate_manifest(self.test_dir, self.manifest_path)

        # Add a new file
        self._create_file("fileD.txt", "delta")

        # Verify
        exit_code = verify_manifest(self.test_dir, self.manifest_path)
        self.assertEqual(exit_code, 1)
        mock_print.assert_any_call("\nVerification found discrepancies:")
        mock_print.assert_any_call("- NEW: fileD.txt")

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_verify_manifest_non_existent_dir(self, mock_print):
        # Create a dummy manifest
        self._create_file("file.txt", "content")
        generate_manifest(self.test_dir, self.manifest_path)

        non_existent_dir = self.test_dir / "non_existent"
        exit_code = verify_manifest(non_existent_dir, self.manifest_path)
        self.assertEqual(exit_code, 1)
        mock_print.assert_any_call(f"Error: Directory '{non_existent_dir}' does not exist or is not a directory.")

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_verify_manifest_non_existent_manifest(self, mock_print):
        exit_code = verify_manifest(self.test_dir, self.test_dir / "non_existent_manifest.json")
        self.assertEqual(exit_code, 1)
        mock_print.assert_any_call(f"Error: Manifest file '{self.test_dir / 'non_existent_manifest.json'}' does not exist.")

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_verify_manifest_invalid_json(self, mock_print):
        # Create an invalid JSON manifest
        self._create_file("test_manifest.json", "{invalid json")

        exit_code = verify_manifest(self.test_dir, self.manifest_path)
        self.assertEqual(exit_code, 1)
        # Check for error message containing the specific phrase
        self.assertTrue(any("Error: Invalid JSON in manifest file" in call.args[0] for call in mock_print.call_args_list if call.args))

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests for cleaner output.
    def test_verify_manifest_mixed_changes(self, mock_print):
        # Initial state
        self._create_file("file1.txt", "original1")
        self._create_file("file2.txt", "original2")
        self._create_file("file3.txt", "original3")
        generate_manifest(self.test_dir, self.manifest_path)

        # Introduce multiple changes
        self._create_file("file1.txt", "modified1") # Changed
        os.remove(self.test_dir / "file2.txt")      # Missing
        self._create_file("file4.txt", "new_file")  # New

        exit_code = verify_manifest(self.test_dir, self.manifest_path)
        self.assertEqual(exit_code, 1)
        mock_print.assert_any_call("\nVerification found discrepancies:")
        output_calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        self.assertIn("- MISSING: file2.txt", output_calls)
        self.assertIn("- NEW: file4.txt", output_calls)
        self.assertTrue(any("CHANGED: file1.txt" in s for s in output_calls))

if __name__ == '__main__':
    unittest.main()
