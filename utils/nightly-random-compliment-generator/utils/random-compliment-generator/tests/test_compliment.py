import unittest
from unittest.mock import patch
import sys
import os

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Mock rationale: we replace random.choice to return a deterministic value,
# ensuring the test is offline and deterministic.
from compliment import get_compliment

class TestCompliment(unittest.TestCase):
    @patch('random.choice')
    def test_get_compliment_returns_mocked(self, mock_choice):
        mock_choice.return_value = "Mocked compliment"
        result = get_compliment()
        self.assertEqual(result, "Mocked compliment")
        mock_choice.assert_called_once()

if __name__ == '__main__':
    unittest.main()
