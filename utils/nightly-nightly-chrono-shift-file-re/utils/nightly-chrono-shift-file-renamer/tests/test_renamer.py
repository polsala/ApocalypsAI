import unittest
import os
import sys
import datetime
from unittest.mock import patch, MagicMock
from io import StringIO

# Adjust path to import renamer from src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from renamer import rename_files_in_directory, get_modification_date, is_already_renamed

class TestRenamer(unittest.TestCase):

    @patch('os.path.getmtime')
    def test_get_modification_date(self, mock_getmtime):
        # Mock rationale: os.path.getmtime returns a timestamp, which is non-deterministic
        # and depends on the actual file system. We need a fixed timestamp for testing.
        mock_getmtime.return_value = 1678886400.0  # Corresponds to 2023-03-15 00:00:00 UTC
        self.assertEqual(get_modification_date("dummy_path"), "2023-03-15")

    def test_is_already_renamed(self):
        self.assertTrue(is_already_renamed("2023-01-01_file.txt", "2023-01-01"))
        self.assertFalse(is_already_renamed("file.txt", "2023-01-01"))
        self.assertFalse(is_already_renamed("2022-12-31_file.txt", "2023-01-01")) # Wrong date prefix

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.getmtime')
    @patch('os.rename')
    @patch('sys.stdout', new_callable=StringIO)
    def test_rename_files_basic(self, mock_stdout, mock_rename, mock_getmtime, mock_listdir, mock_isdir):
        # Mock rationale:
        # os.path.isdir: To simulate the target directory existing.
        # os.listdir: To simulate files present in the directory.
        # os.path.getmtime: To provide deterministic modification times for files.
        # os.rename: To prevent actual file system changes during tests.
        # sys.stdout: To capture print output for assertion.

        mock_isdir.return_value = True
        mock_listdir.return_value = ["file1.txt", "file2.jpg"]
        # Set specific modification times for each file
        mock_getmtime.side_effect = [
            datetime.datetime(2023, 1, 1, 10, 0, 0).timestamp(), # file1.txt
            datetime.datetime(2023, 2, 15, 14, 30, 0).timestamp() # file2.jpg
        ]

        result = rename_files_in_directory("/test/dir", dry_run=False)

        self.assertEqual(result, 0)
        mock_rename.assert_any_call("/test/dir/file1.txt", "/test/dir/2023-01-01_file1.txt")
        mock_rename.assert_any_call("/test/dir/file2.jpg", "/test/dir/2023-02-15_file2.jpg")
        self.assertEqual(mock_rename.call_count, 2)
        output = mock_stdout.getvalue()
        self.assertIn("Renamed: 'file1.txt' -> '2023-01-01_file1.txt'", output)
        self.assertIn("Renamed: 'file2.jpg' -> '2023-02-15_file2.jpg'", output)
        self.assertIn("Files renamed: 2", output)
        self.assertIn("Files skipped: 0", output)
        self.assertIn("Files with errors: 0", output)


    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.getmtime')
    @patch('os.rename')
    @patch('sys.stdout', new_callable=StringIO)
    def test_rename_files_dry_run(self, mock_stdout, mock_rename, mock_getmtime, mock_listdir, mock_isdir):
        # Mock rationale: Same as above, but verifying no actual rename calls.
        mock_isdir.return_value = True
        mock_listdir.return_value = ["file.txt"]
        mock_getmtime.return_value = datetime.datetime(2023, 3, 1, 12, 0, 0).timestamp()

        result = rename_files_in_directory("/test/dir", dry_run=True)

        self.assertEqual(result, 0)
        mock_rename.assert_not_called()
        output = mock_stdout.getvalue()
        self.assertIn("[DRY RUN] Would rename: 'file.txt' -> '2023-03-01_file.txt'", output)
        self.assertIn("Files renamed: 0", output) # In dry run, renamed count is 0
        self.assertIn("Files skipped: 0", output)
        self.assertIn("Files with errors: 0", output)

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.getmtime')
    @patch('os.rename')
    @patch('sys.stdout', new_callable=StringIO)
    def test_skip_already_renamed(self, mock_stdout, mock_rename, mock_getmtime, mock_listdir, mock_isdir):
        # Mock rationale: Verifying the idempotent behavior.
        mock_isdir.return_value = True
        mock_listdir.return_value = ["2023-04-01_existing.doc"]
        mock_getmtime.return_value = datetime.datetime(2023, 4, 1, 9, 0, 0).timestamp()

        result = rename_files_in_directory("/test/dir", dry_run=False)

        self.assertEqual(result, 0)
        mock_rename.assert_not_called()
        output = mock_stdout.getvalue()
        self.assertIn("Skipping '2023-04-01_existing.doc': Already has date prefix '2023-04-01_'.", output)
        self.assertIn("Files renamed: 0", output)
        self.assertIn("Files skipped: 1", output)
        self.assertIn("Files with errors: 0", output)

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.getmtime')
    @patch('os.rename')
    @patch('sys.stdout', new_callable=StringIO)
    def test_skip_directories(self, mock_stdout, mock_rename, mock_getmtime, mock_listdir, mock_isdir):
        # Mock rationale: Ensuring directories are not processed as files.
        mock_isdir.side_effect = [
            True, # For the target directory itself
            False, # For 'file.txt'
            True   # For 'subdir'
        ]
        mock_listdir.return_value = ["file.txt", "subdir"]
        mock_getmtime.return_value = datetime.datetime(2023, 5, 1, 11, 0, 0).timestamp()

        result = rename_files_in_directory("/test/dir", dry_run=False)

        self.assertEqual(result, 0)
        mock_rename.assert_called_once_with("/test/dir/file.txt", "/test/dir/2023-05-01_file.txt")
        output = mock_stdout.getvalue()
        self.assertIn("Skipping directory: subdir", output)
        self.assertIn("Renamed: 'file.txt' -> '2023-05-01_file.txt'", output)
        self.assertIn("Files renamed: 1", output)
        self.assertIn("Files skipped: 0", output) # Directories are skipped, not counted as 'already renamed'
        self.assertIn("Files with errors: 0", output)

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('sys.stderr', new_callable=StringIO)
    def test_directory_not_found(self, mock_stderr, mock_listdir, mock_isdir):
        # Mock rationale: Testing error handling for non-existent directory.
        mock_isdir.return_value = False

        result = rename_files_in_directory("/non/existent/dir")

        self.assertEqual(result, 1)
        mock_listdir.assert_not_called()
        self.assertIn("Error: Directory '/non/existent/dir' not found.", mock_stderr.getvalue())

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.getmtime')
    @patch('os.rename')
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    def test_rename_os_error(self, mock_stdout, mock_stderr, mock_rename, mock_getmtime, mock_listdir, mock_isdir):
        # Mock rationale: Testing error handling for os.rename failure.
        mock_isdir.return_value = True
        mock_listdir.return_value = ["bad_file.txt"]
        mock_getmtime.return_value = datetime.datetime(2023, 6, 1, 13, 0, 0).timestamp()
        mock_rename.side_effect = OSError("Permission denied")

        result = rename_files_in_directory("/test/dir", dry_run=False)

        self.assertEqual(result, 1) # Should return 1 on errors
        mock_rename.assert_called_once()
        self.assertIn("Error processing file 'bad_file.txt': Permission denied", mock_stderr.getvalue())
        self.assertIn("Files renamed: 0", mock_stdout.getvalue())
        self.assertIn("Files skipped: 0", mock_stdout.getvalue())
        self.assertIn("Files with errors: 1", mock_stdout.getvalue())

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.getmtime')
    @patch('os.rename')
    @patch('sys.stdout', new_callable=StringIO)
    def test_no_files_to_rename(self, mock_stdout, mock_rename, mock_getmtime, mock_listdir, mock_isdir):
        # Mock rationale: Test scenario where directory is empty or contains only already-renamed files.
        mock_isdir.return_value = True
        mock_listdir.return_value = [] # Empty directory

        result = rename_files_in_directory("/test/dir", dry_run=False)

        self.assertEqual(result, 0)
        mock_rename.assert_not_called()
        output = mock_stdout.getvalue()
        self.assertIn("Scanning directory: /test/dir", output)
        self.assertIn("Files renamed: 0", output)
        self.assertIn("Files skipped: 0", output)
        self.assertIn("Files with errors: 0", output)
