import unittest
import os
from unittest.mock import patch, mock_open
from collections import defaultdict
from io import StringIO
import sys

# Import the functions to be tested
from src.auditor import audit_directory, format_size, main

class TestAuditor(unittest.TestCase):

    def test_format_size(self):
        self.assertEqual(format_size(0), "0 B")
        self.assertEqual(format_size(500), "500 B")
        self.assertEqual(format_size(1023), "1023 B")
        self.assertEqual(format_size(1024), "1.00 KB")
        self.assertEqual(format_size(1536), "1.50 KB")
        self.assertEqual(format_size(1024 * 1024 - 1), "1023.99 KB")
        self.assertEqual(format_size(1024 * 1024), "1.00 MB")
        self.assertEqual(format_size(1024 * 1024 * 1024 - 1), "1023.99 MB")
        self.assertEqual(format_size(1024 * 1024 * 1024), "1.00 GB")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_audit_directory_basic(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure and file contents without touching the actual filesystem.
        # os.path.isdir: To confirm the base directory exists.
        # os.walk: To simulate iterating through directories and files.
        # os.path.getsize: To provide deterministic file sizes.
        # builtins.open: To provide deterministic file content for keyword searching.

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', ('subdir1',), ('file1.txt', 'file2.py')),
            ('/mock_root/subdir1', (), ('report.md', 'secret.txt')),
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock_root/file1.txt': 100,
            '/mock_root/file2.py': 200,
            '/mock_root/subdir1/report.md': 300,
            '/mock_root/subdir1/secret.txt': 400,
        }.get(p, 0)

        mock_file_open.side_effect = lambda p, mode='r', encoding='utf-8', errors='ignore': {
            '/mock_root/file1.txt': StringIO("Hello world"),
            '/mock_root/file2.py': StringIO("import os"),
            '/mock_root/subdir1/report.md': StringIO("Project report"),
            '/mock_root/subdir1/secret.txt': StringIO("This is a secret base with coordinates 123,456."),
        }.get(p)

        report = audit_directory('/mock_root', allowed_extensions=['.txt', '.py', '.md'], critical_keywords=['secret base', 'coordinates'])

        self.assertIn("Total files scanned: 4", report)
        self.assertIn("Total size scanned: 1.00 KB", report) # 100+200+300+400 = 1000 bytes
        self.assertIn(".txt: 2 files, 500 B", report)
        self.assertIn(".py: 1 file, 200 B", report)
        self.assertIn(".md: 1 file, 300 B", report)
        self.assertIn("Critical Files Found", report)
        self.assertIn("- /mock_root/subdir1/secret.txt (Keywords: secret base, coordinates)", report)
        self.assertNotIn("file1.txt", report) # Not critical

    @patch('os.path.isdir')
    def test_audit_directory_not_found(self, mock_isdir):
        # Mock rationale: Simulate a non-existent directory to test error handling.
        mock_isdir.return_value = False
        with self.assertRaises(FileNotFoundError):
            audit_directory('/non_existent_dir')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_audit_directory_no_extensions_filter(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Test behavior when no specific extensions are provided, all files should be included.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', (), ('file.txt', 'image.jpg')),
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock_root/file.txt': 50,
            '/mock_root/image.jpg': 150,
        }.get(p, 0)
        mock_file_open.return_value = StringIO("content")

        report = audit_directory('/mock_root')
        self.assertIn("Total files scanned: 2", report)
        self.assertIn(".txt: 1 file, 50 B", report)
        self.assertIn(".jpg: 1 file, 150 B", report)
        self.assertIn("No critical files found.", report)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_audit_directory_with_extensions_filter(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Test behavior when specific extensions are provided, only matching files should be included.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', (), ('file.txt', 'image.jpg', 'script.py')),
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock_root/file.txt': 50,
            '/mock_root/image.jpg': 150,
            '/mock_root/script.py': 200,
        }.get(p, 0)
        mock_file_open.return_value = StringIO("content")

        report = audit_directory('/mock_root', allowed_extensions=['.txt', '.py'])
        self.assertIn("Total files scanned: 2", report)
        self.assertIn(".txt: 1 file, 50 B", report)
        self.assertIn(".py: 1 file, 200 B", report)
        self.assertNotIn(".jpg", report) # Should be filtered out
        self.assertIn("No critical files found.", report)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_audit_directory_case_insensitive_extensions(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Ensure extension matching is case-insensitive.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', (), ('file.TXT', 'script.Py', 'doc.md')),
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock_root/file.TXT': 50,
            '/mock_root/script.Py': 100,
            '/mock_root/doc.md': 150,
        }.get(p, 0)
        mock_file_open.return_value = StringIO("content")

        report = audit_directory('/mock_root', allowed_extensions=['.txt', '.py'])
        self.assertIn("Total files scanned: 2", report)
        self.assertIn(".txt: 1 file, 50 B", report)
        self.assertIn(".py: 1 file, 100 B", report)
        self.assertNotIn(".md", report)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_audit_directory_critical_keywords_case_insensitive(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Ensure keyword matching is case-insensitive.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', (), ('note.txt', 'log.txt')),
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock_root/note.txt': 100,
            '/mock_root/log.txt': 100,
        }.get(p, 0)
        mock_file_open.side_effect = lambda p, mode='r', encoding='utf-8', errors='ignore': {
            '/mock_root/note.txt': StringIO("Important SECRET info here."),
            '/mock_root/log.txt': StringIO("No secrets."),
        }.get(p)

        report = audit_directory('/mock_root', critical_keywords=['secret'])
        self.assertIn("Critical Files Found", report)
        self.assertIn("- /mock_root/note.txt (Keywords: secret)", report)
        self.assertNotIn("log.txt", report)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_audit_directory_empty(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Test behavior with an empty directory.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', (), ()), # Empty root
        ]
        report = audit_directory('/mock_root')
        self.assertIn("Total files scanned: 0", report)
        self.assertIn("Total size scanned: 0 B", report)
        self.assertIn("No files found matching criteria.", report)
        self.assertIn("No critical files found.", report)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_audit_directory_unreadable_file(self, mock_file_open, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file that cannot be read (e.g., binary, permission error)
        # but should still be counted for size/type if getsize works.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', (), ('binary.bin', 'text.txt')),
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock_root/binary.bin': 1000,
            '/mock_root/text.txt': 50,
        }.get(p, 0)
        
        # Simulate IOError for binary.bin when trying to open it as text
        def open_side_effect(p, mode='r', encoding='utf-8', errors='ignore'):
            if p == '/mock_root/binary.bin':
                raise IOError("Permission denied or binary file")
            return StringIO("normal text")
        mock_file_open.side_effect = open_side_effect

        report = audit_directory('/mock_root', critical_keywords=['secret'])
        self.assertIn("Total files scanned: 2", report)
        self.assertIn(".bin: 1 file, 1000 B", report)
        self.assertIn(".txt: 1 file, 50 B", report)
        self.assertIn("No critical files found.", report) # 'secret' not in 'normal text'

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO) # Capture stderr for error messages
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_success(self, mock_parse_args, mock_file_open, mock_getsize, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Test the main CLI entry point.
        # argparse.ArgumentParser.parse_args: To control CLI arguments without actual command line input.
        # sys.stdout: To capture printed output.
        # os.path.isdir, os.walk, os.path.getsize, builtins.open: As in other tests, to simulate file system.

        mock_parse_args.return_value = argparse.Namespace(
            directory_path='/mock_root',
            extensions=['.txt'],
            critical_keywords=['important']
        )
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', (), ('file.txt', 'other.log')),
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock_root/file.txt': 100,
            '/mock_root/other.log': 200,
        }.get(p, 0)
        mock_file_open.side_effect = lambda p, mode='r', encoding='utf-8', errors='ignore': {
            '/mock_root/file.txt': StringIO("This is important data."),
            '/mock_root/other.log': StringIO("Just a log."),
        }.get(p)

        # Call main and capture exit code
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0) # Expect successful exit

        output = mock_stdout.getvalue()
        self.assertIn("Total files scanned: 1", output) # Only .txt
        self.assertIn(".txt: 1 file, 100 B", output)
        self.assertIn("Critical Files Found", output)
        self.assertIn("- /mock_root/file.txt (Keywords: important)", output)
        self.assertEqual(mock_stderr.getvalue(), "") # No errors to stderr

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_file_not_found_error(self, mock_parse_args, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Test main's error handling for FileNotFoundError.
        mock_parse_args.return_value = argparse.Namespace(
            directory_path='/non_existent_dir',
            extensions=None,
            critical_keywords=None
        )
        mock_isdir.return_value = False # Simulate directory not existing

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1) # Expect error exit

        output = mock_stderr.getvalue()
        self.assertIn("Error: Directory not found: /non_existent_dir", output)
        self.assertEqual(mock_stdout.getvalue(), "") # No output to stdout

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_unexpected_error(self, mock_parse_args, mock_file_open, mock_getsize, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Test main's error handling for an unexpected exception during audit.
        mock_parse_args.return_value = argparse.Namespace(
            directory_path='/mock_root',
            extensions=None,
            critical_keywords=None
        )
        mock_isdir.return_value = True
        # Simulate an unexpected error during os.walk
        mock_walk.side_effect = Exception("Disk read error!")

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1) # Expect error exit

        output = mock_stderr.getvalue()
        self.assertIn("An unexpected error occurred: Disk read error!", output)
        self.assertEqual(mock_stdout.getvalue(), "") # No output to stdout

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_extension_normalization(self, mock_parse_args, mock_file_open, mock_getsize, mock_walk, mock_isdir, mock_stderr, mock_stdout):
        # Mock rationale: Test that extensions passed via CLI are correctly normalized (e.g., 'txt' becomes '.txt').
        mock_parse_args.return_value = argparse.Namespace(
            directory_path='/mock_root',
            extensions=['txt', '.md', 'PY'], # Mixed formats
            critical_keywords=None
        )
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock_root', (), ('file.txt', 'doc.md', 'script.py', 'image.jpg')),
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock_root/file.txt': 10,
            '/mock_root/doc.md': 20,
            '/mock_root/script.py': 30,
            '/mock_root/image.jpg': 40,
        }.get(p, 0)
        mock_file_open.return_value = StringIO("content")

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0);

        output = mock_stdout.getvalue()
        self.assertIn("Total files scanned: 3", output)
        self.assertIn(".txt: 1 file, 10 B", output)
        self.assertIn(".md: 1 file, 20 B", output)
        self.assertIn(".py: 1 file, 30 B", output)
        self.assertNotIn(".jpg", output) # Should be filtered out

if __name__ == '__main__':
    unittest.main()
