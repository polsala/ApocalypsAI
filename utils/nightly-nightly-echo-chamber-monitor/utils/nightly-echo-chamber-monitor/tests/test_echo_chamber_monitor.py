import unittest
import os
import hashlib
from unittest.mock import patch, mock_open, MagicMock
from io import StringIO
import sys

# Import the functions to be tested
from src.echo_chamber_monitor import (
    calculate_file_hash,
    find_duplicate_files,
    generate_report,
    main
)

class TestEchoChamberMonitor(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = StringIO()
        self.held_stderr = sys.stderr
        sys.stderr = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch("builtins.open", new_callable=mock_open)
    def test_calculate_file_hash(self, mock_file_open):
        # Mock rationale: Avoids actual file system access for hash calculation.
        # We control the content the 'file' returns.
        mock_file_open.return_value.read.side_effect = [b"hello", b" world", b""]
        expected_hash = hashlib.sha256(b"hello world").hexdigest()
        self.assertEqual(calculate_file_hash("dummy_path.txt"), expected_hash)
        mock_file_open.assert_called_with("dummy_path.txt", 'rb')

        # Test with empty file
        mock_file_open.return_value.read.side_effect = [b""]
        expected_hash_empty = hashlib.sha256(b"").hexdigest()
        self.assertEqual(calculate_file_hash("empty.txt"), expected_hash_empty)

        # Test IOError
        mock_file_open.side_effect = IOError("Permission denied")
        self.assertIsNone(calculate_file_hash("inaccessible.txt"))

    @patch("os.walk")
    @patch("os.path.getsize")
    @patch("os.path.islink", return_value=False) # Mock rationale: Prevent actual symlink checks.
    @patch("src.echo_chamber_monitor.calculate_file_hash") # Mock rationale: Isolate hash calculation logic.
    @patch("os.path.isdir", return_value=True) # Mock rationale: Assume paths are valid directories.
    def test_find_duplicate_files(self, mock_isdir, mock_calculate_hash, mock_islink, mock_getsize, mock_walk):
        # Mock rationale: os.walk, os.path.getsize, os.path.islink, and calculate_file_hash are
        # mocked to simulate file system structure and content without actual disk I/O.

        # Scenario 1: No duplicates
        mock_walk.return_value = [
            ("/root", [], ["fileA.txt", "fileB.txt"]),
        ]
        mock_getsize.side_effect = [100, 200]
        mock_calculate_hash.side_effect = ["hashA", "hashB"]
        self.assertEqual(find_duplicate_files(["/root"]), {})

        # Scenario 2: Simple duplicates
        mock_walk.return_value = [
            ("/root", [], ["file1.txt", "file2.txt", "file3.txt"]),
        ]
        mock_getsize.side_effect = [100, 100, 200] # file1 and file2 have same size
        mock_calculate_hash.side_effect = ["hashX", "hashX", "hashY"] # file1 and file2 have same hash
        expected_duplicates = {
            "hashX": ["/root/file1.txt", "/root/file2.txt"]
        }
        result = find_duplicate_files(["/root"])
        # Sort paths in result for deterministic comparison
        for h in result:
            result[h].sort()
        self.assertEqual(result, expected_duplicates)

        # Scenario 3: Duplicates across subdirectories
        mock_walk.side_effect = [
            ("/root/dir1", [], ["fileA.txt"]),
            ("/root/dir2", [], ["fileB.txt"]),
        ]
        mock_getsize.side_effect = [50, 50]
        mock_calculate_hash.side_effect = ["hashZ", "hashZ"]
        expected_duplicates = {
            "hashZ": ["/root/dir1/fileA.txt", "/root/dir2/fileB.txt"]
        }
        result = find_duplicate_files(["/root/dir1", "/root/dir2"])
        for h in result:
            result[h].sort()
        self.assertEqual(result, expected_duplicates)

        # Scenario 4: Files smaller than min_size
        mock_walk.return_value = [
            ("/root", [], ["small.txt", "large.txt"]),
        ]
        mock_getsize.side_effect = [5, 100] # small.txt is 5 bytes
        mock_calculate_hash.side_effect = ["hashL"] # Only large.txt will be hashed
        self.assertEqual(find_duplicate_files(["/root"], min_size=10), {})
        mock_calculate_hash.assert_called_once_with("/root/large.txt")

        # Scenario 5: Inaccessible file during getsize
        mock_walk.return_value = [
            ("/root", [], ["file1.txt", "file2.txt"]),
        ]
        mock_getsize.side_effect = [100, OSError("Permission denied")]
        mock_calculate_hash.side_effect = ["hashA"] # Only file1.txt will be hashed
        self.assertEqual(find_duplicate_files(["/root"]), {})
        mock_calculate_hash.assert_called_once_with("/root/file1.txt")

        # Scenario 6: Invalid path
        mock_isdir.return_value = False
        mock_walk.return_value = [] # No walk happens
        self.assertEqual(find_duplicate_files(["/invalid/path"]), {})
        self.assertIn("Warning: Path '/invalid/path' is not a valid directory. Skipping.", sys.stderr.getvalue())
        mock_isdir.return_value = True # Reset for other tests

    def test_generate_report_no_duplicates(self):
        # Mock rationale: No file system interaction needed, just string formatting.
        generate_report({})
        self.assertIn("No duplicate files found. The void is clear! ✨", sys.stdout.getvalue())

    def test_generate_report_with_duplicates(self):
        # Mock rationale: No file system interaction needed, just string formatting.
        duplicates = {
            "hash123": ["/path/to/fileA.txt", "/path/to/fileB.txt"],
            "hash456": ["/another/fileX.log", "/yet/another/fileY.log"]
        }
        generate_report(duplicates)
        output = sys.stdout.getvalue()
        self.assertIn("--- Duplicate Files Found ---", output)
        self.assertIn("Group 1 (SHA256: hash123)", output)
        self.assertIn("  - /path/to/fileA.txt", output)
        self.assertIn("  - /path/to/fileB.txt", output)
        self.assertIn("Group 2 (SHA256: hash456)", output)
        self.assertIn("  - /another/fileX.log", output)
        self.assertIn("  - /yet/another/fileY.log", output)
        self.assertIn("--- End of Report ---", output)

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_report_to_file(self, mock_file_open):
        # Mock rationale: Avoids actual file system write.
        duplicates = {
            "hash123": ["/path/to/fileA.txt", "/path/to/fileB.txt"]
        }
        output_filename = "report.txt"
        generate_report(duplicates, output_filename)
        mock_file_open.assert_called_with(output_filename, 'w')
        handle = mock_file_open()
        self.assertIn("--- Duplicate Files Found ---", handle.write.call_args[0][0])
        self.assertIn("Report written to report.txt", sys.stdout.getvalue())

    @patch("builtins.open", new_callable=mock_open)
    def test_generate_report_to_file_io_error(self, mock_file_open):
        # Mock rationale: Simulate a file write error.
        mock_file_open.side_effect = IOError("Disk full")
        duplicates = {
            "hash123": ["/path/to/fileA.txt"]
        }
        output_filename = "report.txt"
        with self.assertRaises(SystemExit) as cm:
            generate_report(duplicates, output_filename)
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error writing report to report.txt: Disk full", sys.stderr.getvalue())

    @patch("argparse.ArgumentParser.parse_args")
    @patch("src.echo_chamber_monitor.find_duplicate_files")
    @patch("src.echo_chamber_monitor.generate_report")
    def test_main_function(self, mock_generate_report, mock_find_duplicate_files, mock_parse_args):
        # Mock rationale: Isolate main function logic from argument parsing and core logic.
        mock_args = MagicMock()
        mock_args.path = ["/test/dir1", "/test/dir2"]
        mock_args.min_size = 10
        mock_args.output = None
        mock_parse_args.return_value = mock_args

        mock_find_duplicate_files.return_value = {"hashX": ["/test/dir1/file.txt"]}

        main()

        mock_parse_args.assert_called_once()
        mock_find_duplicate_files.assert_called_once_with(["/test/dir1", "/test/dir2"], 10)
        mock_generate_report.assert_called_once_with({"hashX": ["/test/dir1/file.txt"]}, None)

    @patch("argparse.ArgumentParser.parse_args")
    @patch("sys.exit") # Mock rationale: Prevent actual exit during test
    def test_main_function_no_path_arg(self, mock_exit, mock_parse_args):
        # Mock rationale: Test argument parsing error without exiting the test runner.
        mock_args = MagicMock()
        mock_args.path = []
        mock_parse_args.return_value = mock_args

        # argparse.error calls sys.exit(2)
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2)
        self.assertIn("At least one --path argument is required.", sys.stderr.getvalue())
