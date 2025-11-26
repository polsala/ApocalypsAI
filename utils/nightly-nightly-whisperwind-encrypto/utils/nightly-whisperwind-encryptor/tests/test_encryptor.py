import unittest
from unittest.mock import patch
import io
import argparse
import sys
import os

# Add the src directory to the Python path to allow importing encryptor.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from encryptor import vigenere_encrypt, vigenere_decrypt, main

class TestWhisperwindEncryptor(unittest.TestCase):

    def test_vigenere_encrypt_basic(self):
        message = "ATTACKATDAWN"
        key = "LEMON"
        expected = "LXFOPVEFRNHR"
        self.assertEqual(vigenere_encrypt(message, key), expected)

    def test_vigenere_decrypt_basic(self):
        ciphertext = "LXFOPVEFRNHR"
        key = "LEMON"
        expected = "ATTACKATDAWN"
        self.assertEqual(vigenere_decrypt(ciphertext, key), expected)

    def test_vigenere_encrypt_decrypt_cycle(self):
        message = "The quick brown fox jumps over the lazy dog."
        key = "SECRETKEY"
        encrypted = vigenere_encrypt(message, key)
        decrypted = vigenere_decrypt(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_vigenere_with_spaces_and_punctuation(self):
        message = "Hello, World! 123. How are you?"
        key = "ALPHA"
        encrypted = vigenere_encrypt(message, key)
        decrypted = vigenere_decrypt(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_vigenere_case_preservation(self):
        message = "ApocalypsAI"
        key = "NIGHTLY"
        encrypted = vigenere_encrypt(message, key)
        # Expected: NxujtwxbaGP (calculated manually for verification)
        self.assertEqual(encrypted, "NxujtwxbaGP")
        decrypted = vigenere_decrypt(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_empty_message(self):
        message = ""
        key = "KEY"
        self.assertEqual(vigenere_encrypt(message, key), "")
        self.assertEqual(vigenere_decrypt(message, key), "")

    def test_key_with_non_alpha_chars(self):
        message = "TEST"
        key = "K-E-Y!"
        # Only 'K', 'E', 'Y' should be used from the key
        encrypted = vigenere_encrypt(message, key)
        decrypted = vigenere_decrypt(encrypted, key)
        self.assertEqual(decrypted, message)

    def test_key_with_no_alpha_chars_raises_error(self):
        message = "TEST"
        key = "123!@#"
        with self.assertRaisesRegex(ValueError, "Key must contain at least one alphabetic character."):
            vigenere_encrypt(message, key)
        with self.assertRaisesRegex(ValueError, "Key must contain at least one alphabetic character."):
            vigenere_decrypt(message, key)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encrypt_output(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: We need to simulate command-line arguments without actually running the CLI.
        # argparse.ArgumentParser.parse_args is mocked to return a Namespace object with predefined arguments.
        # sys.stdout is mocked to capture the print output for assertion.
        # sys.stderr is mocked to capture error output, though not expected in this success case.
        mock_parse_args.return_value = argparse.Namespace(
            mode='encrypt',
            text='SECRET',
            key='KEY'
        )
        main()
        self.assertIn("Whisperwind Encrypted: SGCVET", mock_stdout.getvalue().strip())
        self.assertEqual(mock_stderr.getvalue(), "") # No error output

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decrypt_output(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Same as above, but for decryption mode.
        mock_parse_args.return_value = argparse.Namespace(
            mode='decrypt',
            text='SGCVET', # Encrypted 'SECRET' with 'KEY'
            key='KEY'
        )
        main()
        self.assertIn("Whisperwind Decrypted: SECRET", mock_stdout.getvalue().strip())
        self.assertEqual(mock_stderr.getvalue(), "") # No error output

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    def test_main_error_handling(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate an invalid key to trigger the ValueError.
        # sys.exit is mocked to prevent the test runner from terminating.
        # sys.stderr is mocked to capture the error message.
        mock_parse_args.return_value = argparse.Namespace(
            mode='encrypt',
            text='TEST',
            key='123'
        )
        main()
        self.assertIn("Error: Key must contain at least one alphabetic character.", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)
        self.assertEqual(mock_stdout.getvalue(), "") # No stdout output on error
