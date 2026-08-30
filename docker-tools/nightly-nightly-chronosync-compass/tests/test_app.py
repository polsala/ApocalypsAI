import unittest
import json
import datetime
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app, WHISPERS_FROM_THE_VOID, STABILITY_STATUSES

class ChronosyncCompassTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.datetime')
    @patch('app.random')
    def test_get_community_time(self, mock_random, mock_datetime):
        # Mock rationale: Ensure deterministic time and stability reading for consistent test results.
        mock_datetime.utcnow.return_value = datetime.datetime(2023, 10, 27, 10, 30, 0, 123456)
        mock_random.uniform.return_value = 0.75 # A value that maps to "Stable as a pre-collapse clockwork"

        response = self.app.get('/time')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIn('community_consensus_time_utc', data)
        self.assertIn('temporal_stability_reading', data)
        self.assertIn('stability_status', data)

        self.assertEqual(data['community_consensus_time_utc'], '2023-10-27T10:30:00.123456Z')
        self.assertEqual(data['temporal_stability_reading'], 0.75)
        self.assertEqual(data['stability_status'], "Stable as a pre-collapse clockwork")

    @patch('app.random')
    def test_get_whisper(self, mock_random):
        # Mock rationale: Ensure a specific whisper is returned for deterministic testing.
        mock_random.choice.return_value = WHISPERS_FROM_THE_VOID[0]

        response = self.app.get('/whisper')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIn('whisper', data)
        self.assertEqual(data['whisper'], WHISPERS_FROM_THE_VOID[0])

    @patch('app.logging.info')
    def test_report_time_success(self, mock_log_info):
        # Mock rationale: Prevent actual logging during test and verify log call.
        test_payload = {
            "local_time": "2023-10-27T10:30:05Z",
            "source": "Outpost Alpha-7"
        }
        response = self.app.post('/report_time', json=test_payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertEqual(data['status'], "Time observation logged.")
        self.assertEqual(data['received_time'], test_payload['local_time'])
        self.assertEqual(data['source'], test_payload['source'])
        mock_log_info.assert_called_with(f"Received time report from {test_payload['source']}: {test_payload['local_time']}")

    def test_report_time_missing_fields(self):
        response = self.app.post('/report_time', json={"local_time": "2023-10-27T10:30:05Z"})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Missing 'local_time' or 'source' in request body.")

        response = self.app.post('/report_time', json={"source": "Outpost Alpha-7"})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "Missing 'local_time' or 'source' in request body.")

    def test_get_stability_status_boundaries(self):
        # Test boundaries for stability statuses
        from app import get_stability_status # Import directly for testing internal function

        self.assertEqual(get_stability_status(0.0), "Temporal fabric is fraying! Seek shelter!")
        self.assertEqual(get_stability_status(0.1), "Temporal fabric is fraying! Seek shelter!")
        self.assertEqual(get_stability_status(0.2), "Temporal fabric is fraying! Seek shelter!") # Upper bound of first range

        self.assertEqual(get_stability_status(0.21), "Significant temporal flux detected. Proceed with caution.")
        self.assertEqual(get_stability_status(0.3), "Significant temporal flux detected. Proceed with caution.")
        self.assertEqual(get_stability_status(0.4), "Significant temporal flux detected. Proceed with caution.")

        self.assertEqual(get_stability_status(0.41), "Minor temporal anomalies present. Keep an eye on your chronometers.")
        self.assertEqual(get_stability_status(0.5), "Minor temporal anomalies present. Keep an eye on your chronometers.")
        self.assertEqual(get_stability_status(0.6), "Minor temporal anomalies present. Keep an eye on your chronometers.")

        self.assertEqual(get_stability_status(0.61), "Stable as a pre-collapse clockwork. All clear.")
        self.assertEqual(get_stability_status(0.7), "Stable as a pre-collapse clockwork. All clear.")
        self.assertEqual(get_stability_status(0.8), "Stable as a pre-collapse clockwork. All clear.")

        self.assertEqual(get_stability_status(0.81), "Unusually high temporal coherence. A good day for planning!")
        self.assertEqual(get_stability_status(0.9), "Unusually high temporal coherence. A good day for planning!")
        self.assertEqual(get_stability_status(1.0), "Unusually high temporal coherence. A good day for planning!")

if __name__ == '__main__':
    unittest.main()
