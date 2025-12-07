import unittest
import json
import os
from unittest.mock import patch, MagicMock

# Import the lambda handler from the source file
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/lambda'))
from get_message import lambda_handler

class TestMoraleBeaconLambda(unittest.TestCase):

    @patch.dict(os.environ, {'UPLIFTING_MESSAGES': json.dumps(["Test Message 1", "Test Message 2"])})
    @patch('random.choice', MagicMock(side_effect=["Test Message 1", "Test Message 2", "Test Message 1"]))
    def test_lambda_handler_returns_random_message(self):
        # Mock rationale: random.choice is non-deterministic. Mocking it ensures
        # the test always receives expected messages in a predictable order.
        # os.environ is mocked to provide a deterministic set of messages for the test.

        # First call
        response = lambda_handler({}, {})
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertIn('message', body)
        self.assertEqual(body['message'], "Test Message 1")
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        self.assertEqual(response['headers']['Access-Control-Allow-Origin'], '*')

        # Second call
        response = lambda_handler({}, {})
        body = json.loads(response['body'])
        self.assertEqual(body['message'], "Test Message 2")

        # Third call
        response = lambda_handler({}, {})
        body = json.loads(response['body'])
        self.assertEqual(body['message'], "Test Message 1")

    @patch.dict(os.environ, {'UPLIFTING_MESSAGES': '[]'})
    @patch('random.choice', MagicMock(return_value="No messages configured, but keep your spirits high!"))
    def test_lambda_handler_empty_messages(self):
        # Mock rationale: Ensures deterministic behavior when the message list is empty.
        response = lambda_handler({}, {})
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['message'], "No messages configured, but keep your spirits high!")

    @patch.dict(os.environ, {}, clear=True) # Clear UPLIFTING_MESSAGES
    @patch('random.choice', MagicMock(return_value="Keep going!")) # Default message from get_message.py
    def test_lambda_handler_no_env_var(self):
        # Mock rationale: Ensures deterministic behavior when UPLIFTING_MESSAGES env var is missing.
        response = lambda_handler({}, {})
        body = json.loads(response['body'])
        self.assertEqual(body['message'], "Keep going!")

    @patch.dict(os.environ, {'UPLIFTING_MESSAGES': 'invalid json'})
    def test_lambda_handler_invalid_json(self):
        # Mock rationale: Tests error handling for malformed environment variable.
        response = lambda_handler({}, {})
        self.assertEqual(response['statusCode'], 500)
        body = json.loads(response['body'])
        self.assertIn('error', body)
        self.assertIn('Failed to retrieve message', body['error'])
        self.assertIn('Expecting value', body['details']) # JSONDecodeError message
