import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import os
import sys
from datetime import datetime

# Add the src directory to the path to import tracker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from tracker import generate_baseline, check_anomalies, _scan_directory

class TestTemporalAnomalyTracker(unittest.TestCase):

    def setUp(self):
        # Define some mock file system data
        self.mock_dir = "/mock/path"
        self.mock_baseline_file = "test_baseline.json"

        # Mock os.stat results
        self.mock_stat_file1 = MagicMock()
        self.mock_stat_file1.st_size = 100
        self.mock_stat_file1.st_mtime = 1678886400.0 # March 15, 2023 00:00:00 UTC
        self.mock_stat_file1.st_ctime = 1678886300.0

        self.mock_stat_file2 = MagicMock()
        self.mock_stat_file2.st_size = 200
        self.mock_stat_file2.st_mtime = 1678886500.0 # March 15, 2023 00:01:40 UTC
        self.mock_stat_file2.st_ctime = 1678886450.0

        self.mock_stat_file3_modified = MagicMock()
        self.mock_stat_file3_modified.st_size = 350 # Changed size
        self.mock_stat_file3_modified.st_mtime = 1678887000.0 # Changed mtime
        self.mock_stat_file3_modified.st_ctime = 1678886600.0 # ctime might be same or different

        self.mock_stat_file3_original = MagicMock()
        self.mock_stat_file3_original.st_size = 300
        self.mock_stat_file3_original.st_mtime = 1678886600.0
        self.mock_stat_file3_original.st_ctime = 1678886600.0

        self.mock_stat_file_new = MagicMock()
        self.mock_stat_file_new.st_size = 50
        self.mock_stat_file_new.st_mtime = 1678887100.0
        self.mock_stat_file_new.st_ctime = 1678887100.0

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('builtins.print') # Mock print to suppress output during tests
    def test_generate_baseline_success(self, mock_print, mock_json_dump, mock_open_func, mock_os_stat, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Simulate directory existence, file system traversal, file stats, and file writing.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_dir, [], ["file1.txt", "file2.log"])
        ]
        mock_os_stat.side_effect = [
            self.mock_stat_file1,
            self.mock_stat_file2
        ]

        result = generate_baseline(self.mock_dir, self.mock_baseline_file)
        self.assertTrue(result)
        mock_os_path_isdir.assert_called_once_with(self.mock_dir)
        mock_os_walk.assert_called_once_with(self.mock_dir)
        self.assertEqual(mock_os_stat.call_count, 2)
        mock_open_func.assert_called_once_with(self.mock_baseline_file, 'w')
        
        expected_baseline = {
            os.path.join(self.mock_dir, "file1.txt"): {
                "size": 100, "mtime": 1678886400.0, "ctime": 1678886300.0
            },
            os.path.join(self.mock_dir, "file2.log"): {
                "size": 200, "mtime": 1678886500.0, "ctime": 1678886450.0
            }
        }
        mock_json_dump.assert_called_once_with(expected_baseline, mock_open_func(), indent=2)
        mock_print.assert_any_call(f"Baseline saved to '{self.mock_baseline_file}'.")

    @patch('os.path.isdir')
    @patch('builtins.print')
    def test_generate_baseline_invalid_path(self, mock_print, mock_os_path_isdir):
        # Mock rationale: Simulate an invalid target path.
        mock_os_path_isdir.return_value = False
        result = generate_baseline(self.mock_dir, self.mock_baseline_file)
        self.assertFalse(result)
        mock_print.assert_any_call(f"Error: Target path '{self.mock_dir}' is not a directory.")

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.walk')
    @patch('os.stat')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('builtins.print')
    def test_check_anomalies_no_changes(self, mock_print, mock_json_load, mock_open_func, mock_os_stat, mock_os_walk, mock_os_path_exists, mock_os_path_isdir):
        # Mock rationale: Simulate a scenario where no changes have occurred.
        mock_os_path_isdir.return_value = True
        mock_os_path_exists.return_value = True # Baseline file exists

        baseline_content = {
            os.path.join(self.mock_dir, "file1.txt"): {"size": 100, "mtime": 1678886400.0, "ctime": 1678886300.0},
            os.path.join(self.mock_dir, "file2.log"): {"size": 200, "mtime": 1678886500.0, "ctime": 1678886450.0}
        }
        mock_json_load.return_value = baseline_content

        mock_os_walk.return_value = [
            (self.mock_dir, [], ["file1.txt", "file2.log"])
        ]
        mock_os_stat.side_effect = [
            self.mock_stat_file1, # For file1.txt
            self.mock_stat_file2  # For file2.log
        ]

        result = check_anomalies(self.mock_dir, self.mock_baseline_file)
        self.assertFalse(result) # No anomalies found
        mock_os_path_isdir.assert_called_once_with(self.mock_dir)
        mock_os_path_exists.assert_called_once_with(self.mock_baseline_file)
        mock_open_func.assert_called_once_with(self.mock_baseline_file, 'r')
        mock_json_load.assert_called_once()
        mock_os_walk.assert_called_once_with(self.mock_dir)
        self.assertEqual(mock_os_stat.call_count, 2)
        mock_print.assert_any_call("  No temporal anomalies detected. All clear!")

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('os.walk')
    @patch('os.stat')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('builtins.print')
    def test_check_anomalies_with_changes(self, mock_print, mock_json_load, mock_open_func, mock_os_stat, mock_os_walk, mock_os_path_exists, mock_os_path_isdir):
        # Mock rationale: Simulate added, removed, and modified files.
        mock_os_path_isdir.return_value = True
        mock_os_path_exists.return_value = True

        baseline_content = {
            os.path.join(self.mock_dir, "file1.txt"): {"size": 100, "mtime": 1678886400.0, "ctime": 1678886300.0},
            os.path.join(self.mock_dir, "file2.log"): {"size": 200, "mtime": 1678886500.0, "ctime": 1678886450.0},
            os.path.join(self.mock_dir, "file3.dat"): {"size": 300, "mtime": 1678886600.0, "ctime": 1678886600.0}
        }
        mock_json_load.return_value = baseline_content

        # Simulate: file1.txt removed, file2.log modified, file3.dat unchanged, new_file.txt added
        mock_os_walk.return_value = [
            (self.mock_dir, [], ["file2.log", "file3.dat", "new_file.txt"])
        ]
        mock_os_stat.side_effect = [
            self.mock_stat_file3_modified, # For file2.log (modified) - using a different mock stat for modification
            self.mock_stat_file3_original, # For file3.dat (unchanged)
            self.mock_stat_file_new      # For new_file.txt (added)
        ]

        result = check_anomalies(self.mock_dir, self.mock_baseline_file)
        self.assertTrue(result) # Anomalies found

        mock_print.assert_any_call(f"  [REMOVED] {os.path.join(self.mock_dir, 'file1.txt')}")
        mock_print.assert_any_call(f"  [ADDED] {os.path.join(self.mock_dir, 'new_file.txt')}")
        mock_print.assert_any_call(f"  [MODIFIED] {os.path.join(self.mock_dir, 'file2.log')}")
        # Check for specific details of modification
        mock_print.assert_any_call(f"    Baseline: Size={baseline_content[os.path.join(self.mock_dir, 'file2.log')]['size']}, MTime={datetime.fromtimestamp(baseline_content[os.path.join(self.mock_dir, 'file2.log')]['mtime']).strftime('%Y-%m-%d %H:%M:%S')}")
        mock_print.assert_any_call(f"    Current:  Size={self.mock_stat_file3_modified.st_size}, MTime={datetime.fromtimestamp(self.mock_stat_file3_modified.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('builtins.print')
    def test_check_anomalies_baseline_not_found(self, mock_print, mock_os_path_exists, mock_os_path_isdir):
        # Mock rationale: Simulate missing baseline file.
        mock_os_path_isdir.return_value = True
        mock_os_path_exists.return_value = False
        result = check_anomalies(self.mock_dir, self.mock_baseline_file)
        self.assertFalse(result)
        mock_print.assert_any_call(f"Error: Baseline file '{self.mock_baseline_file}' not found. Generate one first.")

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('builtins.print')
    def test_check_anomalies_baseline_corrupt(self, mock_print, mock_json_load, mock_open_func, mock_os_path_exists, mock_os_path_isdir):
        # Mock rationale: Simulate a corrupt baseline file.
        mock_os_path_isdir.return_value = True
        mock_os_path_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        result = check_anomalies(self.mock_dir, self.mock_baseline_file)
        self.assertFalse(result)
        mock_print.assert_any_call(f"Error loading baseline from '{self.mock_baseline_file}': Expecting value: line 1 column 1 (char 0)")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_scan_directory_empty(self, mock_os_stat, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Test scanning an empty directory.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_dir, [], [])
        ]
        result = _scan_directory(self.mock_dir)
        self.assertEqual(result, {})
        mock_os_walk.assert_called_once_with(self.mock_dir)
        mock_os_stat.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.stat')
    def test_scan_directory_with_subdirs(self, mock_os_stat, mock_os_walk, mock_os_path_isdir):
        # Mock rationale: Test scanning a directory with subdirectories.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.mock_dir, ["subdir1"], ["file1.txt"]),
            (os.path.join(self.mock_dir, "subdir1"), [], ["file_in_subdir.log"])
        ]
        mock_os_stat.side_effect = [
            self.mock_stat_file1,
            self.mock_stat_file2
        ]
        
        result = _scan_directory(self.mock_dir)
        expected_data = {
            os.path.join(self.mock_dir, "file1.txt"): {
                "size": 100, "mtime": 1678886400.0, "ctime": 1678886300.0
            },
            os.path.join(self.mock_dir, "subdir1", "file_in_subdir.log"): {
                "size": 200, "mtime": 1678886500.0, "ctime": 1678886450.0
            }
        }
        self.assertEqual(result, expected_data)
        self.assertEqual(mock_os_stat.call_count, 2)
