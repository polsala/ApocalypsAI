import unittest
from unittest.mock import patch
import os, sys

# Adjust path to import the module from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from quote import get_random_quote

class TestQuote(unittest.TestCase):
    def test_get_random_quote_deterministic(self):
        # Mock rationale: Ensure deterministic output without relying on actual randomness.
        with patch('random.choice', return_value="Mocked Quote"):
            self.assertEqual(get_random_quote(), "Mocked Quote")

if __name__ == '__main__':
    unittest.main()
