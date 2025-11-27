import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
import sys

# Add the src directory to the path for importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import checksum_calculator

class TestChecksumCalculator(unittest.TestCase):

    def test_calculate_sha256_basic(self):
        # Mock rationale: Avoid actual file I/O for deterministic testing.
        # We simulate reading file content directly.
        mock_file_content = b"hello world"
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
            # The actual file path doesn't matter here as open is mocked
            checksum = checksum_calculator.calculate_sha256("dummy_path.txt")
            self.assertEqual(checksum, "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824")
            mock_file.assert_called_once_with("dummy_path.txt", "rb")

    def test_calculate_sha256_empty_file(self):
        # Mock rationale: Simulate an empty file.
        mock_file_content = b""
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            checksum = checksum_calculator.calculate_sha256("empty.txt")
            self.assertEqual(checksum, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

    def test_calculate_sha256_io_error(self):
        # Mock rationale: Simulate a file that cannot be opened/read.
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            checksum = checksum_calculator.calculate_sha256("unreadable.txt")
            self.assertIsNone(checksum)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('checksum_calculator.calculate_sha256')
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start + os.sep, '').replace(os.sep, '/')) # Mock relpath for consistent keys
    def test_generate_manifest_success(self, mock_relpath, mock_calculate_sha256, mock_open_file, mock_os_walk, mock_isdir):
        # Mock rationale:
        # - os.path.isdir: Simulate the target directory existing.
        # - os.walk: Simulate a directory structure with files.
        # - builtins.open: Capture the manifest content written to disk.
        # - checksum_calculator.calculate_sha256: Provide deterministic checksums for mocked files.
        # - os.path.relpath: Ensure consistent relative paths for manifest keys.

        test_dir = '/test_dir'
        mock_os_walk.return_value = [
            (test_dir, [], ['file1.txt', 'file2.md']),
            (os.path.join(test_dir, 'subdir'), [], ['subfile.py'])
        ]
        mock_calculate_sha256.side_effect = [
            "hash_file1", "hash_file2", "hash_subfile"
        ]

        output_manifest = 'manifest.json'

        # Capture stdout for verification
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            result = checksum_calculator.generate_manifest(test_dir, output_manifest)
            self.assertEqual(result, 0) # Expect success

            # Verify os.walk was called with the correct directory
            mock_os_walk.assert_called_once_with(test_dir)

            # Verify calculate_sha256 was called for each file
            mock_calculate_sha256.assert_any_call(os.path.join(test_dir, 'file1.txt'))
            mock_calculate_sha256.assert_any_call(os.path.join(test_dir, 'file2.md'))
            mock_calculate_sha256.assert_any_call(os.path.join(test_dir, 'subdir', 'subfile.py'))

            # Verify the manifest content written
            mock_open_file.assert_called_once_with(output_manifest, 'w')
            written_content = mock_open_file().write.call_args[0][0]
            manifest_data = json.loads(written_content)

            expected_manifest = {
                'file1.txt': 'hash_file1',
                'file2.md': 'hash_file2',
                'subdir/subfile.py': 'hash_subfile'
            }
            self.assertEqual(manifest_data, expected_manifest)
            mock_stdout.write.assert_any_call(f"Manifest generated successfully at '{output_manifest}' for directory '{test_dir}'.\n")

    @patch('os.path.isdir', return_value=False)
    def test_generate_manifest_dir_not_found(self, mock_isdir):
        # Mock rationale: Simulate the target directory not existing.
        test_dir = '/non_existent_dir'
        output_manifest = 'manifest.json'
        with patch('sys.stderr', new=MagicMock()) as mock_stderr:
            result = checksum_calculator.generate_manifest(test_dir, output_manifest)
            self.assertEqual(result, 1) # Expect failure
            mock_stderr.write.assert_any_call(f"Error: Directory '{test_dir}' not found.\n")

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    @patch('checksum_calculator.calculate_sha256')
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start + os.sep, '').replace(os.sep, '/')) # Mock relpath for consistent keys
    def test_verify_manifest_success(self, mock_relpath, mock_calculate_sha256, mock_os_walk, mock_open_file, mock_isfile, mock_isdir):
        # Mock rationale:
        # - os.path.isdir, os.path.isfile: Simulate directories and manifest file existing.
        # - builtins.open: Simulate reading the manifest file.
        # - os.walk: Simulate the current directory structure.
        # - checksum_calculator.calculate_sha256: Provide deterministic checksums for current files.
        # - os.path.relpath: Ensure consistent relative paths for manifest keys.

        test_dir = '/test_dir'
        # Mock the manifest file content
        mock_manifest_content = json.dumps({
            'file1.txt': 'hash_file1_expected',
            'file2.md': 'hash_file2_expected',
            'subdir/subfile.py': 'hash_subfile_expected'
        })
        # Configure mock_open for reading the manifest
        mock_open_file.side_effect = [
            mock_open(read_data=mock_manifest_content).return_value, # For reading manifest
            # No more calls to open for file content as calculate_sha256 is mocked
        ]

        mock_os_walk.return_value = [
            (test_dir, [], ['file1.txt', 'file2.md']),
            (os.path.join(test_dir, 'subdir'), [], ['subfile.py'])
        ]
        mock_calculate_sha256.side_effect = [
            "hash_file1_expected", "hash_file2_expected", "hash_subfile_expected" # All match
        ]

        manifest_path = 'manifest.json'

        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            result = checksum_calculator.verify_manifest(test_dir, manifest_path)
            self.assertEqual(result, 0) # Expect success
            mock_stdout.write.assert_any_call(f"Verification successful: All files in '{test_dir}' match the manifest '{manifest_path}'.\n")

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.walk')
    @patch('checksum_calculator.calculate_sha256')
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start + os.sep, '').replace(os.sep, '/')) # Mock relpath for consistent keys
    def test_verify_manifest_with_issues(self, mock_relpath, mock_calculate_sha256, mock_os_walk, mock_open_file, mock_isfile, mock_isdir):
        # Mock rationale: Simulate various discrepancies: missing, altered, new files.

        test_dir = '/test_dir'
        # Mock the manifest file content
        mock_manifest_content = json.dumps({
            'file1.txt': 'hash_file1_expected',
            'file2.md': 'hash_file2_expected', # This one will be altered
            'missing_file.txt': 'hash_missing_expected' # This one will be missing
        })
        mock_open_file.side_effect = [
            mock_open(read_data=mock_manifest_content).return_value,
        ]

        mock_os_walk.return_value = [
            (test_dir, [], ['file1.txt', 'file2.md', 'new_file.txt']), # new_file.txt is new
        ]
        mock_calculate_sha256.side_effect = [
            "hash_file1_expected", # Matches
            "hash_file2_altered",  # Does not match
            "hash_new_file"        # Checksum for new file
        ]

        manifest_path = 'manifest.json'

        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            result = checksum_calculator.verify_manifest(test_dir, manifest_path)
            self.assertEqual(result, 1) # Expect failure due to issues

            mock_stdout.write.assert_any_call(f"MISSING: File 'missing_file.txt' is missing from '{test_dir}'.\n")
            mock_stdout.write.assert_any_call(f"ALTERED: Checksum mismatch for 'file2.md'. Expected 'hash_file2_expected', got 'hash_file2_altered'.\n")
            mock_stdout.write.assert_any_call(f"NEW: File 'new_file.txt' found in '{test_dir}' but not in manifest.\n")
            mock_stdout.write.assert_any_call(f"Verification completed with issues for '{test_dir}' against '{manifest_path}'.\n")

    @patch('os.path.isdir', return_value=False)
    def test_verify_manifest_dir_not_found(self, mock_isdir):
        # Mock rationale: Simulate the target directory not existing.
        test_dir = '/non_existent_dir'
        manifest_path = 'manifest.json'
        with patch('sys.stderr', new=MagicMock()) as mock_stderr:
            result = checksum_calculator.verify_manifest(test_dir, manifest_path)
            self.assertEqual(result, 1)
            mock_stderr.write.assert_any_call(f"Error: Directory '{test_dir}' not found.\n")

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', side_effect=[False, True]) # First call for manifest_path, second for something else if needed
    def test_verify_manifest_file_not_found(self, mock_isfile, mock_isdir):
        # Mock rationale: Simulate the manifest file not existing.
        test_dir = '/test_dir'
        manifest_path = 'non_existent_manifest.json'
        with patch('sys.stderr', new=MagicMock()) as mock_stderr:
            result = checksum_calculator.verify_manifest(test_dir, manifest_path)
            self.assertEqual(result, 1)
            mock_stderr.write.assert_any_call(f"Error: Manifest file '{manifest_path}' not found.\n")

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_verify_manifest_invalid_json(self, mock_open_file, mock_isfile, mock_isdir):
        # Mock rationale: Simulate a corrupted manifest file with invalid JSON.
        mock_open_file.side_effect = [
            mock_open(read_data="this is not valid json").return_value,
        ]
        test_dir = '/test_dir'
        manifest_path = 'invalid.json'
        with patch('sys.stderr', new=MagicMock()) as mock_stderr:
            result = checksum_calculator.verify_manifest(test_dir, manifest_path)
            self.assertEqual(result, 1)
            mock_stderr.write.assert_any_call(f"Error: Invalid JSON in manifest file '{manifest_path}'.\n")

    @patch('sys.exit')
    @patch('sys.argv', ['checksum_calculator.py', 'generate', '/tmp/test_dir', 'output.json'])
    @patch('checksum_calculator.generate_manifest', return_value=0)
    def test_main_generate_command(self, mock_generate, mock_exit):
        # Mock rationale: Simulate command-line arguments and prevent actual sys.exit.
        checksum_calculator.main()
        mock_generate.assert_called_once_with('/tmp/test_dir', 'output.json')
        mock_exit.assert_called_once_with(0)

    @patch('sys.exit')
    @patch('sys.argv', ['checksum_calculator.py', 'verify', '/tmp/test_dir', 'manifest.json'])
    @patch('checksum_calculator.verify_manifest', return_value=0)
    def test_main_verify_command(self, mock_verify, mock_exit):
        # Mock rationale: Simulate command-line arguments and prevent actual sys.exit.
        checksum_calculator.main()
        mock_verify.assert_called_once_with('/tmp/test_dir', 'manifest.json')
        mock_exit.assert_called_once_with(0)

    @patch('sys.exit')
    @patch('sys.argv', ['checksum_calculator.py', 'invalid_command'])
    def test_main_invalid_command(self, mock_exit):
        # Mock rationale: Simulate an invalid command-line argument.
        with patch('sys.stderr', new=MagicMock()):
            checksum_calculator.main()
            mock_exit.assert_called_once_with(1)

    @patch('sys.exit')
    @patch('sys.argv', ['checksum_calculator.py'])
    def test_main_not_enough_args(self, mock_exit):
        # Mock rationale: Simulate not enough command-line arguments.
        with patch('sys.stderr', new=MagicMock()):
            checksum_calculator.main()
            mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
