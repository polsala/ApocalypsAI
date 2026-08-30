import unittest
from unittest.mock import patch
from src import app as app_module

class QuoteEndpointTest(unittest.TestCase):
    def setUp(self):
        self.client = app_module.app.test_client()

    @patch('src.app.random.choice')
    def test_quote_endpoint_returns_mocked(self, mock_choice):
        # Mock rationale: ensure deterministic output without randomness
        mock_choice.return_value = {"quote": "Test quote", "author": "Tester"}
        response = self.client.get("/quote")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"quote": "Test quote", "author": "Tester"})

if __name__ == "__main__":
    unittest.main()
