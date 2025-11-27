import unittest
from unittest import mock
import datetime
import json
import sys
import requests
import argparse

# Add the src directory to the path to allow importing time_sync
sys.path.insert(0, 'src')
import time_sync
sys.path.pop(0)

class TestTimeSync(unittest.TestCase):

    def setUp(self):
        # Capture stdout/stderr for testing print statements
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        self.mock_stdout = mock.StringIO()
        self.mock_stderr = mock.StringIO()
        sys.stdout = self.mock_stdout
        sys.stderr = self.mock_stderr

    def tearDown(self):
        # Restore stdout/stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @mock.patch('datetime.datetime')
    def test_get_local_time(self, mock_dt):
        # Mock rationale: Ensure deterministic local time for testing.
        mock_now = datetime.datetime(2023, 1, 1, 12, 0, 0, 123456)
        mock_dt.now.return_value = mock_now
        mock_dt.return_value = mock_now # For datetime.datetime() constructor calls if any

        local_time = time_sync.get_local_time()
        self.assertEqual(local_time, mock_now)
        mock_dt.now.assert_called_once()

    @mock.patch('requests.get')
    def test_get_external_time_success(self, mock_get):
        # Mock rationale: Simulate a successful API response without actual network calls.
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        # WorldTimeAPI format example
        mock_response.json.return_value = {
            "datetime": "2023-01-01T12:00:00.000000+00:00",
            "utc_offset": "+00:00"
        }
        mock_get.return_value = mock_response

        expected_time = datetime.datetime(2023, 1, 1, 12, 0, 0, 0) # Naive datetime
        external_time = time_sync.get_external_time("http://test.url")

        self.assertEqual(external_time, expected_time)
        mock_get.assert_called_once_with("http://test.url", timeout=5)

    @mock.patch('requests.get')
    def test_get_external_time_timeout(self, mock_get):
        # Mock rationale: Simulate a network timeout without actual network calls.
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

        external_time = time_sync.get_external_time("http://test.url")
        self.assertIsNone(external_time)
        self.assertIn("[ERROR] Request to http://test.url timed out", self.mock_stderr.getvalue())

    @mock.patch('requests.get')
    def test_get_external_time_http_error(self, mock_get):
        # Mock rationale: Simulate an HTTP error (e.g., 404, 500) without actual network calls.
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found", response=mock_response)
        mock_get.return_value = mock_response

        external_time = time_sync.get_external_time("http://test.url")
        self.assertIsNone(external_time)
        self.assertIn("[ERROR] Failed to fetch external time from http://test.url", self.mock_stderr.getvalue())

    @mock.patch('requests.get')
    def test_get_external_time_json_decode_error(self, mock_get):
        # Mock rationale: Simulate a malformed JSON response without actual network calls.
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "{}", 0)
        mock_get.return_value = mock_response

        external_time = time_sync.get_external_time("http://test.url")
        self.assertIsNone(external_time)
        self.assertIn("[ERROR] Failed to decode JSON from external API response", self.mock_stderr.getvalue())

    @mock.patch('requests.get')
    def test_get_external_time_missing_datetime_key(self, mock_get):
        # Mock rationale: Simulate an API response missing the expected 'datetime' key.
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"other_key": "value"}
        mock_get.return_value = mock_response

        external_time = time_sync.get_external_time("http://test.url")
        self.assertIsNone(external_time)
        self.assertIn("[ERROR] 'datetime' key not found in external API response", self.mock_stderr.getvalue())

    def test_calculate_drift_no_drift(self):
        # Mock rationale: Test the calculation logic with identical times.
        time1 = datetime.datetime(2023, 1, 1, 12, 0, 0, 0)
        time2 = datetime.datetime(2023, 1, 1, 12, 0, 0, 0)
        drift = time_sync.calculate_drift(time1, time2)
        self.assertEqual(drift, 0.0)

    def test_calculate_drift_positive_drift(self):
        # Mock rationale: Test the calculation logic when local time is ahead.
        local_time = datetime.datetime(2023, 1, 1, 12, 0, 1, 500000) # 1.5 seconds ahead
        external_time = datetime.datetime(2023, 1, 1, 12, 0, 0, 0)
        drift = time_sync.calculate_drift(local_time, external_time)
        self.assertAlmostEqual(drift, 1.5)

    def test_calculate_drift_negative_drift(self):
        # Mock rationale: Test the calculation logic when local time is behind.
        local_time = datetime.datetime(2023, 1, 1, 12, 0, 0, 0)
        external_time = datetime.datetime(2023, 1, 1, 12, 0, 1, 500000) # 1.5 seconds behind
        drift = time_sync.calculate_drift(local_time, external_time)
        self.assertAlmostEqual(drift, -1.5)

    def test_report_drift_aligned(self):
        # Mock rationale: Test output for minimal drift.
        time_sync.report_drift(0.05)
        self.assertIn("[INFO] System time is closely aligned", self.mock_stdout.getvalue())

    def test_report_drift_ahead_warning(self):
        # Mock rationale: Test output for significant positive drift.
        time_sync.report_drift(1.5)
        self.assertIn("[WARNING] Significant time drift detected: 1.500000 seconds (local is ahead).", self.mock_stdout.getvalue())

    def test_report_drift_behind_warning(self):
        # Mock rationale: Test output for significant negative drift.
        time_sync.report_drift(-2.0)
        self.assertIn("[WARNING] Significant time drift detected: -2.000000 seconds (local is behind).", self.mock_stdout.getvalue())

    @mock.patch('time_sync.get_external_time')
    @mock.patch('time_sync.get_local_time')
    @mock.patch('sys.exit')
    @mock.patch('argparse.ArgumentParser')
    def test_main_no_drift(self, mock_argparse, mock_exit, mock_get_local_time, mock_get_external_time):
        # Mock rationale: Simulate a scenario where times are perfectly aligned.
        mock_args = mock.Mock()
        mock_args.url = time_sync.DEFAULT_EXTERNAL_TIME_URL
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_local_time = datetime.datetime(2023, 1, 1, 12, 0, 0, 100000)
        mock_external_time = datetime.datetime(2023, 1, 1, 12, 0, 0, 0)
        mock_get_local_time.return_value = mock_local_time
        mock_get_external_time.return_value = mock_external_time

        time_sync.main()

        self.assertIn(f"[INFO] Local time: {mock_local_time}", self.mock_stdout.getvalue())
        self.assertIn(f"[INFO] External time: {mock_external_time}", self.mock_stdout.getvalue())
        self.assertIn("[INFO] System time is closely aligned", self.mock_stdout.getvalue())
        mock_exit.assert_called_once_with(0)

    @mock.patch('time_sync.get_external_time')
    @mock.patch('time_sync.get_local_time')
    @mock.patch('sys.exit')
    @mock.patch('argparse.ArgumentParser')
    def test_main_with_drift_exit_1(self, mock_argparse, mock_exit, mock_get_local_time, mock_get_external_time):
        # Mock rationale: Simulate a scenario with significant drift, expecting exit code 1.
        mock_args = mock.Mock()
        mock_args.url = time_sync.DEFAULT_EXTERNAL_TIME_URL
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_local_time = datetime.datetime(2023, 1, 1, 12, 0, 2, 0)
        mock_external_time = datetime.datetime(2023, 1, 1, 12, 0, 0, 0)
        mock_get_local_time.return_value = mock_local_time
        mock_get_external_time.return_value = mock_external_time

        time_sync.main()

        self.assertIn("[WARNING] Significant time drift detected: 2.000000 seconds (local is ahead).", self.mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @mock.patch('time_sync.get_external_time')
    @mock.patch('time_sync.get_local_time')
    @mock.patch('sys.exit')
    @mock.patch('argparse.ArgumentParser')
    def test_main_external_time_failure(self, mock_argparse, mock_exit, mock_get_local_time, mock_get_external_time):
        # Mock rationale: Simulate a failure to retrieve external time, expecting exit code 1.
        mock_args = mock.Mock()
        mock_args.url = time_sync.DEFAULT_EXTERNAL_TIME_URL
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_get_local_time.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0, 0)
        mock_get_external_time.return_value = None

        time_sync.main()

        self.assertIn("[ERROR] Could not retrieve external time. Aborting drift check.", self.mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @mock.patch('time_sync.get_external_time')
    @mock.patch('time_sync.get_local_time')
    @mock.patch('sys.exit')
    @mock.patch('argparse.ArgumentParser')
    def test_main_custom_url(self, mock_argparse, mock_exit, mock_get_local_time, mock_get_external_time):
        # Mock rationale: Test that the --url argument is correctly parsed and used.
        mock_args = mock.Mock()
        mock_args.url = "http://custom.url"
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_local_time = datetime.datetime(2023, 1, 1, 12, 0, 0, 0)
        mock_external_time = datetime.datetime(2023, 1, 1, 12, 0, 0, 0)
        mock_get_local_time.return_value = mock_local_time
        mock_get_external_time.return_value = mock_external_time

        time_sync.main()

        mock_get_external_time.assert_called_once_with("http://custom.url")
        mock_exit.assert_called_once_with(0)
