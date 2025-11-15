import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the functions from the sweeper module
from src.sweeper import find_dust_bunnies, get_file_age_in_days, print_report

class TestSweeper(unittest.TestCase):

    # Mock current time for deterministic age calculations
    MOCK_NOW = datetime(2023, 10, 26, 12, 0, 0)
    MOCK_NOW_TIMESTAMP = MOCK_NOW.timestamp()

    @patch('src.sweeper.datetime')
    def test_get_file_age_in_days(self, mock_datetime):
        # Mock rationale: Ensure `datetime.now()` returns a fixed point in time
        # for deterministic age calculations, regardless of when the test runs.
        mock_datetime.now.return_value = self.MOCK_NOW
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp # Use real fromtimestamp

        # Mock rationale: Simulate os.path.getmtime returning a specific timestamp.
        # This allows testing file age without actual file system interaction.
        with patch('os.path.getmtime', return_value=(self.MOCK_NOW - timedelta(days=100)).timestamp()):
            self.assertEqual(get_file_age_in_days("dummy_file.txt"), 100)

        with patch('os.path.getmtime', return_value=(self.MOCK_NOW - timedelta(days=365)).timestamp()):
            self.assertEqual(get_file_age_in_days("another_dummy.log"), 365)

        # Test file not found scenario
        with patch('os.path.getmtime', side_effect=FileNotFoundError):
            self.assertEqual(get_file_age_in_days("non_existent.txt"), -1)

    @patch('src.sweeper.datetime')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.listdir') # For robust empty directory check
    def test_find_dust_bunnies_basic(self, mock_listdir, mock_isfile, mock_getmtime, mock_getsize, mock_walk, mock_isdir, mock_datetime):
        # Mock rationale: Ensure `datetime.now()` returns a fixed point in time
        # for deterministic age calculations, regardless of when the test runs.
        mock_datetime.now.return_value = self.MOCK_NOW
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp # Use real fromtimestamp

        # Mock rationale: Simulate the root path being a valid directory.
        mock_isdir.return_value = True

        # Mock rationale: Simulate the file system structure and contents.
        # This allows testing the traversal logic without actual file system access.
        mock_walk.return_value = [
            ("/root", ["dir1", "empty_dir"], ["file_old.txt", "file_empty.txt", "file_recent.txt"]),
            ("/root/dir1", [], ["sub_file.log"]),
            ("/root/empty_dir", [], []), # This will be detected as empty by os.listdir
        ]

        # Mock rationale: Simulate file sizes for empty/non-empty files.
        mock_getsize.side_effect = lambda p: {
            "/root/file_old.txt": 100,
            "/root/file_empty.txt": 0,
            "/root/file_recent.txt": 50,
            "/root/dir1/sub_file.log": 20,
        }.get(p, 1) # Default to 1 for other files

        # Mock rationale: Simulate file modification times for old/recent files.
        mock_getmtime.side_effect = lambda p: {
            "/root/file_old.txt": (self.MOCK_NOW - timedelta(days=400)).timestamp(), # Older than 365
            "/root/file_empty.txt": (self.MOCK_NOW - timedelta(days=10)).timestamp(),
            "/root/file_recent.txt": (self.MOCK_NOW - timedelta(days=100)).timestamp(), # Newer than 365
            "/root/dir1/sub_file.log": (self.MOCK_NOW - timedelta(days=500)).timestamp(), # Older than 365
        }.get(p, self.MOCK_NOW_TIMESTAMP)

        # Mock rationale: Simulate os.path.isfile for files.
        mock_isfile.side_effect = lambda p: p in [
            "/root/file_old.txt", "/root/file_empty.txt", "/root/file_recent.txt", "/root/dir1/sub_file.log"
        ]

        # Mock rationale: Simulate os.listdir for checking truly empty directories.
        # This is crucial for accurately identifying empty directories.
        mock_listdir.side_effect = lambda p: {
            "/root": ["dir1", "empty_dir", "file_old.txt", "file_empty.txt", "file_recent.txt"],
            "/root/dir1": ["sub_file.log"],
            "/root/empty_dir": [], # This is truly empty
        }.get(p, [])


        results = find_dust_bunnies("/root", age_threshold_days=365)

        self.assertIsNotNone(results)
        self.assertEqual(len(results["old_files"]), 2)
        self.assertIn("/root/file_old.txt", [f[0] for f in results["old_files"]])
        self.assertIn("/root/dir1/sub_file.log", [f[0] for f in results["old_files"]])

        self.assertEqual(len(results["empty_files"]), 1)
        self.assertIn("/root/file_empty.txt", results["empty_files"])

        self.assertEqual(len(results["empty_dirs"]), 1)
        self.assertIn("/root/empty_dir", results["empty_dirs"])

    @patch('src.sweeper.datetime')
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.listdir')
    def test_find_dust_bunnies_no_issues(self, mock_listdir, mock_isfile, mock_getmtime, mock_getsize, mock_walk, mock_isdir, mock_datetime):
        # Mock rationale: Ensure `datetime.now()` returns a fixed point in time
        # for deterministic age calculations, regardless of when the test runs.
        mock_datetime.now.return_value = self.MOCK_NOW
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp

        # Mock rationale: Simulate a clean file system with no dust bunnies.
        mock_walk.return_value = [
            ("/clean_root", ["sub_dir"], ["recent_file.txt"]),
            ("/clean_root/sub_dir", [], ["another_recent.log"]),
        ]
        mock_getsize.return_value = 100 # All files have size
        mock_getmtime.return_value = (self.MOCK_NOW - timedelta(days=10)).timestamp() # All files are recent
        mock_isfile.return_value = True
        mock_listdir.side_effect = lambda p: {
            "/clean_root": ["sub_dir", "recent_file.txt"],
            "/clean_root/sub_dir": ["another_recent.log"],
        }.get(p, [])

        results = find_dust_bunnies("/clean_root", age_threshold_days=365)

        self.assertIsNotNone(results)
        self.assertEqual(len(results["old_files"]), 0)
        self.assertEqual(len(results["empty_files"]), 0)
        self.assertEqual(len(results["empty_dirs"]), 0)

    @patch('src.sweeper.datetime')
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.isfile')
    @patch('os.listdir')
    def test_find_dust_bunnies_nested_empty_dirs(self, mock_listdir, mock_isfile, mock_getmtime, mock_getsize, mock_walk, mock_isdir, mock_datetime):
        # Mock rationale: Ensure `datetime.now()` returns a fixed point in time
        # for deterministic age calculations, regardless of when the test runs.
        mock_datetime.now.return_value = self.MOCK_NOW
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp

        # Mock rationale: Simulate nested empty directories.
        mock_walk.return_value = [
            ("/root", ["dir_a", "dir_b"], []),
            ("/root/dir_a", ["dir_a_empty"], []),
            ("/root/dir_a/dir_a_empty", [], []),
            ("/root/dir_b", [], []),
        ]
        mock_getsize.return_value = 1 # No empty files
        mock_getmtime.return_value = self.MOCK_NOW_TIMESTAMP # No old files
        mock_isfile.return_value = False # No files
        mock_listdir.side_effect = lambda p: {
            "/root": ["dir_a", "dir_b"],
            "/root/dir_a": ["dir_a_empty"],
            "/root/dir_a/dir_a_empty": [], # Truly empty
            "/root/dir_b": [], # Truly empty
        }.get(p, [])

        results = find_dust_bunnies("/root", age_threshold_days=365)

        self.assertIsNotNone(results)
        self.assertEqual(len(results["old_files"]), 0)
        self.assertEqual(len(results["empty_files"]), 0)
        self.assertEqual(len(results["empty_dirs"]), 2)
        self.assertIn("/root/dir_a/dir_a_empty", results["empty_dirs"])
        self.assertIn("/root/dir_b", results["empty_dirs"])

    @patch('sys.stdout', new_callable=MagicMock)
    def test_print_report(self, mock_stdout):
        # Mock rationale: Capture stdout to verify the printed report content
        # without actually printing to the console during tests.
        mock_results = {
            "old_files": [
                ("/path/to/old_file.txt", "2022-01-01 10:00:00"),
                ("/path/to/another_old.log", "2021-05-15 12:30:00")
            ],
            "empty_files": [
                "/path/to/empty.txt"
            ],
            "empty_dirs": [
                "/path/to/empty_folder"
            ]
        }
        root_path = "/path/to"
        age_threshold = 365

        print_report(mock_results, root_path, age_threshold)

        output = mock_stdout.getvalue()
        self.assertIn("🧹 Digital Dust Bunny Sweeper Report 🧹", output)
        self.assertIn("Scanning: /path/to", output)
        self.assertIn("Files older than 365 days:", output)
        self.assertIn("- /path/to/old_file.txt (Modified: 2022-01-01 10:00:00)", output)
        self.assertIn("- /path/to/another_old.log (Modified: 2021-05-15 12:30:00)", output)
        self.assertIn("Empty Files:", output)
        self.assertIn("- /path/to/empty.txt", output)
        self.assertIn("Empty Directories:", output)
        self.assertIn("- /path/to/empty_folder/", output)
        self.assertIn("Total old files found: 2", output)
        self.assertIn("Total empty files found: 1", output)
        self.assertIn("Total empty directories found: 1", output)
        self.assertIn("Consider sweeping these digital dust bunnies away!", output)

    @patch('sys.stdout', new_callable=MagicMock)
    def test_print_report_no_issues(self, mock_stdout):
        # Mock rationale: Capture stdout to verify the printed report content
        # when no dust bunnies are found.
        mock_results = {
            "old_files": [],
            "empty_files": [],
            "empty_dirs": []
        }
        root_path = "/path/to/clean"
        age_threshold = 365

        print_report(mock_results, root_path, age_threshold)

        output = mock_stdout.getvalue()
        self.assertIn("None found. Your files are spry!", output)
        self.assertIn("None found. No phantom files here!", output)
        self.assertIn("None found. Your directories are bustling!", output)
        self.assertIn("Total old files found: 0", output)
        self.assertIn("Total empty files found: 0", output)
        self.assertIn("Total empty directories found: 0", output)


if __name__ == '__main__':
    unittest.main()
