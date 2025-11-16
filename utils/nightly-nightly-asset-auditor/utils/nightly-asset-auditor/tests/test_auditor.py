import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from io import StringIO

# Import the functions from the auditor script
# Mock rationale: We need to mock sys.path to allow importing the script as a module
# without it being in the standard Python path.
with patch.object(sys, 'path', [os.path.join(os.path.dirname(__file__), '../src')] + sys.path):
    from auditor import audit_directory, print_report, format_size

class TestAuditor(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Capture stdout to test printed output.
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()
        # Mock rationale: Capture stderr to test error messages.
        self.held_stderr = sys.stderr
        sys.stderr = self.mock_stderr = StringIO()

    def tearDown(self):
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_audit_directory_basic(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a valid directory path.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory structure with various files.
        mock_walk.return_value = [
            ('/mock/dir', [], ['file1.txt', 'image.jpg', 'script.py']),
            ('/mock/dir/subdir', [], ['doc.pdf', 'another.txt'])
        ]

        # Mock rationale: Provide deterministic file sizes.
        def getsize_side_effect(path):
            if 'file1.txt' in path: return 100
            if 'image.jpg' in path: return 5000000 # 5MB
            if 'script.py' in path: return 2000
            if 'doc.pdf' in path: return 1000000 # 1MB
            if 'another.txt' in path: return 500
            return 0
        mock_getsize.side_effect = getsize_side_effect

        inventory, total_files, total_size = audit_directory('/mock/dir')

        self.assertEqual(total_files, 5)
        self.assertEqual(total_size, 6002600)
        self.assertEqual(inventory['.txt']['count'], 2)
        self.assertEqual(inventory['.txt']['size'], 600)
        self.assertEqual(inventory['.jpg']['count'], 1)
        self.assertEqual(inventory['.jpg']['size'], 5000000)
        self.assertEqual(inventory['.py']['count'], 1)
        self.assertEqual(inventory['.py']['size'], 2000)
        self.assertEqual(inventory['.pdf']['count'], 1)
        self.assertEqual(inventory['.pdf']['size'], 1000000)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_audit_directory_empty(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a valid but empty directory.
        mock_isdir.return_value = True
        mock_walk.return_value = [('/mock/empty_dir', [], [])]
        mock_getsize.return_value = 0 # Should not be called for empty dir

        inventory, total_files, total_size = audit_directory('/mock/empty_dir')

        self.assertEqual(total_files, 0)
        self.assertEqual(total_size, 0)
        self.assertEqual(inventory, {})

    @patch('os.path.isdir')
    @patch('sys.exit')
    def test_audit_directory_non_existent(self, mock_exit, mock_isdir):
        # Mock rationale: Simulate a non-existent directory.
        mock_isdir.return_value = False

        audit_directory('/mock/non_existent')

        # Mock rationale: Verify that the script exits with an error code.
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Directory '/mock/non_existent' not found", self.mock_stderr.getvalue())

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    def test_audit_directory_no_extension_files(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with files without extensions.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/dir', [], ['README', 'LICENSE', 'binary_file'])
        ]
        def getsize_side_effect(path):
            if 'README' in path: return 100
            if 'LICENSE' in path: return 200
            if 'binary_file' in path: return 5000
            return 0
        mock_getsize.side_effect = getsize_side_effect

        inventory, total_files, total_size = audit_directory('/mock/dir')

        self.assertEqual(total_files, 3)
        self.assertEqual(total_size, 5300)
        self.assertEqual(inventory['(none)']['count'], 3)
        self.assertEqual(inventory['(none)']['size'], 5300)

    def test_format_size(self):
        self.assertEqual(format_size(100), "100 B")
        self.assertEqual(format_size(1024), "1.0 KB")
        self.assertEqual(format_size(1024 * 1024), "1.0 MB")
        self.assertEqual(format_size(1024 * 1024 * 1024), "1.0 GB")
        self.assertEqual(format_size(1500), "1.5 KB")
        self.assertEqual(format_size(1500000), "1.4 MB")

    def test_print_report_basic(self):
        inventory = {
            '.py': {'count': 2, 'size': 2000},
            '.txt': {'count': 1, 'size': 500},
            '.md': {'count': 1, 'size': 1000}
        }
        total_files = 4
        total_size = 3500
        directory_path = '/mock/dir'

        print_report(inventory, total_files, total_size, directory_path)
        output = self.mock_stdout.getvalue()

        self.assertIn("Scanning directory: /mock/dir", output)
        self.assertIn("Total Files: 4", output)
        self.assertIn("Total Size: 3.4 KB", output)
        self.assertIn(".py   : 2 files (2.0 KB) [57.1%]", output)
        self.assertIn(".md   : 1 file  (1.0 KB) [28.6%]", output)
        self.assertIn(".txt  : 1 file  (500 B) [14.3%]", output)

    def test_print_report_empty_inventory(self):
        inventory = {}
        total_files = 0
        total_size = 0
        directory_path = '/mock/empty_dir'

        print_report(inventory, total_files, total_size, directory_path)
        output = self.mock_stdout.getvalue()

        self.assertIn("No files found in the directory.", output)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize', side_effect=OSError("Permission denied"))
    def test_audit_directory_permission_error(self, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory where files cannot be accessed.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/dir', [], ['unreadable.txt', 'another.py'])
        ]

        inventory, total_files, total_size = audit_directory('/mock/dir')

        self.assertEqual(total_files, 0) # No files successfully processed
        self.assertEqual(total_size, 0)
        self.assertEqual(inventory, {})
        self.assertIn("Warning: Could not access '/mock/dir/unreadable.txt': Permission denied", self.mock_stderr.getvalue())
        self.assertIn("Warning: Could not access '/mock/dir/another.py': Permission denied", self.mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
