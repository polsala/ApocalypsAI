import unittest
from utils.nightly-emoji-mood-analyzer.src.analyzer import analyze_emojis

class TestEmojiMoodAnalyzer(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(analyze_emojis(""), {})

    def test_unknown_characters_ignored(self):
        # Mock rationale: ensure non‑emoji characters do not affect the result
        self.assertEqual(analyze_emojis("Hello World!"), {})

    def test_single_mood(self):
        self.assertEqual(analyze_emojis("😀😀😃"), {"happy": 3})

    def test_multiple_moods(self):
        input_text = "😀😂👍😢🤔❤️🤯🥳"
        expected = {
            "happy": 1,
            "joy": 1,
            "approval": 1,
            "sad": 1,
            "thinking": 1,
            "love": 1,
            "mindblown": 1,
            "celebration": 1,
        }
        self.assertEqual(analyze_emojis(input_text), expected)

    def test_mixed_known_and_unknown(self):
        # Mock rationale: unknown emojis are ignored, known ones counted
        input_text = "😀X😂Y👍Z"
        expected = {"happy": 1, "joy": 1, "approval": 1}
        self.assertEqual(analyze_emojis(input_text), expected)

if __name__ == "__main__":
    unittest.main()
