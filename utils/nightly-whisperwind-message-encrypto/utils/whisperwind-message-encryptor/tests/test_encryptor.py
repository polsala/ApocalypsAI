import unittest
import sys
from unittest.mock import patch
from io import StringIO
from src.encryptor import caesar_cipher, main

class TestCaesarCipher(unittest.TestCase):

    def test_encrypt_simple(self):
        self.assertEqual(caesar_cipher("abc", 1, 'encrypt'), "bcd")
        self.assertEqual(caesar_cipher("xyz", 1, 'encrypt'), "yza") # Wrap around
        self.assertEqual(caesar_cipher("Hello World", 3, 'encrypt'), "Khoor Zruog")
        self.assertEqual(caesar_cipher("ApocalypsAI", 5, 'encrypt'), "FuntbhmxusFI")

    def test_decrypt_simple(self):
        self.assertEqual(caesar_cipher("bcd", 1, 'decrypt'), "abc")
        self.assertEqual(caesar_cipher("yza", 1, 'decrypt'), "xyz")
        self.assertEqual(caesar_cipher("Khoor Zruog", 3, 'decrypt'), "Hello World")
        self.assertEqual(caesar_cipher("FuntbhmxusFI", 5, 'decrypt'), "ApocalypsAI")

    def test_zero_shift(self):
        self.assertEqual(caesar_cipher("test", 0, 'encrypt'), "test")
        self.assertEqual(caesar_cipher("test", 0, 'decrypt'), "test")

    def test_large_shift(self):
        self.assertEqual(caesar_cipher("abc", 27, 'encrypt'), "bcd") # 27 % 26 = 1
        self.assertEqual(caesar_cipher("abc", -25, 'encrypt'), "bcd") # -25 % 26 = 1
        self.assertEqual(caesar_cipher("abc", 52, 'encrypt'), "abc") # 52 % 26 = 0

    def test_non_alphabetic_characters(self):
        self.assertEqual(caesar_cipher("123!@#$", 5, 'encrypt'), "123!@#$")
        self.assertEqual(caesar_cipher("Hello, World! 123", 3, 'encrypt'), "Khoor, Zruog! 123")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encryptor.py', '--text', 'hello', '--shift', '3', '--mode', 'encrypt'])
    def test_main_encrypt(self, mock_stdout):
        # Mock rationale: sys.stdout is mocked to capture the print output of the main function,
        # allowing verification of the CLI utility's result without actual console output.
        # sys.argv is mocked to simulate command-line arguments passed to the script,
        # ensuring the main function processes the intended inputs deterministically.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "khoor")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encryptor.py', '--text', 'khoor', '--shift', '3', '--mode', 'decrypt'])
    def test_main_decrypt(self, mock_stdout):
        # Mock rationale: sys.stdout is mocked to capture the print output of the main function,
        # allowing verification of the CLI utility's result without actual console output.
        # sys.argv is mocked to simulate command-line arguments passed to the script,
        # ensuring the main function processes the intended inputs deterministically.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "hello")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encryptor.py', '--text', 'ApocalypsAI', '--shift', '5']) # Default mode is encrypt
    def test_main_default_mode(self, mock_stdout):
        # Mock rationale: sys.stdout is mocked to capture the print output of the main function,
        # allowing verification of the CLI utility's result without actual console output.
        # sys.argv is mocked to simulate command-line arguments passed to the script,
        # ensuring the main function processes the intended inputs deterministically.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "FuntbhmxusFI")

if __name__ == '__main__':
    unittest.main()
