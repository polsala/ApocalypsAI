import unittest
import os
from unittest.mock import patch, MagicMock
from collections import defaultdict
from src.auditor import audit_directory, format_size

class TestAuditor(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_empty_directory(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory structure.
        mock_isdir.return_value = True
        mock_walk.return_value = [] # No files or subdirectories
        mock_getsize.return_value = 0 # Should not be called, but good practice

        result = audit_directory("/fake/path")
        expected = {
            'total_files': 0,
            'total_size_bytes': 0,
            'files_by_extension': {},
            'empty_files': 0,
        }
        self.assertEqual(result, expected)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_single_file_directory(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with one file.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/fake/path', [], ['file.txt'])
        ]
        mock_getsize.side_effect = lambda p: 100 if p == '/fake/path/file.txt' else 0

        result = audit_directory("/fake/path")
        expected = {
            'total_files': 1,
            'total_size_bytes': 100,
            'files_by_extension': {'.txt': 1},
            'empty_files': 0,
        }
        self.assertEqual(result, expected)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_multiple_files_and_extensions(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with multiple files of different types and sizes.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/fake/path', ['subdir'], ['file1.txt', 'image.png']),
            ('/fake/path/subdir', [], ['script.py', 'doc.md', 'empty.log'])
        ]
        # Define specific sizes for mocked files
        file_sizes = {
            '/fake/path/file1.txt': 100,
            '/fake/path/image.png': 5000,
            '/fake/path/subdir/script.py': 250,
            '/fake/path/subdir/doc.md': 75,
            '/fake/path/subdir/empty.log': 0,
        }
        mock_getsize.side_effect = lambda p: file_sizes.get(p, 0)

        result = audit_directory("/fake/path")
        expected = {
            'total_files': 5,
            'total_size_bytes': 100 + 5000 + 250 + 75 + 0, # 5425
            'files_by_extension': {
                '.txt': 1,
                '.png': 1,
                '.py': 1,
                '.md': 1,
                '.log': 1,
            },
            'empty_files': 1,
        }
        self.assertEqual(result, expected)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_directory_with_no_extension_files(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate files without extensions.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/fake/path', [], ['README', 'LICENSE', 'config.yml'])
        ]
        file_sizes = {
            '/fake/path/README': 50,
            '/fake/path/LICENSE': 200,
            '/fake/path/config.yml': 120,
        }
        mock_getsize.side_effect = lambda p: file_sizes.get(p, 0)

        result = audit_directory("/fake/path")
        expected = {
            'total_files': 3,
            'total_size_bytes': 50 + 200 + 120, # 370
            'files_by_extension': {
                '': 2, # README and LICENSE have no extension
                '.yml': 1,
            },
            'empty_files': 0,
        }
        self.assertEqual(result, expected)

    @patch('os.path.isdir')
    def test_invalid_path(self, mock_isdir):
        # Mock rationale: Simulate an invalid directory path.
        mock_isdir.return_value = False
        with self.assertRaises(ValueError):
            audit_directory("/non/existent/path")

    def test_format_size(self):
        self.assertEqual(format_size(0), "0 B")
        self.assertEqual(format_size(100), "100.00 B")
        self.assertEqual(format_size(1024), "1.00 KB")
        self.assertEqual(format_size(1536), "1.50 KB")
        self.assertEqual(format_size(1024 * 1024), "1.00 MB")
        self.assertEqual(format_size(1.5 * 1024 * 1024 * 1024), "1.50 GB")
        self.assertEqual(format_size(2 * (1024**4)), "2.00 TB") # 2 TB
        self.assertEqual(format_size(2.5 * (1024**5)), "2560.00 TB") # 2.5 PB, should cap at TB for now

if __name__ == '__main__':
    unittest.main()
