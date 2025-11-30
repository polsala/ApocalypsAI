import unittest
from src.emoji_rot13 import encode, decode, _EMOJI_MAP

class TestEmojiRot13(unittest.TestCase):
    def test_roundtrip(self):
        original = "Hello, World! 123"
        encoded = encode(original)
        decoded = decode(encoded)
        self.assertEqual(decoded, original.lower())
        # Note: encode lower‑cases letters; decode returns lower‑cased result.

    def test_known_mapping(self):
        # "abc" -> ROT13 => "nop" -> emojis for n, o, p
        expected_emojis = [_EMOJI_MAP["n"], _EMOJI_MAP["o"], _EMOJI_MAP["p"]]
        self.assertEqual(encode("abc"), "".join(expected_emojis))
        # Decoding should give back "abc"
        self.assertEqual(decode("".join(expected_emojis)), "abc")

    def test_non_alpha_preserved(self):
        text = "1234!@#$"
        self.assertEqual(encode(text), text)
        self.assertEqual(decode(text), text)

if __name__ == "__main__":
    unittest.main()
