import os
import unittest
from src.app import get_quote, QUOTES

class TestQuoteServer(unittest.TestCase):
    def test_deterministic_index(self):
        os.environ["QUOTE_INDEX"] = "2"
        self.assertEqual(get_quote(), QUOTES[2])
        del os.environ["QUOTE_INDEX"]

    def test_random_fallback(self):
        if "QUOTE_INDEX" in os.environ:
            del os.environ["QUOTE_INDEX"]
        quote = get_quote()
        self.assertIn(quote, QUOTES)

if __name__ == "__main__":
    unittest.main()
