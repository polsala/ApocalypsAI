import unittest
import sys
from io import StringIO
from unittest.mock import patch
from src.whisperer import encrypt, decrypt, main, _normalize_key

class TestWastelandWhisperer(unittest.TestCase):

    def test_encrypt_decrypt_basic(self):
        key = "LEMON"
        plaintext = "ATTACKATDAWN"
        ciphertext = encrypt(plaintext, key)
        self.assertEqual(ciphertext, "LXFOPVEFRNHR")
        decrypted_text = decrypt(ciphertext, key)
        self.assertEqual(decrypted_text, plaintext)

    def test_encrypt_decrypt_with_spaces_and_punctuation(self):
        key = "SURVIVE"
        plaintext = "Hello, World! This is a secret message."
        ciphertext = encrypt(plaintext, key)
        self.assertEqual(ciphertext, "Pibbu, Xwzld! Tlrs ls a wqfymt qgssagq.")
        decrypted_text = decrypt(ciphertext, key)
        self.assertEqual(decrypted_text, plaintext)

    def test_encrypt_decrypt_case_preservation(self):
        key = "APOCALYPSE"
        plaintext = "Apocalypse Now!"
        ciphertext = encrypt(plaintext, key)
        self.assertEqual(ciphertext, "Apecalypje Nqw!")
        decrypted_text = decrypt(ciphertext, key)
        self.assertEqual(decrypted_text, plaintext)

    def test_empty_message(self):
        key = "KEY"
        plaintext = ""
        ciphertext = encrypt(plaintext, key)
        self.assertEqual(ciphertext, "")
        decrypted_text = decrypt(ciphertext, key)
        self.assertEqual(decrypted_text, "")

    def test_key_with_non_alphabetic_chars(self):
        key = "K3Y!"
        plaintext = "TEST"
        # Mock rationale: _normalize_key is an internal helper, testing its behavior directly.
        self.assertEqual(_normalize_key(key), "KEY")
        ciphertext = encrypt(plaintext, key)
        self.assertEqual(ciphertext, "DIPW") # T+K=D, E+E=I, S+Y=P, T+K=W
        decrypted_text = decrypt(ciphertext, key)
        self.assertEqual(decrypted_text, plaintext)

    def test_short_key_long_message(self):
        key = "A" # Shift 0
        plaintext = "ABCDEF"
        ciphertext = encrypt(plaintext, key)
        self.assertEqual(ciphertext, "ABCDEF")
        decrypted_text = decrypt(ciphertext, key)
        self.assertEqual(decrypted_text, plaintext)

        key = "B" # Shift 1
        plaintext = "ABCDEF"
        ciphertext = encrypt(plaintext, key)
        self.assertEqual(ciphertext, "BCDEFG")
        decrypted_text = decrypt(ciphertext, key)
        self.assertEqual(decrypted_text, plaintext)

    def test_message_with_only_non_alphabetic_chars(self):
        key = "KEY"
        plaintext = "123!@#$"
        ciphertext = encrypt(plaintext, key)
        self.assertEqual(ciphertext, "123!@#$")
        decrypted_text = decrypt(ciphertext, key)
        self.assertEqual(decrypted_text, plaintext)

    def test_key_with_no_alphabetic_chars(self):
        key = "123!@#"
        plaintext = "TEST"
        with self.assertRaisesRegex(ValueError, "Key must contain at least one alphabetic character."):
            encrypt(plaintext, key)
        with self.assertRaisesRegex(ValueError, "Key must contain at least one alphabetic character."):
            decrypt(plaintext, key)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encrypt(self, mock_parse_args, mock_stdout):
        # Mock rationale: Simulate command-line arguments for the main function.
        # This allows testing the CLI interface without actually running it from a shell.
        mock_parse_args.return_value = type('obj', (object,), {
            'mode': 'encrypt',
            'message': 'Hello',
            'key': 'KEY'
        })()
        main()
        self.assertIn("Encrypted message: RIEES", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decrypt(self, mock_parse_args, mock_stdout):
        # Mock rationale: Simulate command-line arguments for the main function.
        mock_parse_args.return_value = type('obj', (object,), {
            'mode': 'decrypt',
            'message': 'RIESS',
            'key': 'KEY'
        })()
        main()
        self.assertIn("Decrypted message: HELLO", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_error_handling(self, mock_parse_args, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments that cause an error (invalid key).
        # Also mock sys.exit to prevent the test runner from exiting, and sys.stderr to capture error output.
        mock_parse_args.return_value = type('obj', (object,), {
            'mode': 'encrypt',
            'message': 'Hello',
            'key': '123' # Invalid key
        })()
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Key must contain at least one alphabetic character.", mock_stderr.getvalue())
