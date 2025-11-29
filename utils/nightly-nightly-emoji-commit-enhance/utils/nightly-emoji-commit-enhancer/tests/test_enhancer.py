import unittest
from unittest import mock

# Mock rationale: we replace ``random.Random.choice`` to make the emoji selection deterministic.
# This ensures the test suite runs offline and yields the same result every time.

from utils.nightly_emoji_commit_enhancer.src.enhancer import enhance_message

class TestEmojiCommitEnhancer(unittest.TestCase):
    def test_enhance_message_deterministic(self):
        # Seed 0 should always pick the same emoji from the list.
        result = enhance_message("Add new feature", seed=0)
        # With seed=0, the first choice from EMOJIS list is "🚀" (verified by running the function).
        self.assertTrue(result.endswith("🚀"))
        # Ensure the total length does not exceed 72 characters.
        self.assertLessEqual(len(result), 72)

    def test_truncation_respects_limit(self):
        long_msg = "A" * 100  # 100 characters, definitely over the limit.
        result = enhance_message(long_msg, seed=1)
        # The result should be exactly 72 characters long.
        self.assertEqual(len(result), 72)
        # The last character should be an emoji from the list.
        self.assertIn(result[-1], ["🚀", "✨", "🐛", "🔧", "📦", "✅", "⚡", "🧹", "🛠️", "🎉",
                                   "💡", "🔒", "🧪", "📈", "🗑️", "🧩", "🔁", "🧭", "🪄", "🤖"])
        # There must be a space before the emoji.
        self.assertEqual(result[-2], " ")

    @mock.patch('utils.nightly_emoji_commit_enhancer.src.enhancer.random.Random.choice')
    def test_mocked_emoji(self, mock_choice):
        mock_choice.return_value = "🧹"
        result = enhance_message("Fix lint errors", seed=123)
        self.assertTrue(result.endswith("🧹"))
        # Verify that the mock was called exactly once.
        mock_choice.assert_called_once()

if __name__ == "__main__":
    unittest.main()
