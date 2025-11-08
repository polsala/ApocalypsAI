import unittest
from unittest.mock import patch, MagicMock
import datetime
import sys
import io
import ntplib

# Mock rationale: We need to control the system's perceived UTC time and the NTP server's response
# to test different scenarios (in-sync, out-of-sync, NTP error) deterministically without
# actual network calls or relying on the host system's clock. We also mock sys.exit and stdout/stderr
# to capture program output and exit codes for assertion.

# Import the module under test. Assuming tests are run from the repository root or PYTHONPATH is set.
# If running from utils/temporal-anomaly-detector/, this would be 'from src import detector'.
# For robustness in CI, using the full path is safer if the test runner doesn't change directories.
from utils.temporal_anomaly_detector.src import detector

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Capture stdout and stderr
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        self.mock_stdout = io.StringIO()
        self.mock_stderr = io.StringIO()
        sys.stdout = self.mock_stdout
        sys.stderr = self.mock_stderr

        # Mock sys.exit to prevent actual program termination during tests
        self.mock_sys_exit = MagicMock()
        self.patcher_sys_exit = patch('sys.exit', self.mock_sys_exit)
        self.patcher_sys_exit.start()

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr
        self.patcher_sys_exit.stop()
        # Clean up the imported module to ensure fresh state for subsequent tests if needed
        # This is important if the module has global state or if sys.exit was patched at import time.
        if 'utils.temporal_anomaly_detector.src.detector' in sys.modules:
            del sys.modules['utils.temporal_anomaly_detector.src.detector']

    @patch('datetime.datetime')
    @patch('ntplib.NTPClient')
    def test_no_anomaly(self, mock_ntp_client, mock_datetime):
        # Mock rationale: Simulate a system clock that is perfectly in sync with NTP.
        # This tests the successful path where no anomaly is detected.
        
        # Configure mock datetime.datetime.now(tz=utc)
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 0, 123456, tzinfo=datetime.timezone.utc)
        # Ensure fromtimestamp behaves correctly for the NTP response conversion
        mock_datetime.fromtimestamp.side_effect = lambda ts, tz: datetime.datetime.fromtimestamp(ts, tz=tz)
        mock_datetime.timezone.utc = datetime.timezone.utc # Ensure utc is available for the module

        # Configure mock ntplib.NTPClient().request()
        mock_response = MagicMock()
        # Simulate NTP server time being exactly 0.12 seconds behind local time
        mock_response.tx_time = datetime.datetime(2023, 10, 27, 10, 0, 0, 0, tzinfo=datetime.timezone.utc).timestamp()
        mock_ntp_client.return_value.request.return_value = mock_response

        detector.main()

        self.mock_sys_exit.assert_called_once_with(0)
        output = self.mock_stdout.getvalue()
        self.assertIn("Time difference: 0.12 seconds (threshold: 5.00s).", output)
        self.assertIn("Status: All clear. No temporal anomalies detected.", output)
        self.assertEqual(self.mock_stderr.getvalue(), "")

    @patch('datetime.datetime')
    @patch('ntplib.NTPClient')
    def test_anomaly_detected(self, mock_ntp_client, mock_datetime):
        # Mock rationale: Simulate a system clock that is significantly out of sync with NTP.
        # This tests the anomaly detection path.

        # Configure mock datetime.datetime.now(tz=utc) to be 15 seconds ahead of NTP
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 15, 123456, tzinfo=datetime.timezone.utc)
        mock_datetime.fromtimestamp.side_effect = lambda ts, tz: datetime.datetime.fromtimestamp(ts, tz=tz)
        mock_datetime.timezone.utc = datetime.timezone.utc

        # Configure mock ntplib.NTPClient().request()
        mock_response = MagicMock()
        mock_response.tx_time = datetime.datetime(2023, 10, 27, 10, 0, 0, 0, tzinfo=datetime.timezone.utc).timestamp()
        mock_ntp_client.return_value.request.return_value = mock_response

        detector.main()

        self.mock_sys_exit.assert_called_once_with(1)
        output = self.mock_stdout.getvalue()
        error_output = self.mock_stderr.getvalue()
        self.assertIn("Time difference: 15.12 seconds (threshold: 5.00s).", output)
        self.assertIn("Status: WARNING! Temporal Anomaly Detected! Your system clock is significantly out of sync.", error_output)

    @patch('datetime.datetime')
    @patch('ntplib.NTPClient')
    def test_ntp_server_error(self, mock_ntp_client, mock_datetime):
        # Mock rationale: Simulate a scenario where the NTP server is unreachable or returns an error.
        # This tests the error handling path for network issues.

        # Configure mock datetime.datetime.now(tz=utc)
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 0, 0, tzinfo=datetime.timezone.utc)
        mock_datetime.fromtimestamp.side_effect = lambda ts, tz: datetime.datetime.fromtimestamp(ts, tz=tz)
        mock_datetime.timezone.utc = datetime.timezone.utc

        # Configure mock ntplib.NTPClient().request() to raise an exception
        mock_ntp_client.return_value.request.side_effect = ntplib.NTPException("NTP server error")

        detector.main()

        self.mock_sys_exit.assert_called_once_with(2)
        output = self.mock_stdout.getvalue()
        error_output = self.mock_stderr.getvalue()
        self.assertIn("Attempting to query NTP server: pool.ntp.org", output)
        self.assertIn("Error: Could not query NTP server 'pool.ntp.org'. NTP server error", error_output)
        self.assertIn("Status: Failed to check for anomalies due to NTP server error.", error_output)

    @patch('datetime.datetime')
    @patch('ntplib.NTPClient')
    def test_custom_server_and_threshold(self, mock_ntp_client, mock_datetime):
        # Mock rationale: Test that command-line arguments for server and threshold are correctly parsed and used.

        # Configure mock datetime.datetime.now(tz=utc) to be 3 seconds ahead of NTP
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 3, 0, tzinfo=datetime.timezone.utc)
        mock_datetime.fromtimestamp.side_effect = lambda ts, tz: datetime.datetime.fromtimestamp(ts, tz=tz)
        mock_datetime.timezone.utc = datetime.timezone.utc

        # Configure mock ntplib.NTPClient().request()
        mock_response = MagicMock()
        mock_response.tx_time = datetime.datetime(2023, 10, 27, 10, 0, 0, 0, tzinfo=datetime.timezone.utc).timestamp()
        mock_ntp_client.return_value.request.return_value = mock_response

        # Mock sys.argv to pass custom arguments
        with patch('sys.argv', ['detector.py', '--server', 'custom.ntp.org', '--threshold', '2.5']):
            detector.main()

        self.mock_sys_exit.assert_called_once_with(1) # 3 seconds diff > 2.5 threshold
        output = self.mock_stdout.getvalue()
        error_output = self.mock_stderr.getvalue()
        self.assertIn("Attempting to query NTP server: custom.ntp.org", output)
        self.assertIn("Time difference: 3.00 seconds (threshold: 2.50s).", output)
        self.assertIn("Status: WARNING! Temporal Anomaly Detected!", error_output)

if __name__ == '__main__':
    unittest.main()
