import unittest
from unittest import mock

# Mock rationale: we want deterministic behavior without relying on actual randomness.
# By providing a fixed seed we can assert the exact emoji returned.

from src.emoji_generator import get_random_emoji

class TestEmojiGenerator(unittest.TestCase):
    def test_random_without_seed_returns_str(self):
        emoji = get_random_emoji()
        self.assertIsInstance(emoji, str)
        self.assertTrue(len(emoji) > 0)

    def test_deterministic_with_seed(self):
        # Seed 42 should always produce the same emoji given the current list.
        expected = "🚀"  # Determined by running get_random_emoji(seed=42) once.
        self.assertEqual(get_random_emoji(seed=42), expected)

    @mock.patch('src.emoji_generator.random.choice')
    def test_mocked_choice(self, mock_choice):
        # Mock rationale: ensure the function forwards the list correctly.
        mock_choice.return_value = "🧩"
        self.assertEqual(get_random_emoji(), "🧩")
        mock_choice.assert_called_once()

if __name__ == "__main__":
    unittest.main()
