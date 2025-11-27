import unittest
from unittest.mock import patch

# Import the module under test
from src.quote_generator import get_quote, QUOTES

class TestQuoteGenerator(unittest.TestCase):
    def test_deterministic_with_seed(self):
        # Seed 0 should always produce the same quote
        expected = "The journey of a thousand miles begins with one step."
        self.assertEqual(get_quote(seed=0), expected)

    def test_random_path_is_mocked(self):
        # Mock random.choice to ensure offline deterministic behavior
        mock_choice = "Silence is a source of great strength."
        with patch('random.choice', return_value=mock_choice) as mock_rand:
            # Mock rationale: replace true randomness with a fixed return value
            result = get_quote(seed=None)
            mock_rand.assert_called_once_with(QUOTES)
            self.assertEqual(result, mock_choice)

    def test_invalid_seed_type_raises(self):
        # Passing a non‑int should raise a TypeError before reaching the function
        with self.assertRaises(TypeError):
            get_quote(seed="not-an-int")

if __name__ == "__main__":
    unittest.main()
