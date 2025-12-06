import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import sys

# Mock rationale: We need to control the file system state and time for deterministic tests.
# os.walk, os.stat, and datetime.datetime.now are external dependencies that would make tests
# non-deterministic or require actual file system manipulation.
# By mocking them, we create a virtual file system and a fixed "current time".

# Import the functions to be tested
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from wayfinder import find_points_of_interest, main, get_file_info

class TestWastelandWayfinder(unittest.TestCase):

    def setUp(self):
        # Define a fixed "now" for consistent 'recent' calculations
        self.mock_now = datetime.datetime(2023, 10, 27, 10, 0, 0)
        
        # Define a mock file system structure and their stats
        self.mock_files = {
            # path: (mtime_timestamp, size_bytes)
            "/mock_root/file1.txt": (self.mock_now - datetime.timedelta(days=1)).timestamp(), 100,
            "/mock_root/file2.py": (self.mock_now - datetime.timedelta(days=5)).timestamp(), 5000,
            "/mock_root/subdir/file3.md": (self.mock_now - datetime.timedelta(days=10)).timestamp(), 150000, # 150KB
            "/mock_root/subdir/nested/file4.log": (self.mock_now - datetime.timedelta(days=2)).timestamp(), 200,
            "/mock_root/subdir/nested/file5.json": (self.mock_now - datetime.timedelta(days=20)).timestamp(), 8000,
            "/mock_root/empty_dir/file6.txt": (self.mock_now - datetime.timedelta(days=1)).timestamp(), 10,
        }

        # Mock os.walk to simulate directory traversal
        self.mock_walk_data = [
            ("/mock_root", ["subdir", "empty_dir"], ["file1.txt", "file2.py"]),
            ("/mock_root/subdir", ["nested"], ["file3.md"]),
            ("/mock_root/subdir/nested", [], ["file4.log", "file5.json"]),
            ("/mock_root/empty_dir", [], ["file6.txt"]),
        ]

    @patch('datetime.datetime')
    @patch('os.stat')
    @patch('os.walk')
    def test_find_points_of_interest_no_filters(self, mock_os_walk, mock_os_stat, mock_dt):
        # Mock rationale: Test basic traversal without any filters.
        mock_dt.now.return_value = self.mock_now
        mock_os_walk.return_value = self.mock_walk_data
        
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mtime, size = self.mock_files.get(path, (0, 0))
            mock_stat_obj.st_mtime = mtime
            mock_stat_obj.st_size = size
            return mock_stat_obj
        mock_os_stat.side_effect = mock_stat_side_effect

        results = list(find_points_of_interest("/mock_root"))
        expected_files = [
            "/mock_root/file1.txt",
            "/mock_root/file2.py",
            "/mock_root/subdir/file3.md",
            "/mock_root/subdir/nested/file4.log",
            "/mock_root/subdir/nested/file5.json",
            "/mock_root/empty_dir/file6.txt",
        ]
        self.assertEqual(len(results), len(expected_files))
        for filepath, _, _, _ in results:
            self.assertIn(filepath, expected_files)

    @patch('datetime.datetime')
    @patch('os.stat')
    @patch('os.walk')
    def test_find_points_of_interest_recent_filter(self, mock_os_walk, mock_os_stat, mock_dt):
        # Mock rationale: Test filtering by recent modification time.
        mock_dt.now.return_value = self.mock_now
        mock_os_walk.return_value = self.mock_walk_data
        
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mtime, size = self.mock_files.get(path, (0, 0))
            mock_stat_obj.st_mtime = mtime
            mock_stat_obj.st_size = size
            return mock_stat_obj
        mock_os_stat.side_effect = mock_stat_side_effect

        # Files modified in last 3 days: file1.txt, file4.log, file6.txt
        results = list(find_points_of_interest("/mock_root", recent_days=3))
        expected_files = {
            "/mock_root/file1.txt",
            "/mock_root/subdir/nested/file4.log",
            "/mock_root/empty_dir/file6.txt",
        }
        self.assertEqual(len(results), len(expected_files))
        for filepath, is_recent, _, _ in results:
            self.assertIn(filepath, expected_files)
            self.assertTrue(is_recent) # Ensure the 'is_recent' flag is set

    @patch('datetime.datetime')
    @patch('os.stat')
    @patch('os.walk')
    def test_find_points_of_interest_large_filter(self, mock_os_walk, mock_os_stat, mock_dt):
        # Mock rationale: Test filtering by file size.
        mock_dt.now.return_value = self.mock_now
        mock_os_walk.return_value = self.mock_walk_data
        
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mtime, size = self.mock_files.get(path, (0, 0))
            mock_stat_obj.st_mtime = mtime
            mock_stat_obj.st_size = size
            return mock_stat_obj
        mock_os_stat.side_effect = mock_stat_side_effect

        # Files larger than 5KB (5000 bytes): file2.py, file3.md, file5.json
        results = list(find_points_of_interest("/mock_root", large_kb=5))
        expected_files = {
            "/mock_root/file2.py",
            "/mock_root/subdir/file3.md",
            "/mock_root/subdir/nested/file5.json",
        }
        self.assertEqual(len(results), len(expected_files))
        for filepath, _, is_large, _ in results:
            self.assertIn(filepath, expected_files)
            self.assertTrue(is_large) # Ensure the 'is_large' flag is set

    @patch('datetime.datetime')
    @patch('os.stat')
    @patch('os.walk')
    def test_find_points_of_interest_extension_filter(self, mock_os_walk, mock_os_stat, mock_dt):
        # Mock rationale: Test filtering by file extension.
        mock_dt.now.return_value = self.mock_now
        mock_os_walk.return_value = self.mock_walk_data
        
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mtime, size = self.mock_files.get(path, (0, 0))
            mock_stat_obj.st_mtime = mtime
            mock_stat_obj.st_size = size
            return mock_stat_obj
        mock_os_stat.side_effect = mock_stat_side_effect

        # Files with .py or .md extensions: file2.py, file3.md
        results = list(find_points_of_interest("/mock_root", extensions={"py", "md"}))
        expected_files = {
            "/mock_root/file2.py",
            "/mock_root/subdir/file3.md",
        }
        self.assertEqual(len(results), len(expected_files))
        for filepath, _, _, is_matching_ext in results:
            self.assertIn(filepath, expected_files)
            self.assertTrue(is_matching_ext) # Ensure the 'is_matching_ext' flag is set

    @patch('datetime.datetime')
    @patch('os.stat')
    @patch('os.walk')
    def test_find_points_of_interest_combined_filters(self, mock_os_walk, mock_os_stat, mock_dt):
        # Mock rationale: Test combining multiple filters.
        mock_dt.now.return_value = self.mock_now
        mock_os_walk.return_value = self.mock_walk_data
        
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mtime, size = self.mock_files.get(path, (0, 0))
            mock_stat_obj.st_mtime = mtime
            mock_stat_obj.st_size = size
            return mock_stat_obj
        mock_os_stat.side_effect = mock_stat_side_effect

        # Files recent (last 7 days) AND large (over 1KB) AND .py or .txt
        # file1.txt (recent, not large, .txt)
        # file2.py (recent, large, .py) -> MATCH
        # file3.md (not recent, very large, .md)
        # file4.log (recent, not large, .log)
        # file5.json (not recent, large, .json)
        # file6.txt (recent, not large, .txt)
        results = list(find_points_of_interest("/mock_root", recent_days=7, large_kb=1, extensions={"py", "txt"}))
        expected_files = {
            "/mock_root/file1.txt", # Matches recent and ext
            "/mock_root/file2.py",  # Matches recent, large, and ext
            "/mock_root/empty_dir/file6.txt", # Matches recent and ext
        }
        self.assertEqual(len(results), len(expected_files))
        for filepath, is_recent, is_large, is_matching_ext in results:
            self.assertIn(filepath, expected_files)
            # Check if at least one condition is met for the file to be included
            self.assertTrue(is_recent or is_large or is_matching_ext)

    @patch('datetime.datetime')
    @patch('os.stat')
    @patch('os.walk')
    def test_find_points_of_interest_depth_filter(self, mock_os_walk, mock_os_stat, mock_dt):
        # Mock rationale: Test filtering by maximum recursion depth.
        mock_dt.now.return_value = self.mock_now
        mock_os_walk.return_value = self.mock_walk_data
        
        def mock_stat_side_effect(path):
            mock_stat_obj = MagicMock()
            mtime, size = self.mock_files.get(path, (0, 0))
            mock_stat_obj.st_mtime = mtime
            mock_stat_obj.st_size = size
            return mock_stat_obj
        mock_os_stat.side_effect = mock_stat_side_effect

        # Max depth 1: /mock_root (depth 0), /mock_root/subdir (depth 1), /mock_root/empty_dir (depth 1)
        # Should include files in /mock_root and its direct subdirectories, but not nested ones.
        results = list(find_points_of_interest("/mock_root", max_depth=1))
        expected_files = {
            "/mock_root/file1.txt",
            "/mock_root/file2.py",
            "/mock_root/subdir/file3.md",
            "/mock_root/empty_dir/file6.txt",
        }
        self.assertEqual(len(results), len(expected_files))
        for filepath, _, _, _ in results:
            self.assertIn(filepath, expected_files)
            self.assertFalse("nested" in filepath) # Ensure no files from deeper than depth 1

    @patch('os.path.isdir', return_value=True) # Mock rationale: Simulate a valid starting directory.
    @patch('sys.stdout', new_callable=MagicMock) # Mock rationale: Capture stdout for assertion.
    @patch('sys.stderr', new_callable=MagicMock) # Mock rationale: Capture stderr for assertion.
    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Control CLI arguments.
    @patch('wayfinder.find_points_of_interest') # Mock rationale: Isolate main function logic.
    def test_main_no_results(self, mock_find_poi, mock_parse_args, mock_stderr, mock_stdout, mock_isdir):
        # Mock rationale: Test scenario where no files match criteria.
        mock_parse_args.return_value = MagicMock(
            path=".", recent=1, large=1000, ext="xyz", depth=None
        )
        mock_find_poi.return_value = [] # Simulate no results
        
        main()
        mock_stdout.assert_any_call("--- Wasteland Wayfinder: Scavenging '.' ---\n")
        mock_stdout.assert_any_call("No points of interest found matching your criteria.\n")
        mock_stdout.assert_any_call("--- Scavenging Complete ---\n")
        self.assertFalse(mock_stderr.called)

    @patch('os.path.isdir', return_value=True) # Mock rationale: Simulate a valid starting directory.
    @patch('sys.stdout', new_callable=MagicMock) # Mock rationale: Capture stdout for assertion.
    @patch('sys.stderr', new_callable=MagicMock) # Mock rationale: Capture stderr for assertion.
    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Control CLI arguments.
    @patch('wayfinder.find_points_of_interest') # Mock rationale: Isolate main function logic.
    def test_main_with_results(self, mock_find_poi, mock_parse_args, mock_stderr, mock_stdout, mock_isdir):
        # Mock rationale: Test scenario where files match criteria and are printed.
        mock_parse_args.return_value = MagicMock(
            path=".", recent=None, large=None, ext=None, depth=None
        )
        mock_find_poi.return_value = [
            ("/mock_root/file1.txt", True, False, True), # recent, matching ext (if ext was set)
            ("/mock_root/file2.py", False, True, False), # large
        ]
        
        main()
        mock_stdout.assert_any_call("--- Wasteland Wayfinder: Scavenging '.' ---\n")
        mock_stdout.assert_any_call("  [FRESH TRACKS] /mock_root/file1.txt\n")
        mock_stdout.assert_any_call("  [VALUABLE CACHE] /mock_root/file2.py\n")
        mock_stdout.assert_any_call("--- Scavenging Complete ---\n")
        self.assertFalse(mock_stderr.called)

    @patch('os.path.isdir', return_value=False) # Mock rationale: Simulate an invalid starting directory.
    @patch('sys.stdout', new_callable=MagicMock) # Mock rationale: Capture stdout for assertion.
    @patch('sys.stderr', new_callable=MagicMock) # Mock rationale: Capture stderr for assertion.
    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Control CLI arguments.
    @patch('sys.exit') # Mock rationale: Prevent actual exit during test.
    def test_main_invalid_path(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout, mock_isdir):
        # Mock rationale: Test error handling for invalid path.
        mock_parse_args.return_value = MagicMock(
            path="/nonexistent", recent=None, large=None, ext=None, depth=None
        )
        
        main()
        mock_stderr.assert_any_call("Error: Path '/nonexistent' is not a valid directory.\n")
        mock_exit.assert_called_once_with(1)
        self.assertFalse(mock_stdout.called)

    @patch('os.stat')
    def test_get_file_info_success(self, mock_os_stat):
        # Mock rationale: Test successful retrieval of file info.
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_mtime = self.mock_now.timestamp()
        mock_stat_obj.st_size = 12345
        mock_os_stat.return_value = mock_stat_obj

        mtime, size = get_file_info("/some/path/file.txt")
        self.assertEqual(mtime, self.mock_now)
        self.assertEqual(size, 12345)

    @patch('os.stat', side_effect=OSError)
    def test_get_file_info_os_error(self, mock_os_stat):
        # Mock rationale: Test error handling when os.stat fails (e.g., file not found, permissions).
        mtime, size = get_file_info("/nonexistent/file.txt")
        self.assertIsNone(mtime)
        self.assertIsNone(size)

if __name__ == '__main__':
    unittest.main()
