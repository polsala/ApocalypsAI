import unittest
import os
import hashlib
import json
import yaml
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime

# Import the functions to be tested
from src.manifest_generator import calculate_file_hash, generate_manifest

class TestManifestGenerator(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    def test_calculate_file_hash(self, mock_file):
        # Mock rationale: Avoids actual file system interaction. We provide dummy content to ensure deterministic hash calculation.
        expected_hash = hashlib.sha256(b'test content').hexdigest()
        self.assertEqual(calculate_file_hash('dummy_path.txt'), expected_hash)
        mock_file.assert_called_once_with('dummy_path.txt', 'rb')

    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('src.manifest_generator.calculate_file_hash')
    @patch('datetime.datetime')
    def test_generate_manifest(self, mock_datetime, mock_calculate_hash, mock_os_walk, mock_getmtime, mock_getsize):
        # Mock rationale:
        # - os.path.getsize: Avoids actual file system interaction, provides deterministic file sizes.
        # - os.path.getmtime: Avoids actual file system interaction, provides deterministic modification timestamps.
        # - os.walk: Simulates a directory structure without creating real files, ensuring deterministic traversal.
        # - calculate_file_hash: Avoids actual file content reading, provides deterministic hash values.
        # - datetime.datetime: Ensures deterministic scan_timestamp and last_modified_timestamp for consistent output.

        # Setup mocks for os.walk to simulate a directory structure
        mock_os_walk.return_value = [
            ('/mock_root', ['subdir'], ['file1.txt']),
            ('/mock_root/subdir', [], ['file2.log'])
        ]
        # Setup mocks for file metadata
        mock_getsize.side_effect = [100, 200] # Sizes for file1.txt, file2.log
        mock_getmtime.side_effect = [1678886400, 1678972800] # March 15, 2023 00:00:00 UTC, March 16, 2023 00:00:00 UTC
        mock_calculate_hash.side_effect = ['hash1', 'hash2'] # Hashes for file1.txt, file2.log

        # Mock datetime.now() and fromtimestamp() for deterministic output
        mock_now = datetime(2023, 10, 27, 10, 30, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = [
            datetime(2023, 3, 15, 0, 0, 0),
            datetime(2023, 3, 16, 0, 0, 0)
        ]
        # Allow direct calls to datetime.datetime() constructor to work (e.g., for internal datetime operations)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) if args else mock_now

        root_dir = '/mock_root'
        manifest = generate_manifest(root_dir)

        expected_manifest = {
            "scan_root": os.path.abspath(root_dir), # os.path.abspath will still work on mock paths deterministically
            "scan_timestamp": "2023-10-27T10:30:00Z",
            "files": [
                {
                    "path": "file1.txt",
                    "size_bytes": 100,
                    "sha256_hash": "hash1",
                    "last_modified_timestamp": "2023-03-15T00:00:00Z"
                },
                {
                    "path": "subdir/file2.log",
                    "size_bytes": 200,
                    "sha256_hash": "hash2",
                    "last_modified_timestamp": "2023-03-16T00:00:00Z"
                }
            ]
        }
        
        # Sort files by path for deterministic comparison, as os.walk order might vary slightly across platforms/Python versions
        manifest['files'].sort(key=lambda x: x['path'])
        expected_manifest['files'].sort(key=lambda x: x['path'])

        self.assertEqual(manifest, expected_manifest)

    @patch('builtins.open', new_callable=mock_open, read_data=b'file content')
    @patch('os.path.getsize', return_value=123)
    @patch('os.path.getmtime', return_value=1678886400)
    @patch('os.walk')
    @patch('src.manifest_generator.calculate_file_hash', return_value='mock_hash')
    @patch('datetime.datetime')
    def test_generate_manifest_empty_dir(self, mock_datetime, mock_calculate_hash, mock_os_walk, mock_getmtime, mock_getsize, mock_file_open):
        # Mock rationale: Same as above, specifically testing the scenario of an empty directory for deterministic output.
        mock_os_walk.return_value = [
            ('/mock_empty_root', [], []) # Simulate an empty directory
        ]
        mock_now = datetime(2023, 10, 27, 10, 30, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.return_value = datetime(2023, 3, 15, 0, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) if args else mock_now

        root_dir = '/mock_empty_root'
        manifest = generate_manifest(root_dir)

        expected_manifest = {
            "scan_root": os.path.abspath(root_dir),
            "scan_timestamp": "2023-10-27T10:30:00Z",
            "files": []
        }
        self.assertEqual(manifest, expected_manifest)

    @patch('builtins.open', new_callable=mock_open, read_data=b'file content')
    @patch('os.path.getsize', return_value=123)
    @patch('os.path.getmtime', return_value=1678886400)
    @patch('os.walk')
    @patch('src.manifest_generator.calculate_file_hash', return_value='mock_hash')
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture printed output
    def test_main_json_output_stdout(self, mock_stdout, mock_datetime, mock_calculate_hash, mock_os_walk, mock_getmtime, mock_getsize, mock_file_open):
        # Mock rationale:
        # - sys.stdout: Captures print output without affecting the actual console, ensuring deterministic output capture.
        # - Other mocks: Same as above for deterministic manifest generation.

        mock_os_walk.return_value = [
            ('/mock_root', [], ['test_file.txt'])
        ]
        mock_now = datetime(2023, 10, 27, 10, 30, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.return_value = datetime(2023, 3, 15, 0, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) if args else mock_now

        # Mock argparse to simulate command line arguments for the main function
        with patch('argparse.ArgumentParser.parse_args') as mock_args:
            mock_args.return_value = MagicMock(
                path='/mock_root',
                output_format='json',
                output_file=None # Simulate printing to stdout
            )
            from src.manifest_generator import main
            main()

            expected_output_dict = {
                "scan_root": os.path.abspath('/mock_root'),
                "scan_timestamp": "2023-10-27T10:30:00Z",
                "files": [
                    {
                        "path": "test_file.txt",
                        "size_bytes": 123,
                        "sha256_hash": "mock_hash",
                        "last_modified_timestamp": "2023-03-15T00:00:00Z"
                    }
                ]
            }
            mock_stdout.write.assert_called_once()
            # The output will have a newline, so we strip it for comparison
            actual_output = json.loads(mock_stdout.write.call_args[0][0].strip())
            self.assertEqual(actual_output, expected_output_dict)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize', return_value=123)
    @patch('os.path.getmtime', return_value=1678886400)
    @patch('os.walk')
    @patch('src.manifest_generator.calculate_file_hash', return_value='mock_hash')
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture print statements (e.g., success message)
    def test_main_yaml_output_file(self, mock_stdout, mock_datetime, mock_calculate_hash, mock_os_walk, mock_getmtime, mock_getsize, mock_file_open):
        # Mock rationale: Same as above, specifically testing YAML output written to a file for deterministic file content.

        mock_os_walk.return_value = [
            ('/mock_root', [], ['test_file.txt'])
        ]
        mock_now = datetime(2023, 10, 27, 10, 30, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.return_value = datetime(2023, 3, 15, 0, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) if args else mock_now

        # Mock argparse to simulate command line arguments for the main function
        with patch('argparse.ArgumentParser.parse_args') as mock_args:
            mock_args.return_value = MagicMock(
                path='/mock_root',
                output_format='yaml',
                output_file='output.yaml' # Simulate writing to a file
            )
            from src.manifest_generator import main
            main()

            expected_output_dict = {
                "scan_root": os.path.abspath('/mock_root'),
                "scan_timestamp": "2023-10-27T10:30:00Z",
                "files": [
                    {
                        "path": "test_file.txt",
                        "size_bytes": 123,
                        "sha256_hash": "mock_hash",
                        "last_modified_timestamp": "2023-03-15T00:00:00Z"
                    }
                ]
            }
            mock_file_open.assert_called_once_with('output.yaml', 'w')
            # Check the content written to the mock file handle
            handle = mock_file_open()
            actual_output = yaml.safe_load(handle.write.call_args[0][0])
            self.assertEqual(actual_output, expected_output_dict)
            mock_stdout.write.assert_called_once_with('Manifest successfully written to output.yaml\n')

    @patch('os.walk')
    @patch('os.path.getsize', side_effect=OSError('Permission denied')) # Simulate an error during file access
    @patch('src.manifest_generator.calculate_file_hash')
    @patch('datetime.datetime')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture warning messages
    def test_generate_manifest_os_error_handling(self, mock_stdout, mock_datetime, mock_calculate_hash, mock_getsize, mock_os_walk):
        # Mock rationale: Simulates an OSError (e.g., permission denied) during file processing to test error handling.
        mock_os_walk.return_value = [
            ('/mock_root', [], ['unreadable_file.txt']) # Simulate a file that causes an error
        ]
        mock_now = datetime(2023, 10, 27, 10, 30, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.return_value = datetime(2023, 3, 15, 0, 0, 0)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) if args else mock_now

        root_dir = '/mock_root'
        manifest = generate_manifest(root_dir)

        expected_manifest = {
            "scan_root": os.path.abspath(root_dir),
            "scan_timestamp": "2023-10-27T10:30:00Z",
            "files": [] # No files should be in the manifest if they cause an OSError
        }
        self.assertEqual(manifest, expected_manifest)
        # Verify that a warning message was printed to stdout
        mock_stdout.write.assert_any_call("Warning: Could not process /mock_root/unreadable_file.txt: Permission denied\n")

if __name__ == '__main__':
    unittest.main()
