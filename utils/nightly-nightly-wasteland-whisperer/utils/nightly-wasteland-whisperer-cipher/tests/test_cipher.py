import unittest
import sys
from io import StringIO
from unittest.mock import patch
from src.cipher import caesar_cipher, main

class TestCaesarCipher(unittest.TestCase):

    def test_encrypt_lowercase(self):
        self.assertEqual(caesar_cipher("abc", 1, "encrypt"), "bcd")
        self.assertEqual(caesar_cipher("xyz", 3, "encrypt"), "abc")
        self.assertEqual(caesar_cipher("hello", 5, "encrypt"), "mjqqt")

    def test_decrypt_lowercase(self):
        self.assertEqual(caesar_cipher("bcd", 1, "decrypt"), "abc")
        self.assertEqual(caesar_cipher("abc", 3, "decrypt"), "xyz")
        self.assertEqual(caesar_cipher("mjqqt", 5, "decrypt"), "hello")

    def test_encrypt_uppercase(self):
        self.assertEqual(caesar_cipher("ABC", 1, "encrypt"), "BCD")
        self.assertEqual(caesar_cipher("XYZ", 3, "encrypt"), "ABC")
        self.assertEqual(caesar_cipher("WORLD", 10, "encrypt"), "GYBVF")

    def test_decrypt_uppercase(self):
        self.assertEqual(caesar_cipher("BCD", 1, "decrypt"), "ABC")
        self.assertEqual(caesar_cipher("ABC", 3, "decrypt"), "XYZ")
        self.assertEqual(caesar_cipher("GYBVF", 10, "decrypt"), "WORLD")

    def test_encrypt_mixed_case(self):
        self.assertEqual(caesar_cipher("Hello World", 3, "encrypt"), "Khoor Zruog")
        self.assertEqual(caesar_cipher("ApocalypsAI", 5, "encrypt"), "FuntbknuyxFL")

    def test_decrypt_mixed_case(self):
        self.assertEqual(caesar_cipher("Khoor Zruog", 3, "decrypt"), "Hello World")
        self.assertEqual(caesar_cipher("FuntbknuyxFL", 5, "decrypt"), "ApocalypsAI")

    def test_non_alphabetic_characters(self):
        self.assertEqual(caesar_cipher("Hello, World! 123", 3, "encrypt"), "Khoor, Zruog! 123")
        self.assertEqual(caesar_cipher("Khoor, Zruog! 123", 3, "decrypt"), "Hello, World! 123")
        self.assertEqual(caesar_cipher("123 @#$", 5, "encrypt"), "123 @#$")
        self.assertEqual(caesar_cipher("123 @#$", 5, "decrypt"), "123 @#$")

    def test_zero_key(self):
        self.assertEqual(caesar_cipher("Test", 0, "encrypt"), "Test")
        self.assertEqual(caesar_cipher("Test", 0, "decrypt"), "Test")

    def test_large_key(self):
        # Key 27 is equivalent to key 1 (27 % 26 = 1)
        self.assertEqual(caesar_cipher("abc", 27, "encrypt"), "bcd")
        self.assertEqual(caesar_cipher("bcd", 27, "decrypt"), "abc")
        self.assertEqual(caesar_cipher("abc", 52, "encrypt"), "abc") # 52 % 26 = 0
        self.assertEqual(caesar_cipher("abc", 52, "decrypt"), "abc")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encrypt(self, mock_parse_args, mock_stdout):
        # Mock rationale: We need to test the main function's CLI behavior without
        # actually parsing command-line arguments or affecting the real stdout.
        # `parse_args` is mocked to return a predefined Namespace object,
        # and `sys.stdout` is redirected to a StringIO object to capture print output.
        mock_parse_args.return_value = argparse.Namespace(
            mode="encrypt",
            message="Secret",
            key=1
        )
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), 'Encrypted message: "Tfdsfu"')

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decrypt(self, mock_parse_args, mock_stdout):
        # Mock rationale: Similar to test_main_encrypt, this mocks argparse and stdout
        # to test the decryption path of the main function's CLI behavior.
        mock_parse_args.return_value = argparse.Namespace(
            mode="decrypt",
            message="Tfdsfu",
            key=1
        )
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), 'Decrypted message: "Secret"')

if __name__ == '__main__':
    unittest.main()
