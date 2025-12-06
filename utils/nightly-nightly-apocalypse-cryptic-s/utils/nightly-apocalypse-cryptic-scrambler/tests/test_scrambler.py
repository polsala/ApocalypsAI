import unittest
# Mock rationale: No external resources are required; the cipher is deterministic and self‑contained.
from src.scrambler import encrypt, decrypt

class TestScrambler(unittest.TestCase):
    def test_round_trip(self):
        original = "Apocalypse Now! 123"
        encrypted = encrypt(original)
        decrypted = decrypt(encrypted)
        self.assertEqual(decrypted, original)

    def test_known_mapping(self):
        # A -> Q, B -> W, Z -> M, a -> q, etc.
        self.assertEqual(encrypt("ABZabz"), "QWMqwm")
        self.assertEqual(decrypt("QWMqwm"), "ABZabz")

    def test_non_alpha_unchanged(self):
        self.assertEqual(encrypt("!@# 456"), "!@# 456")
        self.assertEqual(decrypt("!@# 456"), "!@# 456")

if __name__ == "__main__":
    unittest.main()
