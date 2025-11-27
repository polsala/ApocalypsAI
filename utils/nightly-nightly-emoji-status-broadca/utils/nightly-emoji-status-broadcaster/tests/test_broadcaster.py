import unittest
from src.broadcaster import status_to_emoji, summarize_statuses

class TestEmojiStatusBroadcaster(unittest.TestCase):
    def test_known_statuses(self):
        self.assertEqual(status_to_emoji("success"), "✅")
        self.assertEqual(status_to_emoji("SUCCESS"), "✅")  # case‑insensitive
        self.assertEqual(status_to_emoji("  failure  "), "❌")  # whitespace tolerant
        self.assertEqual(status_to_emoji("in-progress"), "⏳")

    def test_unknown_status(self):
        # Mock rationale: we want a deterministic fallback for any unrecognised token.
        self.assertEqual(status_to_emoji("foobar"), "❓")
        self.assertEqual(status_to_emoji(""), "❓")

    def test_summarize_multiple(self):
        statuses = ["success", "failure", "in-progress", "unknown"]
        expected = "✅ ❌ ⏳ ❓ (4)"
        self.assertEqual(summarize_statuses(statuses), expected)

    def test_summarize_empty(self):
        # Mock rationale: an empty list should still produce a sensible output.
        self.assertEqual(summarize_statuses([]), " (0)")

if __name__ == "__main__":
    unittest.main()
