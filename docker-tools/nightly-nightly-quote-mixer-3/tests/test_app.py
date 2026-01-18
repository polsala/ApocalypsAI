import unittest
from unittest.mock import patch
from src.app import app

class QuoteTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("src.app.random.choice")
    def test_blended_quote(self, mock_choice):
        # Mock the two calls to random.choice with deterministic returns
        mock_choice.side_effect = [
            "The only limit to our realization of tomorrow is our doubts of today.",
            "When the sky falls, we shall dance."
        ]
        response = self.client.get("/quote")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        expected = "The only limit to our realization of tomorrow is our doubts of today. When the sky falls, we shall dance."
        self.assertEqual(data["quote"], expected)

if __name__ == "__main__":
    unittest.main()
