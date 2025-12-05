import unittest
import os
import shutil
import tempfile
import datetime
from unittest.mock import patch, MagicMock
from src.scavenger import scavenge_files, get_file_metadata

class TestScavenger(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = tempfile.mkdtemp()
        self.sub_dir = os.path.join(self.test_dir, "sub_dir")
        os.makedirs(self.sub_dir)

        # Create test files with specific modification times and sizes
        self.file1_path = os.path.join(self.test_dir, "report.log")
        self.file2_path = os.path.join(self.test_dir, "data.json")
        self.file3_path = os.path.join(self.sub_dir, "config.txt")
        self.file4_path = os.path.join(self.sub_dir, "archive.zip")
        self.file5_path = os.path.join(self.test_dir, "old_data.csv") # For age testing

        # Mock rationale: We need to control file creation and modification times
        # to ensure deterministic age-based filtering. `os.utime` is used to set
        # modification times, and `open` for content and size.
        with open(self.file1_path, "w") as f:
            f.write("Log content " * 10) # 120 bytes
        os.utime(self.file1_path, (datetime.datetime.now().timestamp(), (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()))

        with open(self.file2_path, "w") as f:
            f.write('{"key": "value"}') # 17 bytes
        os.utime(self.file2_path, (datetime.datetime.now().timestamp(), (datetime.datetime.now() - datetime.timedelta(days=5)).timestamp()))

        with open(self.file3_path, "w") as f:
            f.write("Configuration settings.") # 23 bytes
        os.utime(self.file3_path, (datetime.datetime.now().timestamp(), (datetime.datetime.now() - datetime.timedelta(days=2)).timestamp()))

        with open(self.file4_path, "w") as f:
            f.write("A very large archive file content " * 100) # 3300 bytes
        os.utime(self.file4_path, (datetime.datetime.now().timestamp(), (datetime.datetime.now() - datetime.timedelta(days=10)).timestamp()))

        with open(self.file5_path, "w") as f:
            f.write("Old data.") # 9 bytes
        os.utime(self.file5_path, (datetime.datetime.now().timestamp(), (datetime.datetime.now() - datetime.timedelta(days=15)).timestamp()))

        # Store expected metadata for easier comparison
        self.expected_metadata = {
            self.file1_path: get_file_metadata(self.file1_path),
            self.file2_path: get_file_metadata(self.file2_path),
            self.file3_path: get_file_metadata(self.file3_path),
            self.file4_path: get_file_metadata(self.file4_path),
            self.file5_path: get_file_metadata(self.file5_path),
        }

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def assertFilePathsEqual(self, actual_results, expected_paths):
        """Helper to compare only file paths from results."""
        actual_paths = sorted([r["path"] for r in actual_results])
        expected_paths = sorted(expected_paths)
        self.assertEqual(actual_paths, expected_paths)

    def test_scavenge_all_files(self):
        results = scavenge_files(self.test_dir)
        self.assertEqual(len(results), 5)
        self.assertFilePathsEqual(results, [self.file1_path, self.file2_path, self.file3_path, self.file4_path, self.file5_path])

    def test_scavenge_with_pattern(self):
        results = scavenge_files(self.test_dir, pattern=r".*\\.log$")
        self.assertEqual(len(results), 1)
        self.assertFilePathsEqual(results, [self.file1_path])

        results = scavenge_files(self.test_dir, pattern=r".*\\.txt$")
        self.assertEqual(len(results), 1)
        self.assertFilePathsEqual(results, [self.file3_path])

        results = scavenge_files(self.test_dir, pattern=r".*\\.(log|json)$")
        self.assertEqual(len(results), 2)
        self.assertFilePathsEqual(results, [self.file1_path, self.file2_path])

    def test_scavenge_with_min_size(self):
        # file1: 120, file2: 17, file3: 23, file4: 3300, file5: 9
        results = scavenge_files(self.test_dir, min_size=100)
        self.assertEqual(len(results), 2)
        self.assertFilePathsEqual(results, [self.file1_path, self.file4_path])

        results = scavenge_files(self.test_dir, min_size=3000)
        self.assertEqual(len(results), 1)
        self.assertFilePathsEqual(results, [self.file4_path])

    def test_scavenge_with_max_size(self):
        results = scavenge_files(self.test_dir, max_size=50)
        self.assertEqual(len(results), 3)
        self.assertFilePathsEqual(results, [self.file2_path, self.file3_path, self.file5_path])

        results = scavenge_files(self.test_dir, max_size=10)
        self.assertEqual(len(results), 1)
        self.assertFilePathsEqual(results, [self.file5_path])

    def test_scavenge_with_min_and_max_size(self):
        results = scavenge_files(self.test_dir, min_size=20, max_size=100)
        self.assertEqual(len(results), 1)
        self.assertFilePathsEqual(results, [self.file3_path])

    @patch('src.scavenger.datetime')
    def test_scavenge_with_max_age_days(self, mock_datetime):
        # Mock rationale: `datetime.datetime.now()` needs to be fixed for
        # deterministic age-based filtering.
        fixed_now = datetime.datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.datetime.now.return_value = fixed_now
        mock_datetime.datetime.fromtimestamp = datetime.datetime.fromtimestamp
        mock_datetime.datetime.fromisoformat = datetime.datetime.fromisoformat
        mock_datetime.timedelta = datetime.timedelta

        # file1: 1 day old (Oct 25)
        # file2: 5 days old (Oct 21)
        # file3: 2 days old (Oct 24)
        # file4: 10 days old (Oct 16)
        # file5: 15 days old (Oct 11)

        results = scavenge_files(self.test_dir, max_age_days=3)
        self.assertEqual(len(results), 2)
        self.assertFilePathsEqual(results, [self.file1_path, self.file3_path])

        results = scavenge_files(self.test_dir, max_age_days=7)
        self.assertEqual(len(results), 3)
        self.assertFilePathsEqual(results, [self.file1_path, self.file2_path, self.file3_path])

        results = scavenge_files(self.test_dir, max_age_days=0) # Only files modified today (none in our setup)
        self.assertEqual(len(results), 0)

    @patch('src.scavenger.datetime')
    def test_scavenge_combined_filters(self, mock_datetime):
        # Mock rationale: Same as above, fix `datetime.datetime.now()`
        fixed_now = datetime.datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.datetime.now.return_value = fixed_now
        mock_datetime.datetime.fromtimestamp = datetime.datetime.fromtimestamp
        mock_datetime.datetime.fromisoformat = datetime.datetime.fromisoformat
        mock_datetime.timedelta = datetime.timedelta

        # Find .log files, min size 50 bytes, max age 3 days
        # file1: report.log, 120 bytes, 1 day old -> should match
        # file2: data.json, 17 bytes, 5 days old
        # file3: config.txt, 23 bytes, 2 days old
        # file4: archive.zip, 3300 bytes, 10 days old
        # file5: old_data.csv, 9 bytes, 15 days old

        results = scavenge_files(self.test_dir, pattern=r".*\\.log$", min_size=50, max_age_days=3)
        self.assertEqual(len(results), 1)
        self.assertFilePathsEqual(results, [self.file1_path])

        # Find any file, min size 20 bytes, max age 6 days
        # file1: 120 bytes, 1 day old -> match
        # file2: 17 bytes, 5 days old -> too small
        # file3: 23 bytes, 2 days old -> match
        # file4: 3300 bytes, 10 days old -> too old
        # file5: 9 bytes, 15 days old -> too small & too old
        results = scavenge_files(self.test_dir, min_size=20, max_age_days=6)
        self.assertEqual(len(results), 2)
        self.assertFilePathsEqual(results, [self.file1_path, self.file3_path])

    def test_scavenge_empty_directory(self):
        empty_dir = tempfile.mkdtemp()
        results = scavenge_files(empty_dir)
        self.assertEqual(len(results), 0)
        shutil.rmtree(empty_dir)

    def test_scavenge_non_existent_directory(self):
        with self.assertRaises(FileNotFoundError):
            scavenge_files("/non/existent/path")

    def test_prioritization(self):
        # Ensure sorting works as expected: newer and larger first
        # file1: 120 bytes, 1 day old
        # file2: 17 bytes, 5 days old
        # file3: 23 bytes, 2 days old
        # file4: 3300 bytes, 10 days old
        # file5: 9 bytes, 15 days old

        # Expected order (descending modified_at, then descending size):
        # 1. file1 (1 day old, 120 bytes)
        # 2. file3 (2 days old, 23 bytes)
        # 3. file2 (5 days old, 17 bytes)
        # 4. file4 (10 days old, 3300 bytes)
        # 5. file5 (15 days old, 9 bytes)

        # Mock rationale: `datetime.datetime.now()` needs to be fixed for
        # deterministic age-based filtering, which impacts `get_file_metadata`
        # and thus the `modified_at` string. While `st_mtime` is from the OS,
        # fixing `now` ensures consistency if `get_file_metadata` were to use it,
        # and provides a stable reference for age calculations in other tests.
        with patch('src.scavenger.datetime') as mock_datetime:
            fixed_now = datetime.datetime(2023, 10, 26, 12, 0, 0)
            mock_datetime.datetime.now.return_value = fixed_now
            mock_datetime.datetime.fromtimestamp = datetime.datetime.fromtimestamp
            mock_datetime.datetime.fromisoformat = datetime.datetime.fromisoformat
            mock_datetime.timedelta = datetime.timedelta

            results = scavenge_files(self.test_dir)

            # Extract just the paths for comparison
            actual_paths_ordered = [r["path"] for r in results]

            # Re-fetch metadata to ensure `modified_at` strings are consistent with mock
            # This is a bit redundant but ensures the test is robust to how `get_file_metadata`
            # generates the timestamp string.
            file1_meta = get_file_metadata(self.file1_path)
            file2_meta = get_file_metadata(self.file2_path)
            file3_meta = get_file_metadata(self.file3_path)
            file4_meta = get_file_metadata(self.file4_path)
            file5_meta = get_file_metadata(self.file5_path)

            # Create a list of these metadata dicts and sort them manually to get expected order
            all_meta = [file1_meta, file2_meta, file3_meta, file4_meta, file5_meta]
            all_meta.sort(key=lambda x: (x["modified_at"], x["size"]), reverse=True)
            expected_paths_ordered = [m["path"] for m in all_meta]

            self.assertEqual(actual_paths_ordered, expected_paths_ordered)


if __name__ == "__main__":
    unittest.main()
