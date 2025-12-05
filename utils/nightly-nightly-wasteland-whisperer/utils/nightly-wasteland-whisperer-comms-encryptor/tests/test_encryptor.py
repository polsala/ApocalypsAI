import unittest
from unittest.mock import patch
import sys
from io import StringIO
from src.encryptor import caesar_cipher, _calculate_shift, main

class TestEncryptor(unittest.TestCase):

    def test_calculate_shift(self):
        self.assertEqual(_calculate_shift("a"), 97 % 26) # 19
        self.assertEqual(_calculate_shift("z"), 122 % 26) # 18
        self.assertEqual(_calculate_shift("key"), (ord('k') + ord('e') + ord('y')) % 26) # (107+101+121)%26 = 329%26 = 17
        self.assertEqual(_calculate_shift(""), 0)
        self.assertEqual(_calculate_shift("ApocalypsAI"), (ord('A')+ord('p')+ord('o')+ord('c')+ord('a')+ord('l')+ord('y')+ord('p')+ord('s')+ord('A')+ord('I')) % 26) # (65+112+111+99+97+108+121+112+115+65+73)%26 = 1068%26 = 2

    def test_encrypt_decrypt_cycle(self):
        message = "Hello, World! 123"
        key = "secret"
        encrypted = caesar_cipher(message, key, 'encrypt')
        decrypted = caesar_cipher(encrypted, key, 'decrypt')
        self.assertEqual(decrypted, message)

    def test_encrypt_lowercase(self):
        message = "abc"
        key = "a" # shift = 19
        expected = "tuv" # a+19=t, b+19=u, c+19=v
        self.assertEqual(caesar_cipher(message, key, 'encrypt'), expected)

    def test_decrypt_lowercase(self):
        message = "tuv"
        key = "a" # shift = 19
        expected = "abc"
        self.assertEqual(caesar_cipher(message, key, 'decrypt'), expected)

    def test_encrypt_uppercase(self):
        message = "ABC"
        key = "b" # shift = 20
        expected = "UVW" # A+20=U, B+20=V, C+20=W
        self.assertEqual(caesar_cipher(message, key, 'encrypt'), expected)

    def test_decrypt_uppercase(self):
        message = "UVW"
        key = "b" # shift = 20
        expected = "ABC"
        self.assertEqual(caesar_cipher(message, key, 'decrypt'), expected)

    def test_encrypt_mixed_case_and_symbols(self):
        message = "Attack at Dawn! 123"
        key = "night" # shift = (ord('n')+ord('i')+ord('g')+ord('h')+ord('t'))%26 = (110+105+103+104+116)%26 = 538%26 = 18
        expected = "Sllsuk sl Vswo! 123"
        self.assertEqual(caesar_cipher(message, key, 'encrypt'), expected)

    def test_decrypt_mixed_case_and_symbols(self):
        message = "Sllsuk sl Vswo! 123"
        key = "night" # shift = 18
        expected = "Attack at Dawn! 123"
        self.assertEqual(caesar_cipher(message, key, 'decrypt'), expected)

    def test_empty_message(self):
        message = ""
        key = "test"
        self.assertEqual(caesar_cipher(message, key, 'encrypt'), "")
        self.assertEqual(caesar_cipher(message, key, 'decrypt'), "")

    def test_empty_key(self):
        message = "Hello"
        key = "" # shift = 0
        self.assertEqual(caesar_cipher(message, key, 'encrypt'), "Hello")
        self.assertEqual(caesar_cipher(message, key, 'decrypt'), "Hello")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encryptor.py', 'encrypt', 'Secret Message', 'key123'])
    def test_main_encrypt(self, mock_stdout):
        # Mock rationale: We need to capture stdout and simulate command-line arguments
        # to test the main function's CLI behavior without actually running it as a separate process.
        main()
        # shift for 'key123' is 11
        expected_output = caesar_cipher("Secret Message", "key123", 'encrypt') + "\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encryptor.py', 'decrypt', 'Eqodqf Xqddljq', 'key123'])
    def test_main_decrypt(self, mock_stdout):
        # Mock rationale: Same as above, capturing stdout and simulating CLI args.
        main()
        # 'Eqodqf Xqddljq' is 'Secret Message' encrypted with shift 11 (from 'key123')
        expected_output = caesar_cipher("Eqodqf Xqddljq", "key123", 'decrypt') + "\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)
