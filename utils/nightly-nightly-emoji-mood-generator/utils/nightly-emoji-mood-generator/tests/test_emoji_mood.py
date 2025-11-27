import unittest
from utils.nightly-emoji-mood-generator.src.emoji_mood import get_mood, EMOJIS

class TestEmojiMood(unittest.TestCase):
    def test_output_is_valid_emoji(self):
        """The function must always return an emoji from the predefined list."""
        result = get_mood("2025-01-01")
        self.assertIn(result, EMOJIS)

    def test_different_inputs_yield_different_emojis(self):
        """Two distinct strings should map to two distinct emojis (high probability).
        This deterministic test ensures the hash mapping works as expected.
        """
        mood_a = get_mood("2025-01-01")
        mood_b = get_mood("2025-01-02")
        # In the extremely unlikely case they collide, the test would be flaky.
        # To avoid flakiness we assert they are *not* equal, and document the rationale.
        self.assertNotEqual(mood_a, mood_b, "# Mock rationale: deterministic hash should produce different indices for different inputs")

if __name__ == "__main__":
    unittest.main()
