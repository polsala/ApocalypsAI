import unittest
from unittest.mock import patch

from src.tip_generator import get_random_tip, TIPS

class TestTipGenerator(unittest.TestCase):
    def test_get_random_tip_deterministic(self):
        # Mock rationale: ensure deterministic output by forcing random.choice to return the first tip.
        with patch('random.choice', return_value=TIPS[0]):
            tip = get_random_tip()
            self.assertEqual(tip, TIPS[0])

    def test_tip_list_non_empty(self):
        self.assertTrue(len(TIPS) > 0, "TIPS list should contain at least one tip")

if __name__ == '__main__':
    unittest.main()
