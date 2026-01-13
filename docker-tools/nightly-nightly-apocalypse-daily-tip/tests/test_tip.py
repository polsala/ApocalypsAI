import unittest
from unittest.mock import patch
from src import tip

class TestTip(unittest.TestCase):
    @patch('random.choice', return_value=\"Always keep a spare bottle of water in your boot.\")
    def test_get_tip(self, mock_choice):
        self.assertEqual(tip.get_tip(), \"Always keep a spare bottle of water in your boot.\")
        mock_choice.assert_called_once_with(tip.TIPS)

if __name__ == \"__main__\":
    unittest.main()

