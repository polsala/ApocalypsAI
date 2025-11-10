import unittest
from unittest.mock import patch
import sys
import pathlib

# Add src directory to sys.path so we can import the module directly
src_path = pathlib.Path(__file__).resolve().parents[1] / 'src'
sys.path.append(str(src_path))

from quote import get_zen_quote, _QUOTES

class TestZenQuote(unittest.TestCase):
    def test_random_choice_mock(self):
        # Mock random.choice to always return the first element
        with patch('random.choice', lambda seq: seq[0]):
            self.assertEqual(get_zen_quote(), _QUOTES[0])

    def test_max_length_filter(self):
        short_quotes = [q for q in _QUOTES if len(q) <= 30]
        self.assertTrue(short_quotes)  # Ensure at least one short quote exists
        with patch('random.choice', lambda seq: seq[0]):
            quote = get_zen_quote(max_length=30)
            self.assertIn(quote, short_quotes)

    def test_no_match_raises(self):
        with self.assertRaises(ValueError):
            get_zen_quote(max_length=1)

if __name__ == '__main__':
    unittest.main()
