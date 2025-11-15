import unittest
import datetime
from unittest.mock import patch, MagicMock
import sys
import io

# Add src directory to path for importing the module under test
sys.path.append('utils/temporal-anomaly-detector/src')
from detector import get_local_time, get_simulated_ntp_time, check_for_anomalies, main

class TestTemporalAnomalyDetector(unittest.TestCase):

    @patch('detector.datetime')
    def test_get_local_time(self, mock_datetime):
        # Mock rationale: We need to control the exact time returned by datetime.now()
        # to ensure deterministic tests for time-sensitive functions.
        mock_now = datetime.datetime(2023, 10, 27, 10, 0, 0, 123456)
        mock_datetime.datetime.now.return_value = mock_now
        # Ensure datetime.datetime is still accessible for other operations like timedelta
        mock_datetime.datetime = MagicMock(wraps=datetime.datetime)

        self.assertEqual(get_local_time(), mock_now)

    @patch('detector.datetime')
    def test_get_simulated_ntp_time(self, mock_datetime):
        # Mock rationale: Similar to get_local_time, we need to control the base time
        # for simulating NTP offsets deterministically.
        base_time = datetime.datetime(2023, 10, 27, 10, 0, 0)
        # Ensure datetime.datetime is still accessible for other operations like timedelta
        mock_datetime.datetime = MagicMock(wraps=datetime.datetime)

        # Test with no offset
        self.assertEqual(get_simulated_ntp_time(base_time, 0.0), base_time)

        # Test with positive offset
        expected_time_ahead = datetime.datetime(2023, 10, 27, 10, 0, 5)
        self.assertEqual(get_simulated_ntp_time(base_time, 5.0), expected_time_ahead)

        # Test with negative offset
        expected_time_behind = datetime.datetime(2023, 10, 27, 9, 59, 55)
        self.assertEqual(get_simulated_ntp_time(base_time, -5.0), expected_time_behind)

    @patch('detector.get_local_time')
    @patch('detector.get_simulated_ntp_time')
    def test_check_for_anomalies_no_drift(self, mock_get_simulated_ntp_time, mock_get_local_time):
        # Mock rationale: We need to control both local and simulated NTP times
        # to test specific drift scenarios without relying on actual system time.
        mock_local_time = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_get_local_time.return_value = mock_local_time
        mock_get_simulated_ntp_time.return_value = mock_local_time # NTP time matches local

        is_anomaly, drift, local_time, reference_time = check_for_anomalies(tolerance_seconds=1.0, ntp_offset_seconds=0.0)

        self.assertFalse(is_anomaly)
        self.assertAlmostEqual(drift, 0.0)
        self.assertEqual(local_time, mock_local_time)
        self.assertEqual(reference_time, mock_local_time)
        mock_get_local_time.assert_called_once()
        mock_get_simulated_ntp_time.assert_called_once_with(mock_local_time, 0.0)

    @patch('detector.get_local_time')
    @patch('detector.get_simulated_ntp_time')
    def test_check_for_anomalies_within_tolerance(self, mock_get_simulated_ntp_time, mock_get_local_time):
        # Mock rationale: Control times to simulate a small drift that should not trigger an anomaly.
        mock_local_time = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_ntp_time = datetime.datetime(2023, 10, 27, 10, 0, 0, 500000) # 0.5 seconds ahead
        mock_get_local_time.return_value = mock_local_time
        mock_get_simulated_ntp_time.return_value = mock_ntp_time

        is_anomaly, drift, local_time, reference_time = check_for_anomalies(tolerance_seconds=1.0, ntp_offset_seconds=0.5)

        self.assertFalse(is_anomaly)
        self.assertAlmostEqual(drift, 0.5)
        self.assertEqual(local_time, mock_local_time)
        self.assertEqual(reference_time, mock_ntp_time)

    @patch('detector.get_local_time')
    @patch('detector.get_simulated_ntp_time')
    def test_check_for_anomalies_above_tolerance_ahead(self, mock_get_simulated_ntp_time, mock_get_local_time):
        # Mock rationale: Control times to simulate a significant drift (NTP ahead) that should trigger an anomaly.
        mock_local_time = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_ntp_time = datetime.datetime(2023, 10, 27, 10, 0, 2) # 2 seconds ahead
        mock_get_local_time.return_value = mock_local_time
        mock_get_simulated_ntp_time.return_value = mock_ntp_time

        is_anomaly, drift, local_time, reference_time = check_for_anomalies(tolerance_seconds=1.0, ntp_offset_seconds=2.0)

        self.assertTrue(is_anomaly)
        self.assertAlmostEqual(drift, 2.0)
        self.assertEqual(local_time, mock_local_time)
        self.assertEqual(reference_time, mock_ntp_time)

    @patch('detector.get_local_time')
    @patch('detector.get_simulated_ntp_time')
    def test_check_for_anomalies_above_tolerance_behind(self, mock_get_simulated_ntp_time, mock_get_local_time):
        # Mock rationale: Control times to simulate a significant drift (NTP behind) that should trigger an anomaly.
        mock_local_time = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_ntp_time = datetime.datetime(2023, 10, 27, 9, 59, 58) # 2 seconds behind
        mock_get_local_time.return_value = mock_local_time
        mock_get_simulated_ntp_time.return_value = mock_ntp_time

        is_anomaly, drift, local_time, reference_time = check_for_anomalies(tolerance_seconds=1.0, ntp_offset_seconds=-2.0)

        self.assertTrue(is_anomaly)
        self.assertAlmostEqual(drift, -2.0)
        self.assertEqual(local_time, mock_local_time)
        self.assertEqual(reference_time, mock_ntp_time)

    @patch('detector.check_for_anomalies')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('detector.datetime') # Mock datetime for consistent logging timestamps
    def test_main_no_anomaly(self, mock_datetime, mock_exit, mock_stdout, mock_check_for_anomalies):
        # Mock rationale: Control the outcome of check_for_anomalies and system exit behavior
        # to test the main function's output and exit code. Also mock datetime for logging.
        mock_local_time = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_ref_time = datetime.datetime(2023, 10, 27, 10, 0, 0, 100000) # 0.1s drift
        mock_check_for_anomalies.return_value = (False, 0.1, mock_local_time, mock_ref_time)
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 0) # Consistent log time
        # Ensure datetime.datetime is still accessible for other operations like timedelta
        mock_datetime.datetime = MagicMock(wraps=datetime.datetime)

        # Simulate command-line arguments
        with patch('sys.argv', ['detector.py', '--tolerance', '0.5', '--ntp-offset', '0.1']):
            main()

        mock_check_for_anomalies.assert_called_once_with(0.5, 0.1)
        self.assertIn("All temporal vectors aligned. Drift: 0.100000 seconds.", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(0)

    @patch('detector.check_for_anomalies')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('detector.datetime') # Mock datetime for consistent logging timestamps
    def test_main_anomaly_ahead(self, mock_datetime, mock_exit, mock_stdout, mock_check_for_anomalies):
        # Mock rationale: Control the outcome of check_for_anomalies and system exit behavior
        # to test the main function's output and exit code for an anomaly. Also mock datetime for logging.
        mock_local_time = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_ref_time = datetime.datetime(2023, 10, 27, 10, 0, 2) # 2s drift
        mock_check_for_anomalies.return_value = (True, 2.0, mock_local_time, mock_ref_time)
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 0) # Consistent log time
        # Ensure datetime.datetime is still accessible for other operations like timedelta
        mock_datetime.datetime = MagicMock(wraps=datetime.datetime)

        with patch('sys.argv', ['detector.py', '--tolerance', '1.0', '--ntp-offset', '2.0']):
            main()

        mock_check_for_anomalies.assert_called_once_with(1.0, 2.0)
        self.assertIn("🚨 TEMPORAL ANOMALY DETECTED! Reference time is 2.000000 seconds ahead of local time. 🚨", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('detector.check_for_anomalies')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('detector.datetime') # Mock datetime for consistent logging timestamps
    def test_main_anomaly_behind(self, mock_datetime, mock_exit, mock_stdout, mock_check_for_anomalies):
        # Mock rationale: Control the outcome of check_for_anomalies and system exit behavior
        # to test the main function's output and exit code for an anomaly. Also mock datetime for logging.
        mock_local_time = datetime.datetime(2023, 10, 27, 10, 0, 0)
        mock_ref_time = datetime.datetime(2023, 10, 27, 9, 59, 58) # -2s drift
        mock_check_for_anomalies.return_value = (True, -2.0, mock_local_time, mock_ref_time)
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 0) # Consistent log time
        # Ensure datetime.datetime is still accessible for other operations like timedelta
        mock_datetime.datetime = MagicMock(wraps=datetime.datetime)

        with patch('sys.argv', ['detector.py', '--tolerance', '1.0', '--ntp-offset', '-2.0']):
            main()

        mock_check_for_anomalies.assert_called_once_with(1.0, -2.0)
        self.assertIn("🚨 TEMPORAL ANOMALY DETECTED! Reference time is 2.000000 seconds behind local time. 🚨", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
