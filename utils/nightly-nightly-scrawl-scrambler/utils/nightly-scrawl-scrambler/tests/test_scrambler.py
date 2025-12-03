import unittest
from unittest.mock import patch
import io
from src.scrambler import caesar_cipher, main

class TestScrambler(unittest.TestCase):

    def test_encrypt_basic(self):
        # Test basic encryption with a positive shift
        self.assertEqual(caesar_cipher("abc", 1), "bcd")
        self.assertEqual(caesar_cipher("xyz", 1), "yza") # Wrap around
        self.assertEqual(caesar_cipher("Hello World", 3), "Khoor Zruog")

    def test_decrypt_basic(self):
        # Test basic decryption with a positive shift
        self.assertEqual(caesar_cipher("bcd", 1, encrypt=False), "abc")
        self.assertEqual(caesar_cipher("yza", 1, encrypt=False), "xyz") # Wrap around
        self.assertEqual(caesar_cipher("Khoor Zruog", 3, encrypt=False), "Hello World")

    def test_encrypt_zero_shift(self):
        # Test encryption with zero shift (no change)
        self.assertEqual(caesar_cipher("Test", 0), "Test")

    def test_decrypt_zero_shift(self):
        # Test decryption with zero shift (no change)
        self.assertEqual(caesar_cipher("Test", 0, encrypt=False), "Test")

    def test_encrypt_negative_shift(self):
        # Test encryption with a negative shift (effectively decrypts with positive shift)
        self.assertEqual(caesar_cipher("abc", -1), "zab")
        self.assertEqual(caesar_cipher("Hello", -3), "Ebiil")

    def test_decrypt_negative_shift(self):
        # Test decryption with a negative shift (effectively encrypts with positive shift)
        self.assertEqual(caesar_cipher("zab", -1, encrypt=False), "abc")
        self.assertEqual(caesar_cipher("Ebiil", -3, encrypt=False), "Hello")

    def test_non_alphabetic_characters(self):
        # Test that numbers, symbols, and spaces are unchanged
        self.assertEqual(caesar_cipher("123!@# Hello World.", 3), "123!@# Khoor Zruog.")
        self.assertEqual(caesar_cipher("123!@# Khoor Zruog.", 3, encrypt=False), "123!@# Hello World.")

    def test_empty_string(self):
        # Test with an empty string
        self.assertEqual(caesar_cipher("", 5), "")
        self.assertEqual(caesar_cipher("", 5, encrypt=False), "")

    def test_large_shift(self):
        # Test with a shift larger than the alphabet size
        self.assertEqual(caesar_cipher("abc", 27), "bcd") # 27 is equivalent to 1
        self.assertEqual(caesar_cipher("abc", 52), "abc") # 52 is equivalent to 0
        self.assertEqual(caesar_cipher("abc", 27, encrypt=False), "zab") # 27 is equivalent to 1, so decrypts by -1

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encrypt(self, mock_parse_args, mock_stdout):
        # Mock rationale: We need to test the main function's CLI behavior without
        # actually running it as a script or affecting the real sys.argv.
        # Mocking parse_args allows us to simulate command-line arguments.
        # Mocking sys.stdout allows us to capture and assert the printed output.
        mock_parse_args.return_value = type('obj', (object,), {
            'text': 'Hello', 'shift': 3, 'decrypt': False
        })()
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Encrypted: Khoor")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decrypt(self, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, for testing decryption via CLI.
        mock_parse_args.return_value = type('obj', (object,), {
            'text': 'Khoor', 'shift': 3, 'decrypt': True
        })()
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Decrypted: Hello")

if __name__ == '__main__':
    unittest.main()
