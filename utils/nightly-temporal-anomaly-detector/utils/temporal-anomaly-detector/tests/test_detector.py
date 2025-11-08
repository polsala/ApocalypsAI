import unittest
import io
from datetime import datetime, timedelta
from unittest.mock import patch

# Mock rationale: We need to test the detector's logic without actual file I/O.
# io.StringIO allows us to simulate reading from a file in memory.
# patch('datetime.now') is used for syslog-like formats that assume the current year,
# ensuring deterministic tests regardless of when they are run.

from src.detector import TemporalAnomalyDetector

class TestTemporalAnomalyDetector(unittest.TestCase):

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_no_anomalies(self, mock_now):
        log_content = io.StringIO(
            "[2023-01-01 10:00:00] INFO: Event A occurred\n"
            "[2023-01-01 10:00:01] INFO: Event B occurred\n"
            "[2023-01-01 10:00:02] INFO: Event C occurred\n"
        )
        detector = TemporalAnomalyDetector(temporal_jump_threshold_seconds=10)
        anomalies = detector.detect_anomalies(log_content)
        self.assertEqual(len(anomalies), 0)

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_out_of_order_anomaly(self, mock_now):
        log_content = io.StringIO(
            "[2023-01-01 10:00:00] Event 1\n"
            "[2023-01-01 09:59:59] Event 2 (out of order)\n"
            "[2023-01-01 10:00:01] Event 3\n"
        )
        detector = TemporalAnomalyDetector()
        anomalies = detector.detect_anomalies(log_content)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'OUT_OF_ORDER')
        self.assertEqual(anomalies[0]['line'], 2)
        self.assertIn('09:59:59', anomalies[0]['context'])

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_temporal_jump_anomaly(self, mock_now):
        log_content = io.StringIO(
            "[2023-01-01 10:00:00] Event A\n"
            "[2023-01-01 11:00:01] Event B (large jump)\n"
            "[2023-01-01 11:00:02] Event C\n"
        )
        # Threshold is 1 hour (3600s). Jump is 1h 1s, so it should be detected.
        detector = TemporalAnomalyDetector(temporal_jump_threshold_seconds=3600)
        anomalies = detector.detect_anomalies(log_content)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'TEMPORAL_JUMP')
        self.assertEqual(anomalies[0]['line'], 2)
        self.assertIn('Time jump of 1:00:01', anomalies[0]['details'])

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_temporal_jump_within_threshold(self, mock_now):
        log_content = io.StringIO(
            "[2023-01-01 10:00:00] Event A\n"
            "[2023-01-01 10:59:59] Event B (within threshold)\n"
        )
        # Threshold is 1 hour (3600s). Jump is 59m 59s, so it should NOT be detected.
        detector = TemporalAnomalyDetector(temporal_jump_threshold_seconds=3600)
        anomalies = detector.detect_anomalies(log_content)
        self.assertEqual(len(anomalies), 0)

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_impossible_date_anomaly(self, mock_now):
        log_content = io.StringIO(
            "[2023-02-30 10:00:00] Event with impossible date\n"
        )
        detector = TemporalAnomalyDetector()
        anomalies = detector.detect_anomalies(log_content)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'IMPOSSIBLE_DATE')
        self.assertEqual(anomalies[0]['line'], 1)
        self.assertIn('Could not parse timestamp', anomalies[0]['details'])

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_mixed_log_formats(self, mock_now):
        log_content = io.StringIO(
            "2023-01-01 10:00:00.123 Event A\n"
            "01/01/2023 10:00:01 Event B\n"
            "[01/Jan/2023:10:00:02 +0000] Event C\n"
            "Jan  1 10:00:03 myhost process: Event D\n"
        )
        detector = TemporalAnomalyDetector()
        anomalies = detector.detect_anomalies(log_content)
        self.assertEqual(len(anomalies), 0)

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_custom_regex_format(self, mock_now):
        log_content = io.StringIO(
            "LOG_ENTRY: 2023-01-01T10:00:00Z - Message 1\n"
            "LOG_ENTRY: 2023-01-01T10:00:01Z - Message 2\n"
        )
        custom_regex = r'LOG_ENTRY: (?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)'
        detector = TemporalAnomalyDetector(custom_format_regex=custom_regex)
        anomalies = detector.detect_anomalies(log_content)
        self.assertEqual(len(anomalies), 0)

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_custom_regex_with_anomaly(self, mock_now):
        log_content = io.StringIO(
            "LOG_ENTRY: 2023-01-01T10:00:00Z - Message 1\n"
            "LOG_ENTRY: 2023-01-01T09:59:59Z - Message 2 (out of order)\n"
        )
        custom_regex = r'LOG_ENTRY: (?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)'
        detector = TemporalAnomalyDetector(custom_format_regex=custom_regex)
        anomalies = detector.detect_anomalies(log_content)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'OUT_OF_ORDER')

    def test_custom_regex_missing_named_group(self):
        with self.assertRaisesRegex(ValueError, "Custom regex must contain a named group 'timestamp'"):
            TemporalAnomalyDetector(custom_format_regex=r'(\d{4}-\d{2}-\d{2})')

    def test_invalid_custom_regex(self):
        with self.assertRaisesRegex(ValueError, "Invalid custom regex pattern"):
            TemporalAnomalyDetector(custom_format_regex=r'['))

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_empty_file(self, mock_now):
        log_content = io.StringIO("")
        detector = TemporalAnomalyDetector()
        anomalies = detector.detect_anomalies(log_content)
        self.assertEqual(len(anomalies), 0)

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_file_not_found(self, mock_now):
        # Mock rationale: We need to test the scenario where the file path provided to the CLI doesn't exist.
        # Instead of creating a dummy file, we test the error handling path directly.
        # The `detect_anomalies` method handles `FileNotFoundError` internally when given a string path.
        detector = TemporalAnomalyDetector()
        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            anomalies = detector.detect_anomalies("non_existent_file.log")
            self.assertEqual(len(anomalies), 0)
            self.assertIn("Error: File not found", mock_stderr.getvalue())

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_syslog_like_format_with_year_assumption(self, mock_now):
        log_content = io.StringIO(
            "Jan  1 10:00:00 myhost process: Event A\n"
            "Jan  1 10:00:01 myhost process: Event B\n"
        )
        detector = TemporalAnomalyDetector()
        anomalies = detector.detect_anomalies(log_content)
        self.assertEqual(len(anomalies), 0)

    @patch('datetime.now', return_value=datetime(2023, 1, 1, 0, 0, 0))
    def test_syslog_like_format_out_of_order(self, mock_now):
        log_content = io.StringIO(
            "Jan  2 10:00:00 myhost process: Event A\n"
            "Jan  1 10:00:00 myhost process: Event B (out of order)\n"
        )
        detector = TemporalAnomalyDetector()
        anomalies = detector.detect_anomalies(log_content)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'OUT_OF_ORDER')
        self.assertIn('Jan  1 10:00:00', anomalies[0]['context'])


if __name__ == '__main__':
    unittest.main()
