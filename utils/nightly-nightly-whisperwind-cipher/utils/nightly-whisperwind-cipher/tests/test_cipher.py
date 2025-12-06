import unittest
import sys
from unittest.mock import patch
from io import StringIO

# Mock rationale: We need to import the cipher functions directly for unit testing
# without running the command-line interface. For CLI tests, we mock sys.argv
# and sys.stdout/stderr to capture output and prevent actual program exit.
from utils.nightly_whisperwind_cipher.src.cipher import encrypt, decrypt, validate_key, ALPHABET, DEFAULT_KEY, main

class TestCipherFunctions(unittest.TestCase):

    def test_validate_key_valid(self):
        self.assertIsNone(validate_key(DEFAULT_KEY))
        self.assertIsNone(validate_key(ALPHABET)) # Identity key

    def test_validate_key_invalid_length(self):
        with self.assertRaisesRegex(ValueError, "Key must be a 26-character string."):
            validate_key("SHORT")
        with self.assertRaisesRegex(ValueError, "Key must be a 26-character string."):
            validate_key("LONGERTHAN26CHARACTERSABCDEF")

    def test_validate_key_invalid_case(self):
        with self.assertRaisesRegex(ValueError, "Key must contain only uppercase letters."):
            validate_key("xpmgtdhlyonzweqjruvicakfb") # Lowercase
        with self.assertRaisesRegex(ValueError, "Key must contain only uppercase letters."):
            validate_key("XPMGTDHLYONZWEQJRUVICSAKFB!") # Contains symbol

    def test_validate_key_duplicate_chars(self):
        with self.assertRaisesRegex(ValueError, "Key must contain 26 unique uppercase letters."):
            validate_key("AAAAAAAAAAAAAAAAAAAAAAAAAA") # All A's
        with self.assertRaisesRegex(ValueError, "Key must contain 26 unique uppercase letters."):
            validate_key("AABBCDEFGHIJKLMNOPQRSTUVWXYZ") # Duplicate A, B

    def test_encrypt_decrypt_roundtrip_default_key(self):
        plaintext = "Hello, wasteland! This is a secret message 123."
        ciphertext = encrypt(plaintext, DEFAULT_KEY)
        self.assertEqual(ciphertext, "TGUUX, PXCGUFXCP! HTHF HF G FQOQQT MQFFGZQ 123.")
        decrypted_text = decrypt(ciphertext, DEFAULT_KEY)
        self.assertEqual(decrypted_text, "HELLO, WASTELAND! THIS IS A SECRET MESSAGE 123.")

    def test_encrypt_decrypt_roundtrip_custom_key(self):
        custom_key = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
        plaintext = "Attack at dawn!"
        ciphertext = encrypt(plaintext, custom_key)
        self.assertEqual(ciphertext, "ZGGZXP ZG WZDM!")
        decrypted_text = decrypt(ciphertext, custom_key)
        self.assertEqual(decrypted_text, "ATTACK AT DAWN!")

    def test_encrypt_empty_string(self):
        self.assertEqual(encrypt("", DEFAULT_KEY), "")

    def test_decrypt_empty_string(self):
        self.assertEqual(decrypt("", DEFAULT_KEY), "")

    def test_encrypt_non_alphabetic_chars(self):
        text = "123 !@#$"
        self.assertEqual(encrypt(text, DEFAULT_KEY), "123 !@#$")

    def test_decrypt_non_alphabetic_chars(self):
        text = "123 !@#$"
        self.assertEqual(decrypt(text, DEFAULT_KEY), "123 !@#$")

    def test_encrypt_case_insensitivity(self):
        plaintext = "hello world"
        ciphertext = encrypt(plaintext, DEFAULT_KEY)
        self.assertEqual(ciphertext, "TGUUX DXJUM")

    def test_decrypt_case_insensitivity(self):
        ciphertext = "TGUUX DXJUM"
        plaintext = decrypt(ciphertext, DEFAULT_KEY)
        self.assertEqual(plaintext, "HELLO WORLD")

class TestCipherCLI(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.argv', ['cipher.py', '--encrypt', '--text', 'Test message'])
    def test_cli_encrypt_default_key(self, mock_stderr, mock_stdout):
        # Mock rationale: We mock sys.stdout to capture the printed output
        # and sys.argv to simulate command-line arguments without actual user input.
        # sys.stderr is mocked to ensure no errors are printed unexpectedly.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), 'TQFH MQFFGZQ')
        self.assertEqual(mock_stderr.getvalue(), '')

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.argv', ['cipher.py', '--decrypt', '--text', 'TQFH MQFFGZQ'])
    def test_cli_decrypt_default_key(self, mock_stderr, mock_stdout):
        # Mock rationale: Same as above, for decrypting via CLI.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), 'TEST MESSAGE')
        self.assertEqual(mock_stderr.getvalue(), '')

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.argv', ['cipher.py', '--encrypt', '--text', 'Hello', '--key', 'ZYXWVUTSRQPONMLKJIHGFEDCBA'])
    def test_cli_encrypt_custom_key(self, mock_stderr, mock_stdout):
        # Mock rationale: Testing custom key usage via CLI.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), 'SVOOL')
        self.assertEqual(mock_stderr.getvalue(), '')

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.argv', ['cipher.py', '--decrypt', '--text', 'SVOOL', '--key', 'ZYXWVUTSRQPONMLKJIHGFEDCBA'])
    def test_cli_decrypt_custom_key(self, mock_stderr, mock_stdout):
        # Mock rationale: Testing custom key decryption via CLI.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), 'HELLO')
        self.assertEqual(mock_stderr.getvalue(), '')

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.argv', ['cipher.py', '--text', 'No operation'])
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    def test_cli_no_operation_specified(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: Testing error handling when no --encrypt or --decrypt is given.
        # sys.exit is mocked to prevent the test runner from exiting.
        main()
        self.assertIn('error: Please specify either --encrypt or --decrypt.', mock_stderr.getvalue())
        mock_exit.assert_called_with(2) # argparse exits with 2 for usage errors

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.argv', ['cipher.py', '--encrypt', '--decrypt', '--text', 'Both ops'])
    @patch('sys.exit')
    def test_cli_both_operations_specified(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: Testing error handling when both --encrypt and --decrypt are given.
        main()
        self.assertIn('error: Cannot specify both --encrypt and --decrypt.', mock_stderr.getvalue())
        mock_exit.assert_called_with(2)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.argv', ['cipher.py', '--encrypt', '--text', 'Invalid', '--key', 'BADKEY'])
    @patch('sys.exit')
    def test_cli_invalid_key_error(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: Testing error handling for invalid key provided via CLI.
        main()
        self.assertIn('Error: Key must be a 26-character string.', mock_stderr.getvalue())
        mock_exit.assert_called_with(1)
