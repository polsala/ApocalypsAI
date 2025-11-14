import unittest
from unittest import mock
import sys
from io import StringIO

# Mock rationale: The utility's core logic is pure functions.
# The main() function interacts with sys.argv and builtins.print.
# Mocking these allows testing the CLI behavior deterministically
# without actual command-line arguments or printing to stdout.

from src.whisperer import _vigenere_transform, encode, decode, main

class TestWastelandWhisperer(unittest.TestCase):

    def test_vigenere_encrypt_basic(self):
        # Test basic encryption with a known plaintext and key
        plaintext = "HELLO"
        key = "KEY"
        expected_ciphertext = "RIJVS"
        self.assertEqual(_vigenere_transform(plaintext, key, encrypt=True), expected_ciphertext)

    def test_vigenere_decrypt_basic(self):
        # Test basic decryption with a known ciphertext and key
        ciphertext = "RIJVS"
        key = "KEY"
        expected_plaintext = "HELLO"
        self.assertEqual(_vigenere_transform(ciphertext, key, encrypt=False), expected_plaintext)

    def test_vigenere_encrypt_with_spaces_and_punctuation(self):
        # Test encryption preserving non-alphabetic characters
        plaintext = "HELLO WORLD, THIS IS A SECRET MESSAGE!"
        key = "SURVIVE"
        expected_ciphertext = "ZYCGW RSJFU, BCMK CJ V AZGJYK UZWKU XZ!"
        self.assertEqual(encode(plaintext, key), expected_ciphertext)

    def test_vigenere_decrypt_with_spaces_and_punctuation(self):
        # Test decryption preserving non-alphabetic characters
        ciphertext = "ZYCGW RSJFU, BCMK CJ V AZGJYK UZWKU XZ!"
        key = "SURVIVE"
        expected_plaintext = "HELLO WORLD, THIS IS A SECRET MESSAGE!"
        self.assertEqual(decode(ciphertext, key), expected_plaintext)

    def test_vigenere_encrypt_lowercase(self):
        # Test encryption with lowercase input, should preserve case
        plaintext = "hello world"
        key = "survive"
        expected_ciphertext = "zycgw rsjfu"
        self.assertEqual(encode(plaintext, key), expected_ciphertext)

    def test_vigenere_decrypt_lowercase(self):
        # Test decryption with lowercase input, should preserve case
        ciphertext = "zycgw rsjfu"
        key = "survive"
        expected_plaintext = "hello world"
        self.assertEqual(decode(ciphertext, key), expected_plaintext)

    def test_vigenere_encrypt_mixed_case(self):
        # Test encryption with mixed case input
        plaintext = "ApocalypsAI"
        key = "NIGHTLY"
        expected_ciphertext = "Nxujtwwcagp"
        self.assertEqual(encode(plaintext, key), expected_ciphertext)

    def test_vigenere_decrypt_mixed_case(self):
        # Test decryption with mixed case input
        ciphertext = "Nxujtwwcagp"
        key = "NIGHTLY"
        expected_plaintext = "ApocalypsAI"
        self.assertEqual(decode(ciphertext, key), expected_plaintext)

    def test_vigenere_empty_message(self):
        # Test with an empty message
        plaintext = ""
        key = "KEY"
        expected_ciphertext = ""
        self.assertEqual(encode(plaintext, key), expected_ciphertext)

    def test_vigenere_message_no_alphabetic(self):
        # Test with a message containing only non-alphabetic characters
        plaintext = "123!@#$ %^&"
        key = "KEY"
        expected_ciphertext = "123!@#$ %^&"
        self.assertEqual(encode(plaintext, key), expected_ciphertext)
        self.assertEqual(decode(expected_ciphertext, key), plaintext)

    def test_vigenere_key_with_non_alphabetic(self):
        # Test with a key containing non-alphabetic characters (should be ignored)
        plaintext = "TEST"
        key = "K3Y!"
        expected_ciphertext = "DILW" # Using "KEY" as key
        self.assertEqual(encode(plaintext, key), expected_ciphertext)
        self.assertEqual(decode(expected_ciphertext, key), plaintext)

    def test_vigenere_empty_key_raises_error(self):
        # Test that an empty key raises a ValueError
        with self.assertRaisesRegex(ValueError, "Key cannot be empty."):
            encode("TEST", "")

    def test_vigenere_non_alphabetic_key_raises_error(self):
        # Test that a key with no alphabetic characters raises a ValueError
        with self.assertRaisesRegex(ValueError, "Key must contain at least one alphabetic character."):
            encode("TEST", "123!@#")

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv', ['whisperer.py', 'encode', 'Hello', 'KEY'])
    def test_main_encode(self, mock_stdout):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments.
        # sys.stdout is mocked to capture the printed output for assertion.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "RIJVS")

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.argv', ['whisperer.py', 'decode', 'RIJVS', 'KEY'])
    def test_main_decode(self, mock_stdout):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments.
        # sys.stdout is mocked to capture the printed output for assertion.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "HELLO")

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.stderr', new_callable=StringIO) # Capture stderr for error messages
    @mock.patch('sys.exit')
    @mock.patch('sys.argv', ['whisperer.py', 'invalid_command', 'message', 'key'])
    def test_main_invalid_command(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments.
        # sys.stdout and sys.stderr are mocked to capture printed output.
        # sys.exit is mocked to prevent the test runner from exiting prematurely.
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Unknown command 'invalid_command'.", mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.stderr', new_callable=StringIO)
    @mock.patch('sys.exit')
    @mock.patch('sys.argv', ['whisperer.py', 'encode', 'message']) # Missing key
    def test_main_missing_arguments(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments.
        # sys.stdout and sys.stderr are mocked to capture printed output.
        # sys.exit is mocked to prevent the test runner from exiting prematurely.
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Usage: python src/whisperer.py <encode|decode> <message> <key>", mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('sys.stderr', new_callable=StringIO)
    @mock.patch('sys.exit')
    @mock.patch('sys.argv', ['whisperer.py', 'encode', 'message', '']) # Empty key
    def test_main_empty_key_error(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: sys.argv is mocked to simulate command-line arguments.
        # sys.stdout and sys.stderr are mocked to capture printed output.
        # sys.exit is mocked to prevent the test runner from exiting prematurely.
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Key cannot be empty.", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
