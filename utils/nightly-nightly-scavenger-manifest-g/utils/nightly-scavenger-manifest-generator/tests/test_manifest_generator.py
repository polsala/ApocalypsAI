import unittest
import os
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

# Mock rationale: We need to simulate file system interactions (os.walk, os.path.isdir,
# os.path.getsize, os.path.getmtime) without actually touching the disk. This ensures
# tests are deterministic, fast, and don't rely on the host file system state.
# We also mock os.path.abspath to ensure consistent path representation in tests.

# Import the function to be tested
from src.manifest_generator import generate_manifest, main

class TestManifestGenerator(unittest.TestCase):

    @patch('os.path.abspath', side_effect=lambda x: f"/mock_root/{x.lstrip('/')}")
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_generate_manifest_basic(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Mock rationale: Simulate a basic directory structure with a few files.
        # os.path.isdir should return True for the target path.
        # os.walk should yield a predefined structure.
        # os.path.getsize and os.path.getmtime should return specific values for mocked files.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root/test_dir', [], ['file1.txt', 'file2.log']),
            ('/mock_root/test_dir/subdir', [], ['image.jpg', 'data.json'])
        ]
        
        # Define mock return values for file sizes and modification times
        # Keys are full paths, values are (size, mtime_timestamp)
        mock_file_data = {
            '/mock_root/test_dir/file1.txt': (100, datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc).timestamp()),
            '/mock_root/test_dir/file2.log': (200, datetime(2023, 1, 2, 11, 0, 0, tzinfo=timezone.utc).timestamp()),
            '/mock_root/test_dir/subdir/image.jpg': (500, datetime(2023, 1, 3, 12, 0, 0, tzinfo=timezone.utc).timestamp()),
            '/mock_root/test_dir/subdir/data.json': (150, datetime(2023, 1, 4, 13, 0, 0, tzinfo=timezone.utc).timestamp()),
        }

        def getsize_side_effect(path):
            return mock_file_data[path][0]

        def getmtime_side_effect(path):
            return mock_file_data[path][1]

        mock_getsize.side_effect = getsize_side_effect
        mock_getmtime.side_effect = getmtime_side_effect

        scan_path = 'test_dir'
        manifest = generate_manifest(scan_path)

        expected_manifest = {
            "scan_path": "/mock_root/test_dir",
            "total_files_scanned": 4,
            "total_size_bytes": 950,
            "most_recent_modification_utc": "2023-01-04T13:00:00Z",
            "file_types": {
                ".txt": {"count": 1, "total_size_bytes": 100},
                ".log": {"count": 1, "total_size_bytes": 200},
                ".jpg": {"count": 1, "total_size_bytes": 500},
                ".json": {"count": 1, "total_size_bytes": 150}
            }
        }
        self.assertEqual(manifest, expected_manifest)

    @patch('os.path.abspath', side_effect=lambda x: f"/mock_root/{x.lstrip('/')}")
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_generate_manifest_empty_dir(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Mock rationale: Simulate an empty directory.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root/empty_dir', [], [])
        ]
        
        scan_path = 'empty_dir'
        manifest = generate_manifest(scan_path)

        expected_manifest = {
            "scan_path": "/mock_root/empty_dir",
            "total_files_scanned": 0,
            "total_size_bytes": 0,
            "most_recent_modification_utc": None,
            "file_types": {}
        }
        self.assertEqual(manifest, expected_manifest)

    @patch('os.path.abspath', side_effect=lambda x: f"/mock_root/{x.lstrip('/')}")
    @patch('os.path.isdir')
    def test_generate_manifest_invalid_path(self, mock_isdir, mock_abspath):
        # Mock rationale: Simulate an invalid directory path.
        mock_isdir.return_value = False
        scan_path = 'non_existent_dir'
        with self.assertRaisesRegex(ValueError, "Path 'non_existent_dir' is not a valid directory."):
            generate_manifest(scan_path)

    @patch('os.path.abspath', side_effect=lambda x: f"/mock_root/{x.lstrip('/')}")
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_generate_manifest_mixed_extensions_and_no_extension(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Mock rationale: Simulate files with various extensions, including some without.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root/mixed_dir', [], ['doc.pdf', 'archive.tar.gz', 'README', 'script.py']),
        ]

        mock_file_data = {
            '/mock_root/mixed_dir/doc.pdf': (1000, datetime(2023, 2, 1, 10, 0, 0, tzinfo=timezone.utc).timestamp()),
            '/mock_root/mixed_dir/archive.tar.gz': (5000, datetime(2023, 2, 2, 11, 0, 0, tzinfo=timezone.utc).timestamp()),
            '/mock_root/mixed_dir/README': (50, datetime(2023, 2, 3, 12, 0, 0, tzinfo=timezone.utc).timestamp()),
            '/mock_root/mixed_dir/script.py': (200, datetime(2023, 2, 4, 13, 0, 0, tzinfo=timezone.utc).timestamp()),
        }

        def getsize_side_effect(path):
            return mock_file_data[path][0]

        def getmtime_side_effect(path):
            return mock_file_data[path][1]

        mock_getsize.side_effect = getsize_side_effect
        mock_getmtime.side_effect = getmtime_side_effect

        scan_path = 'mixed_dir'
        manifest = generate_manifest(scan_path)

        expected_manifest = {
            "scan_path": "/mock_root/mixed_dir",
            "total_files_scanned": 4,
            "total_size_bytes": 6250,
            "most_recent_modification_utc": "2023-02-04T13:00:00Z",
            "file_types": {
                ".pdf": {"count": 1, "total_size_bytes": 1000},
                ".gz": {"count": 1, "total_size_bytes": 5000}, # .tar.gz should yield .gz
                "[no_extension]": {"count": 1, "total_size_bytes": 50},
                ".py": {"count": 1, "total_size_bytes": 200}
            }
        }
        self.assertEqual(manifest, expected_manifest)

    @patch('os.path.abspath', side_effect=lambda x: f"/mock_root/{x.lstrip('/')}")
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_generate_manifest_os_error_on_file(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Mock rationale: Simulate a scenario where some files cannot be accessed (e.g., permission denied).
        # The utility should gracefully skip such files and continue processing others.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root/error_dir', [], ['good_file.txt', 'bad_file.log']),
        ]

        mock_file_data = {
            '/mock_root/error_dir/good_file.txt': (100, datetime(2023, 3, 1, 10, 0, 0, tzinfo=timezone.utc).timestamp()),
        }

        def getsize_side_effect(path):
            if path == '/mock_root/error_dir/bad_file.log':
                raise OSError("Permission denied")
            return mock_file_data[path][0]

        def getmtime_side_effect(path):
            if path == '/mock_root/error_dir/bad_file.log':
                raise OSError("Permission denied")
            return mock_file_data[path][1]

        mock_getsize.side_effect = getsize_side_effect
        mock_getmtime.side_effect = getmtime_side_effect

        scan_path = 'error_dir'
        manifest = generate_manifest(scan_path)

        expected_manifest = {
            "scan_path": "/mock_root/error_dir",
            "total_files_scanned": 1, # Only good_file.txt should be counted
            "total_size_bytes": 100,
            "most_recent_modification_utc": "2023-03-01T10:00:00Z",
            "file_types": {
                ".txt": {"count": 1, "total_size_bytes": 100},
            }
        }
        self.assertEqual(manifest, expected_manifest)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('src.manifest_generator.generate_manifest')
    @patch('os.sys.exit')
    def test_main_stdout_output(self, mock_exit, mock_generate_manifest, mock_print, mock_parse_args):
        # Mock rationale: Test the main function's behavior when outputting to stdout.
        # We mock argparse to control CLI arguments, generate_manifest for its return value,
        # print to capture output, and sys.exit to prevent actual exit during testing.
        mock_parse_args.return_value = MagicMock(path='test_dir', output=None)
        mock_generate_manifest.return_value = {"key": "value"}
        mock_exit.side_effect = SystemExit # Prevent actual exit

        main()
        mock_print.assert_called_once_with(json.dumps({"key": "value"}, indent=2))
        mock_exit.assert_not_called() # Should not exit on success

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('builtins.print')
    @patch('src.manifest_generator.generate_manifest')
    @patch('os.sys.exit')
    def test_main_file_output(self, mock_exit, mock_generate_manifest, mock_print, mock_open, mock_parse_args):
        # Mock rationale: Test the main function's behavior when outputting to a file.
        # We mock file operations (`open`) to ensure no actual file is written.
        mock_parse_args.return_value = MagicMock(path='test_dir', output='output.json')
        mock_generate_manifest.return_value = {"key": "value"}
        mock_exit.side_effect = SystemExit # Prevent actual exit

        main()
        mock_open.assert_called_once_with('output.json', 'w')
        mock_open().write.assert_called_once_with(json.dumps({"key": "value"}, indent=2))
        mock_print.assert_called_once_with("Manifest successfully written to output.json")
        mock_exit.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    @patch('src.manifest_generator.generate_manifest')
    @patch('os.sys.exit')
    def test_main_error_handling(self, mock_exit, mock_generate_manifest, mock_print, mock_parse_args):
        # Mock rationale: Test error handling in main.
        mock_parse_args.return_value = MagicMock(path='invalid_dir', output=None)
        mock_generate_manifest.side_effect = ValueError("Test error")
        mock_exit.side_effect = SystemExit # Prevent actual exit

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Error: Test error", file=os.sys.stderr)

if __name__ == '__main__':
    unittest.main()
