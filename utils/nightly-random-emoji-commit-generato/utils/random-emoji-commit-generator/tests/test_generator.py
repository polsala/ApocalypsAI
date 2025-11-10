import unittest
from random_emoji_commit_generator.src.generator import generate_commit_message

class TestRandomEmojiCommitGenerator(unittest.TestCase):
    def test_deterministic_output_with_seed(selfn):
        # Using a fixed seed should always produce the same emoji placement.
        msg = "Add support for multi‑factor authentication"
        result = generate_commit_message(msg, count=3, seed=12345)
        expected = "Add 🐍 support 🦄 for multi‑factor authentication 🚀"
        self.assertEqual(result, expected)

    def test_zero_emoji_count_returns_original(selfn):
        msg = "Refactor login flow"
        self.assertEqual(generate_commit_message(msg, count=0), msg)

    def test_more_emojis_than_pool_cycles(selfn):
        # Request more emojis than the pool size to test cycling logic.
        msg = "Update docs"
        result = generate_commit_message(msg, count=15, seed=0)
        # We don't assert exact string (cycling order depends on shuffle),
        # but we assert the number of emojis inserted.
        emoji_count = sum(1 for token in result.split() if token in [
            "🚀", "✨", "🐛", "🛠️", "📦", "🔧", "🦄", "🐍", "⚡", "🔥", "💡", "✅",
        ])
        self.assertEqual(emoji_count, 15)

if __name__ == "__main__":
    unittest.main()
