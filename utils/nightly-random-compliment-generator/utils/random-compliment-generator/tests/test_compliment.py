import unittest
from unittest.mock import patch

# Import the function from the utility's source module
from utils.random-compliment-generator.src.compliment import get_random_compliment, _COMPLIMENTS

class TestRandomComplimentGenerator(unittest.TestCase):
    def test_compliment_is_from_list(self):
        """Ensure the returned compliment is one of the predefined options.
        This test runs without mocking to verify normal behavior.
        """
        compliment = get_random_compliment()
        self.assertIn(compliment, _COMPLIMENTS)

    def test_deterministic_with_mock(self):
        """# Mock rationale: Force `random.choice` to return the first element
        to make the test deterministic and offline.
        """
        with patch('random.choice', lambda seq: seq[0]):
            compliment = get_random_compliment()
            self.assertEqual(compliment, _COMPLIMENTS[0])

if __name__ == "__main__":
    unittest.main()
