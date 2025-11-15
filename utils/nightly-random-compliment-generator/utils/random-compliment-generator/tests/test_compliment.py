import unittest
from unittest.mock import patch

# Mock rationale: we patch `random.choice` to return a predictable value,
# ensuring the test suite runs offline and deterministically.

from utils.random-compliment-generator.src.compliment import get_compliment


class TestComplimentGenerator(unittest.TestCase):
    def test_general_compliment(self):
        # Force `random.choice` to return the first element of the pool.
        with patch('random.choice', side_effect=lambda seq: seq[0]):
            result = get_compliment()
            # The first element after flattening is the first of 'work' list.
            self.assertEqual(result, "Your code is a masterpiece of elegance.")

    def test_category_compliment(self):
        with patch('random.choice', side_effect=lambda seq: seq[-1]):
            result = get_compliment(category='self')
            # The last element of the 'self' list.
            self.assertEqual(result, "You have a brilliant mind and a kind soul.")

    def test_unknown_category_falls_back(self):
        with patch('random.choice', side_effect=lambda seq: seq[1]):
            result = get_compliment(category='nonexistent')
            # Second element of the flattened list (second of 'work').
            self.assertEqual(result, "You turn bugs into features with style.")


if __name__ == '__main__':
    unittest.main()
