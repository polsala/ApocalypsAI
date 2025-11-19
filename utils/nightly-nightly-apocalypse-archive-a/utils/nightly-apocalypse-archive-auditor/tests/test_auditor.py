import unittest
import os
import datetime
from unittest.mock import patch, MagicMock
from collections import defaultdict

# Mock rationale: We need to simulate a file system without actually creating files
# on disk, ensuring tests are deterministic and fast.
# os.walk, os.path.getsize, os.path.getmtime are core file system interactions.
# datetime.datetime.now is mocked to ensure consistent "current time" for age calculations.

# Import the function to be tested
from src.auditor import audit_archive

class TestApocalypseArchiveAuditor(unittest.TestCase):

    # Define a fixed current time for deterministic age calculations
    MOCK_CURRENT_TIME = datetime.datetime(2023, 10, 26, 10, 0, 0)

    @patch('datetime.datetime')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_empty_directory(self, mock_isdir, mock_walk, mock_getsize, mock_getmtime, mock_datetime):
        mock_isdir.return_value = True
        mock_walk.return_value = [] # Simulate an empty directory
        mock_datetime.now.return_value = self.MOCK_CURRENT_TIME
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp # Allow real timestamp conversion

        report = audit_archive("/mock/path")
        self.assertEqual(report["total_files"], 0)
        self.assertEqual(report["total_size_bytes"], 0)
        self.assertEqual(report["files_by_extension"], defaultdict(int))
        self.assertEqual(report["old_files"], [])
        self.assertIn("Total files: 0", report["summary"])

    @patch('datetime.datetime')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_basic_file_scan(self, mock_isdir, mock_walk, mock_getsize, mock_getmtime, mock_datetime):
        mock_isdir.return_value = True
        # Simulate a directory with a few files
        mock_walk.return_value = [
            ("/mock/path", [], ["file1.txt", "document.pdf"]),
            ("/mock/path/subdir", [], ["image.jpg", "notes.md"])
        ]

        # Mock file sizes
        mock_getsize.side_effect = lambda p: {
            "/mock/path/file1.txt": 100,
            "/mock/path/document.pdf": 5000,
            "/mock/path/subdir/image.jpg": 15000,
            "/mock/path/subdir/notes.md": 200,
        }.get(p, 0)

        # Mock modification times (all recent, within age threshold)
        recent_timestamp = (self.MOCK_CURRENT_TIME - datetime.timedelta(days=365)).timestamp() # 1 year ago
        mock_getmtime.return_value = recent_timestamp

        mock_datetime.now.return_value = self.MOCK_CURRENT_TIME
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp

        report = audit_archive("/mock/path")

        self.assertEqual(report["total_files"], 4)
        self.assertEqual(report["total_size_bytes"], 100 + 5000 + 15000 + 200)
        self.assertEqual(dict(report["files_by_extension"]), {
            ".txt": 1,
            ".pdf": 1,
            ".jpg": 1,
            ".md": 1,
        })
        self.assertEqual(report["old_files"], [])
        self.assertIn("Total files: 4", report["summary"])
        self.assertIn("Total size: 0.02 MB", report["summary"]) # (100+5000+15000+200) / (1024*1024) = 0.019...

    @patch('datetime.datetime')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_file_filtering_by_extension(self, mock_isdir, mock_walk, mock_getsize, mock_getmtime, mock_datetime):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ("/mock/path", [], ["report.txt", "image.png", "data.json"])
        ]
        mock_getsize.side_effect = lambda p: {
            "/mock/path/report.txt": 100,
            "/mock/path/image.png": 2000,
            "/mock/path/data.json": 500,
        }.get(p, 0)
        recent_timestamp = (self.MOCK_CURRENT_TIME - datetime.timedelta(days=365)).timestamp()
        mock_getmtime.return_value = recent_timestamp
        mock_datetime.now.return_value = self.MOCK_CURRENT_TIME
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp

        report = audit_archive("/mock/path", include_extensions=['.txt', '.json'])

        self.assertEqual(report["total_files"], 2)
        self.assertEqual(report["total_size_bytes"], 100 + 500)
        self.assertEqual(dict(report["files_by_extension"]), {
            ".txt": 1,
            ".json": 1,
        })
        self.assertEqual(report["old_files"], [])

    @patch('datetime.datetime')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_old_files_identification(self, mock_isdir, mock_walk, mock_getsize, mock_getmtime, mock_datetime):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ("/mock/path", [], ["recent.txt", "old_doc.pdf", "ancient_log.log"])
        ]

        # Define specific modification times
        recent_mtime = (self.MOCK_CURRENT_TIME - datetime.timedelta(days=365 * 2)).timestamp() # 2 years ago
        old_mtime = (self.MOCK_CURRENT_TIME - datetime.timedelta(days=365 * 6)).timestamp() # 6 years ago
        ancient_mtime = (self.MOCK_CURRENT_TIME - datetime.timedelta(days=365 * 10)).timestamp() # 10 years ago

        def mock_getmtime_side_effect(path):
            if "recent.txt" in path: return recent_mtime
            if "old_doc.pdf" in path: return old_mtime
            if "ancient_log.log" in path: return ancient_mtime
            return 0

        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_getsize.return_value = 100 # Arbitrary size for all files

        mock_datetime.now.return_value = self.MOCK_CURRENT_TIME
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp

        # Test with default age threshold (5 years)
        report = audit_archive("/mock/path")

        self.assertEqual(report["total_files"], 3)
        self.assertEqual(len(report["old_files"]), 2) # old_doc.pdf and ancient_log.log
        
        old_file_paths = {f['path'] for f in report['old_files']}
        self.assertIn("/mock/path/old_doc.pdf", old_file_paths)
        self.assertIn("/mock/path/ancient_log.log", old_file_paths)

        # Check age values (approximate due to 365.25)
        for f in report['old_files']:
            if "old_doc.pdf" in f['path']:
                self.assertAlmostEqual(f['age_years'], 6.0, delta=0.1)
            if "ancient_log.log" in f['path']:
                self.assertAlmostEqual(f['age_years'], 10.0, delta=0.1)
        
        self.assertIn("Old files (>5 years): 2", report["summary"])

        # Test with a different age threshold (e.g., 8 years)
        report_8_years = audit_archive("/mock/path", age_threshold_years=8)
        self.assertEqual(len(report_8_years["old_files"]), 1) # Only ancient_log.log
        self.assertIn("/mock/path/ancient_log.log", {f['path'] for f in report_8_years['old_files']})
        self.assertIn("Old files (>8 years): 1", report_8_years["summary"])


    @patch('datetime.datetime')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_directory_not_found(self, mock_isdir, mock_walk, mock_getsize, mock_getmtime, mock_datetime):
        mock_isdir.return_value = False # Simulate directory not existing
        mock_datetime.now.return_value = self.MOCK_CURRENT_TIME
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp

        with self.assertRaises(FileNotFoundError):
            audit_archive("/nonexistent/path")

    @patch('datetime.datetime')
    @patch('os.path.getmtime')
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_os_error_during_scan(self, mock_isdir, mock_walk, mock_getsize, mock_getmtime, mock_datetime):
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ("/mock/path", [], ["good_file.txt", "bad_file.txt"])
        ]
        
        def getsize_side_effect(path):
            if "bad_file.txt" in path:
                raise OSError("Permission denied")
            return 100
        
        mock_getsize.side_effect = getsize_side_effect
        mock_getmtime.return_value = (self.MOCK_CURRENT_TIME - datetime.timedelta(days=365)).timestamp()
        mock_datetime.now.return_value = self.MOCK_CURRENT_TIME
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp

        # The function should not raise an error, but print a warning and continue
        # We can capture stdout if needed, but for now, just ensure it doesn't crash
        report = audit_archive("/mock/path")
        self.assertEqual(report["total_files"], 1) # Only good_file.txt should be counted
        self.assertEqual(report["total_size_bytes"], 100)
        self.assertEqual(dict(report["files_by_extension"]), {".txt": 1})
        self.assertEqual(report["old_files"], [])
