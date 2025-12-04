import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import hashlib
from pathlib import Path

# Import the functions to be tested
from src.echo_recorder import take_snapshot, compare_snapshots, save_snapshot, load_snapshot

class TestEchoRecorder(unittest.TestCase):

    # Mock rationale: We need to simulate file system interactions (reading files, listing directories)
    # without actually touching the disk, to ensure deterministic and offline tests.
    # We mock Path.exists, Path.is_file, Path.is_dir, Path.rglob, and the open() function.
    # We also mock hashlib.sha256 to control hash values for specific content.

    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    @patch('pathlib.Path.is_file', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=False)
    @patch('pathlib.Path.exists', return_value=True)
    def test_take_snapshot_single_file(self, mock_exists, mock_is_dir, mock_is_file, mock_sha256, mock_open_func):
        # Mock rationale: Simulate a single file existing and its content for hashing.
        mock_file_content = b"file content"
        mock_open_func.return_value.__enter__.return_value.read.side_effect = [mock_file_content, b'']

        mock_digest = MagicMock()
        mock_digest.hexdigest.return_value = "mock_hash_123"
        mock_sha256.return_value = mock_digest

        mock_path = Path("/mock/path/file.txt")
        mock_path.name = "file.txt" # Mock the name attribute for relative path

        snapshot = take_snapshot(mock_path)

        self.assertEqual(snapshot, {"file.txt": "mock_hash_123"})
        mock_exists.assert_called_once_with()
        mock_is_file.assert_called_once_with()
        mock_open_func.assert_called_once_with(mock_path, 'rb')
        mock_sha256.assert_called_once()
        mock_digest.update.assert_called_once_with(mock_file_content)

    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    @patch('pathlib.Path.rglob')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.is_dir', return_value=True)
    @patch('pathlib.Path.exists', return_value=True)
    def test_take_snapshot_directory(self, mock_exists, mock_is_dir, mock_is_file, mock_rglob, mock_sha256, mock_open_func):
        # Mock rationale: Simulate a directory with multiple files and their contents.
        mock_dir_path = Path("/mock/dir")

        # Mock files within the directory
        mock_file1 = MagicMock(spec=Path)
        mock_file1.is_file.return_value = True
        mock_file1.relative_to.return_value = Path("sub/file1.txt")
        mock_file1.as_posix.return_value = "sub/file1.txt"
        mock_file1_content = b"content of file1"

        mock_file2 = MagicMock(spec=Path)
        mock_file2.is_file.return_value = True
        mock_file2.relative_to.return_value = Path("file2.txt")
        mock_file2.as_posix.return_value = "file2.txt"
        mock_file2_content = b"content of file2"

        # Mock a subdirectory that is not a file
        mock_subdir = MagicMock(spec=Path)
        mock_subdir.is_file.return_value = False

        mock_rglob.return_value = [mock_file1, mock_file2, mock_subdir]
        mock_is_file.side_effect = [True, True, False] # For mock_file1, mock_file2, mock_subdir

        # Mock open calls for each file
        mock_open_func.side_effect = [
            mock_open(read_data=mock_file1_content).return_value,
            mock_open(read_data=mock_file2_content).return_value
        ]

        # Mock hash calculations
        mock_digest1 = MagicMock()
        mock_digest1.hexdigest.return_value = "hash1"
        mock_digest2 = MagicMock()
        mock_digest2.hexdigest.return_value = "hash2"
        mock_sha256.side_effect = [MagicMock(return_value=mock_digest1), MagicMock(return_value=mock_digest2)]
        mock_digest1.update.return_value = None # Prevent actual update call
        mock_digest2.update.return_value = None # Prevent actual update call


        snapshot = take_snapshot(mock_dir_path)

        self.assertEqual(snapshot, {
            "sub/file1.txt": "hash1",
            "file2.txt": "hash2"
        })
        mock_exists.assert_called_once_with()
        mock_is_dir.assert_called_once_with()
        mock_rglob.assert_called_once_with('*')
        self.assertEqual(mock_open_func.call_count, 2)
        self.assertEqual(mock_sha256.call_count, 2)

    @patch('pathlib.Path.exists', return_value=False)
    def test_take_snapshot_path_not_found(self, mock_exists):
        # Mock rationale: Test error handling when the target path does not exist.
        with self.assertRaises(FileNotFoundError):
            take_snapshot(Path("/non/existent/path"))
        mock_exists.assert_called_once_with()

    def test_compare_snapshots_no_changes(self):
        # Mock rationale: Test comparison when snapshots are identical.
        snap1 = {"file1.txt": "hashA", "file2.txt": "hashB"}
        snap2 = {"file1.txt": "hashA", "file2.txt": "hashB"}
        changes = compare_snapshots(snap1, snap2)
        self.assertEqual(changes, {
            "new_files": [],
            "deleted_files": [],
            "modified_files": [],
            "unchanged_files": ["file1.txt", "file2.txt"]
        })

    def test_compare_snapshots_new_file(self):
        # Mock rationale: Test detection of a new file.
        snap1 = {"file1.txt": "hashA"}
        snap2 = {"file1.txt": "hashA", "file2.txt": "hashB"}
        changes = compare_snapshots(snap1, snap2)
        self.assertEqual(changes, {
            "new_files": ["file2.txt"],
            "deleted_files": [],
            "modified_files": [],
            "unchanged_files": ["file1.txt"]
        })

    def test_compare_snapshots_deleted_file(self):
        # Mock rationale: Test detection of a deleted file.
        snap1 = {"file1.txt": "hashA", "file2.txt": "hashB"}
        snap2 = {"file1.txt": "hashA"}
        changes = compare_snapshots(snap1, snap2)
        self.assertEqual(changes, {
            "new_files": [],
            "deleted_files": ["file2.txt"],
            "modified_files": [],
            "unchanged_files": ["file1.txt"]
        })

    def test_compare_snapshots_modified_file(self):
        # Mock rationale: Test detection of a modified file (hash change).
        snap1 = {"file1.txt": "hashA", "file2.txt": "hashB"}
        snap2 = {"file1.txt": "hashA", "file2.txt": "hashC"} # hashB -> hashC
        changes = compare_snapshots(snap1, snap2)
        self.assertEqual(changes, {
            "new_files": [],
            "deleted_files": [],
            "modified_files": ["file2.txt"],
            "unchanged_files": ["file1.txt"]
        })

    def test_compare_snapshots_mixed_changes(self):
        # Mock rationale: Test a scenario with multiple types of changes.
        snap1 = {"fileA": "hashA1", "fileB": "hashB1", "fileC": "hashC1"}
        snap2 = {"fileA": "hashA1", "fileB": "hashB2", "fileD": "hashD1"} # C deleted, B modified, D new
        changes = compare_snapshots(snap1, snap2)
        self.assertIn("fileD", changes["new_files"])
        self.assertIn("fileC", changes["deleted_files"])
        self.assertIn("fileB", changes["modified_files"])
        self.assertIn("fileA", changes["unchanged_files"])
        self.assertEqual(len(changes["new_files"]), 1)
        self.assertEqual(len(changes["deleted_files"]), 1)
        self.assertEqual(len(changes["modified_files"]), 1)
        self.assertEqual(len(changes["unchanged_files"]), 1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_snapshot(self, mock_json_dump, mock_open_func):
        # Mock rationale: Simulate saving a snapshot to a file without actual disk I/O.
        snapshot_data = {"file1.txt": "hashA"}
        output_path = Path("/mock/output.json")
        save_snapshot(snapshot_data, output_path)
        mock_open_func.assert_called_once_with(output_path, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with(snapshot_data, mock_open_func(), indent=2)

    @patch('builtins.open', new_callable=mock_open, read_data='{"file1.txt": "hashA"}')
    @patch('json.load', return_value={"file1.txt": "hashA"})
    @patch('pathlib.Path.exists', return_value=True)
    def test_load_snapshot(self, mock_exists, mock_json_load, mock_open_func):
        # Mock rationale: Simulate loading a snapshot from a file without actual disk I/O.
        input_path = Path("/mock/input.json")
        loaded_snapshot = load_snapshot(input_path)
        self.assertEqual(loaded_snapshot, {"file1.txt": "hashA"})
        mock_exists.assert_called_once_with()
        mock_open_func.assert_called_once_with(input_path, 'r', encoding='utf-8')
        mock_json_load.assert_called_once_with(mock_open_func())

    @patch('pathlib.Path.exists', return_value=False)
    def test_load_snapshot_file_not_found(self, mock_exists):
        # Mock rationale: Test error handling when the snapshot file does not exist.
        with self.assertRaises(FileNotFoundError):
            load_snapshot(Path("/non/existent/snapshot.json"))
        mock_exists.assert_called_once_with()

    @patch('builtins.open', new_callable=mock_open, read_data='{"file1.txt": "hashA"}')
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "doc", 0))
    @patch('pathlib.Path.exists', return_value=True)
    def test_load_snapshot_invalid_json(self, mock_exists, mock_json_load, mock_open_func):
        # Mock rationale: Test error handling when the snapshot file contains invalid JSON.
        input_path = Path("/mock/invalid.json")
        with self.assertRaises(json.JSONDecodeError):
            load_snapshot(input_path)
        mock_exists.assert_called_once_with()
        mock_open_func.assert_called_once_with(input_path, 'r', encoding='utf-8')
        mock_json_load.assert_called_once_with(mock_open_func())
