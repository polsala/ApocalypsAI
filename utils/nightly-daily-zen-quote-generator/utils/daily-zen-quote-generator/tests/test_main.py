import unittest
from unittest.mock import patch

# Mock rationale: we patch `random.choice` to return a known value, making the test deterministic and offline.

from src.main import get_quote

class TestDailyZenQuoteGenerator(unittest.TestCase):
    def test_random_general_quote(self):
        with patch('random.choice', return_value='The obstacle is the path.'):
            quote = get_quote()
            self.assertEqual(quote, 'The obstacle is the path.')

    def test_tagged_mindfulness_quote(self):
        with patch('random.choice', return_value='Walk as if you are kissing the Earth with your feet.'):
            quote = get_quote(tag='mindfulness')
            self.assertEqual(quote, 'Walk as if you are kissing the Earth with your feet.')

    def test_unknown_tag_falls_back_to_general(self):
        with patch('random.choice', return_value='Silence is a source of great strength.'):
            quote = get_quote(tag='nonexistent')
            self.assertEqual(quote, 'Silence is a source of great strength.')

if __name__ == '__main__':
    unittest.main()
