import unittest
import os
import json
import hashlib
from unittest.mock import patch, mock_open
from io import BytesIO

# Import the functions to be tested
from src.checksum_checker import (
    calculate_file_checksum,
    generate_manifest,
    verify_manifest
)

class TestChecksumChecker(unittest.TestCase):

    def test_calculate_file_checksum(self):
        # Mock rationale: We don't want to hit the actual filesystem. We simulate file content using BytesIO.
        mock_file_content = b"This is a test file content."
        expected_sha256 = hashlib.sha256(mock_file_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            checksum = calculate_file_checksum("dummy_path/test.txt")
            self.assertEqual(checksum, expected_sha256)
            m_open.assert_called_once_with("dummy_path/test.txt", 'rb')

        # Test with a different algorithm (md5)
        expected_md5 = hashlib.md5(mock_file_content).hexdigest()
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            checksum = calculate_file_checksum("dummy_path/test.txt", algorithm='md5')
            self.assertEqual(checksum, expected_md5)

    def test_calculate_file_checksum_file_not_found(self):
        # Mock rationale: Simulate a FileNotFoundError when trying to open a file.
        with patch('builtins.open', side_effect=FileNotFoundError) as m_open:
            checksum = calculate_file_checksum("non_existent_path/test.txt")
            self.assertIsNone(checksum)
            m_open.assert_called_once_with("non_existent_path/test.txt", 'rb')

    @patch('src.checksum_checker.calculate_file_checksum')
    @patch('os.walk')
    @patch('os.path.isdir', return_value=True) # Mock rationale: Ensure directory is considered valid
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_manifest(self, m_open, m_isdir, m_walk, m_calculate_checksum):
        # Mock rationale:
        # - os.path.isdir: Simulate the input directory existing.
        # - os.walk: Simulate directory structure without actual files.
        # - calculate_file_checksum: Avoid actual file reading and hashing, return predictable values.
        # - builtins.open: Capture the manifest written to the output file.

        mock_dir = "/mock/repo"
        mock_output_file = "/mock/repo/manifest.json"

        # Simulate directory structure
        m_walk.return_value = [
            (mock_dir, [], ["file1.txt", "file2.md"]),
            (os.path.join(mock_dir, "subdir"), [], ["subfile.py"])
        ]

        # Simulate checksums
        m_calculate_checksum.side_effect = [
            "checksum_file1",
            "checksum_file2",
            "checksum_subfile"
        ]

        expected_manifest = {
            "file1.txt": "checksum_file1",
            "file2.md": "checksum_file2",
            "subdir/subfile.py": "checksum_subfile"
        }

        result_manifest = generate_manifest(mock_dir, mock_output_file)

        self.assertEqual(result_manifest, expected_manifest)
        m_isdir.assert_called_once_with(mock_dir)
        m_walk.assert_called_once_with(mock_dir)
        self.assertEqual(m_calculate_checksum.call_count, 3) # One for each file
        m_open.assert_called_once_with(mock_output_file, 'w')
        
        # Verify the content written to the manifest file
        written_content = m_open().write.call_args[0][0]
        self.assertEqual(json.loads(written_content), expected_manifest)

    @patch('os.path.isdir', return_value=False) # Mock rationale: Simulate directory not found
    def test_generate_manifest_dir_not_found(self, m_isdir):
        result = generate_manifest("/non_existent_dir", "manifest.json")
        self.assertIsNone(result)
        m_isdir.assert_called_once_with("/non_existent_dir")

    @patch('src.checksum_checker.calculate_file_checksum')
    @patch('os.walk')
    @patch('os.path.exists', return_value=True) # Mock rationale: Manifest file exists
    @patch('os.path.isdir', return_value=True) # Mock rationale: Directory exists
    @patch('builtins.open', new_callable=mock_open)
    def test_verify_manifest_success(self, m_open, m_isdir, m_exists, m_walk, m_calculate_checksum):
        # Mock rationale:
        # - os.path.exists: Ensure manifest file is "found".
        # - os.path.isdir: Ensure target directory is "found".
        # - os.walk: Simulate directory structure.
        # - calculate_file_checksum: Return predictable checksums for current files.
        # - builtins.open: Simulate reading the manifest file.

        mock_dir = "/mock/repo"
        mock_manifest_file = "/mock/repo/manifest.json"

        # Simulate existing manifest content
        expected_manifest_content = {
            "file1.txt": "checksum_file1",
            "file2.md": "checksum_file2"
        }
        m_open.side_effect = [
            mock_open(read_data=json.dumps(expected_manifest_content)).return_value # For reading manifest
        ]

        # Simulate current directory structure and checksums
        m_walk.return_value = [
            (mock_dir, [], ["file1.txt", "file2.md"])
        ]
        m_calculate_checksum.side_effect = [
            "checksum_file1", # For file1.txt
            "checksum_file2"  # For file2.md
        ]

        result = verify_manifest(mock_dir, mock_manifest_file)
        self.assertTrue(result)
        m_exists.assert_called_once_with(mock_manifest_file)
        m_isdir.assert_called_once_with(mock_dir)
        m_open.assert_called_once_with(mock_manifest_file, 'r')
        m_walk.assert_called_once_with(mock_dir)
        self.assertEqual(m_calculate_checksum.call_count, 2)

    @patch('src.checksum_checker.calculate_file_checksum')
    @patch('os.walk')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_verify_manifest_missing_file(self, m_open, m_isdir, m_exists, m_walk, m_calculate_checksum):
        mock_dir = "/mock/repo"
        mock_manifest_file = "/mock/repo/manifest.json"

        expected_manifest_content = {
            "file1.txt": "checksum_file1",
            "file2.md": "checksum_file2"
        }
        m_open.side_effect = [
            mock_open(read_data=json.dumps(expected_manifest_content)).return_value
        ]

        # Simulate one file missing in current directory
        m_walk.return_value = [
            (mock_dir, [], ["file1.txt"])
        ]
        m_calculate_checksum.side_effect = [
            "checksum_file1"
        ]

        result = verify_manifest(mock_dir, mock_manifest_file)
        self.assertFalse(result)
        self.assertEqual(m_calculate_checksum.call_count, 1) # Only one file was found and hashed

    @patch('src.checksum_checker.calculate_file_checksum')
    @patch('os.walk')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_verify_manifest_modified_file(self, m_open, m_isdir, m_exists, m_walk, m_calculate_checksum):
        mock_dir = "/mock/repo"
        mock_manifest_file = "/mock/repo/manifest.json"

        expected_manifest_content = {
            "file1.txt": "checksum_file1_original",
            "file2.md": "checksum_file2"
        }
        m_open.side_effect = [
            mock_open(read_data=json.dumps(expected_manifest_content)).return_value
        ]

        # Simulate one file having a different checksum
        m_walk.return_value = [
            (mock_dir, [], ["file1.txt", "file2.md"])
        ]
        m_calculate_checksum.side_effect = [
            "checksum_file1_modified", # This one is different
            "checksum_file2"
        ]

        result = verify_manifest(mock_dir, mock_manifest_file)
        self.assertFalse(result)
        self.assertEqual(m_calculate_checksum.call_count, 2)

    @patch('src.checksum_checker.calculate_file_checksum')
    @patch('os.walk')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_verify_manifest_new_file(self, m_open, m_isdir, m_exists, m_walk, m_calculate_checksum):
        mock_dir = "/mock/repo"
        mock_manifest_file = "/mock/repo/manifest.json"

        expected_manifest_content = {
            "file1.txt": "checksum_file1"
        }
        m_open.side_effect = [
            mock_open(read_data=json.dumps(expected_manifest_content)).return_value
        ]

        # Simulate an extra file in the current directory
        m_walk.return_value = [
            (mock_dir, [], ["file1.txt", "new_file.log"])
        ]
        m_calculate_checksum.side_effect = [
            "checksum_file1",
            "checksum_new_file"
        ]

        result = verify_manifest(mock_dir, mock_manifest_file)
        self.assertFalse(result)
        self.assertEqual(m_calculate_checksum.call_count, 2)

    @patch('os.path.exists', return_value=False) # Mock rationale: Simulate the manifest file not existing.
    @patch('os.path.isdir', return_value=True)
    def test_verify_manifest_file_not_found(self, m_isdir, m_exists):
        result = verify_manifest("/mock/repo", "/mock/repo/non_existent_manifest.json")
        self.assertFalse(result)
        m_exists.assert_called_once_with("/mock/repo/non_existent_manifest.json")
        m_isdir.assert_called_once_with("/mock/repo")

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=False) # Mock rationale: Simulate the directory not existing.
    def test_verify_manifest_dir_not_found(self, m_isdir, m_exists):
        result = verify_manifest("/non_existent_dir", "/mock/repo/manifest.json")
        self.assertFalse(result)
        m_exists.assert_called_once_with("/mock/repo/manifest.json")
        m_isdir.assert_called_once_with("/non_existent_dir")

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.open', side_effect=IOError("Permission denied")) # Mock rationale: Simulate an IOError when reading manifest
    def test_verify_manifest_io_error_reading_manifest(self, m_open, m_isdir, m_exists):
        result = verify_manifest("/mock/repo", "/mock/repo/manifest.json")
        self.assertFalse(result)
        m_open.assert_called_once_with("/mock/repo/manifest.json", 'r')

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json') # Mock rationale: Simulate invalid JSON in manifest
    def test_verify_manifest_json_decode_error(self, m_open, m_isdir, m_exists):
        result = verify_manifest("/mock/repo", "/mock/repo/manifest.json")
        self.assertFalse(result)
        m_open.assert_called_once_with("/mock/repo/manifest.json", 'r')
