import unittest
from unittest.mock import patch, MagicMock
import datetime
import sys
import io

# Add src directory to path for import, then remove it to keep path clean
sys.path.insert(0, 'utils/nightly-chrono-sync-beacon/src')
from chrono_sync import get_system_time, get_mock_reference_time, check_time_drift, main
sys.path.pop(0)

class TestChronoSync(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = io.StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('datetime.datetime')
    def test_get_system_time(self, mock_datetime):
        # Mock rationale: We need to control the system time for deterministic testing.
        # By patching datetime.datetime, we can ensure datetime.datetime.now() returns
        # a predictable value. We also ensure datetime.timezone.utc is available.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 0, 5, tzinfo=datetime.timezone.utc)
        mock_datetime.timezone = MagicMock()
        mock_datetime.timezone.utc = datetime.timezone.utc

        system_time = get_system_time()
        self.assertEqual(system_time, datetime.datetime(2023, 10, 27, 10, 0, 5, tzinfo=datetime.timezone.utc))
        mock_datetime.now.assert_called_once_with(datetime.timezone.utc)

    def test_get_mock_reference_time(self):
        # This function is already a mock for real NTP calls, so we just test its fixed output.
        expected_time = datetime.datetime(2023, 10, 27, 10, 0, 0, tzinfo=datetime.timezone.utc)
        self.assertEqual(get_mock_reference_time(), expected_time)

    @patch('chrono_sync.get_system_time')
    def test_check_time_drift_no_drift(self, mock_get_system_time):
        # Mock rationale: Control system time to simulate no drift against the reference.
        mock_get_system_time.return_value = datetime.datetime(2023, 10, 27, 10, 0, 0, tzinfo=datetime.timezone.utc)
        
        # Mock rationale: Provide a fixed reference time for deterministic testing.
        mock_reference_provider = MagicMock(return_value=datetime.datetime(2023, 10, 27, 10, 0, 0, tzinfo=datetime.timezone.utc))

        drift, message = check_time_drift(mock_reference_provider, 1)
        self.assertAlmostEqual(drift, 0.0, places=2)
        self.assertIn("INFO: System clock is within 1 seconds of reference. Drift: 0.00 seconds.", message)

    @patch('chrono_sync.get_system_time')
    def test_check_time_drift_ahead(self, mock_get_system_time):
        # Mock rationale: Control system time to simulate being ahead of the reference.
        mock_get_system_time.return_value = datetime.datetime(2023, 10, 27, 10, 0, 5, tzinfo=datetime.timezone.utc)
        
        # Mock rationale: Provide a fixed reference time for deterministic testing.
        mock_reference_provider = MagicMock(return_value=datetime.datetime(2023, 10, 27, 10, 0, 0, tzinfo=datetime.timezone.utc))

        drift, message = check_time_drift(mock_reference_provider, 1)
        self.assertAlmostEqual(drift, 5.0, places=2)
        self.assertIn("WARNING: System clock is ahead by 5.00 seconds (>1s threshold).", message)

    @patch('chrono_sync.get_system_time')
    def test_check_time_drift_behind(self, mock_get_system_time):
        # Mock rationale: Control system time to simulate being behind the reference.
        mock_get_system_time.return_value = datetime.datetime(2023, 10, 27, 9, 59, 55, tzinfo=datetime.timezone.utc)
        
        # Mock rationale: Provide a fixed reference time for deterministic testing.
        mock_reference_provider = MagicMock(return_value=datetime.datetime(2023, 10, 27, 10, 0, 0, tzinfo=datetime.timezone.utc))

        drift, message = check_time_drift(mock_reference_provider, 1)
        self.assertAlmostEqual(drift, -5.0, places=2)
        self.assertIn("WARNING: System clock is behind by 5.00 seconds (>1s threshold).", message)

    @patch('chrono_sync.get_system_time')
    def test_check_time_drift_within_threshold(self, mock_get_system_time):
        # Mock rationale: Control system time to simulate being slightly ahead but within threshold.
        mock_get_system_time.return_value = datetime.datetime(2023, 10, 27, 10, 0, 0, 500000, tzinfo=datetime.timezone.utc) # 0.5 seconds ahead
        
        # Mock rationale: Provide a fixed reference time for deterministic testing.
        mock_reference_provider = MagicMock(return_value=datetime.datetime(2023, 10, 27, 10, 0, 0, tzinfo=datetime.timezone.utc))

        drift, message = check_time_drift(mock_reference_provider, 1)
        self.assertAlmostEqual(drift, 0.5, places=2)
        self.assertIn("INFO: System clock is within 1 seconds of reference. Drift: 0.50 seconds.", message)

    @patch('chrono_sync.check_time_drift')
    @patch('sys.argv', ['chrono_sync.py', '--threshold', '2'])
    def test_main_exit_0_on_no_drift(self, mock_check_time_drift):
        # Mock rationale: Simulate a scenario where drift is within the threshold.
        # This allows testing the main function's exit code without actual time calculations.
        mock_check_time_drift.return_value = (1.5, "INFO: System clock is within 2 seconds of reference. Drift: 1.50 seconds.")

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("INFO: System clock is within 2 seconds of reference. Drift: 1.50 seconds.", self.mock_stdout.getvalue())

    @patch('chrono_sync.check_time_drift')
    @patch('sys.argv', ['chrono_sync.py', '--threshold', '2'])
    def test_main_exit_1_on_drift_exceeds_threshold(self, mock_check_time_drift):
        # Mock rationale: Simulate a scenario where drift exceeds the threshold.
        # This allows testing the main function's exit code without actual time calculations.
        mock_check_time_drift.return_value = (2.5, "WARNING: System clock is ahead by 2.50 seconds (>2s threshold).")

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("WARNING: System clock is ahead by 2.50 seconds (>2s threshold).", self.mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
