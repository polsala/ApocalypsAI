import unittest
from unittest.mock import patch
import sys
import io
from src.encryptor import caesar_cipher, main

class TestCaesarCipher(unittest.TestCase):

    def test_encrypt_basic(self):
        # Test basic encryption with a positive shift
        self.assertEqual(caesar_cipher("abc", 1, 'encrypt'), "bcd")
        self.assertEqual(caesar_cipher("xyz", 1, 'encrypt'), "yza")
        self.assertEqual(caesar_cipher("Hello", 3, 'encrypt'), "Khoor")
        self.assertEqual(caesar_cipher("ApocalypsAI", 5, 'encrypt'), "FubnfqbmxFI")

    def test_decrypt_basic(self):
        # Test basic decryption with a positive shift
        self.assertEqual(caesar_cipher("bcd", 1, 'decrypt'), "abc")
        self.assertEqual(caesar_cipher("yza", 1, 'decrypt'), "xyz")
        self.assertEqual(caesar_cipher("Khoor", 3, 'decrypt'), "Hello")
        self.assertEqual(caesar_cipher("FubnfqbmxFI", 5, 'decrypt'), "ApocalypsAI")

    def test_encrypt_negative_shift(self):
        # Test encryption with a negative shift (shifts left)
        self.assertEqual(caesar_cipher("abc", -1, 'encrypt'), "zab")
        self.assertEqual(caesar_cipher("bcd", -3, 'encrypt'), "yza")
        self.assertEqual(caesar_cipher("Hello", -3, 'encrypt'), "Ebiil")

    def test_decrypt_negative_shift(self):
        # Test decryption with a negative shift
        self.assertEqual(caesar_cipher("zab", -1, 'decrypt'), "abc")
        self.assertEqual(caesar_cipher("yza", -3, 'decrypt'), "bcd")
        self.assertEqual(caesar_cipher("Ebiil", -3, 'decrypt'), "Hello")

    def test_encrypt_mixed_case(self):
        # Test encryption with mixed case letters
        self.assertEqual(caesar_cipher("AbC", 1, 'encrypt'), "BcD")
        self.assertEqual(caesar_cipher("aBcDeF", 2, 'encrypt'), "cDeFgH")

    def test_decrypt_mixed_case(self):
        # Test decryption with mixed case letters
        self.assertEqual(caesar_cipher("BcD", 1, 'decrypt'), "AbC")
        self.assertEqual(caesar_cipher("cDeFgH", 2, 'decrypt'), "aBcDeF")

    def test_non_alphabetic_characters(self):
        # Test that non-alphabetic characters remain unchanged
        self.assertEqual(caesar_cipher("Hello, World! 123", 3, 'encrypt'), "Khoor, Zruog! 123")
        self.assertEqual(caesar_cipher("Khoor, Zruog! 123", 3, 'decrypt'), "Hello, World! 123")
        self.assertEqual(caesar_cipher("123!@#$", 5, 'encrypt'), "123!@#$")

    def test_large_shift_values(self):
        # Test with large shift values that wrap around multiple times
        self.assertEqual(caesar_cipher("abc", 27, 'encrypt'), "bcd") # 27 % 26 = 1
        self.assertEqual(caesar_cipher("abc", 52, 'encrypt'), "abc") # 52 % 26 = 0
        self.assertEqual(caesar_cipher("abc", -27, 'encrypt'), "zab") # -27 % 26 = -1 (or 25)

    def test_main_encrypt(self):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments
        # sys.stdout is mocked to capture the output of the main function
        test_args = ['encryptor.py', '--message', 'Secret', '--shift', '1', '--mode', 'encrypt']
        with patch('sys.argv', test_args),
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()
            self.assertEqual(mock_stdout.getvalue().strip(), "Tfdsfu")

    def test_main_decrypt(self):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments
        # sys.stdout is mocked to capture the output of the main function
        test_args = ['encryptor.py', '--message', 'Tfdsfu', '--shift', '1', '--mode', 'decrypt']
        with patch('sys.argv', test_args),
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()
            self.assertEqual(mock_stdout.getvalue().strip(), "Secret")

    def test_main_invalid_mode(self):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments
        # sys.stderr and SystemExit are mocked to capture error output and prevent actual program exit
        test_args = ['encryptor.py', '--message', 'Test', '--shift', '1', '--mode', 'invalid']
        with patch('sys.argv', test_args),
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
             self.assertRaises(SystemExit) as cm:
            main()
            self.assertEqual(cm.exception.code, 2) # argparse exits with 2 for invalid arguments
            self.assertIn("argument --mode: invalid choice: 'invalid'", mock_stderr.getvalue())

    def test_main_missing_argument(self):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments
        # sys.stderr and SystemExit are mocked to capture error output and prevent actual program exit
        test_args = ['encryptor.py', '--message', 'Test', '--mode', 'encrypt'] # Missing --shift
        with patch('sys.argv', test_args),
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr,
             self.assertRaises(SystemExit) as cm:
            main()
            self.assertEqual(cm.exception.code, 2)
            self.assertIn("the following arguments are required: --shift", mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
