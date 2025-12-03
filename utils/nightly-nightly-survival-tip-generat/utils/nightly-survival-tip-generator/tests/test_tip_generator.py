import os
import sys
import unittest
from unittest.mock import patch

# Adjust path so the src module can be imported.
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'src'))
sys.path.append(SRC_DIR)

from tip_generator import get_random_tip, _TIPS

class TestTipGenerator(unittest.TestCase):
    def test_get_random_tip_returns_string(self):
        tip = get_random_tip()
        self.assertIsInstance(tip, str)

    @patch('random.choice')
    def test_get_random_tip_mocked(self, mock_choice):
        # Mock rationale: ensure deterministic output without randomness.
        mock_choice.return_value = _TIPS[3]  # "Barter with canned beans; they're the new gold."
        tip = get_random_tip()
        self.assertEqual(tip, _TIPS[3])
        mock_choice.assert_called_once_with(_TIPS)

if __name__ == '__main__':
    unittest.main()
