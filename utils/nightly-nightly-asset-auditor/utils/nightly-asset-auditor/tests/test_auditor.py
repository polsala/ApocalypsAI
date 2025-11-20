import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from io import StringIO

# Add the src directory to the path to import auditor.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import auditor

class TestAuditor(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime') # Mock getmtime for report timestamp
    def test_audit_directory_basic(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure and file sizes without actual disk I/O.
        # This ensures deterministic and fast tests.
        mock_isdir.return_value = True
        mock_getmtime.return_value = 1678886400.0 # A fixed timestamp for consistency

        # Simulate a simple directory with various files
        mock_walk.return_value = [
            ('/mock/root', ['subdir1'], ['file1.md', 'config.json']),
            ('/mock/root/subdir1', [], ['script.py', 'data.txt', 'image.png', 'no_ext_file']),
        ]

        # Map file paths to their sizes
        mock_getsize.side_effect = lambda p: {
            '/mock/root/file1.md': 100,
            '/mock/root/config.json': 50,
            '/mock/root/subdir1/script.py': 200,
            '/mock/root/subdir1/data.txt': 75,
            '/mock/root/subdir1/image.png': 5000,
            '/mock/root/subdir1/no_ext_file': 25,
        }.get(p, 0)

        results = auditor.audit_directory('/mock/root')

        self.assertEqual(results['total_files'], 6)
        self.assertEqual(results['total_size'], 5450)
        self.assertEqual(results['root_dir'], '/mock/root')

        summary = results['file_type_summary']
        self.assertEqual(summary['.md']['count'], 1)
        self.assertEqual(summary['.md']['size'], 100)
        self.assertEqual(summary['.md']['category'], 'Critical')

        self.assertEqual(summary['.json']['count'], 1)
        self.assertEqual(summary['.json']['size'], 50)
        self.assertEqual(summary['.json']['category'], 'Critical')

        self.assertEqual(summary['.py']['count'], 1)
        self.assertEqual(summary['.py']['size'], 200)
        self.assertEqual(summary['.py']['category'], 'Important')

        self.assertEqual(summary['.txt']['count'], 1)
        self.assertEqual(summary['.txt']['size'], 75)
        self.assertEqual(summary['.txt']['category'], 'Critical')

        self.assertEqual(summary['.png']['count'], 1)
        self.assertEqual(summary['.png']['size'], 5000)
        self.assertEqual(summary['.png']['category'], 'Unknown')

        self.assertEqual(summary['[no_extension]']['count'], 1)
        self.assertEqual(summary['[no_extension]']['size'], 25)
        self.assertEqual(summary['[no_extension]']['category'], 'Unknown')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_audit_directory_empty(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Test behavior with an empty directory.
        mock_isdir.return_value = True
        mock_getmtime.return_value = 1678886400.0
        mock_walk.return_value = [
            ('/mock/empty_root', [], []),
        ]
        mock_getsize.return_value = 0

        results = auditor.audit_directory('/mock/empty_root')

        self.assertEqual(results['total_files'], 0)
        self.assertEqual(results['total_size'], 0)
        self.assertEqual(results['file_type_summary'], {})

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_audit_directory_inaccessible_files(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Ensure the auditor gracefully handles files it cannot access (e.g., permission errors).
        mock_isdir.return_value = True
        mock_getmtime.return_value = 1678886400.0

        mock_walk.return_value = [
            ('/mock/root', [], ['accessible.txt', 'inaccessible.log']),
        ]

        def getsize_side_effect(path):
            if 'inaccessible.log' in path:
                raise OSError("Permission denied")
            return 100 # For accessible.txt

        mock_getsize.side_effect = getsize_side_effect

        results = auditor.audit_directory('/mock/root')

        self.assertEqual(results['total_files'], 1)
        self.assertEqual(results['total_size'], 100)
        self.assertIn('.txt', results['file_type_summary'])
        self.assertNotIn('.log', results['file_type_summary'])

    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    def test_audit_directory_not_found(self, mock_getmtime, mock_isdir):
        # Mock rationale: Test error handling for non-existent directories.
        mock_isdir.return_value = False
        mock_getmtime.return_value = 1678886400.0

        with self.assertRaisesRegex(ValueError, "Directory not found: /non/existent/path"):
            auditor.audit_directory('/non/existent/path')

    def test_format_size(self):
        # Mock rationale: Test the size formatting utility function.
        self.assertEqual(auditor.format_size(0), "0 B")
        self.assertEqual(auditor.format_size(500), "500.00 B")
        self.assertEqual(auditor.format_size(1024), "1.00 KB")
        self.assertEqual(auditor.format_size(1536), "1.50 KB")
        self.assertEqual(auditor.format_size(1024 * 1024), "1.00 MB")
        self.assertEqual(auditor.format_size(1024**3 * 2.5), "2.50 GB")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_generate_report(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Verify the output format of the generated Markdown report.
        mock_isdir.return_value = True
        mock_getmtime.return_value = 1678886400.0 # Fixed timestamp for deterministic output

        mock_walk.return_value = [
            ('/mock/root', [], ['file.md', 'script.py', 'log.log', 'unknown.xyz', 'no_ext']),
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock/root/file.md': 100,
            '/mock/root/script.py': 200,
            '/mock/root/log.log': 500,
            '/mock/root/unknown.xyz': 150,
            '/mock/root/no_ext': 50,
        }.get(p, 0)

        results = auditor.audit_directory('/mock/root')
        report = auditor.generate_report(results)

        expected_report_lines = [
            "# Asset Audit Report for '/mock/root'\n",
            "*Generated on: 1678886400.0*\n",
            "\n## Summary\n",
            "- **Total Files Scanned**: 5\n",
            "- **Total Size**: 1.00 KB\n",
            "## File Type Breakdown\n",
            "| Extension | Count | Total Size | Survival Score |\n",
            "| :-------- | :---- | :--------- | :------------- |\n",
            "| `.md` | 1 | 100.00 B | Critical |\n",
            "| `.py` | 1 | 200.00 B | Important |\n",
            "| `.log` | 1 | 500.00 B | Useful |\n",
            "| `[no_extension]` | 1 | 50.00 B | Unknown |\n",
            "| `.xyz` | 1 | 150.00 B | Unknown |\n"
        ]
        self.assertEqual(report, "".join(expected_report_lines))

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_main_success(self, mock_getmtime, mock_getsize, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Test the main CLI entry point for a successful run.
        mock_isdir.return_value = True
        mock_getmtime.return_value = 1678886400.0
        mock_walk.return_value = [
            ('/mock/root', [], ['test.md']),
        ]
        mock_getsize.return_value = 100

        # Temporarily modify sys.argv to simulate command-line arguments
        with patch('sys.argv', ['auditor.py', '/mock/root']):
            auditor.main()
            output = mock_stdout.getvalue()
            self.assertIn("Asset Audit Report for '/mock/root'", output)
            self.assertIn("Total Files Scanned: 1", output)
            self.assertIn("| `.md` | 1 | 100.00 B | Critical |", output)
            self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    def test_main_no_args(self, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Test the main CLI entry point for missing arguments.
        mock_isdir.return_value = False

        with patch('sys.argv', ['auditor.py']):
            with self.assertRaises(SystemExit) as cm:
                auditor.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Usage: python src/auditor.py <path_to_directory>", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    def test_main_invalid_directory(self, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Test the main CLI entry point for an invalid directory path.
        mock_isdir.return_value = False

        with patch('sys.argv', ['auditor.py', '/non/existent']):
            with self.assertRaises(SystemExit) as cm:
                auditor.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Directory not found: /non/existent", mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
