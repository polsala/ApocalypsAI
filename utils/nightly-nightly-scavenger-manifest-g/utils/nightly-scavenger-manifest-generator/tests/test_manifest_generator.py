import unittest
import os
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.manifest_generator import generate_manifest

class TestManifestGenerator(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.abspath')
    def test_empty_directory(self, mock_abspath, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory structure for testing.
        mock_isdir.return_value = True
        mock_walk.return_value = [] # No files or subdirectories
        mock_abspath.side_effect = lambda x: f"/mock/path/{x.lstrip('./')}"

        result = generate_manifest("./empty_dir")
        self.assertEqual(result["total_files"], 0)
        self.assertEqual(result["total_size_bytes"], 0)
        self.assertEqual(result["summary_by_extension"], {})
        self.assertEqual(result["recent_files"], [])
        self.assertEqual(result["scanned_directory"], "/mock/path/empty_dir")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.abspath')
    def test_directory_with_various_files(self, mock_abspath, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with different file types and sizes.
        mock_isdir.return_value = True
        
        # Simulate current time for modification dates
        now = datetime.now()
        
        # File data: (path, size, mtime)
        files_data = {
            "/mock/path/dir1/file1.txt": (100, (now - timedelta(days=10)).timestamp()),
            "/mock/path/dir1/file2.log": (200, (now - timedelta(days=20)).timestamp()),
            "/mock/path/dir2/file3.json": (300, (now - timedelta(days=30)).timestamp()),
            "/mock/path/dir2/file4.txt": (150, (now - timedelta(days=40)).timestamp()),
            "/mock/path/dir1/no_ext_file": (50, (now - timedelta(days=50)).timestamp()),
        }

        # os.walk returns (root, dirs, files)
        mock_walk.return_value = [
            ("/mock/path/dir1", [], ["file1.txt", "file2.log", "no_ext_file"]),
            ("/mock/path/dir2", [], ["file3.json", "file4.txt"])
        ]
        
        mock_getsize.side_effect = lambda p: files_data[p][0]
        mock_getmtime.side_effect = lambda p: files_data[p][1]
        mock_abspath.side_effect = lambda x: x # For simplicity, assume paths are already absolute in mock

        result = generate_manifest("/mock/path")

        self.assertEqual(result["total_files"], 5)
        self.assertEqual(result["total_size_bytes"], 800)
        self.assertEqual(result["scanned_directory"], "/mock/path")
        self.assertIn(".txt", result["summary_by_extension"])
        self.assertEqual(result["summary_by_extension"][".txt"]["count"], 2)
        self.assertEqual(result["summary_by_extension"][".txt"]["total_size_bytes"], 250)
        self.assertIn(".log", result["summary_by_extension"])
        self.assertEqual(result["summary_by_extension"][".log"]["count"], 1)
        self.assertEqual(result["summary_by_extension"][".log"]["total_size_bytes"], 200)
        self.assertIn(".json", result["summary_by_extension"])
        self.assertEqual(result["summary_by_extension"][".json"]["count"], 1)
        self.assertEqual(result["summary_by_extension"][".json"]["total_size_bytes"], 300)
        self.assertIn("no_extension", result["summary_by_extension"])
        self.assertEqual(result["summary_by_extension"]["no_extension"]["count"], 1)
        self.assertEqual(result["summary_by_extension"]["no_extension"]["total_size_bytes"], 50)
        self.assertEqual(result["recent_files"], []) # No recent_days specified

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.abspath')
    def test_directory_with_recent_files(self, mock_abspath, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate files with modification times, some within the 'recent' threshold.
        mock_isdir.return_value = True
        
        now = datetime.now()
        
        files_data = {
            "/mock/path/old_file.txt": (100, (now - timedelta(days=10)).timestamp()),
            "/mock/path/recent_file1.log": (200, (now - timedelta(days=1)).timestamp()),
            "/mock/path/recent_file2.json": (300, (now - timedelta(hours=12)).timestamp()),
            "/mock/path/very_old_file.md": (50, (now - timedelta(days=100)).timestamp()),
        }

        mock_walk.return_value = [
            ("/mock/path", [], ["old_file.txt", "recent_file1.log", "recent_file2.json", "very_old_file.md"])
        ]
        
        mock_getsize.side_effect = lambda p: files_data[p][0]
        mock_getmtime.side_effect = lambda p: files_data[p][1]
        mock_abspath.side_effect = lambda x: x

        result = generate_manifest("/mock/path", recent_days=2)

        self.assertEqual(result["total_files"], 4)
        self.assertEqual(result["total_size_bytes"], 650)
        self.assertEqual(len(result["recent_files"]), 2)
        
        # Check that recent files are sorted newest first
        self.assertEqual(result["recent_files"][0]["path"], "/mock/path/recent_file2.json")
        self.assertEqual(result["recent_files"][1]["path"], "/mock/path/recent_file1.log")

        # Verify content of recent files
        recent_file2 = next(f for f in result["recent_files"] if f["path"] == "/mock/path/recent_file2.json")
        self.assertEqual(recent_file2["size_bytes"], 300)
        
        recent_file1 = next(f for f in result["recent_files"] if f["path"] == "/mock/path/recent_file1.log")
        self.assertEqual(recent_file1["size_bytes"], 200)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.abspath')
    def test_no_recent_files_in_period(self, mock_abspath, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate files that are all older than the 'recent' threshold.
        mock_isdir.return_value = True
        
        now = datetime.now()
        
        files_data = {
            "/mock/path/file1.txt": (100, (now - timedelta(days=5)).timestamp()),
            "/mock/path/file2.log": (200, (now - timedelta(days=6)).timestamp()),
        }

        mock_walk.return_value = [
            ("/mock/path", [], ["file1.txt", "file2.log"])
        ]
        
        mock_getsize.side_effect = lambda p: files_data[p][0]
        mock_getmtime.side_effect = lambda p: files_data[p][1]
        mock_abspath.side_effect = lambda x: x

        result = generate_manifest("/mock/path", recent_days=3) # Only look back 3 days

        self.assertEqual(result["total_files"], 2)
        self.assertEqual(result["total_size_bytes"], 300)
        self.assertEqual(result["recent_files"], []) # Expect no recent files

    @patch('os.path.isdir')
    @patch('os.path.abspath')
    def test_invalid_directory_path(self, mock_abspath, mock_isdir):
        # Mock rationale: Simulate a non-existent directory to test error handling.
        mock_isdir.return_value = False
        mock_abspath.return_value = "/non/existent/path"

        with self.assertRaises(FileNotFoundError) as cm:
            generate_manifest("/non/existent/path")
        self.assertIn("Directory not found", str(cm.exception))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.abspath')
    def test_file_access_error_handling(self, mock_abspath, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a scenario where some files cannot be accessed (e.g., permission denied).
        mock_isdir.return_value = True
        
        now = datetime.now()
        
        files_data = {
            "/mock/path/accessible.txt": (100, (now - timedelta(days=1)).timestamp()),
            "/mock/path/inaccessible.log": (None, None), # This will cause OSError
        }

        mock_walk.return_value = [
            ("/mock/path", [], ["accessible.txt", "inaccessible.log"])
        ]
        
        def getsize_side_effect(path):
            if path == "/mock/path/inaccessible.log":
                raise OSError("Permission denied")
            return files_data[path][0]

        def getmtime_side_effect(path):
            if path == "/mock/path/inaccessible.log":
                raise OSError("Permission denied")
            return files_data[path][1]

        mock_getsize.side_effect = getsize_side_effect
        mock_getmtime.side_effect = getmtime_side_effect
        mock_abspath.side_effect = lambda x: x

        result = generate_manifest("/mock/path")

        # Only the accessible file should be counted
        self.assertEqual(result["total_files"], 1)
        self.assertEqual(result["total_size_bytes"], 100)
        self.assertIn(".txt", result["summary_by_extension"])
        self.assertEqual(result["summary_by_extension"][".txt"]["count"], 1)
        self.assertEqual(result["summary_by_extension"][".txt"]["total_size_bytes"], 100)
        self.assertNotIn(".log", result["summary_by_extension"]) # Inaccessible file should not contribute
        self.assertEqual(len(result["recent_files"]), 0) # No recent_days, so empty

if __name__ == '__main__':
    unittest.main()
