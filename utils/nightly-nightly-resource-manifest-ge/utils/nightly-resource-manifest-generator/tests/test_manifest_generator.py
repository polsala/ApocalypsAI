import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

# Import the function to be tested
from src.manifest_generator import generate_manifest, get_file_metadata

class TestManifestGenerator(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_path = os.path.join(self.temp_dir, "test_hoard")
        os.makedirs(self.test_path)

        # Create some dummy files and directories
        self.file1_path = os.path.join(self.test_path, "data_fragment_alpha.txt")
        with open(self.file1_path, "w") as f:
            f.write("content alpha") # 13 bytes

        self.subdir_path = os.path.join(self.test_path, "archive")
        os.makedirs(self.subdir_path)

        self.file2_path = os.path.join(self.subdir_path, "old_logs.zip")
        with open(self.file2_path, "w") as f:
            f.write("zip content" * 100) # 1100 bytes

        self.file3_path = os.path.join(self.test_path, "config.json")
        with open(self.file3_path, "w") as f:
            f.write('{"key": "value"}') # 16 bytes

        # Mock os.stat to ensure deterministic file modification times and sizes
        # Mock rationale: os.stat returns actual system file stats which are non-deterministic
        # (e.g., mtime changes on file creation). We need fixed values for testing.
        self.mock_stat_results = {
            self.file1_path: MagicMock(st_size=13, st_mtime=datetime(2023, 10, 26, 10, 0, 0, tzinfo=timezone.utc).timestamp()),
            self.file2_path: MagicMock(st_size=1100, st_mtime=datetime(2023, 9, 15, 14, 30, 0, tzinfo=timezone.utc).timestamp()),
            self.file3_path: MagicMock(st_size=16, st_mtime=datetime(2023, 10, 27, 4, 0, 0, tzinfo=timezone.utc).timestamp()),
        }

        # Patch os.stat globally for the duration of the test
        self.patcher_stat = patch('os.stat', side_effect=lambda p: self.mock_stat_results.get(p, os.stat(p)))
        self.mock_os_stat = self.patcher_stat.start()

        # Mock datetime.utcnow to ensure deterministic scan_timestamp
        # Mock rationale: datetime.utcnow returns the current time, which is non-deterministic.
        # We need a fixed timestamp for consistent test results.
        self.mock_utcnow = datetime(2023, 10, 27, 4, 42, 0, tzinfo=timezone.utc)
        self.patcher_datetime = patch('src.manifest_generator.datetime', wraps=datetime)
        self.mock_datetime = self.patcher_datetime.start()
        self.mock_datetime.utcnow.return_value = self.mock_utcnow
        self.mock_datetime.fromtimestamp.side_effect = lambda ts: datetime.fromtimestamp(ts, tz=timezone.utc)


    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.temp_dir)
        self.patcher_stat.stop()
        self.patcher_datetime.stop()

    def test_get_file_metadata(self):
        metadata = get_file_metadata(self.file1_path, self.test_path)
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["name"], "data_fragment_alpha.txt")
        self.assertEqual(metadata["path"], self.file1_path)
        self.assertEqual(metadata["size_bytes"], 13)
        self.assertEqual(metadata["last_modified"], "2023-10-26T10:00:00Z")

        # Test with a non-existent file
        non_existent_path = os.path.join(self.test_path, "non_existent.txt")
        self.mock_os_stat.side_effect = lambda p: self.mock_stat_results.get(p, FileNotFoundError)
        metadata = get_file_metadata(non_existent_path, self.test_path)
        self.assertIsNone(metadata)
        self.mock_os_stat.side_effect = lambda p: self.mock_stat_results.get(p, os.stat(p)) # Reset for other tests

    def test_generate_manifest_basic(self):
        manifest = generate_manifest(self.test_path);

        self.assertEqual(manifest["scan_path"], os.path.abspath(self.test_path))
        self.assertEqual(manifest["scan_timestamp"], "2023-10-27T04:42:00Z")
        self.assertEqual(manifest["total_files"], 3)
        self.assertEqual(manifest["total_size_bytes"], 13 + 1100 + 16) # Sum of mocked sizes

        file_names = {f["name"] for f in manifest["files"]}
        self.assertIn("data_fragment_alpha.txt", file_names)
        self.assertIn("archive/old_logs.zip", file_names)
        self.assertIn("config.json", file_names)

        # Verify specific file data
        file1_data = next(f for f in manifest["files"] if f["name"] == "data_fragment_alpha.txt")
        self.assertEqual(file1_data["size_bytes"], 13)
        self.assertEqual(file1_data["last_modified"], "2023-10-26T10:00:00Z")

        file2_data = next(f for f in manifest["files"] if f["name"] == "archive/old_logs.zip")
        self.assertEqual(file2_data["size_bytes"], 1100)
        self.assertEqual(file2_data["last_modified"], "2023-09-15T14:30:00Z")

    def test_generate_manifest_empty_directory(self):
        empty_dir = os.path.join(self.temp_dir, "empty_hoard")
        os.makedirs(empty_dir)
        manifest = generate_manifest(empty_dir)

        self.assertEqual(manifest["scan_path"], os.path.abspath(empty_dir))
        self.assertEqual(manifest["total_files"], 0)
        self.assertEqual(manifest["total_size_bytes"], 0)
        self.assertEqual(len(manifest["files"]), 0)

    def test_generate_manifest_invalid_path(self):
        with self.assertRaises(ValueError) as cm:
            generate_manifest("/path/that/does/not/exist")
        self.assertIn("is not a valid directory", str(cm.exception))

    @patch('builtins.print') # Mock rationale: Capture stdout to verify CLI output without actual printing.
    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Control CLI arguments for testing.
    @patch('src.manifest_generator.generate_manifest') # Mock rationale: Isolate CLI logic from core manifest generation.
    def test_main_success(self, mock_generate_manifest, mock_parse_args, mock_print):
        mock_parse_args.return_value = MagicMock(path=self.test_path)
        mock_generate_manifest.return_value = {
            "scan_path": self.test_path,
            "scan_timestamp": "2023-10-27T04:42:00Z",
            "total_files": 1,
            "total_size_bytes": 100,
            "files": []
        }

        from src.manifest_generator import main
        main()

        mock_generate_manifest.assert_called_once_with(self.test_path)
        mock_print.assert_called_once()
        printed_output = json.loads(mock_print.call_args[0][0])
        self.assertEqual(printed_output["total_files"], 1)

    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stderr', new_callable=MagicMock) # Mock rationale: Capture stderr for error messages.
    @patch('sys.exit') # Mock rationale: Prevent actual program exit during testing.
    def test_main_invalid_path_error(self, mock_exit, mock_stderr, mock_parse_args, mock_print):
        mock_parse_args.return_value = MagicMock(path="/invalid/path")

        from src.manifest_generator import main
        main()

        mock_stderr.write.assert_called_once()
        self.assertIn("Error: Scan path '/invalid/path' is not a valid directory.", mock_stderr.write.call_args[0][0])
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
