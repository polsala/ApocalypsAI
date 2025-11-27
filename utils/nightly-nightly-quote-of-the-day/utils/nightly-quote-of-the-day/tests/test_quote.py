import os
import sys
import unittest
from unittest.mock import patch

# Add the src directory to sys.path so we can import the module
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'src'))
sys.path.append(SRC_DIR)

from quote import get_random_quote

class TestQuote(unittest.TestCase):
    def test_get_random_quote_deterministic(self):
        """Ensure deterministic output by mocking random.choice.
        # Mock rationale: isolates randomness to make the test repeatable offline.
        """
        with patch('random.choice', return_value="Mocked Quote"):
            self.assertEqual(get_random_quote(), "Mocked Quote")

if __name__ == '__main__':
    unittest.main()
