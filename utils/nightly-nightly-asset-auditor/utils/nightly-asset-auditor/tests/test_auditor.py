import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the path to allow importing auditor.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from auditor import audit_directory, format_size

class TestAuditor(unittest.TestCase):

    def test_format_size(self):
        self.assertEqual(format_size(0), "0 Bytes")
        self.assertEqual(format_size(100), "100 Bytes")
        self.assertEqual(format_size(1024), "1.0 KB")
        self.assertEqual(format_size(1024 * 1024), "1.0 MB")
        self.assertEqual(format_size(1536), "1.5 KB")
        self.assertEqual(format_size(1024 * 1024 * 1.75), "1.75 MB")
        self.assertEqual(format_size(1024 * 1024 * 1024 * 2), "2.0 GB")

    @patch('os.path.isdir')
    def test_audit_directory_not_found(self, mock_isdir):
        # Mock rationale: Simulate a non-existent directory for error handling.
        mock_isdir.return_value = False
        result = audit_directory('/nonexistent/path')
        self.assertIn("Error: Directory '/nonexistent/path' not found", result)

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_audit_directory_basic(self, mock_isdir, mock_walk, mock_getsize):
        # Mock rationale: Simulate a simple directory structure with various files.
        # This allows deterministic testing without actual file system access.
        mock_isdir.return_value = True

        # Define a mock file system structure for os.walk
        mock_walk.return_value = [
            ('/mock/root', ['subdir1', 'subdir2'], ['file1.txt', 'main.py']),
            ('/mock/root/subdir1', [], ['data.json', 'config.yaml']),
            ('/mock/root/subdir2', [], ['image.png', 'another.py']),
        ]

        # Define mock file sizes for os.path.getsize
        # Mock rationale: Assign fixed sizes to files for predictable total size calculations.
        def getsize_side_effect(path):
            if 'file1.txt' in path: return 100
            if 'main.py' in path: return 200
            if 'data.json' in path: return 300
            if 'config.yaml' in path: return 150
            if 'image.png' in path: return 500
            if 'another.py' in path: return 250
            return 0 # Default for unexpected paths

        mock_getsize.side_effect = getsize_side_effect

        report = audit_directory('/mock/root')

        self.assertIn("Apocalypse Asset Audit Report for: /mock/root", report)
        self.assertIn("Total Files Scanned: 6", report)
        self.assertIn("Total Size: 1.46 KB", report) # 100+200+300+150+500+250 = 1500 bytes = 1.46 KB
        self.assertIn("| .png      | 1     | 500 Bytes  |", report)
        self.assertIn("| .py       | 2     | 450 Bytes  |", report)
        self.assertIn("| .json     | 1     | 300 Bytes  |", report)
        self.assertIn("| .yaml     | 1     | 150 Bytes  |", report)
        self.assertIn("| .txt      | 1     | 100 Bytes  |", report)

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_audit_directory_empty(self, mock_isdir, mock_walk, mock_getsize):
        # Mock rationale: Simulate an empty directory to ensure correct reporting.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/empty', [], []),
        ]
        mock_getsize.return_value = 0

        report = audit_directory('/mock/empty')

        self.assertIn("Total Files Scanned: 0", report)
        self.assertIn("Total Size: 0 Bytes", report)
        self.assertIn("No files found matching criteria.", report)

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_audit_directory_with_ignored_dirs(self, mock_isdir, mock_walk, mock_getsize):
        # Mock rationale: Verify that specified directories (e.g., .git, node_modules) are ignored.
        mock_isdir.return_value = True

        mock_walk.return_value = [
            ('/mock/project', ['src', '.git', 'node_modules', 'docs'], ['README.md']),
            ('/mock/project/src', [], ['app.py']),
            ('/mock/project/.git', ['hooks'], ['config']),
            ('/mock/project/node_modules', ['express'], ['package.json']),
            ('/mock/project/docs', [], ['guide.md']),
        ]

        def getsize_side_effect(path):
            if 'README.md' in path: return 100
            if 'app.py' in path: return 200
            if 'config' in path: return 50 # Should be ignored
            if 'package.json' in path: return 75 # Should be ignored
            if 'guide.md' in path: return 150
            return 0

        mock_getsize.side_effect = getsize_side_effect

        report = audit_directory('/mock/project')

        self.assertIn("Total Files Scanned: 3", report) # README.md, app.py, guide.md
        self.assertIn("Total Size: 450 Bytes", report) # 100 + 200 + 150
        self.assertIn("| .md       | 2     | 250 Bytes  |", report) # README.md, guide.md
        self.assertIn("| .py       | 1     | 200 Bytes  |", report) # app.py
        self.assertNotIn(".git", report)
        self.assertNotIn("node_modules", report)
        self.assertNotIn("config", report)
        self.assertNotIn("package.json", report)

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_audit_directory_no_extension_files(self, mock_isdir, mock_walk, mock_getsize):
        # Mock rationale: Test handling of files without extensions.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/root', [], ['Dockerfile', 'LICENSE', 'script']),
        ]

        def getsize_side_effect(path):
            if 'Dockerfile' in path: return 100
            if 'LICENSE' in path: return 200
            if 'script' in path: return 50
            return 0

        mock_getsize.side_effect = getsize_side_effect

        report = audit_directory('/mock/root')

        self.assertIn("Total Files Scanned: 3", report)
        self.assertIn("Total Size: 350 Bytes", report)
        self.assertIn("| (no ext)  | 3     | 350 Bytes  |", report)

    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('os.path.isdir')
    def test_audit_directory_os_error_during_getsize(self, mock_isdir, mock_walk, mock_getsize):
        # Mock rationale: Simulate a file disappearing or permission error during scan.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/root', [], ['good.txt', 'bad.txt']),
        ]

        def getsize_side_effect(path):
            if 'good.txt' in path: return 100
            if 'bad.txt' in path: raise OSError("Permission denied")
            return 0

        mock_getsize.side_effect = getsize_side_effect

        report = audit_directory('/mock/root')

        self.assertIn("Total Files Scanned: 1", report)
        self.assertIn("Total Size: 100 Bytes", report)
        self.assertIn("| .txt      | 1     | 100 Bytes  |", report)
        self.assertNotIn("bad.txt", report)
