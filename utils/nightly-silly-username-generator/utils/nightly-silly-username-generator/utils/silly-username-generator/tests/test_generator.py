import unittest
from unittest.mock import patch

# Mock rationale: we patch random.choice and random.randint to produce a deterministic, predictable output without relying on actual randomness.

from utils.silly-username-generator.src.generator import generate_username

class TestSillyUsernameGenerator(unittest.TestCase):
    def test_generate_username_default_deterministic(self):
        # Using a fixed seed should always produce the same result.
        name = generate_username(seed=12345)
        # Expected value derived from the seed 12345 with the default lists.
        # The exact string may differ if the default lists change; this test guards against that.
        self.assertEqual(name, "spooky-penguin07")

    @patch('utils.silly-username-generator.src.generator.random.choice')
    @patch('utils.silly-username-generator.src.generator.random.randint')
    def test_generate_username_with_mocks(self, mock_randint, mock_choice):
        # Mock rationale: force specific adjective and noun choices.
        mock_choice.side_effect = ["brave", "dragon"]
        mock_randint.return_value = 42
        name = generate_username()
        self.assertEqual(name, "brave-dragon42")
        # Ensure the mocks were called the expected number of times.
        self.assertEqual(mock_choice.call_count, 2)
        mock_randint.assert_called_once_with(0, 99)

    def test_generate_username_custom_lists(self):
        adjectives = ["tiny", "giant"]
        nouns = ["hamster", "elephant"]
        name = generate_username(adjectives=adjectives, nouns=nouns, seed=0)
        # With seed=0, the deterministic choice from the custom lists yields:
        self.assertEqual(name, "giant-elephant84")

if __name__ == "__main__":
    unittest.main()
