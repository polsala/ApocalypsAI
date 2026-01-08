import unittest
from src.app import app, QUOTES

class QuoteServerTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_quote_endpoint_returns_known_quote(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        # Ensure the response is one of the predefined quotes
        self.assertIn(text, QUOTES)

if __name__ == "__main__":
    unittest.main()
