import unittest
from unittest.mock import patch
import datetime
import sys
import io

# Adjust sys.path to allow importing from src directory when running tests
# from the repository root or within the util directory.
# This ensures 'tracker' can be found.
original_sys_path = sys.path.copy()
if 'utils/temporal-anomaly-tracker/src' not in sys.path:
    sys.path.insert(0, 'utils/temporal-anomaly-tracker/src')

try:
    import tracker
finally:
    # Restore sys.path to its original state after import
    sys.path = original_sys_path

class TestTemporalAnomalyTracker(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = io.StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('tracker.get_reference_time')
    @patch('tracker.get_local_time')
    def test_no_anomaly(self, mock_get_local_time, mock_get_reference_time):
        # Mock rationale: Simulate a scenario where local time and reference time are perfectly aligned.
        # This ensures the detection logic correctly identifies no anomaly.
        mock_now = datetime.datetime(2023, 10, 27, 10, 0, 0, 0)
        mock_get_local_time.return_value = mock_now
        mock_get_reference_time.return_value = mock_now

        is_anomaly, drift = tracker.detect_anomaly(mock_now, mock_now, threshold_seconds=5)
        self.assertFalse(is_anomaly)
        self.assertAlmostEqual(drift, 0.0)

        # Test main function output
        result_code = tracker.main()
        self.assertEqual(result_code, 0)
        output = self.mock_stdout.getvalue()
        self.assertIn("All temporal vectors aligned", output)
        self.assertNotIn("TEMPORAL ANOMALY DETECTED", output)

    @patch('tracker.get_reference_time')
    @patch('tracker.get_local_time')
    def test_positive_anomaly(self, mock_get_local_time, mock_get_reference_time):
        # Mock rationale: Simulate a scenario where local time is ahead of the reference time
        # by more than the threshold, triggering an anomaly detection.
        reference_time = datetime.datetime(2023, 10, 27, 10, 0, 0, 0)
        local_time = reference_time + datetime.timedelta(seconds=10) # 10 seconds ahead
        mock_get_local_time.return_value = local_time
        mock_get_reference_time.return_value = reference_time

        is_anomaly, drift = tracker.detect_anomaly(local_time, reference_time, threshold_seconds=5)
        self.assertTrue(is_anomaly)
        self.assertAlmostEqual(drift, 10.0)

        # Test main function output
        result_code = tracker.main()
        self.assertEqual(result_code, 1)
        output = self.mock_stdout.getvalue()
        self.assertIn("TEMPORAL ANOMALY DETECTED", output)
        self.assertIn("Drift of 10.00 seconds exceeds threshold", output)

    @patch('tracker.get_reference_time')
    @patch('tracker.get_local_time')
    def test_negative_anomaly(self, mock_get_local_time, mock_get_reference_time):
        # Mock rationale: Simulate a scenario where local time is behind the reference time
        # by more than the threshold, triggering an anomaly detection.
        reference_time = datetime.datetime(2023, 10, 27, 10, 0, 0, 0)
        local_time = reference_time - datetime.timedelta(seconds=8) # 8 seconds behind
        mock_get_local_time.return_value = local_time
        mock_get_reference_time.return_value = reference_time

        is_anomaly, drift = tracker.detect_anomaly(local_time, reference_time, threshold_seconds=5)
        self.assertTrue(is_anomaly)
        self.assertAlmostEqual(drift, -8.0)

        # Test main function output
        result_code = tracker.main()
        self.assertEqual(result_code, 1)
        output = self.mock_stdout.getvalue()
        self.assertIn("TEMPORAL ANOMALY DETECTED", output)
        self.assertIn("Drift of -8.00 seconds exceeds threshold", output)

    @patch('tracker.get_reference_time')
    @patch('tracker.get_local_time')
    def test_drift_within_threshold(self, mock_get_local_time, mock_get_reference_time):
        # Mock rationale: Simulate a scenario where local time has a small drift
        # but it's within the acceptable threshold, so no anomaly is reported.
        reference_time = datetime.datetime(2023, 10, 27, 10, 0, 0, 0)
        local_time = reference_time + datetime.timedelta(seconds=3) # 3 seconds ahead, within 5s threshold
        mock_get_local_time.return_value = local_time
        mock_get_reference_time.return_value = reference_time

        is_anomaly, drift = tracker.detect_anomaly(local_time, reference_time, threshold_seconds=5)
        self.assertFalse(is_anomaly)
        self.assertAlmostEqual(drift, 3.0)

        # Test main function output
        result_code = tracker.main()
        self.assertEqual(result_code, 0)
        output = self.mock_stdout.getvalue()
        self.assertIn("All temporal vectors aligned", output)
        self.assertNotIn("TEMPORAL ANOMALY DETECTED", output)

if __name__ == '__main__':
    unittest.main()
