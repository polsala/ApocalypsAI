import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the src directory to the path to allow importing detector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from detector import (
    get_current_timestamp,
    read_last_timestamp,
    write_current_timestamp,
    detect_temporal_anomaly,
    LAST_TIME_FILE,
    EXPECTED_INTERVAL_SECONDS,
    DRIFT_TOLERANCE_SECONDS
)

class TestTemporalDriftDetector(unittest.TestCase):

    def setUp(self):
        # Ensure the test environment is clean
        self.test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src', LAST_TIME_FILE)
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    @patch('time.time', return_value=1678886400.0)
    def test_get_current_timestamp(self, mock_time):
        # Mock rationale: `time.time()` is non-deterministic, so we mock it to return a fixed value for testing.
        self.assertEqual(get_current_timestamp(), 1678886400.0)

    @patch('builtins.open', new_callable=mock_open, read_data="12345.678")
    @patch('os.path.exists', return_value=True)
    def test_read_last_timestamp_success(self, mock_exists, mock_file_open):
        # Mock rationale: File I/O is non-deterministic and has side effects.
        # We mock `open` to simulate reading a specific timestamp from a file,
        # and `os.path.exists` to confirm the file's presence.
        self.assertEqual(read_last_timestamp("dummy_path"), 12345.678)
        mock_file_open.assert_called_once_with("dummy_path", 'r')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_read_last_timestamp_no_file(self, mock_exists, mock_file_open):
        # Mock rationale: We mock `os.path.exists` to simulate the absence of the file.
        self.assertIsNone(read_last_timestamp("dummy_path"))
        mock_file_open.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_read_last_timestamp_empty_file(self, mock_exists, mock_file_open):
        # Mock rationale: We mock `open` to simulate reading an empty file.
        mock_file_open.return_value.read.return_value = ""
        self.assertIsNone(read_last_timestamp("dummy_path"))

    @patch('builtins.open', new_callable=mock_open)
    def test_write_current_timestamp(self, mock_file_open):
        # Mock rationale: File I/O has side effects. We mock `open` to verify
        # that the correct timestamp string is written to the file.
        write_current_timestamp("dummy_path", 98765.432)
        mock_file_open.assert_called_once_with("dummy_path", 'w')
        mock_file_open().write.assert_called_once_with("98765.432")

    def test_detect_temporal_anomaly_no_last_timestamp(self):
        # Test rationale: The first run should not detect an anomaly.
        self.assertIsNone(detect_temporal_anomaly(None, 100.0, EXPECTED_INTERVAL_SECONDS, DRIFT_TOLERANCE_SECONDS))

    def test_detect_temporal_anomaly_within_tolerance(self):
        # Test rationale: Simulate a normal time progression within the allowed drift.
        last_time = 100.0
        current_time = last_time + EXPECTED_INTERVAL_SECONDS + (DRIFT_TOLERANCE_SECONDS / 2) # Slightly over, but within tolerance
        self.assertIsNone(detect_temporal_anomaly(last_time, current_time, EXPECTED_INTERVAL_SECONDS, DRIFT_TOLERANCE_SECONDS))

        current_time = last_time + EXPECTED_INTERVAL_SECONDS - (DRIFT_TOLERANCE_SECONDS / 2) # Slightly under, but within tolerance
        self.assertIsNone(detect_temporal_anomaly(last_time, current_time, EXPECTED_INTERVAL_SECONDS, DRIFT_TOLERANCE_SECONDS))

    def test_detect_temporal_anomaly_jump_forward(self):
        # Test rationale: Simulate a significant jump forward in time.
        last_time = 100.0
        current_time = last_time + EXPECTED_INTERVAL_SECONDS + DRIFT_TOLERANCE_SECONDS + 1.0 # Beyond tolerance
        result = detect_temporal_anomaly(last_time, current_time, EXPECTED_INTERVAL_SECONDS, DRIFT_TOLERANCE_SECONDS)
        self.assertIsNotNone(result)
        self.assertIn("jumped forward", result)
        self.assertIn(f"{(DRIFT_TOLERANCE_SECONDS + 1.0):.1f} seconds", result)

    def test_detect_temporal_anomaly_jump_backward(self):
        # Test rationale: Simulate a significant jump backward in time.
        last_time = 100.0
        current_time = last_time + EXPECTED_INTERVAL_SECONDS - DRIFT_TOLERANCE_SECONDS - 1.0 # Beyond tolerance
        result = detect_temporal_anomaly(last_time, current_time, EXPECTED_INTERVAL_SECONDS, DRIFT_TOLERANCE_SECONDS)
        self.assertIsNotNone(result)
        self.assertIn("jumped backward", result)
        self.assertIn(f"{(DRIFT_TOLERANCE_SECONDS + 1.0):.1f} seconds", result)

    @patch('detector.read_last_timestamp', return_value=None)
    @patch('detector.get_current_timestamp', return_value=100.0)
    @patch('detector.write_current_timestamp')
    @patch('builtins.print') # Mock print to capture output
    def test_main_first_run(self, mock_print, mock_write, mock_get_current, mock_read_last):
        # Mock rationale: We mock `read_last_timestamp` to simulate no previous file,
        # `get_current_timestamp` for a fixed time, `write_current_timestamp` to prevent file I/O,
        # and `print` to capture console output for verification.
        from detector import main
        main()
        mock_read_last.assert_called_once()
        mock_get_current.assert_called_once()
        mock_write.assert_called_once_with(self.test_file_path, 100.0)
        mock_print.assert_any_call(f"[INFO] No previous timestamp found. Initializing {LAST_TIME_FILE}.")
        mock_print.assert_any_call("[INFO] Current time recorded: 100.0")

    @patch('detector.read_last_timestamp', return_value=100.0)
    @patch('detector.get_current_timestamp', return_value=100.0 + EXPECTED_INTERVAL_SECONDS + 1.0) # Small drift, within tolerance
    @patch('detector.write_current_timestamp')
    @patch('builtins.print')
    def test_main_normal_run_within_tolerance(self, mock_print, mock_write, mock_get_current, mock_read_last):
        # Mock rationale: Similar to above, but simulating a subsequent run with normal time progression.
        from detector import main
        main()
        mock_read_last.assert_called_once()
        mock_get_current.assert_called_once()
        mock_write.assert_called_once_with(self.test_file_path, 100.0 + EXPECTED_INTERVAL_SECONDS + 1.0)
        mock_print.assert_any_call("[INFO] Time is within expected bounds.")
        mock_print.assert_any_call(f"[INFO] Current time recorded: {100.0 + EXPECTED_INTERVAL_SECONDS + 1.0}")
        # Ensure no error message was printed
        self.assertFalse(any("ERROR" in call.args[0] for call in mock_print.call_args_list))

    @patch('detector.read_last_timestamp', return_value=100.0)
    @patch('detector.get_current_timestamp', return_value=100.0 + EXPECTED_INTERVAL_SECONDS + DRIFT_TOLERANCE_SECONDS + 10.0) # Significant jump forward
    @patch('detector.write_current_timestamp')
    @patch('builtins.print')
    def test_main_anomaly_detected(self, mock_print, mock_write, mock_get_current, mock_read_last):
        # Mock rationale: Simulating a significant time jump to trigger an anomaly detection.
        from detector import main
        main()
        mock_read_last.assert_called_once()
        mock_get_current.assert_called_once()
        mock_write.assert_called_once_with(self.test_file_path, 100.0 + EXPECTED_INTERVAL_SECONDS + DRIFT_TOLERANCE_SECONDS + 10.0)
        mock_print.assert_any_call(unittest.mock.ANY) # Check for any print call
        # Check for the specific error message
        error_message_found = False
        for call in mock_print.call_args_list:
            if "Temporal anomaly detected! Time jumped forward by" in call.args[0]:
                error_message_found = True
                break
        self.assertTrue(error_message_found)
