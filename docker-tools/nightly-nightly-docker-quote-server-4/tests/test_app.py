import unittest
from src import app as quote_app\n\nclass TestQuoteApp(unittest.TestCase):
    def test_get_random_quote(self):
        # Mock rationale: the function should return a string that exists in the predefined list
        quote = quote_app.get_random_quote()
        self.assertIn(quote, quote_app.QUOTES)\n\n    def test_quote_endpoint(self):
        # Mock rationale: use Flask test client to ensure endpoint returns 200 and plain text
        client = quote_app.app.test_client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/plain")
        self.assertIn(response.data.decode(), quote_app.QUOTES)\n\nif __name__ == "__main__":
    unittest.main()\n
