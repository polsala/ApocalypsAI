import unittest
import os
from unittest.mock import patch
from src.app import app

class MoodBeaconTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    @patch.dict(os.environ, {}, clear=True) # Mock rationale: Ensure a clean environment for default testing.
    def test_default_message_and_color(self):
        """Test that the beacon displays default message and color when no env vars are set."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Status: Unknown. Proceed with caution.', response.data)
        self.assertIn(b'background-color: lightgray;', response.data)

    @patch.dict(os.environ, {'BEACON_MESSAGE': 'Testing 1-2-3', 'BEACON_COLOR': 'blue'}, clear=True) # Mock rationale: Simulate specific environment variables for testing custom inputs.
    def test_custom_message_and_color(self):
        """Test that the beacon displays custom message and color from env vars."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Testing 1-2-3', response.data)
        self.assertIn(b'background-color: blue;', response.data)

    @patch.dict(os.environ, {'BEACON_MESSAGE': 'Emergency!'}, clear=True) # Mock rationale: Test with only message set.
    def test_custom_message_only(self):
        """Test that the beacon displays custom message and default color when only message is set."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Emergency!', response.data)
        self.assertIn(b'background-color: lightgray;', response.data) # Should fall back to default color

    @patch.dict(os.environ, {'BEACON_COLOR': 'red'}, clear=True) # Mock rationale: Test with only color set.
    def test_custom_color_only(self):
        """Test that the beacon displays default message and custom color when only color is set."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Status: Unknown. Proceed with caution.', response.data) # Should fall back to default message
        self.assertIn(b'background-color: red;', response.data)

    def test_non_existent_route(self):
        """Test that a non-existent route returns a 404."""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
