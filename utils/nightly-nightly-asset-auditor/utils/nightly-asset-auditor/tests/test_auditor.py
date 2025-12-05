import unittest
import os
from unittest.mock import patch, MagicMock

# Mock rationale: We need to simulate file system interactions (os.walk, os.path.getsize, os.path.isdir)
# without actually touching the disk. This ensures tests are fast, deterministic, and don't rely on
# the state of the actual file system.

# Import the functions to be tested
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from auditor import audit_directory, format_bytes, print_report
sys.path.pop(0)

class TestAuditor(unittest.TestCase):

    def test_format_bytes(self):
        self.assertEqual(format_bytes(0), "0.0 B")
        self.assertEqual(format_bytes(500), "500.0 B")
        self.assertEqual(format_bytes(1024), "1.0 KB")
        self.assertEqual(format_bytes(1536), "1.5 KB")
        self.assertEqual(format_bytes(1024**2), "1.0 MB")
        self.assertEqual(format_bytes(1.5 * (1024**3)), "1.5 GB")
        self.assertEqual(format_bytes(1.5 * (1024**4)), "1.5 TB")
        self.assertEqual(format_bytes(1.5 * (1024**5)), "1.5 PB")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_audit_directory_basic(self, mock_getsize, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        # Mock rationale: Simulate a directory existing.

        # Mock rationale: Simulate a simple directory structure with various files and sizes.
        mock_walk.return_value = [
            ('/mock/dir', [], ['file1.txt', 'image.jpg']),
            ('/mock/dir/subdir', [], ['doc.pdf', 'script.py'])
        ]

        # Mock rationale: Define specific sizes for each mocked file.
        mock_getsize.side_effect = lambda x: {
            '/mock/dir/file1.txt': 100,
            '/mock/dir/image.jpg': 5000000,
            '/mock/dir/subdir/doc.pdf': 200000,
            '/mock/dir/subdir/script.py': 500
        }.get(x, 0)

        report = audit_directory('/mock/dir')

        self.assertEqual(report['scanned_path'], '/mock/dir')
        self.assertEqual(report['total_files_scanned'], 4)
        self.assertEqual(report['total_size_scanned'], 5200600)

        expected_summary = {
            '.jpg': {'count': 1, 'size': 5000000},
            '.pdf': {'count': 1, 'size': 200000},
            '.py': {'count': 1, 'size': 500},
            '.txt': {'count': 1, 'size': 100}
        }
        self.assertEqual(report['file_type_summary'], expected_summary)

        expected_largest = [
            {'path': '/mock/dir/image.jpg', 'size': 5000000},
            {'path': '/mock/dir/subdir/doc.pdf', 'size': 200000},
            {'path': '/mock/dir/subdir/script.py', 'size': 500},
            {'path': '/mock/dir/file1.txt', 'size': 100}
        ]
        self.assertEqual(report['largest_files'], expected_largest)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_audit_directory_empty(self, mock_getsize, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        # Mock rationale: Simulate an empty directory.
        mock_walk.return_value = [
            ('/mock/empty_dir', [], [])
        ]
        mock_getsize.return_value = 0 # Mock rationale: No files, so getsize won't be called for real files.

        report = audit_directory('/mock/empty_dir')

        self.assertEqual(report['scanned_path'], '/mock/empty_dir')
        self.assertEqual(report['total_files_scanned'], 0)
        self.assertEqual(report['total_size_scanned'], 0)
        self.assertEqual(report['file_type_summary'], {})
        self.assertEqual(report['largest_files'], [])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_audit_directory_no_extension(self, mock_getsize, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        # Mock rationale: Simulate files without extensions.
        mock_walk.return_value = [
            ('/mock/dir', [], ['README', 'LICENSE', 'config.yml'])
        ]
        mock_getsize.side_effect = lambda x: {
            '/mock/dir/README': 1000,
            '/mock/dir/LICENSE': 2000,
            '/mock/dir/config.yml': 500
        }.get(x, 0)

        report = audit_directory('/mock/dir')

        self.assertEqual(report['total_files_scanned'], 3)
        self.assertEqual(report['total_size_scanned'], 3500)
        expected_summary = {
            '(no_extension)': {'count': 2, 'size': 3000},
            '.yml': {'count': 1, 'size': 500}
        }
        self.assertEqual(report['file_type_summary'], expected_summary)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_audit_directory_top_n_largest(self, mock_getsize, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        # Mock rationale: Simulate many files to test the top_n_largest logic.
        mock_walk.return_value = [
            ('/mock/dir', [], [f'file_{i}.bin' for i in range(20)])
        ]
        # Mock rationale: Assign varying sizes to files.
        mock_getsize.side_effect = lambda x: int(x.split('_')[1].split('.')[0]) * 1000 # file_0.bin = 0, file_1.bin = 1000, ..., file_19.bin = 19000

        report = audit_directory('/mock/dir', top_n_largest=5)

        self.assertEqual(len(report['largest_files']), 5)
        # Expect files 19, 18, 17, 16, 15
        expected_largest_sizes = [19000, 18000, 17000, 16000, 15000]
        actual_largest_sizes = [f['size'] for f in report['largest_files']]
        self.assertEqual(actual_largest_sizes, expected_largest_sizes)

    @patch('os.path.isdir')
    def test_audit_directory_invalid_path(self, mock_isdir):
        mock_isdir.return_value = False
        # Mock rationale: Simulate an invalid directory path.
        with self.assertRaises(ValueError):
            audit_directory('/non/existent/path')

    @patch('sys.stdout', new_callable=MagicMock)
    def test_print_report_empty(self, mock_stdout):
        report = {
            "scanned_path": "/mock/empty_dir",
            "total_files_scanned": 0,
            "total_size_scanned": 0,
            "file_type_summary": {},
            "largest_files": []
        }
        print_report(report)
        mock_stdout.assert_called()
        output = mock_stdout.call_args_list[0].args[0] # Get the first print call's argument
        self.assertIn("No files found", output)

    @patch('sys.stdout', new_callable=MagicMock)
    def test_print_report_full(self, mock_stdout):
        report = {
            "scanned_path": "/mock/dir",
            "total_files_scanned": 4,
            "total_size_scanned": 5200600,
            "file_type_summary": {
                '.jpg': {'count': 1, 'size': 5000000},
                '.pdf': {'count': 1, 'size': 200000},
                '.py': {'count': 1, 'size': 500},
                '.txt': {'count': 1, 'size': 100}
            },
            "largest_files": [
                {'path': '/mock/dir/image.jpg', 'size': 5000000},
                {'path': '/mock/dir/subdir/doc.pdf', 'size': 200000}
            ]
        }
        print_report(report)
        mock_stdout.assert_called()
        # Concatenate all print calls to reconstruct the full output
        output = "\n".join([call.args[0] for call in mock_stdout.call_args_list if call.args])

        self.assertIn("Asset Audit Report for: /mock/dir", output)
        self.assertIn("Total Files Scanned: 4", output)
        self.assertIn("Total Size Scanned: 5.0 MB", output) # 5200600 bytes is ~5.0 MB
        self.assertIn(".jpg           : 1 files (4.8 MB)", output) # 5000000 bytes is ~4.8 MB
        self.assertIn("Top Largest Files:", output)
        self.assertIn("1. /mock/dir/image.jpg (4.8 MB)", output)

if __name__ == '__main__':
    unittest.main()
