import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
from datetime import datetime

# Import the functions to be tested
from src.echo_recorder import record_directory_snapshot, calculate_file_hash

class TestEchoRecorder(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    def test_calculate_file_hash(self, mock_sha256, mock_open_file):
        # Mock rationale: Simulate file reading and hashing without actual file I/O.
        mock_file_handle = mock_open_file.return_value
        mock_file_handle.read.side_effect = [b'block1', b'block2', b''] # Simulate reading in blocks

        mock_hasher = MagicMock()
        mock_hasher.hexdigest.return_value = 'mock_hash_value'
        mock_sha256.return_value = mock_hasher

        result = calculate_file_hash('dummy_path.txt')

        mock_open_file.assert_called_once_with('dummy_path.txt', 'rb')
        mock_hasher.update.assert_any_call(b'block1')
        mock_hasher.update.assert_any_call(b'block2')
        self.assertEqual(result, 'mock_hash_value')

    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    def test_calculate_file_hash_io_error(self, mock_sha256, mock_open_file):
        # Mock rationale: Simulate an IOError during file reading for hashing.
        mock_open_file.side_effect = IOError("Permission denied")

        with self.assertRaisesRegex(IOError, "Could not read file dummy_path.txt: Permission denied"):
            calculate_file_hash('dummy_path.txt')
        mock_open_file.assert_called_once_with('dummy_path.txt', 'rb')

    @patch('src.echo_recorder.calculate_file_hash')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.echo_recorder.datetime') # Mock datetime to control timestamp
    def test_record_directory_snapshot_success(self, mock_datetime, mock_open_file, mock_os_walk, mock_os_isdir, mock_os_getsize, mock_os_getmtime, mock_calculate_file_hash):
        # Mock rationale: Simulate a directory structure and file properties without actual file system access.
        # Mock datetime to ensure deterministic timestamp in the snapshot.
        
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts) # Allow actual conversion for mtime

        mock_os_isdir.return_value = True
        
        # Simulate os.walk output
        mock_os_walk.return_value = [
            ('/mock/target', ('subdir',), ('file1.txt',)),
            ('/mock/target/subdir', (), ('file2.log', 'empty.txt'))
        ]

        # Mock file properties
        mock_os_getsize.side_effect = [100, 200, 0] # file1.txt, file2.log, empty.txt
        mock_os_getmtime.side_effect = [
            datetime(2023, 1, 1, 12, 0, 0).timestamp(), # file1.txt
            datetime(2023, 2, 1, 13, 0, 0).timestamp(), # file2.log
            datetime(2023, 3, 1, 14, 0, 0).timestamp()  # empty.txt
        ]
        mock_calculate_file_hash.side_effect = ['hash1', 'hash2', 'hash3']

        target_dir = '/mock/target'
        output_file = 'snapshot.json'

        result = record_directory_snapshot(target_dir, output_file)

        mock_os_isdir.assert_called_once_with(target_dir)
        mock_os_walk.assert_called_once_with(target_dir)
        
        # Assert calls for file properties and hashing
        mock_os_getsize.assert_any_call('/mock/target/file1.txt')
        mock_os_getmtime.assert_any_call('/mock/target/file1.txt')
        mock_calculate_file_hash.assert_any_call('/mock/target/file1.txt')

        mock_os_getsize.assert_any_call('/mock/target/subdir/file2.log')
        mock_os_getmtime.assert_any_call('/mock/target/subdir/file2.log')
        mock_calculate_file_hash.assert_any_call('/mock/target/subdir/file2.log')

        mock_os_getsize.assert_any_call('/mock/target/subdir/empty.txt')
        mock_os_getmtime.assert_any_call('/mock/target/subdir/empty.txt')
        mock_calculate_file_hash.assert_any_call('/mock/target/subdir/empty.txt')

        # Assert output file content
        mock_open_file.assert_called_once_with(output_file, 'w')
        written_content = mock_open_file.return_value.write.call_args[0][0]
        snapshot_data = json.loads(written_content)

        self.assertEqual(snapshot_data["timestamp"], "2023-10-27T10:00:00")
        self.assertEqual(snapshot_data["target_directory"], os.path.abspath(target_dir)) # os.path.abspath is not mocked, so it will return real path
        self.assertEqual(len(snapshot_data["files"]), 3)

        self.assertEqual(snapshot_data["files"][0]["path"], "file1.txt")
        self.assertEqual(snapshot_data["files"][0]["hash"], "hash1")
        self.assertEqual(snapshot_data["files"][0]["size"], 100)
        self.assertEqual(snapshot_data["files"][0]["mtime"], "2023-01-01T12:00:00")

        self.assertEqual(snapshot_data["files"][1]["path"], "subdir/file2.log")
        self.assertEqual(snapshot_data["files"][1]["hash"], "hash2")
        self.assertEqual(snapshot_data["files"][1]["size"], 200)
        self.assertEqual(snapshot_data["files"][1]["mtime"], "2023-02-01T13:00:00")

        self.assertEqual(snapshot_data["files"][2]["path"], "subdir/empty.txt")
        self.assertEqual(snapshot_data["files"][2]["hash"], "hash3")
        self.assertEqual(snapshot_data["files"][2]["size"], 0)
        self.assertEqual(snapshot_data["files"][2]["mtime"], "2023-03-01T14:00:00")

        self.assertEqual(result, snapshot_data)


    @patch('os.path.isdir')
    def test_record_directory_snapshot_target_dir_not_found(self, mock_os_isdir):
        # Mock rationale: Simulate the scenario where the target directory does not exist.
        mock_os_isdir.return_value = False
        target_dir = '/nonexistent/dir'
        output_file = 'snapshot.json'

        with self.assertRaises(FileNotFoundError) as cm:
            record_directory_snapshot(target_dir, output_file)
        
        self.assertIn("Target directory not found", str(cm.exception))
        mock_os_isdir.assert_called_once_with(target_dir)

    @patch('src.echo_recorder.calculate_file_hash')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.echo_recorder.datetime')
    def test_record_directory_snapshot_file_processing_error(self, mock_datetime, mock_open_file, mock_os_walk, mock_os_isdir, mock_os_getsize, mock_os_getmtime, mock_calculate_file_hash):
        # Mock rationale: Simulate an error during file processing (e.g., permission denied, IOError, OSError)
        # to ensure the utility handles it gracefully without crashing, and logs a warning.
        mock_datetime.now.return_value = datetime(2023, 10, 27, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts)

        mock_os_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/target', (), ('file1.txt', 'unreadable.txt'))
        ]

        # Simulate one file succeeding, one failing
        mock_os_getsize.side_effect = [100, OSError("Permission denied")]
        mock_os_getmtime.side_effect = [datetime(2023, 1, 1, 12, 0, 0).timestamp(), OSError("Permission denied")]
        mock_calculate_file_hash.side_effect = ['hash1', IOError("Could not read file /mock/target/unreadable.txt: Permission denied")]

        target_dir = '/mock/target'
        output_file = 'snapshot.json'

        # We expect a warning to be printed, but the function should not crash.
        with patch('builtins.print') as mock_print:
            result = record_directory_snapshot(target_dir, output_file)
            mock_print.assert_called_with("Warning: Could not process file /mock/target/unreadable.txt: Could not read file /mock/target/unreadable.txt: Permission denied")

        mock_open_file.assert_called_once_with(output_file, 'w')
        written_content = mock_open_file.return_value.write.call_args[0][0]
        snapshot_data = json.loads(written_content)

        self.assertEqual(len(snapshot_data["files"]), 1) # Only the successfully processed file
        self.assertEqual(snapshot_data["files"][0]["path"], "file1.txt")
        self.assertEqual(snapshot_data["files"][0]["hash"], "hash1")
