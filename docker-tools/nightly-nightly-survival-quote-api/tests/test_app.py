import unittest
from src.app import app, get_quote

class SurvivalQuoteAPITest(unittest.TestCase):
    def setUp(self):
        # Flask provides a test client for making requests without a live server
        self.client = app.test_client()

    def test_get_quote_function(self):
        # Ensure the deterministic function returns the expected first quote
        expected = "When the world ends, remember: a well‑stocked pantry is the ultimate weapon."
        self.assertEqual(get_quote(), expected)

    def test_quote_endpoint(self):
        response = self.client.get('/quote')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('quote', data)
        self.assertEqual(data['quote'], get_quote())

if __name__ == '__main__':
    unittest.main()
