import unittest
from unittest import mock

# Import the module using its full package path
from utils.random-compliment-generator.src.compliment import get_compliment

class TestComplimentGenerator(unittest.TestCase):
    def test_deterministic_with_seed(self):
        # Same seed should always produce the same compliment
        first = get_compliment(seed=12345)
        second = get_compliment(seed=12345)
        self.assertEqual(first, second)

    def test_randomness_without_seed(self):
        # Without a seed, two consecutive calls are likely different
        first = get_compliment()
        second = get_compliment()
        # It's possible they match, but extremely unlikely; we guard against false failures
        self.assertNotEqual(first, second, "Two random compliments should differ")

    def test_mocked_choice(self):
        # Mock rationale: ensure get_compliment returns a known value without relying on randomness.
        with mock.patch('random.choice', return_value='Mocked compliment'):
            result = get_compliment()
            self.assertEqual(result, 'Mocked compliment')

if __name__ == '__main__':
    unittest.main()
