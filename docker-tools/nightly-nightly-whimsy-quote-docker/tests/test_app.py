import unittest
from unittest.mock import patch
from src.app import get_random_quote, QUOTES

class TestQuote(unittest.TestCase):
    @patch('random.choice')
    def test_get_random_quote(self, mock_choice):
        mock_choice.return_value = QUOTES[0]
        self.assertEqual(get_random_quote(), QUOTES[0])
        mock_choice.assert_called_once_with(QUOTES)

if __name__ == "__main__":
    unittest.main()
