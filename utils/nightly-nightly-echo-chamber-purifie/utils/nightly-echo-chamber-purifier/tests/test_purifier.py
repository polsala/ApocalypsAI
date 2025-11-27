import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from pathlib import Path
import hashlib

# Import the functions to be tested
from src.purifier import calculate_file_hash, find_duplicates

class TestPurifier(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash(self, mock_file_open):
        # Mock rationale: We need to simulate reading file content without actual disk I/O.
        # `mock_open` allows us to control what `open()` returns when called.
        mock_file_open.return_value.read.side_effect = [b"hello", b" world", b""]
        
        # Mock rationale: We need to ensure hashlib.sha256 produces a deterministic output
        # for a given input, without relying on its internal implementation details
        # or actual file content hashing.
        with patch('hashlib.sha256') as mock_sha256:
            mock_hasher = MagicMock()
            mock_hasher.hexdigest.return_value = "mocked_hash_value"
            mock_sha256.return_value = mock_hasher

            test_path = Path("/fake/path/to/file.txt")
            result_hash = calculate_file_hash(test_path)

            self.assertEqual(result_hash, "mocked_hash_value")
            mock_file_open.assert_called_once_with(test_path, 'rb')
            mock_hasher.update.assert_any_call(b"hello")
            mock_hasher.update.assert_any_call(b" world")
            mock_hasher.hexdigest.assert_called_once()

    @patch('src.purifier.calculate_file_hash')
    @patch('os.walk')
    @patch.object(Path, 'is_dir', return_value=True) # Mock rationale: Assume all provided paths are directories by default
    def test_find_duplicates_no_duplicates(self, mock_is_dir, mock_os_walk, mock_calculate_hash):
        # Mock rationale: `os.walk` is mocked to simulate a directory structure
        # without needing to create actual files or directories on disk.
        mock_os_walk.side_effect = [
            [
                ("/dir1", [], ["fileA.txt", "fileB.txt"]),
            ]
        ]
        # Mock rationale: `calculate_file_hash` is mocked to return predictable,
        # distinct hash values for each simulated file, ensuring no duplicates are found.
        mock_calculate_hash.side_effect = [
            "hash_A", "hash_B"
        ]

        test_dirs = [Path("/dir1")]
        duplicates = find_duplicates(test_dirs)
        self.assertEqual(duplicates, {})
        mock_calculate_hash.assert_any_call(Path("/dir1/fileA.txt"))
        mock_calculate_hash.assert_any_call(Path("/dir1/fileB.txt"))

    @patch('src.purifier.calculate_file_hash')
    @patch('os.walk')
    @patch.object(Path, 'is_dir', return_value=True)
    def test_find_duplicates_with_duplicates_in_same_dir(self, mock_is_dir, mock_os_walk, mock_calculate_hash):
        # Mock rationale: Simulate files in a directory, with some having identical content (hashes).
        mock_os_walk.side_effect = [
            [
                ("/dir1", [], ["file1.txt", "file2.txt", "file3.txt"]),
            ]
        ]
        # Mock rationale: Assign specific hashes to simulate duplicates.
        mock_calculate_hash.side_effect = [
            "hash_X",  # file1.txt
            "hash_Y",  # file2.txt
            "hash_X"   # file3.txt (duplicate of file1.txt)
        ]

        test_dirs = [Path("/dir1")]
        duplicates = find_duplicates(test_dirs)

        expected_duplicates = {
            "hash_X": [Path("/dir1/file1.txt"), Path("/dir1/file3.txt")]
        }
        self.assertEqual(duplicates, expected_duplicates)

    @patch('src.purifier.calculate_file_hash')
    @patch('os.walk')
    @patch.object(Path, 'is_dir', return_value=True)
    def test_find_duplicates_across_multiple_dirs(self, mock_is_dir, mock_os_walk, mock_calculate_hash):
        # Mock rationale: Simulate files across multiple directories, including duplicates.
        mock_os_walk.side_effect = [
            [
                ("/dirA", [], ["doc.txt", "image.png"]),
            ],
            [
                ("/dirB", [], ["report.pdf", "doc_copy.txt"]),
            ]
        ]
        # Mock rationale: Assign specific hashes to simulate duplicates across directories.
        mock_calculate_hash.side_effect = [
            "hash_doc",    # /dirA/doc.txt
            "hash_image",  # /dirA/image.png
            "hash_report", # /dirB/report.pdf
            "hash_doc"     # /dirB/doc_copy.txt (duplicate of /dirA/doc.txt)
        ]

        test_dirs = [Path("/dirA"), Path("/dirB")]
        duplicates = find_duplicates(test_dirs)

        expected_duplicates = {
            "hash_doc": [Path("/dirA/doc.txt"), Path("/dirB/doc_copy.txt")]
        }
        self.assertEqual(duplicates, expected_duplicates)

    @patch('src.purifier.calculate_file_hash')
    @patch('os.walk')
    @patch.object(Path, 'is_dir', return_value=True)
    def test_find_duplicates_empty_directory(self, mock_is_dir, mock_os_walk, mock_calculate_hash):
        # Mock rationale: Simulate an empty directory.
        mock_os_walk.side_effect = [
            [
                ("/empty_dir", [], []),
            ]
        ]
        test_dirs = [Path("/empty_dir")]
        duplicates = find_duplicates(test_dirs)
        self.assertEqual(duplicates, {})
        mock_calculate_hash.assert_not_called()

    @patch('src.purifier.calculate_file_hash')
    @patch('os.walk')
    def test_find_duplicates_non_existent_directory(self, mock_os_walk, mock_calculate_hash):
        # Mock rationale: Simulate a non-existent directory by not having os.walk yield anything for it.
        # We also need to mock Path.is_dir() to return False.
        mock_os_walk.return_value = [] # No files walked
        
        # Mock rationale: Simulate Path.is_dir() returning False for a non-existent path.
        mock_path_is_dir = MagicMock(return_value=False)
        with patch.object(Path, 'is_dir', new=mock_path_is_dir):
            test_dirs = [Path("/non_existent_dir")]
            duplicates = find_duplicates(test_dirs)
            self.assertEqual(duplicates, {})
            mock_calculate_hash.assert_not_called()
            mock_path_is_dir.assert_called_once()

    @patch('src.purifier.calculate_file_hash')
    @patch('os.walk')
    @patch.object(Path, 'is_dir', return_value=True)
    def test_find_duplicates_with_subdirectories(self, mock_is_dir, mock_os_walk, mock_calculate_hash):
        # Mock rationale: Simulate a more complex directory structure with subdirectories.
        mock_os_walk.side_effect = [
            [
                ("/root", ["sub1", "sub2"], ["file_root.txt"]),
                ("/root/sub1", [], ["file_sub1.txt", "duplicate.txt"]),
                ("/root/sub2", [], ["file_sub2.txt", "another_duplicate.txt"]),
            ]
        ]
        # Mock rationale: Assign hashes to simulate duplicates across subdirectories.
        mock_calculate_hash.side_effect = [
            "hash_root",
            "hash_sub1",
            "hash_dup",  # /root/sub1/duplicate.txt
            "hash_sub2",
            "hash_dup"   # /root/sub2/another_duplicate.txt (duplicate of /root/sub1/duplicate.txt)
        ]

        test_dirs = [Path("/root")]
        duplicates = find_duplicates(test_dirs)

        expected_duplicates = {
            "hash_dup": [Path("/root/sub1/duplicate.txt"), Path("/root/sub2/another_duplicate.txt")]
        }
        self.assertEqual(duplicates, expected_duplicates)

    @patch('src.purifier.calculate_file_hash')
    @patch('os.walk')
    @patch.object(Path, 'is_dir', return_value=True)
    def test_find_duplicates_file_processing_error(self, mock_is_dir, mock_os_walk, mock_calculate_hash):
        # Mock rationale: Simulate an OSError during file processing (e.g., permission denied).
        mock_os_walk.side_effect = [
            [
                ("/dir", [], ["good_file.txt", "bad_file.txt"]),
            ]
        ]
        # Mock rationale: Make calculate_file_hash raise an OSError for one file.
        mock_calculate_hash.side_effect = [
            "hash_good",
            OSError("Permission denied")
        ]

        test_dirs = [Path("/dir")]
        # We expect the error to be printed, but the function should still return results for other files.
        # We can capture stderr if needed, but for now, just ensure it doesn't crash.
        duplicates = find_duplicates(test_dirs)
        self.assertEqual(duplicates, {}) # No duplicates found among the good files
        mock_calculate_hash.assert_any_call(Path("/dir/good_file.txt"))
        mock_calculate_hash.assert_any_call(Path("/dir/bad_file.txt"))
