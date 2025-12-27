import unittest
import json
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

# Import the Flask app from the src directory
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import app, message_bottles

class TemporalMessageBottleTest(unittest.TestCase):

    def setUp(self):
        """Set up test client and clear message_bottles before each test."""
        self.app = app.test_client()
        self.app.testing = True
        message_bottles.clear() # Clear messages for a clean slate

    def tearDown(self):
        """Clean up after each test."""
        message_bottles.clear()

    @patch('app.datetime') # Mock rationale: To control the current time for deterministic testing of time-sensitive logic.
    def test_bottle_message_success(self, mock_datetime):
        """Test successfully bottling a message."""
        # Mock current time to a fixed point for consistent test results
        mock_datetime.utcnow.return_value = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_datetime.fromisoformat = datetime.fromisoformat # Ensure fromisoformat works normally
        mock_datetime.timezone = timezone # Ensure timezone is available

        test_timestamp = "2024-01-01T11:00:00Z"
        response = self.app.post('/bottle',
                                 data=json.dumps({
                                     'message': 'Hello Future!',
                                     'timestamp': test_timestamp
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['status'], 'Message bottled successfully')
        self.assertEqual(data['bottled_at'], test_timestamp)
        self.assertEqual(len(message_bottles), 1)
        self.assertEqual(message_bottles[data['id']]['message'], 'Hello Future!')

    def test_bottle_message_missing_fields(self):
        """Test bottling a message with missing fields."""
        response = self.app.post('/bottle',
                                 data=json.dumps({'message': 'No timestamp'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing "message" or "timestamp" field', json.loads(response.data)['error'])

        response = self.app.post('/bottle',
                                 data=json.dumps({'timestamp': '2024-01-01T12:00:00Z'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing "message" or "timestamp" field', json.loads(response.data)['error'])

    def test_bottle_message_invalid_timestamp(self):
        """Test bottling a message with an invalid timestamp format."""
        response = self.app.post('/bottle',
                                 data=json.dumps({
                                     'message': 'Invalid time',
                                     'timestamp': 'not-a-timestamp'
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid timestamp format', json.loads(response.data)['error'])

    @patch('app.datetime') # Mock rationale: To control the current time for deterministic testing of time-sensitive logic.
    def test_uncork_no_messages(self, mock_datetime):
        """Test uncorking when no messages are bottled."""
        mock_datetime.utcnow.return_value = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_datetime.fromisoformat = datetime.fromisoformat
        mock_datetime.timezone = timezone

        response = self.app.get('/uncork')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['messages'], [])

    @patch('app.datetime') # Mock rationale: To control the current time for deterministic testing of time-sensitive logic.
    def test_uncork_future_message(self, mock_datetime):
        """Test uncorking a message whose time has not yet arrived."""
        # Bottle a message for the future
        future_time = datetime(2024, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        message_bottles['future_id'] = {'message': 'Still waiting', 'timestamp': future_time}

        # Mock current time to be before the bottled message's time
        mock_datetime.utcnow.return_value = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_datetime.fromisoformat = datetime.fromisoformat
        mock_datetime.timezone = timezone

        response = self.app.get('/uncork')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['messages'], [])

    @patch('app.datetime') # Mock rationale: To control the current time for deterministic testing of time-sensitive logic.
    def test_uncork_past_message(self, mock_datetime):
        """Test uncorking a message whose time has passed."""
        # Bottle a message for the past
        past_time = datetime(2024, 1, 1, 9, 0, 0, tzinfo=timezone.utc)
        message_bottles['past_id'] = {'message': 'From the past', 'timestamp': past_time}

        # Mock current time to be after the bottled message's time
        mock_datetime.utcnow.return_value = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_datetime.fromisoformat = datetime.fromisoformat
        mock_datetime.timezone = timezone

        response = self.app.get('/uncork')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['messages']), 1)
        self.assertEqual(data['messages'][0]['message'], 'From the past')
        self.assertEqual(data['messages'][0]['timestamp'], past_time.isoformat().replace('+00:00', 'Z'))

    @patch('app.datetime') # Mock rationale: To control the current time for deterministic testing of time-sensitive logic.
    def test_uncork_multiple_messages(self, mock_datetime):
        """Test uncorking multiple messages with mixed timestamps."""
        now = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_datetime.utcnow.return_value = now
        mock_datetime.fromisoformat = datetime.fromisoformat
        mock_datetime.timezone = timezone

        # Bottle messages
        message_bottles['id1'] = {'message': 'Message 1 (Past)', 'timestamp': now - timedelta(hours=2)}
        message_bottles['id2'] = {'message': 'Message 2 (Now)', 'timestamp': now}
        message_bottles['id3'] = {'message': 'Message 3 (Future)', 'timestamp': now + timedelta(hours=1)}
        message_bottles['id4'] = {'message': 'Message 4 (Past, later)', 'timestamp': now - timedelta(hours=1)}

        response = self.app.get('/uncork')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['messages']), 3) # id1, id2, id4 should be uncorked

        # Check content and order (should be sorted by timestamp)
        self.assertEqual(data['messages'][0]['message'], 'Message 1 (Past)')
        self.assertEqual(data['messages'][1]['message'], 'Message 4 (Past, later)')
        self.assertEqual(data['messages'][2]['message'], 'Message 2 (Now)')

    @patch('app.datetime') # Mock rationale: To control the current time for deterministic testing of time-sensitive logic.
    def test_bottle_and_uncork_integration(self, mock_datetime):
        """Test a full bottle-then-uncork cycle."""
        # Mock current time for bottling
        mock_datetime.utcnow.return_value = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        mock_datetime.fromisoformat = datetime.fromisoformat
        mock_datetime.timezone = timezone

        # Bottle a message for the near future
        future_timestamp = (mock_datetime.utcnow.return_value + timedelta(minutes=5)).isoformat().replace('+00:00', 'Z')
        bottle_response = self.app.post('/bottle',
                                        data=json.dumps({
                                            'message': 'Future note!',
                                            'timestamp': future_timestamp
                                        }),
                                        content_type='application/json')
        self.assertEqual(bottle_response.status_code, 201)
        bottled_id = json.loads(bottle_response.data)['id']

        # Try to uncork immediately (should be empty)
        uncork_response_1 = self.app.get('/uncork')
        self.assertEqual(uncork_response_1.status_code, 200)
        self.assertEqual(json.loads(uncork_response_1.data)['messages'], [])

        # Advance time past the bottled message's timestamp
        mock_datetime.utcnow.return_value = datetime(2024, 1, 1, 10, 10, 0, tzinfo=timezone.utc) # 10 minutes later

        # Uncork again (should now find the message)
        uncork_response_2 = self.app.get('/uncork')
        self.assertEqual(uncork_response_2.status_code, 200)
        uncorked_messages = json.loads(uncork_response_2.data)['messages']
        self.assertEqual(len(uncorked_messages), 1)
        self.assertEqual(uncorked_messages[0]['id'], bottled_id)
        self.assertEqual(uncorked_messages[0]['message'], 'Future note!')
        self.assertEqual(uncorked_messages[0]['timestamp'], future_timestamp)

if __name__ == '__main__':
    unittest.main()
