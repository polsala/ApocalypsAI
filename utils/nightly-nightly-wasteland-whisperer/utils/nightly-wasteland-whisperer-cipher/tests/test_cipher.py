import unittest
import sys
import os

# Mock rationale: We need to test the cipher logic directly without relying on
# the command-line interface. By importing the function directly, we bypass
# argparse and sys.argv, ensuring deterministic, offline unit tests.
# We also need to adjust the path to import the module from src/.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cipher import caesar_cipher

class TestCaesarCipher(unittest.TestCase):

    def test_encrypt_basic(self):
        self.assertEqual(caesar_cipher("abc", 1, "encrypt"), "bcd")
        self.assertEqual(caesar_cipher("xyz", 1, "encrypt"), "yza") # Wrap around
        self.assertEqual(caesar_cipher("Hello", 3, "encrypt"), "Khoor")
        self.assertEqual(caesar_cipher("WORLD", 5, "encrypt"), "BTQWI")

    def test_decrypt_basic(self):
        self.assertEqual(caesar_cipher("bcd", 1, "decrypt"), "abc")
        self.assertEqual(caesar_cipher("yza", 1, "decrypt"), "xyz") # Wrap around
        self.assertEqual(caesar_cipher("Khoor", 3, "decrypt"), "Hello")
        self.assertEqual(caesar_cipher("BTQWI", 5, "decrypt"), "WORLD")

    def test_encrypt_with_spaces_and_punctuation(self):
        self.assertEqual(caesar_cipher("Hello, World!", 3, "encrypt"), "Khoor, Zruog!")
        self.assertEqual(caesar_cipher("123 ApocalypsAI!", 1, "encrypt"), "123 BqpdqmjqpsBJ!")

    def test_decrypt_with_spaces_and_punctuation(self):
        self.assertEqual(caesar_cipher("Khoor, Zruog!", 3, "decrypt"), "Hello, World!")
        self.assertEqual(caesar_cipher("123 BqpdqmjqpsBJ!", 1, "decrypt"), "123 ApocalypsAI!")

    def test_zero_shift(self):
        self.assertEqual(caesar_cipher("Test", 0, "encrypt"), "Test")
        self.assertEqual(caesar_cipher("Test", 0, "decrypt"), "Test")

    def test_large_shift(self):
        self.assertEqual(caesar_cipher("abc", 27, "encrypt"), "bcd") # 27 % 26 = 1
        self.assertEqual(caesar_cipher("abc", 52, "encrypt"), "abc") # 52 % 26 = 0
        self.assertEqual(caesar_cipher("abc", -1, "encrypt"), "zab") # Negative shift should wrap correctly
        self.assertEqual(caesar_cipher("zab", -1, "decrypt"), "abc") # Negative shift should wrap correctly

    def test_empty_string(self):
        self.assertEqual(caesar_cipher("", 5, "encrypt"), "")
        self.assertEqual(caesar_cipher("", 5, "decrypt"), "")

    def test_mixed_case(self):
        self.assertEqual(caesar_cipher("aBcDeF", 1, "encrypt"), "bCdEfG")
        self.assertEqual(caesar_cipher("bCdEfG", 1, "decrypt"), "aBcDeF")

    def test_non_alphabetic_only(self):
        self.assertEqual(caesar_cipher("123!@#$", 5, "encrypt"), "123!@#$")
        self.assertEqual(caesar_cipher("123!@#$", 5, "decrypt"), "123!@#$")

if __name__ == '__main__':
    unittest.main()
