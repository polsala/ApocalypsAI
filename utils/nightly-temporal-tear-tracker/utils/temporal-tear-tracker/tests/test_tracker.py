import unittest
from unittest import mock
import json
import pathlib
import time
import os
import sys

# Add the src directory to the Python path to allow importing tracker.py
# Mock rationale: This allows the test suite to import the module under test
# without needing to install it or modify sys.path globally.
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))
import tracker

class TestTemporalTearTracker(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Create a temporary directory for tests to simulate a file system
        # without touching the actual disk, ensuring tests are isolated and clean up after themselves.
        self.test_dir = pathlib.Path(f"/tmp/test_tracker_{os.getpid()}_{time.time_ns()}")
        self.test_dir.mkdir(parents=True, exist_ok=True)

        # Mock rationale: The state file path is relative to the script's location.
        # We need to control this path to point to our temporary test directory.
        self.mock_script_dir = self.test_dir
        self.state_path = self.mock_script_dir / tracker.STATE_FILE_NAME

        # Mock rationale: We need to control the current time for deterministic calculations
        # of "time since tear" and "time since creation".
        self.mock_time = mock.patch('time.time', return_value=1000.0)
        self.mock_time_val = self.mock_time.start()

        # Mock rationale: We need to capture log output to assert on messages.
        self.mock_logging_info = mock.patch('logging.info')
        self.mock_logging_info_obj = self.mock_logging_info.start()

        self.mock_logging_warning = mock.patch('logging.warning')
        self.mock_logging_warning_obj = self.mock_logging_warning.start()

        self.mock_logging_error = mock.patch('logging.error')
        self.mock_logging_error_obj = self.mock_logging_error.start()

        # Mock rationale: We need to control the script's parent directory for state file location.
        self.mock_pathlib_path_parent = mock.patch.object(pathlib.Path, 'parent', new_callable=mock.PropertyMock)
        self.mock_pathlib_path_parent_obj = self.mock_pathlib_path_parent.start()
        self.mock_pathlib_path_parent_obj.return_value = self.mock_script_dir

    def tearDown(self):
        self.mock_time.stop()
        self.mock_logging_info.stop()
        self.mock_logging_warning.stop()
        self.mock_logging_error.stop()
        self.mock_pathlib_path_parent.stop()

        # Clean up the temporary directory
        if self.test_dir.exists():
            for item in self.test_dir.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    import shutil
                    shutil.rmtree(item)
            self.test_dir.rmdir()

    @mock.patch('os.walk')
    @mock.patch('os.path.getmtime')
    @mock.patch('pathlib.Path.is_dir')
    @mock.patch('pathlib.Path.exists')
    def test_initial_run_no_files(self, mock_path_exists, mock_is_dir, mock_getmtime, mock_os_walk):
        # Mock rationale: Simulate an empty directory and no existing state file.
        # This tests the initial setup and state creation.
        mock_path_exists.side_effect = lambda p: p == self.test_dir or p == self.state_path # state_path exists check for load_state
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [] # No files in directory
        mock_getmtime.return_value = self.mock_time_val - 10 # Arbitrary past time

        # Mock rationale: Simulate argparse behavior for CLI arguments.
        with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(dir=str(self.test_dir))):
            tracker.main()

        self.mock_logging_info_obj.assert_any_call(f"Monitoring directory: {self.test_dir}")
        self.mock_logging_info_obj.assert_any_call("No previous temporal tears detected. Reality is pristine.")
        self.mock_logging_info_obj.assert_any_call("Current reality scan complete.")
        self.mock_logging_info_obj.assert_any_call(f"State saved to {self.state_path}")

        # Verify state file content
        with open(self.state_path, 'r') as f:
            state = json.load(f)
        self.assertEqual(state["last_scan_files"], {})
        self.assertIsNone(state["last_tear_timestamp"])

    @mock.patch('os.walk')
    @mock.patch('os.path.getmtime')
    @mock.patch('pathlib.Path.is_dir')
    @mock.patch('pathlib.Path.exists')
    def test_initial_run_with_existing_files(self, mock_path_exists, mock_is_dir, mock_getmtime, mock_os_walk):
        # Mock rationale: Simulate a directory with existing files on the first run.
        # These files should be recorded but not reported as 'new tears'.
        file1 = self.test_dir / "existing_file1.txt"
        file2 = self.test_dir / "existing_file2.log"

        mock_path_exists.side_effect = lambda p: p == self.test_dir or p == self.state_path or p == file1 or p == file2
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [
            (str(self.test_dir), [], [file1.name, file2.name])
        ]
        mock_getmtime.side_effect = lambda p: {
            file1: self.mock_time_val - 100,
            file2: self.mock_time_val - 50,
        }.get(p, self.mock_time_val - 10)

        with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(dir=str(self.test_dir))):
            tracker.main()

        self.mock_logging_info_obj.assert_any_call("No previous temporal tears detected. Reality is pristine.")
        self.mock_logging_info_obj.assert_any_call("Current reality scan complete.")

        # Verify state file content
        with open(self.state_path, 'r') as f:
            state = json.load(f)
        self.assertEqual(len(state["last_scan_files"]), 2)
        self.assertIn(str(file1), state["last_scan_files"])
        self.assertIn(str(file2), state["last_scan_files"])
        self.assertIsNone(state["last_tear_timestamp"])

    @mock.patch('os.walk')
    @mock.patch('os.path.getmtime')
    @mock.patch('pathlib.Path.is_dir')
    @mock.patch('pathlib.Path.exists')
    def test_new_files_detected(self, mock_path_exists, mock_is_dir, mock_getmtime, mock_os_walk):
        # Mock rationale: Simulate a scenario where new files appear after an initial run.
        # This tests the core 'temporal tear' detection and reporting.
        file1 = self.test_dir / "old_file.txt"
        new_file1 = self.test_dir / "new_anomaly.log"
        new_file2 = self.test_dir / "another_tear.dat"

        # Simulate initial state (before new files appear)
        initial_state = {
            "last_scan_files": {
                str(file1): self.mock_time_val - 200
            },
            "last_tear_timestamp": None
        }
        with open(self.state_path, 'w') as f:
            json.dump(initial_state, f)

        mock_path_exists.side_effect = lambda p: p == self.test_dir or p == self.state_path or p == file1 or p == new_file1 or p == new_file2
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [
            (str(self.test_dir), [], [file1.name, new_file1.name, new_file2.name])
        ]
        mock_getmtime.side_effect = lambda p: {
            file1: self.mock_time_val - 200,
            new_file1: self.mock_time_val - 10,
            new_file2: self.mock_time_val - 5,
        }.get(p, self.mock_time_val - 10)

        with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(dir=str(self.test_dir))):
            tracker.main()

        self.mock_logging_info_obj.assert_any_call("A new temporal tear has opened!")
        self.mock_logging_info_obj.assert_any_call(f"  - New file detected: {new_file1} (appeared 10.0 seconds ago)")
        self.mock_logging_info_obj.assert_any_call(f"  - New file detected: {new_file2} (appeared 5.0 seconds ago)")
        self.mock_logging_info_obj.assert_any_call("Current reality scan complete.")

        # Verify state file content
        with open(self.state_path, 'r') as f:
            state = json.load(f)
        self.assertEqual(len(state["last_scan_files"]), 3)
        self.assertIn(str(file1), state["last_scan_files"])
        self.assertIn(str(new_file1), state["last_scan_files"])
        self.assertIn(str(new_file2), state["last_scan_files"])
        self.assertEqual(state["last_tear_timestamp"], self.mock_time_val)

    @mock.patch('os.walk')
    @mock.patch('os.path.getmtime')
    @mock.patch('pathlib.Path.is_dir')
    @mock.patch('pathlib.Path.exists')
    def test_no_new_files(self, mock_path_exists, mock_is_dir, mock_getmtime, mock_os_walk):
        # Mock rationale: Simulate a stable reality where no new files appear.
        # This tests the 'no tear' reporting and time since last tear calculation.
        file1 = self.test_dir / "stable_file.txt"

        # Simulate previous state with a tear timestamp
        initial_state = {
            "last_scan_files": {
                str(file1): self.mock_time_val - 200
            },
            "last_tear_timestamp": self.mock_time_val - 100 # Last tear was 100 seconds ago
        }
        with open(self.state_path, 'w') as f:
            json.dump(initial_state, f)

        mock_path_exists.side_effect = lambda p: p == self.test_dir or p == self.state_path or p == file1
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [
            (str(self.test_dir), [], [file1.name])
        ]
        mock_getmtime.return_value = self.mock_time_val - 200 # mtime unchanged

        with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(dir=str(self.test_dir))):
            tracker.main()

        self.mock_logging_info_obj.assert_any_call("No new temporal tears detected. Reality remains stable.")
        self.mock_logging_info_obj.assert_any_call("It has been 100.0 seconds since the last tear.")
        self.mock_logging_info_obj.assert_any_call("Current reality scan complete.")

        # Verify state file content (timestamp should not change)
        with open(self.state_path, 'r') as f:
            state = json.load(f)
        self.assertEqual(len(state["last_scan_files"]), 1)
        self.assertEqual(state["last_tear_timestamp"], self.mock_time_val - 100)

    @mock.patch('os.walk')
    @mock.patch('os.path.getmtime')
    @mock.patch('pathlib.Path.is_dir')
    @mock.patch('pathlib.Path.exists')
    def test_corrupted_state_file(self, mock_path_exists, mock_is_dir, mock_getmtime, mock_os_walk):
        # Mock rationale: Test robustness against a malformed state file.
        # The tracker should recover by starting with an empty state.
        with open(self.state_path, 'w') as f:
            f.write("this is not valid json")

        mock_path_exists.side_effect = lambda p: p == self.test_dir or p == self.state_path
        mock_is_dir.return_value = True
        mock_os_walk.return_value = []
        mock_getmtime.return_value = self.mock_time_val - 10

        with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(dir=str(self.test_dir))):
            tracker.main()

        self.mock_logging_warning_obj.assert_any_call(f"Corrupted state file detected at {self.state_path}. Starting fresh.")
        self.mock_logging_info_obj.assert_any_call("No previous temporal tears detected. Reality is pristine.")

        # Verify that a new, valid state file was saved
        with open(self.state_path, 'r') as f:
            state = json.load(f)
        self.assertEqual(state["last_scan_files"], {})
        self.assertIsNone(state["last_tear_timestamp"])

    @mock.patch('os.walk')
    @mock.patch('os.path.getmtime')
    @mock.patch('pathlib.Path.is_dir')
    @mock.patch('pathlib.Path.exists')
    def test_target_directory_does_not_exist(self, mock_path_exists, mock_is_dir, mock_getmtime, mock_os_walk):
        # Mock rationale: Ensure the utility handles cases where the monitored directory is invalid.
        mock_path_exists.side_effect = lambda p: p == self.state_path # Only state_path exists
        mock_is_dir.return_value = False # Target dir is not a directory
        mock_os_walk.return_value = []
        mock_getmtime.return_value = self.mock_time_val - 10

        non_existent_dir = self.test_dir / "non_existent"

        with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(dir=str(non_existent_dir))):
            tracker.main()

        self.mock_logging_error_obj.assert_any_call(f"Target directory does not exist or is not a directory: {non_existent_dir}")
        # It should still try to save an empty state
        self.mock_logging_info_obj.assert_any_call(f"State saved to {self.state_path}")

        with open(self.state_path, 'r') as f:
            state = json.load(f)
        self.assertEqual(state["last_scan_files"], {})
        self.assertIsNone(state["last_tear_timestamp"])

if __name__ == '__main__':
    unittest.main()
