import unittest
from utils.nightly-emoji-mood-logger.src.emoji_mood import translate, EMOJI_MAP


class TestEmojiMood(unittest.TestCase):
    def test_basic_replacements(self):
        self.assertEqual(translate("I love coding"), "I ❤️ 💻")
        self.assertEqual(translate("Happy and excited"), "😊 and 🤩")
        self.assertEqual(translate("Python is fun"), "🐍 is fun")

    def test_case_insensitivity(self):
        self.assertEqual(translate("I LOVE CODING"), "I ❤️ 💻")
        self.assertEqual(translate("happy HAPPY Happy"), "😊 😊 😊")

    def test_punctuation_preservation(self):
        self.assertEqual(translate("I love coding!"), "I ❤️ 💻!")
        self.assertEqual(translate("Coffee, tea, and cake..."), "☕, 🍵, and 🍰...")

    def test_no_replacements(self):
        self.assertEqual(translate("Just a normal sentence."), "Just a normal sentence.")

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            translate(123)  # type: ignore

    def test_emoji_map_integrity(self):
        # Mock rationale: ensure the static map contains expected keys without external calls.
        expected_keys = {"love", "happy", "sad", "excited", "code", "python", "coffee"}
        self.assertTrue(expected_keys.issubset(set(EMOJI_MAP.keys())))


if __name__ == "__main__":
    unittest.main()
