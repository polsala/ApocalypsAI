import unittest
from unittest.mock import patch
from src import app as flask_app

class QuoteTest(unittest.TestCase):
    def setUp(self):
        self.client = flask_app.app.test_client()

    @patch('random.choice')
    def test_quote_endpoint(self, mock_choice):
        # Mock rationale: ensure deterministic output without randomness
        mock_choice.return_value = "Test quote for unit testing"
        response = self.client.get('/quote')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"quote": "Test quote for unit testing"})

if __name__ == '__main__':
    unittest.main()
