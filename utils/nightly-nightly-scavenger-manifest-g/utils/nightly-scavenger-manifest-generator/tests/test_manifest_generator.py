import unittest
import json
import os
from unittest.mock import patch, MagicMock
from datetime import datetime

# Import the function to be tested
from src.manifest_generator import generate_manifest

class TestManifestGenerator(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_empty_directory(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir, os.walk, os.path.getsize, os.path.getmtime are file system operations and need to be faked for deterministic tests.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ("/mock_empty_dir", [], [])
        ]
        mock_getsize.return_value = 0
        mock_getmtime.return_value = 0

        expected_manifest = {
            "directory": os.path.abspath("/mock_empty_dir"),
            "summary": {
                "total_files": 0,
                "total_directories": 0,
                "total_size_bytes": 0,
                "unique_extensions": []
            },
            "file_type_breakdown": {}
        }

        result = generate_manifest("/mock_empty_dir")
        self.assertEqual(result, expected_manifest)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_directory_with_files(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir, os.walk, os.path.getsize, os.path.getmtime are file system operations and need to be faked for deterministic tests.
        mock_isdir.return_value = True

        # Define mock file system structure and properties
        mock_walk_data = [
            ("/mock_dir", ["subdir1"], ["file1.txt", "data.json"]),
            ("/mock_dir/subdir1", [], ["file2.log", "no_ext_file", "another.txt"]),
        ]
        mock_walk.return_value = mock_walk_data

        # Define mock file sizes and modification times
        # Using fixed timestamps for deterministic ISO 8601 output
        file_info = {
            os.path.join("/mock_dir", "file1.txt"): {"size": 100, "mtime": 1672531200}, # Jan 1, 2023 00:00:00 UTC
            os.path.join("/mock_dir", "data.json"): {"size": 200, "mtime": 1672617600}, # Jan 2, 2023 00:00:00 UTC
            os.path.join("/mock_dir/subdir1", "file2.log"): {"size": 50, "mtime": 1672704000}, # Jan 3, 2023 00:00:00 UTC
            os.path.join("/mock_dir/subdir1", "no_ext_file"): {"size": 75, "mtime": 1672790400}, # Jan 4, 2023 00:00:00 UTC
            os.path.join("/mock_dir/subdir1", "another.txt"): {"size": 150, "mtime": 1672876800}, # Jan 5, 2023 00:00:00 UTC
        }

        mock_getsize.side_effect = lambda p: file_info.get(p, {"size": 0})["size"]
        mock_getmtime.side_effect = lambda p: file_info.get(p, {"mtime": 0})["mtime"]

        expected_manifest = {
            "directory": os.path.abspath("/mock_dir"),
            "summary": {
                "total_files": 5,
                "total_directories": 1,
                "total_size_bytes": 575,
                "unique_extensions": [".json", ".log", ".txt", "no_extension"]
            },
            "file_type_breakdown": {
                ".txt": {
                    "count": 2,
                    "total_size_bytes": 250,
                    "latest_modified": "2023-01-05T00:00:00Z" # Latest of file1.txt and another.txt
                },
                ".json": {
                    "count": 1,
                    "total_size_bytes": 200,
                    "latest_modified": "2023-01-02T00:00:00Z"
                },
                ".log": {
                    "count": 1,
                    "total_size_bytes": 50,
                    "latest_modified": "2023-01-03T00:00:00Z"
                },
                "no_extension": {
                    "count": 1,
                    "total_size_bytes": 75,
                    "latest_modified": "2023-01-04T00:00:00Z"
                }
            }
        }

        result = generate_manifest("/mock_dir")
        self.assertEqual(result, expected_manifest)

    @patch('os.path.isdir')
    def test_non_existent_directory(self, mock_isdir):
        # Mock rationale: os.path.isdir is a file system operation and needs to be faked for deterministic tests.
        mock_isdir.return_value = False
        with self.assertRaises(FileNotFoundError):
            generate_manifest("/non_existent_dir")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_file_inaccessibility_during_walk(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir, os.walk, os.path.getsize, os.path.getmtime are file system operations and need to be faked for deterministic tests.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ("/mock_dir", [], ["accessible.txt", "inaccessible.txt"])
        ]

        # accessible.txt will work, inaccessible.txt will raise OSError
        file_info = {
            os.path.join("/mock_dir", "accessible.txt"): {"size": 100, "mtime": 1672531200}, # Jan 1, 2023 00:00:00 UTC
        }
        
        def getsize_side_effect(path):
            if path == os.path.join("/mock_dir", "inaccessible.txt"):
                raise OSError("Permission denied")
            return file_info.get(path, {"size": 0})["size"]

        def getmtime_side_effect(path):
            if path == os.path.join("/mock_dir", "inaccessible.txt"):
                raise OSError("Permission denied")
            return file_info.get(path, {"mtime": 0})["mtime"]

        mock_getsize.side_effect = getsize_side_effect
        mock_getmtime.side_effect = getmtime_side_effect

        expected_manifest = {
            "directory": os.path.abspath("/mock_dir"),
            "summary": {
                "total_files": 1, # Only accessible.txt is counted
                "total_directories": 0,
                "total_size_bytes": 100,
                "unique_extensions": [".txt"]
            },
            "file_type_breakdown": {
                ".txt": {
                    "count": 1,
                    "total_size_bytes": 100,
                    "latest_modified": "2023-01-01T00:00:00Z"
                }
            }
        }

        result = generate_manifest("/mock_dir")
        self.assertEqual(result, expected_manifest)
