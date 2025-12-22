import unittest
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytz
from src.app import app, calculate_time_status # Assuming src/app.py

class TestApocalypseChronometer(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('src.app.datetime') # Mock rationale: datetime.now() needs to be fixed for deterministic tests.
    def test_calculate_time_status_countdown(self, mock_datetime):
        # Set a fixed 'now' for the test
        fixed_now = datetime(2024, 7, 20, 10, 0, 0, tzinfo=pytz.utc)
        mock_datetime.now.return_value = fixed_now
        # Ensure fromisoformat and timedelta are available on the mocked datetime module
        mock_datetime.fromisoformat = datetime.fromisoformat
        mock_datetime.timedelta = timedelta
        # Ensure datetime.datetime is still the original datetime class for type checks/instantiation
        mock_datetime.datetime = datetime 

        event_name = "The Great Glitch"
        # Event is 1 day, 2 hours, 3 minutes, 4 seconds in the future
        event_dt_str = "2024-07-21T12:03:04Z"
        
        result = calculate_time_status(event_name, event_dt_str)
        expected_status = "Countdown to The Great Glitch: 1 days, 2 hours, 3 minutes, 4 seconds"
        self.assertEqual(result['name'], event_name)
        self.assertEqual(result['status'], expected_status)

    @patch('src.app.datetime') # Mock rationale: datetime.now() needs to be fixed for deterministic tests.
    def test_calculate_time_status_countup(self, mock_datetime):
        # Set a fixed 'now' for the test
        fixed_now = datetime(2024, 7, 20, 10, 0, 0, tzinfo=pytz.utc)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.fromisoformat = datetime.fromisoformat
        mock_datetime.timedelta = timedelta
        mock_datetime.datetime = datetime

        event_name = "The First Whisper"
        # Event was 1 day, 1 hour, 4 minutes, 0 seconds in the past
        event_dt_str = "2024-07-19T08:56:00Z" # 2024-07-20 10:00:00 - (1 day, 1 hour, 4 minutes, 0 seconds) = 2024-07-19 08:56:00
        
        result = calculate_time_status(event_name, event_dt_str)
        expected_status = "Time since The First Whisper: 1 days, 1 hours, 4 minutes, 0 seconds"
        self.assertEqual(result['name'], event_name)
        self.assertEqual(result['status'], expected_status)

    @patch('src.app.datetime') # Mock rationale: datetime.now() needs to be fixed for deterministic tests.
    def test_calculate_time_status_malformed_datetime(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 7, 20, 10, 0, 0, tzinfo=pytz.utc)
        mock_datetime.fromisoformat = datetime.fromisoformat
        mock_datetime.timedelta = timedelta
        mock_datetime.datetime = datetime

        event_name = "Bad Date"
        event_dt_str = "not-a-date"
        
        result = calculate_time_status(event_name, event_dt_str)
        self.assertEqual(result['name'], event_name)
        self.assertIn("Error parsing datetime", result['status'])

    @patch('src.app.os') # Mock rationale: Environment variables need to be controlled for deterministic tests.
    @patch('src.app.datetime') # Mock rationale: datetime.now() needs to be fixed for deterministic tests.
    def test_index_route_with_events(self, mock_datetime, mock_os):
        fixed_now = datetime(2024, 7, 20, 10, 0, 0, tzinfo=pytz.utc)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.fromisoformat = datetime.fromisoformat
        mock_datetime.timedelta = timedelta
        mock_datetime.datetime = datetime

        mock_os.environ.get.return_value = json.dumps([
            {"name": "The Great Glitch", "datetime": "2024-07-21T12:03:04Z"},
            {"name": "The First Whisper", "datetime": "2024-07-19T08:56:00Z"}
        ])

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Countdown to The Great Glitch: 1 days, 2 hours, 3 minutes, 4 seconds", response.data)
        self.assertIn(b"Time since The First Whisper: 1 days, 1 hours, 4 minutes, 0 seconds", response.data)

    @patch('src.app.os') # Mock rationale: Environment variables need to be controlled for deterministic tests.
    def test_index_route_no_events(self, mock_os):
        mock_os.environ.get.return_value = '[]' # No events configured

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No apocalyptic events configured. The void is calm... for now.", response.data)

    @patch('src.app.os') # Mock rationale: Environment variables need to be controlled for deterministic tests.
    def test_index_route_malformed_json(self, mock_os):
        mock_os.environ.get.return_value = '{"name": "malformed"}' # Malformed JSON string

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # If JSON is malformed, configured_events becomes empty, leading to the 'no events' message.
        self.assertIn(b"No apocalyptic events configured. The void is calm... for now.", response.data)

    @patch('src.app.os') # Mock rationale: Environment variables need to be controlled for deterministic tests.
    @patch('src.app.datetime') # Mock rationale: datetime.now() needs to be fixed for deterministic tests.
    def test_index_route_malformed_event_data(self, mock_datetime, mock_os):
        fixed_now = datetime(2024, 7, 20, 10, 0, 0, tzinfo=pytz.utc)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.fromisoformat = datetime.fromisoformat
        mock_datetime.timedelta = timedelta
        mock_datetime.datetime = datetime

        mock_os.environ.get.return_value = json.dumps([
            {"name": "Missing Datetime"},
            {"datetime": "2024-07-21T12:00:00Z"} 
        ])

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Malformed Event", response.data)
        self.assertIn(b"Missing 'name' or 'datetime'", response.data)
        self.assertIn(b"Countdown to ", response.data) # The second (valid) event should still be processed.
