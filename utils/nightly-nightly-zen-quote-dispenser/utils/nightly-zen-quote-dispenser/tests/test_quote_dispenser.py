import builtins
import unittest
from unittest import mock

# Import the module under test.
from src.quote_dispenser import get_random_quote

class TestQuoteDispenser(unittest.TestCase):
    def test_get_random_quote_returns_mocked_value(self):
        """Ensure the function returns the value supplied by a mock.

        # Mock rationale: We replace `random.choice` with a deterministic lambda
        that returns a known string, guaranteeing the test is offline and repeatable.
        """
        with mock.patch('random.choice', return_value='Mocked Zen Quote'):
            result = get_random_quote()
            self.assertEqual(result, 'Mocked Zen Quote')

    def test_get_random_quote_is_string(self):
        """Check that the returned value is a string and non‑empty.

        # Mock rationale: No external state; we rely on the real implementation
        but the test only asserts type and truthiness, which is deterministic.
        """
        result = get_random_quote()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

if __name__ == '__main__':
    unittest.main()
