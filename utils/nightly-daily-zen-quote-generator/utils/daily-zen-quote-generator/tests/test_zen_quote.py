import unittest
from unittest import mock
from utils.daily-zen-quote-generator.src import zen_quote

class TestZenQuote(unittest.TestCase):
    def test_deterministic_seed(self):
        # With seed 42 we expect the third quote (index 2) due to 42 % 5 == 2
        expected = "Simplicity is the ultimate sophistication."
        result = zen_quote.get_random_quote(seed=42)
        self.assertEqual(result, expected)

    def test_random_choice_mocked(self):
        # Mock random.choice to ensure deterministic behaviour without a seed
        with mock.patch('random.choice') as mock_choice:
            mock_choice.return_value = "Let go or be dragged."
            # Mock rationale: we replace the randomness with a fixed return value to keep the test offline and deterministic.
            result = zen_quote.get_random_quote()
            self.assertEqual(result, "Let go or be dragged.")
            mock_choice.assert_called_once()

if __name__ == "__main__":
    unittest.main()
