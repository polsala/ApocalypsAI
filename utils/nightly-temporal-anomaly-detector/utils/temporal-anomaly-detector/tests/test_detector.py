import unittest
from unittest.mock import patch, MagicMock
import time
import datetime
import io
import sys
import os

# Get the directory of the current test file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the src directory to sys.path for importing the module
sys.path.append(os.path.join(current_dir, '..', 'src'))

# Import the detector class and constants from the source file
from detector import TemporalAnomalyDetector, CHECK_INTERVAL_SECONDS, TIME_JUMP_THRESHOLD_SECONDS, DRIFT_THRESHOLD_PERCENT

# Remove the added path to avoid interfering with other tests
sys.path.pop()

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        self.detector = TemporalAnomalyDetector()
        self.mock_stderr = io.StringIO()
        self.original_stderr = sys.stderr
        sys.stderr = self.mock_stderr

    def tearDown(self):
        sys.stderr = self.original_stderr

    @patch('time.time')
    @patch('time.monotonic')
    def test_initialization(self, mock_monotonic, mock_time):
        # Mock rationale: Simulate initial system and monotonic times to ensure detector initializes correctly.
        mock_time.return_value = 1678886400.0 # March 15, 2023 00:00:00 UTC
        mock_monotonic.return_value = 100.0

        self.detector.detect_anomalies()

        self.assertIsNotNone(self.detector.last_system_time)
        self.assertIsNotNone(self.detector.last_monotonic_time)
        self.assertIn("Initialized monitoring.", self.mock_stderr.getvalue())

    @patch('time.time')
    @patch('time.monotonic')
    def test_no_anomaly_normal_progression(self, mock_monotonic, mock_time):
        # Mock rationale: Simulate normal time progression without jumps or significant drift.
        # First call: Initialize
        mock_time.side_effect = [1678886400.0, 1678886400.0 + CHECK_INTERVAL_SECONDS]
        mock_monotonic.side_effect = [100.0, 100.0 + CHECK_INTERVAL_SECONDS]

        self.detector.detect_anomalies()
        self.mock_stderr.seek(0)
        self.mock_stderr.truncate(0)

        # Second call: Check for anomalies after normal progression
        self.detector.detect_anomalies()

        output = self.mock_stderr.getvalue()
        self.assertNotIn("ANOMALY DETECTED", output)

    @patch('time.time')
    @patch('time.monotonic')
    def test_forward_time_jump(self, mock_monotonic, mock_time):
        # Mock rationale: Simulate a system time jump forward, while monotonic time progresses normally.
        # First call: Initialize
        mock_time.side_effect = [1678886400.0, 1678886400.0 + CHECK_INTERVAL_SECONDS + TIME_JUMP_THRESHOLD_SECONDS + 10]
        mock_monotonic.side_effect = [100.0, 100.0 + CHECK_INTERVAL_SECONDS]

        self.detector.detect_anomalies()
        self.mock_stderr.seek(0)
        self.mock_stderr.truncate(0)

        # Second call: Check for anomalies after a forward jump
        self.detector.detect_anomalies()

        output = self.mock_stderr.getvalue()
        expected_jump_amount = CHECK_INTERVAL_SECONDS + TIME_JUMP_THRESHOLD_SECONDS + 10
        self.assertIn(f"ANOMALY DETECTED: Time jumped forward by {expected_jump_amount:.1f} seconds!", output)

    @patch('time.time')
    @patch('time.monotonic')
    def test_backward_time_jump(self, mock_monotonic, mock_time):
        # Mock rationale: Simulate a system time jump backward, while monotonic time progresses normally.
        # First call: Initialize
        mock_time.side_effect = [1678886400.0, 1678886400.0 + CHECK_INTERVAL_SECONDS - (TIME_JUMP_THRESHOLD_SECONDS + 10)]
        mock_monotonic.side_effect = [100.0, 100.0 + CHECK_INTERVAL_SECONDS]

        self.detector.detect_anomalies()
        self.mock_stderr.seek(0)
        self.mock_stderr.truncate(0)

        # Second call: Check for anomalies after a backward jump
        self.detector.detect_anomalies()

        output = self.mock_stderr.getvalue()
        expected_jump_amount = abs(CHECK_INTERVAL_SECONDS - (TIME_JUMP_THRESHOLD_SECONDS + 10))
        self.assertIn(f"ANOMALY DETECTED: Time jumped backward by {expected_jump_amount:.1f} seconds!", output)

    @patch('time.time')
    @patch('time.monotonic')
    def test_clock_drift_fast(self, mock_monotonic, mock_time):
        # Mock rationale: Simulate system clock running faster than real time.
        # First call: Initialize
        mock_time.side_effect = [1678886400.0, 1678886400.0 + CHECK_INTERVAL_SECONDS * (1 + DRIFT_THRESHOLD_PERCENT/100 + 0.01)]
        mock_monotonic.side_effect = [100.0, 100.0 + CHECK_INTERVAL_SECONDS]

        self.detector.detect_anomalies()
        self.mock_stderr.seek(0)
        self.mock_stderr.truncate(0)

        # Second call: Check for anomalies after drift
        self.detector.detect_anomalies()

        output = self.mock_stderr.getvalue()
        # Calculate the actual drift percentage that should be detected
        system_time_elapsed = CHECK_INTERVAL_SECONDS * (1 + DRIFT_THRESHOLD_PERCENT/100 + 0.01)
        monotonic_time_elapsed = CHECK_INTERVAL_SECONDS
        deviation_percent = ((system_time_elapsed - monotonic_time_elapsed) / monotonic_time_elapsed) * 100
        self.assertIn(f"ANOMALY DETECTED: System clock drifted fast by {deviation_percent:.1f}%", output)

    @patch('time.time')
    @patch('time.monotonic')
    def test_clock_drift_slow(self, mock_monotonic, mock_time):
        # Mock rationale: Simulate system clock running slower than real time.
        # First call: Initialize
        mock_time.side_effect = [1678886400.0, 1678886400.0 + CHECK_INTERVAL_SECONDS * (1 - DRIFT_THRESHOLD_PERCENT/100 - 0.01)]
        mock_monotonic.side_effect = [100.0, 100.0 + CHECK_INTERVAL_SECONDS]

        self.detector.detect_anomalies()
        self.mock_stderr.seek(0)
        self.mock_stderr.truncate(0)

        # Second call: Check for anomalies after drift
        self.detector.detect_anomalies()

        output = self.mock_stderr.getvalue()
        # Calculate the actual drift percentage that should be detected
        system_time_elapsed = CHECK_INTERVAL_SECONDS * (1 - DRIFT_THRESHOLD_PERCENT/100 - 0.01)
        monotonic_time_elapsed = CHECK_INTERVAL_SECONDS
        deviation_percent = ((system_time_elapsed - monotonic_time_elapsed) / monotonic_time_elapsed) * 100
        self.assertIn(f"ANOMALY DETECTED: System clock drifted slow by {deviation_percent:.1f}%", output)

    @patch('time.time')
    @patch('time.monotonic')
    def test_small_jump_ignored(self, mock_monotonic, mock_time):
        # Mock rationale: Simulate a jump smaller than the threshold, which should be ignored.
        # First call: Initialize
        mock_time.side_effect = [1678886400.0, 1678886400.0 + CHECK_INTERVAL_SECONDS + TIME_JUMP_THRESHOLD_SECONDS - 10]
        mock_monotonic.side_effect = [100.0, 100.0 + CHECK_INTERVAL_SECONDS]

        self.detector.detect_anomalies()
        self.mock_stderr.seek(0)
        self.mock_stderr.truncate(0)

        # Second call: Check for anomalies after a small jump
        self.detector.detect_anomalies()

        output = self.mock_stderr.getvalue()
        self.assertNotIn("ANOMALY DETECTED: Time jumped", output)

    @patch('time.time')
    @patch('time.monotonic')
    def test_small_drift_ignored(self, mock_monotonic, mock_time):
        # Mock rationale: Simulate drift smaller than the threshold, which should be ignored.
        # First call: Initialize
        mock_time.side_effect = [1678886400.0, 1678886400.0 + CHECK_INTERVAL_SECONDS * (1 + DRIFT_THRESHOLD_PERCENT/100 - 0.01)]
        mock_monotonic.side_effect = [100.0, 100.0 + CHECK_INTERVAL_SECONDS]

        self.detector.detect_anomalies()
        self.mock_stderr.seek(0)
        self.mock_stderr.truncate(0)

        # Second call: Check for anomalies after small drift
        self.detector.detect_anomalies()

        output = self.mock_stderr.getvalue()
        self.assertNotIn("ANOMALY DETECTED: System clock drifted", output)

    @patch('time.sleep', MagicMock())
    @patch('time.time')
    @patch('time.monotonic')
    def test_run_method_stops_on_keyboard_interrupt(self, mock_monotonic, mock_time):
        # Mock rationale: Simulate a KeyboardInterrupt to test graceful shutdown of the run loop.
        mock_time.side_effect = [1678886400.0, 1678886400.0 + CHECK_INTERVAL_SECONDS, 1678886400.0 + 2*CHECK_INTERVAL_SECONDS]
        mock_monotonic.side_effect = [100.0, 100.0 + CHECK_INTERVAL_SECONDS, 100.0 + 2*CHECK_INTERVAL_SECONDS]

        # Make the second call to detect_anomalies (inside the loop) raise KeyboardInterrupt
        with patch.object(self.detector, 'detect_anomalies', side_effect=[None, KeyboardInterrupt]):
            self.detector.run()

        output = self.mock_stderr.getvalue()
        self.assertIn("Detector stopped by user.", output)
        self.assertIn("Starting Temporal Anomaly Detector...", output)

    @patch('time.sleep', MagicMock())
    @patch('time.time')
    @patch('time.monotonic')
    def test_run_method_handles_other_exceptions(self, mock_monotonic, mock_time):
        # Mock rationale: Simulate an unexpected exception during anomaly detection.
        mock_time.side_effect = [1678886400.0, 1678886400.0 + CHECK_INTERVAL_SECONDS, 1678886400.0 + 2*CHECK_INTERVAL_SECONDS]
        mock_monotonic.side_effect = [100.0, 100.0 + CHECK_INTERVAL_SECONDS, 100.0 + 2*CHECK_INTERVAL_SECONDS]

        # Make the second call to detect_anomalies (inside the loop) raise a generic Exception
        with patch.object(self.detector, 'detect_anomalies', side_effect=[None, ValueError("Test Error")]):
            self.detector.run()

        output = self.mock_stderr.getvalue()
        self.assertIn("An unexpected error occurred: Test Error", output)
        self.assertIn("Starting Temporal Anomaly Detector...", output)
