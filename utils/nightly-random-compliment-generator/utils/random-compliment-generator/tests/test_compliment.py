import unittest
from unittest.mock import patch

# Mock rationale: Ensure deterministic output by forcing random.choice to return the first element.

from src.compliment import get_compliment, _COMPLIMENTS

class TestComplimentGenerator(unittest.TestCase):
    def test_get_compliment_returns_string(self):
        # Basic sanity check – the function returns a string from the list.
        result = get_compliment()
        self.assertIsInstance(result, str)
        self.assertIn(result, _COMPLIMENTS)

    @patch('random.choice', lambda seq: seq[0])
    def test_get_compliment_deterministic_with_mock(self):
        # With random.choice mocked to always pick the first element,
        # the output should be the first compliment in the list.
        expected = _COMPLIMENTS[0]
        self.assertEqual(get_compliment(), expected)

if __name__ == "__main__":
    unittest.main()
