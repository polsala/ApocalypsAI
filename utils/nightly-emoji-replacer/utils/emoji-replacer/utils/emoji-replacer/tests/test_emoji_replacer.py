import unittest
from utils.emoji-replacer.utils.emoji-replacer.src.emoji_replacer import replace_emoticons

class TestEmojiReplacer(unittest.TestCase):
    def test_basic_replacements(self):
        cases = {
            "Hello :)": "Hello 😊",
            "Sad :-( today": "Sad 🙁 today",
            "Wink ;) and laugh :D": "Wink 😉 and laugh 😊",
            "Mixed :-P and :/": "Mixed 😛 and 😕",
            "Edge case :') not mapped": "Edge case :') not mapped",
        }
        for inp, expected in cases.items():
            with self.subTest(inp=inp):
                self.assertEqual(replace_emoticons(inp), expected)

    def test_multiple_occurrences(self):
        text = ":) :) :)"
        expected = "😊 😊 😊"
        self.assertEqual(replace_emoticons(text), expected)

    def test_no_emoticons(self):
        text = "Just a normal sentence."
        self.assertEqual(replace_emoticons(text), text)

if __name__ == "__main__":
    unittest.main()
