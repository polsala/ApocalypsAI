import unittest
import os
import sys
import io
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import chrono_compass

class TestChronoCompass(unittest.TestCase):

    @patch('ntplib.NTPClient')
    def test_get_ntp_time_offset_success(self, MockNTPClient):
        # Mock rationale: We cannot reliably query external NTP servers in a deterministic, offline test.
        # We need to control the NTP response to test offset calculation.
        mock_response = MagicMock()
        mock_response.offset = 0.05  # Simulate local time being 50ms ahead
        MockNTPClient.return_value.request.return_value = mock_response

        offset = chrono_compass.get_ntp_time_offset("test.ntp.server")
        self.assertAlmostEqual(offset, 0.05)
        MockNTPClient.return_value.request.assert_called_once_with("test.ntp.server", version=3)

    @patch('ntplib.NTPClient')
    def test_get_ntp_time_offset_failure(self, MockNTPClient):
        # Mock rationale: We need to simulate network or NTP server errors without actual network calls.
        MockNTPClient.return_value.request.side_effect = ntplib.NTPException("Connection error")

        # Capture stdout to check error message
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        offset = chrono_compass.get_ntp_time_offset("bad.ntp.server")
        
        sys.stdout = sys.__stdout__ # Restore stdout
        self.assertIsNone(offset)
        self.assertIn("ERROR: Failed to query NTP server bad.ntp.server: Connection error", captured_output.getvalue())

    @patch('chrono_compass.get_ntp_time_offset')
    @patch('chrono_compass.datetime')
    @patch('time.sleep', return_value=None) # Mock sleep to prevent infinite loop
    def test_main_with_drift(self, mock_sleep, mock_datetime, mock_get_offset):
        # Mock rationale:
        # 1. `get_ntp_time_offset`: To provide deterministic NTP offsets without actual network calls.
        # 2. `datetime`: To control the "current local time" for consistent drift calculation and output.
        # 3. `time.sleep`: To prevent the main loop from running indefinitely in a test.

        # Configure mock_datetime to return a fixed time for `datetime.now()`
        fixed_now = datetime(2023, 10, 27, 12, 0, 0, 123456)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime.datetime() calls

        # Simulate NTP servers returning different offsets
        mock_get_offset.side_effect = [
            0.010,  # Server 1: local is 10ms ahead
            0.020,  # Server 2: local is 20ms ahead
            0.005   # Server 3: local is 5ms ahead
        ]

        # Set environment variables for the test
        os.environ["NTP_SERVERS"] = "server1,server2,server3"
        os.environ["CHECK_INTERVAL_SECONDS"] = "1" # Short interval for test

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Run main once (mock_sleep will prevent further iterations)
        chrono_compass.main()

        sys.stdout = sys.__stdout__ # Restore stdout

        output = captured_output.getvalue()

        # Assertions
        self.assertIn("Chrono-Compass initiating temporal scan...", output)
        self.assertIn("NTP Server: server1, Offset: 0.010000s", output)
        self.assertIn("NTP Server: server2, Offset: 0.020000s", output)
        self.assertIn("NTP Server: server3, Offset: 0.005000s", output)
        
        # Expected average offset: (0.010 + 0.020 + 0.005) / 3 = 0.0116666...
        self.assertIn("Average NTP Offset: 0.011667s", output)
        self.assertIn(f"Local System Time: {fixed_now.strftime('%Y-%m-%d %H:%M:%S.%f')}", output)
        
        # Adjusted NTP Time = fixed_now - timedelta(seconds=0.0116666...)
        expected_adjusted_time = fixed_now - timedelta(seconds=0.011666666666666666)
        self.assertIn(f"Adjusted NTP Time:   {expected_adjusted_time.strftime('%Y-%m-%d %H:%M:%S.%f')}", output)
        
        self.assertIn("Local clock drift detected: ahead of average NTP by 0.011667 seconds.", output)
        self.assertIn("Next scan in 1 seconds.", output)
        
        # Ensure get_ntp_time_offset was called for each server
        self.assertEqual(mock_get_offset.call_count, 3)
        mock_get_offset.assert_any_call("server1")
        mock_get_offset.assert_any_call("server2")
        mock_get_offset.assert_any_call("server3")
        
        # Ensure sleep was called once
        mock_sleep.assert_called_once_with(1)

    @patch('chrono_compass.get_ntp_time_offset')
    @patch('chrono_compass.datetime')
    @patch('time.sleep', return_value=None)
    def test_main_no_drift(self, mock_sleep, mock_datetime, mock_get_offset):
        # Mock rationale: Same as above, for deterministic testing of no drift scenario.
        fixed_now = datetime(2023, 10, 27, 12, 0, 0, 123456)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        mock_get_offset.side_effect = [
            0.000001,  # Server 1: negligible drift
            -0.000001, # Server 2: negligible drift
            0.000000   # Server 3: no drift
        ]

        os.environ["NTP_SERVERS"] = "server1,server2,server3"
        os.environ["CHECK_INTERVAL_SECONDS"] = "1"

        captured_output = io.StringIO()
        sys.stdout = captured_output

        chrono_compass.main()

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn("Average NTP Offset: 0.000000s", output)
        self.assertIn("Local clock drift detected: ahead of average NTP by 0.000000 seconds.", output) # Due to float precision, it might be 0.000000 or -0.000000, so 'ahead' is fine.
        self.assertEqual(mock_get_offset.call_count, 3)
        mock_sleep.assert_called_once_with(1)

    @patch('chrono_compass.get_ntp_time_offset')
    @patch('chrono_compass.datetime')
    @patch('time.sleep', return_value=None)
    def test_main_no_successful_responses(self, mock_sleep, mock_datetime, mock_get_offset):
        # Mock rationale: To simulate a scenario where all NTP server queries fail.
        fixed_now = datetime(2023, 10, 27, 12, 0, 0, 123456)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        mock_get_offset.side_effect = [None, None, None] # All queries fail

        os.environ["NTP_SERVERS"] = "server1,server2,server3"
        os.environ["CHECK_INTERVAL_SECONDS"] = "1"

        captured_output = io.StringIO()
        sys.stdout = captured_output

        chrono_compass.main()

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn("WARNING: No successful NTP server responses. Cannot determine average offset.", output)
        self.assertEqual(mock_get_offset.call_count, 3)
        mock_sleep.assert_called_once_with(1)

    @patch('chrono_compass.datetime')
    @patch('time.sleep', return_value=None)
    def test_main_no_ntp_servers_configured(self, mock_sleep, mock_datetime):
        # Mock rationale: To test the edge case where no NTP servers are provided.
        fixed_now = datetime(2023, 10, 27, 12, 0, 0, 123456)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        os.environ["NTP_SERVERS"] = "" # No servers
        os.environ["CHECK_INTERVAL_SECONDS"] = "1"

        captured_output = io.StringIO()
        sys.stdout = captured_output

        chrono_compass.main()

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn("ERROR: No NTP servers configured. Exiting.", output)
        mock_sleep.assert_not_called() # Should exit immediately, no sleep

    def tearDown(self):
        # Clean up environment variables after each test
        if "NTP_SERVERS" in os.environ:
            del os.environ["NTP_SERVERS"]
        if "CHECK_INTERVAL_SECONDS" in os.environ:
            del os.environ["CHECK_INTERVAL_SECONDS"]

if __name__ == '__main__':
    unittest.main()
