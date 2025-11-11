import unittest
from unittest.mock import patch, mock_open
import os
import json
import datetime
import time # Import time module for time.time()

# Import the functions to be tested
from src.anomaly_tracker import (
    get_current_timestamp, load_last_known_time, save_current_time,
    check_for_anomalies, STATE_FILE, THRESHOLD_SECONDS
)

class TestTemporalAnomalyTracker(unittest.TestCase):

    def setUp(self):
        # Ensure STATE_FILE does not exist before each test
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)

    def tearDown(self):
        # Clean up STATE_FILE after each test
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)

    @patch('time.time')
    def test_get_current_timestamp(self, mock_time):
        # Mock rationale: time.time() is a system call, needs to be deterministic.
        mock_time.return_value = 1678886400.0 # March 15, 2023 12:00:00 PM UTC
        self.assertEqual(get_current_timestamp(), 1678886400.0)

    def test_load_save_last_known_time(self):
        test_timestamp = 1678886400.0
        save_current_time(STATE_FILE, test_timestamp)
        loaded_timestamp = load_last_known_time(STATE_FILE)
        self.assertEqual(loaded_timestamp, test_timestamp)

    def test_load_last_known_time_no_file(self):
        self.assertIsNone(load_last_known_time(STATE_FILE))

    def test_load_last_known_time_corrupted_file(self):
        # Mock rationale: Simulate a corrupted state file for robust error handling.
        with open(STATE_FILE, 'w') as f:
            f.write("not valid json")
        self.assertIsNone(load_last_known_time(STATE_FILE))

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests.
    @patch('time.time')
    def test_check_for_anomalies_first_run(self, mock_time, mock_print):
        # Mock rationale: time.time() is a system call, needs to be deterministic.
        mock_time.return_value = 1678886400.0
        self.assertFalse(check_for_anomalies())
        # Verify state file was created
        self.assertTrue(os.path.exists(STATE_FILE))
        self.assertEqual(load_last_known_time(STATE_FILE), 1678886400.0)
        mock_print.assert_called_with(
            f"First run or state file missing/corrupted. Initializing with current time: {datetime.datetime.fromtimestamp(1678886400.0, tz=datetime.timezone.utc)}"
        )

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests.
    @patch('time.time')
    def test_check_for_anomalies_stable_time(self, mock_time, mock_print):
        # Mock rationale: time.time() is a system call, needs to be deterministic.
        # Simulate a previous run
        initial_time = 1678886400.0
        save_current_time(STATE_FILE, initial_time)

        # Simulate current time slightly ahead, but within threshold
        mock_time.return_value = initial_time + (THRESHOLD_SECONDS / 2)
        self.assertFalse(check_for_anomalies())
        mock_print.assert_called_with(
            f"System time stable. Difference: {THRESHOLD_SECONDS / 2:.2f} seconds (within {THRESHOLD_SECONDS}s threshold)."
        )
        # Verify state file was updated
        self.assertEqual(load_last_known_time(STATE_FILE), mock_time.return_value)

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests.
    @patch('time.time')
    def test_check_for_anomalies_forward_jump(self, mock_time, mock_print):
        # Mock rationale: time.time() is a system call, needs to be deterministic.
        # Simulate a previous run
        initial_time = 1678886400.0
        save_current_time(STATE_FILE, initial_time)

        # Simulate current time significantly ahead (anomaly)
        mock_time.return_value = initial_time + THRESHOLD_SECONDS + 10
        self.assertTrue(check_for_anomalies())
        mock_print.assert_any_call("🚨 Temporal Anomaly Detected! 🚨")
        # Verify state file was updated to the new time
        self.assertEqual(load_last_known_time(STATE_FILE), mock_time.return_value)

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests.
    @patch('time.time')
    def test_check_for_anomalies_backward_jump(self, mock_time, mock_print):
        # Mock rationale: time.time() is a system call, needs to be deterministic.
        # Simulate a previous run
        initial_time = 1678886400.0
        save_current_time(STATE_FILE, initial_time)

        # Simulate current time significantly behind (anomaly)
        mock_time.return_value = initial_time - THRESHOLD_SECONDS - 10
        self.assertTrue(check_for_anomalies())
        mock_print.assert_any_call("🚨 Temporal Anomaly Detected! 🚨")
        # Verify state file was updated to the new time
        self.assertEqual(load_last_known_time(STATE_FILE), mock_time.return_value)

    @patch('builtins.print') # Mock rationale: Suppress print statements during tests.
    @patch('time.time')
    def test_check_for_anomalies_corrupted_state_file_then_stable(self, mock_time, mock_print):
        # Mock rationale: Simulate a corrupted state file, then a subsequent stable run.
        # Create a corrupted state file
        with open(STATE_FILE, 'w') as f:
            f.write("invalid json content")

        # First run: should treat as first run due to corruption
        mock_time.return_value = 1678886400.0
        self.assertFalse(check_for_anomalies())
        mock_print.assert_any_call(f"Warning: Could not read or parse state file '{STATE_FILE}'. Starting fresh.")
        self.assertEqual(load_last_known_time(STATE_FILE), mock_time.return_value)

        # Second run: stable time
        mock_time.return_value = 1678886400.0 + (THRESHOLD_SECONDS / 2)
        self.assertFalse(check_for_anomalies())
        mock_print.assert_any_call(
            f"System time stable. Difference: {THRESHOLD_SECONDS / 2:.2f} seconds (within {THRESHOLD_SECONDS}s threshold)."
        )
        self.assertEqual(load_last_known_time(STATE_FILE), mock_time.return_value)


if __name__ == '__main__':
    unittest.main()
