import unittest
from unittest.mock import patch
import os
import sys

# Ensure the src directory is on the import path
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'src'))
sys.path.insert(0, SRC_DIR)

from cat_fact_generator import get_fact, FACTS

class TestCatFactGenerator(unittest.TestCase):
    @patch('random.choice')
    def test_get_fact_returns_mocked(self, mock_choice):
        # Mock rationale: ensure deterministic output without randomness.
        mock_choice.return_value = "Mocked cat fact."
        self.assertEqual(get_fact(), "Mocked cat fact.")
        mock_choice.assert_called_once_with(FACTS)

if __name__ == '__main__':
    unittest.main()
