import unittest
from unittest.mock import patch
import sys
import os

# Add src directory to sys.path for import
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'src'))
sys.path.insert(0, SRC_DIR)

from zen_quote import get_random_quote

class TestZenQuote(unittest.TestCase):
    def test_get_random_quote_deterministic(self):
        # Mock rationale: replace random.choice to return a known string.
        with patch('random.choice', return_value="Mocked Zen Quote") as mock_choice:
            result = get_random_quote()
            mock_choice.assert_called_once()
            self.assertEqual(result, "Mocked Zen Quote")

if __name__ == '__main__':
    unittest.main()
