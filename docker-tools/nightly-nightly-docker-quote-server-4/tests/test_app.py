import unittest
import json
from src import app as quote_app

class TestQuoteApp(unittest.TestCase):
    def setUp(self):
        self.client = quote_app.app.test_client()

    def test_get_random_quote_returns_valid(self):
        quote = quote_app.get_random_quote()
        self.assertIn(quote, quote_app.QUOTES)

    def test_quote_endpoint(self):
        response = self.client.get("/quote")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("quote", data)
        self.assertIn(data["quote"], quote_app.QUOTES)

if __name__ == "__main__":
    unittest.main()
