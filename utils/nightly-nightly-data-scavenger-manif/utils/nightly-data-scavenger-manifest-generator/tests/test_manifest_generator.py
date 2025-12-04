import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timezone

# Mock rationale: os.walk, os.path.getsize, os.path.getmtime interact with the filesystem
# and system time, making tests non-deterministic and dependent on the environment.
# Mocking these functions allows for controlled, deterministic, and offline testing.

# Import the function to be tested
from src.manifest_generator import generate_manifest

class TestManifestGenerator(unittest.TestCase):

    def setUp(self):
        # Define a consistent base path for mocking
        self.mock_base_path = '/mock/repo'

        # Mock timestamps for deterministic testing
        self.mock_timestamp1 = datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc).timestamp()
        self.mock_timestamp2 = datetime(2023, 1, 2, 11, 30, 0, tzinfo=timezone.utc).timestamp()
        self.mock_timestamp3 = datetime(2023, 1, 3, 12, 45, 0, tzinfo=timezone.utc).timestamp()

        # Expected ISO 8601 format
        self.expected_iso_timestamp1 = '2023-01-01T10:00:00Z'
        self.expected_iso_timestamp2 = '2023-01-02T11:30:00Z'
        self.expected_iso_timestamp3 = '2023-01-03T12:45:00Z'

    @patch('os.path.abspath', side_effect=lambda x: x) # Mock abspath to return input directly for simplicity in tests
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start, '').lstrip('/')) # Mock relpath for consistent relative paths
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    def test_generate_manifest_basic(self, mock_walk, mock_getsize, mock_getmtime, mock_relpath, mock_abspath):
        # Mock rationale: Simulate a simple directory structure with a few files.
        mock_walk.return_value = [
            (self.mock_base_path, [], ['file1.py', 'README.md']),
            (os.path.join(self.mock_base_path, 'sub_dir'), [], ['data.json', 'temp.txt'])
        ]

        # Mock rationale: Provide deterministic file sizes for specific paths.
        mock_getsize.side_effect = lambda p: {
            os.path.join(self.mock_base_path, 'file1.py'): 100,
            os.path.join(self.mock_base_path, 'README.md'): 200,
            os.path.join(self.mock_base_path, 'sub_dir', 'data.json'): 300,
            os.path.join(self.mock_base_path, 'sub_dir', 'temp.txt'): 50
        }.get(p, 0)

        # Mock rationale: Provide deterministic modification times for specific paths.
        mock_getmtime.side_effect = lambda p: {
            os.path.join(self.mock_base_path, 'file1.py'): self.mock_timestamp1,
            os.path.join(self.mock_base_path, 'README.md'): self.mock_timestamp2,
            os.path.join(self.mock_base_path, 'sub_dir', 'data.json'): self.mock_timestamp3,
            os.path.join(self.mock_base_path, 'sub_dir', 'temp.txt'): self.mock_timestamp1
        }.get(p, 0)

        extensions = ['py', 'md', 'json']
        manifest = generate_manifest(self.mock_base_path, extensions)

        expected_manifest = [
            {
                'path': 'file1.py',
                'size_bytes': 100,
                'last_modified_utc': self.expected_iso_timestamp1
            },
            {
                'path': 'README.md',
                'size_bytes': 200,
                'last_modified_utc': self.expected_iso_timestamp2
            },
            {
                'path': 'sub_dir/data.json',
                'size_bytes': 300,
                'last_modified_utc': self.expected_iso_timestamp3
            }
        ]

        self.assertCountEqual(manifest, expected_manifest)

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start, '').lstrip('/'))
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    def test_generate_manifest_no_matching_files(self, mock_walk, mock_getsize, mock_getmtime, mock_relpath, mock_abspath):
        # Mock rationale: Simulate a directory with files, but none match the requested extensions.
        mock_walk.return_value = [
            (self.mock_base_path, [], ['image.png', 'document.pdf'])
        ]
        mock_getsize.return_value = 100
        mock_getmtime.return_value = self.mock_timestamp1

        extensions = ['py', 'md']
        manifest = generate_manifest(self.mock_base_path, extensions)
        self.assertEqual(manifest, [])

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start, '').lstrip('/'))
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    def test_generate_manifest_empty_directory(self, mock_walk, mock_getsize, mock_getmtime, mock_relpath, mock_abspath):
        # Mock rationale: Simulate an empty directory (no files).
        mock_walk.return_value = [
            (self.mock_base_path, [], [])
        ]
        extensions = ['py', 'md']
        manifest = generate_manifest(self.mock_base_path, extensions)
        self.assertEqual(manifest, [])

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start, '').lstrip('/'))
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    def test_generate_manifest_different_base_path(self, mock_walk, mock_getsize, mock_getmtime, mock_relpath, mock_abspath):
        custom_base_path = '/another/location'
        # Mock rationale: Simulate a directory structure under a different base path.
        mock_walk.return_value = [
            (custom_base_path, [], ['config.json'])
        ]
        mock_getsize.side_effect = lambda p: {
            os.path.join(custom_base_path, 'config.json'): 75
        }.get(p, 0)
        mock_getmtime.side_effect = lambda p: {
            os.path.join(custom_base_path, 'config.json'): self.mock_timestamp3
        }.get(p, 0)

        extensions = ['json']
        manifest = generate_manifest(custom_base_path, extensions)

        expected_manifest = [
            {
                'path': 'config.json',
                'size_bytes': 75,
                'last_modified_utc': self.expected_iso_timestamp3
            }
        ]
        self.assertCountEqual(manifest, expected_manifest)

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start, '').lstrip('/'))
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    def test_generate_manifest_os_error_handling(self, mock_walk, mock_getsize, mock_getmtime, mock_relpath, mock_abspath):
        # Mock rationale: Simulate a scenario where os.path.getsize or os.path.getmtime raises an OSError
        # (e.g., due to permission issues or a broken symlink).
        mock_walk.return_value = [
            (self.mock_base_path, [], ['good_file.py', 'bad_file.py'])
        ]

        def getsize_side_effect(path):
            if 'bad_file.py' in path:
                raise OSError("Permission denied")
            return 100

        def getmtime_side_effect(path):
            if 'bad_file.py' in path:
                raise OSError("Permission denied")
            return self.mock_timestamp1

        mock_getsize.side_effect = getsize_side_effect
        mock_getmtime.side_effect = getmtime_side_effect

        extensions = ['py']
        manifest = generate_manifest(self.mock_base_path, extensions)

        expected_manifest = [
            {
                'path': 'good_file.py',
                'size_bytes': 100,
                'last_modified_utc': self.expected_iso_timestamp1
            }
        ]
        self.assertCountEqual(manifest, expected_manifest)

if __name__ == '__main__':
    unittest.main()
