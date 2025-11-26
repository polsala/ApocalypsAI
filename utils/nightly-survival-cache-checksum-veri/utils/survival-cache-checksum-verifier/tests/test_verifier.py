import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
import hashlib
from pathlib import Path

# Import the functions to be tested
from src.verifier import calculate_sha256, load_manifest, verify_cache

class TestVerifier(unittest.TestCase):

    # Mock rationale: We need to simulate file system interactions (reading files, checking existence)
    # without actually touching the disk, to ensure deterministic and offline tests.
    # `patch` is used to replace `open` and `os.path.exists` with mock objects.

    def test_calculate_sha256_success(self):
        mock_file_content = b"test content for checksum"
        expected_checksum = hashlib.sha256(mock_file_content).hexdigest()

        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
            checksum = calculate_sha256("dummy_path.txt")
            self.assertEqual(checksum, expected_checksum)
            mock_file.assert_called_once_with("dummy_path.txt", "rb")

    def test_calculate_sha256_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            checksum = calculate_sha256("non_existent_path.txt")
            self.assertEqual(checksum, "FILE_NOT_FOUND")

    def test_calculate_sha256_read_error(self):
        with patch("builtins.open", mock_open()) as mock_file:
            mock_file().read.side_effect = IOError("Disk full")
            checksum = calculate_sha256("error_path.txt")
            self.assertIn("ERROR: Disk full", checksum)

    def test_load_manifest_success(self):
        manifest_data = {"file1.txt": "checksum1", "dir/file2.txt": "checksum2"}
        mock_json_content = json.dumps(manifest_data)

        with patch("builtins.open", mock_open(read_data=mock_json_content)) as mock_file:
            with patch("os.path.exists", return_value=True): # Mock rationale: Ensure manifest file is considered existing
                manifest = load_manifest("manifest.json")
                self.assertEqual(manifest, manifest_data)
                mock_file.assert_called_once_with("manifest.json", "r")

    def test_load_manifest_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with patch("os.path.exists", return_value=False): # Mock rationale: Simulate manifest file not existing
                manifest = load_manifest("non_existent_manifest.json")
                self.assertEqual(manifest, {})

    def test_load_manifest_invalid_json(self):
        mock_json_content = "{invalid json"
        with patch("builtins.open", mock_open(read_data=mock_json_content)):
            with patch("os.path.exists", return_value=True): # Mock rationale: Simulate manifest file existing
                manifest = load_manifest("invalid.json")
                self.assertEqual(manifest, {})

    def test_load_manifest_invalid_format(self):
        mock_json_content = json.dumps(["list", "not", "dict"])
        with patch("builtins.open", mock_open(read_data=mock_json_content)):
            with patch("os.path.exists", return_value=True): # Mock rationale: Simulate manifest file existing
                manifest = load_manifest("invalid_format.json")
                self.assertEqual(manifest, {})

        mock_json_content = json.dumps({"file1.txt": 123}) # Value not string
        with patch("builtins.open", mock_open(read_data=mock_json_content)):
            with patch("os.path.exists", return_value=True): # Mock rationale: Simulate manifest file existing
                manifest = load_manifest("invalid_format2.json")
                self.assertEqual(manifest, {})

    @patch("os.path.isdir", return_value=True) # Mock rationale: Simulate the cache directory existing
    @patch("os.path.exists") # Mock rationale: Control existence of individual files in the cache
    @patch("src.verifier.calculate_sha256") # Mock rationale: Avoid actual file reading during verification
    @patch("builtins.print") # Mock rationale: Capture print statements for assertion
    def test_verify_cache_all_ok(self, mock_print, mock_calculate_sha256, mock_os_path_exists, mock_os_isdir):
        manifest = {
            "file1.txt": "checksum_a",
            "subdir/file2.txt": "checksum_b"
        }
        cache_dir = "/mock/cache"

        # Configure mocks for individual file existence and checksum calculation
        mock_os_path_exists.side_effect = lambda path: path in [
            os.path.join(cache_dir, "file1.txt"),
            os.path.join(cache_dir, "subdir/file2.txt")
        ]
        mock_calculate_sha256.side_effect = ["checksum_a", "checksum_b"]

        result = verify_cache(cache_dir, manifest)
        self.assertTrue(result)
        self.assertEqual(mock_calculate_sha256.call_count, 2)
        mock_print.assert_any_call("    OK: Checksum matches for 'file1.txt'.")
        mock_print.assert_any_call("    OK: Checksum matches for 'subdir/file2.txt'.")
        mock_print.assert_any_call("Verifying cache in '/mock/cache'...")


    @patch("os.path.isdir", return_value=True) # Mock rationale: Simulate the cache directory existing
    @patch("os.path.exists")
    @patch("src.verifier.calculate_sha256")
    @patch("builtins.print")
    def test_verify_cache_missing_file(self, mock_print, mock_calculate_sha256, mock_os_path_exists, mock_os_isdir):
        manifest = {
            "file1.txt": "checksum_a",
            "subdir/file2.txt": "checksum_b"
        }
        cache_dir = "/mock/cache"

        # file1.txt exists, file2.txt does not
        mock_os_path_exists.side_effect = lambda path: path == os.path.join(cache_dir, "file1.txt")
        mock_calculate_sha256.return_value = "checksum_a" # Only called for file1.txt

        result = verify_cache(cache_dir, manifest)
        self.assertFalse(result)
        self.assertEqual(mock_calculate_sha256.call_count, 1) # Only called for the existing file
        mock_print.assert_any_call("    MISSING: File 'subdir/file2.txt' not found in cache.")
        mock_print.assert_any_call("    OK: Checksum matches for 'file1.txt'.")

    @patch("os.path.isdir", return_value=True) # Mock rationale: Simulate the cache directory existing
    @patch("os.path.exists", return_value=True) # Mock rationale: All files are considered existing
    @patch("src.verifier.calculate_sha256")
    @patch("builtins.print")
    def test_verify_cache_corrupted_file(self, mock_print, mock_calculate_sha256, mock_os_path_exists, mock_os_isdir):
        manifest = {
            "file1.txt": "checksum_a",
            "subdir/file2.txt": "checksum_b"
        }
        cache_dir = "/mock/cache"

        # file1.txt matches, file2.txt has wrong checksum
        mock_calculate_sha256.side_effect = ["checksum_a", "wrong_checksum_b"]

        result = verify_cache(cache_dir, manifest)
        self.assertFalse(result)
        self.assertEqual(mock_calculate_sha256.call_count, 2)
        mock_print.assert_any_call("    OK: Checksum matches for 'file1.txt'.")
        mock_print.assert_any_call("    CORRUPTED: Checksum mismatch for 'subdir/file2.txt'.")
        mock_print.assert_any_call("      Expected: checksum_b")
        mock_print.assert_any_call("      Actual:   wrong_checksum_b")

    @patch("os.path.isdir", return_value=False) # Mock rationale: Simulate the cache directory not existing
    @patch("builtins.print")
    def test_verify_cache_dir_not_found(self, mock_print, mock_os_isdir):
        manifest = {"file1.txt": "checksum_a"}
        cache_dir = "/non_existent_cache"
        result = verify_cache(cache_dir, manifest)
        self.assertFalse(result)
        mock_print.assert_any_call("Error: Cache directory '/non_existent_cache' does not exist.")

    @patch("os.path.isdir", return_value=True) # Mock rationale: Simulate the cache directory existing
    @patch("builtins.print")
    def test_verify_cache_empty_manifest(self, mock_print, mock_os_isdir):
        manifest = {}
        cache_dir = "/mock/cache"
        result = verify_cache(cache_dir, manifest)
        self.assertTrue(result) # Empty manifest means nothing to verify, so it's "OK"
        mock_print.assert_any_call("Warning: Manifest is empty. No files to verify.")

    @patch("argparse.ArgumentParser.parse_args", return_value=MagicMock(cache_directory="/mock/cache", manifest_file="/mock/manifest.json"))
    @patch("src.verifier.load_manifest", return_value={"file1.txt": "checksum_a"})
    @patch("src.verifier.verify_cache", return_value=True)
    @patch("builtins.print")
    @patch("sys.exit") # Mock rationale: Prevent actual exit during test
    def test_main_success(self, mock_exit, mock_print, mock_verify_cache, mock_load_manifest, mock_parse_args):
        from src.verifier import main
        main()
        mock_load_manifest.assert_called_once_with("/mock/manifest.json")
        mock_verify_cache.assert_called_once_with("/mock/cache", {"file1.txt": "checksum_a"})
        mock_print.assert_any_call("\nVerification SUCCESS: All files in the cache are intact!")
        mock_exit.assert_called_once_with(0)

    @patch("argparse.ArgumentParser.parse_args", return_value=MagicMock(cache_directory="/mock/cache", manifest_file="/mock/manifest.json"))
    @patch("src.verifier.load_manifest", return_value={"file1.txt": "checksum_a"})
    @patch("src.verifier.verify_cache", return_value=False)
    @patch("builtins.print")
    @patch("sys.exit")
    def test_main_failure(self, mock_exit, mock_print, mock_verify_cache, mock_load_manifest, mock_parse_args):
        from src.verifier import main
        main()
        mock_print.assert_any_call("\nVerification FAILED: Some files are missing or corrupted!")
        mock_exit.assert_called_once_with(1)

    @patch("argparse.ArgumentParser.parse_args", return_value=MagicMock(cache_directory="/mock/cache", manifest_file="/mock/manifest.json"))
    @patch("src.verifier.load_manifest", return_value={}) # Simulate empty/invalid manifest
    @patch("os.path.exists", return_value=True) # Mock rationale: Manifest file exists but is invalid
    @patch("builtins.print")
    @patch("sys.exit")
    def test_main_manifest_invalid_or_empty(self, mock_exit, mock_print, mock_os_path_exists, mock_load_manifest, mock_parse_args):
        from src.verifier import main
        main()
        mock_print.assert_any_call("Verification aborted due to invalid or empty manifest.")
        mock_exit.assert_called_once_with(1)

    @patch("argparse.ArgumentParser.parse_args", return_value=MagicMock(cache_directory="/mock/cache", manifest_file="/mock/manifest.json"))
    @patch("src.verifier.load_manifest", return_value={}) # Simulate manifest not found
    @patch("os.path.exists", return_value=False) # Mock rationale: Manifest file does not exist
    @patch("builtins.print")
    @patch("sys.exit")
    def test_main_manifest_not_found(self, mock_exit, mock_print, mock_os_path_exists, mock_load_manifest, mock_parse_args):
        from src.verifier import main
        main()
        mock_print.assert_any_call("Verification aborted as manifest file was not found.")
        mock_exit.assert_called_once_with(1)
