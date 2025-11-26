import unittest
from unittest.mock import patch
import sys
import io
from src.cipher_scribe import create_cipher_map, transform_message, DEFAULT_ALPHABET, DEFAULT_KEY, main

class TestCipherScribe(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Ensure consistent alphabet and key for all tests.
        # These are internal constants, so direct use is fine, but if they were
        # loaded from a file or env var, mocking would be essential.
        self.alphabet = DEFAULT_ALPHABET
        self.key = DEFAULT_KEY
        self.encrypt_map, self.decrypt_map = create_cipher_map(self.alphabet, self.key)

    def test_create_cipher_map_valid(self):
        # Test with default valid alphabet and key
        enc_map, dec_map = create_cipher_map(self.alphabet, self.key)
        self.assertIsInstance(enc_map, dict)
        self.assertIsInstance(dec_map, dict)
        self.assertEqual(len(enc_map), len(self.alphabet))
        self.assertEqual(len(dec_map), len(self.key))
        # Test a specific mapping
        self.assertEqual(enc_map['A'], self.key[self.alphabet.index('A')])
        self.assertEqual(dec_map[self.key[self.alphabet.index('A')]], 'A')

        # Test with a custom valid alphabet and key
        custom_alphabet = "abc"
        custom_key = "bca"
        enc_map_custom, dec_map_custom = create_cipher_map(custom_alphabet, custom_key)
        self.assertEqual(enc_map_custom['a'], 'b')
        self.assertEqual(dec_map_custom['b'], 'a')

    def test_create_cipher_map_invalid_length(self):
        # Mock rationale: Testing error handling for invalid inputs.
        with self.assertRaisesRegex(ValueError, "Alphabet and key must be of the same length."):
            create_cipher_map("abc", "ab")

    def test_create_cipher_map_duplicate_alphabet(self):
        # Mock rationale: Testing error handling for invalid inputs.
        with self.assertRaisesRegex(ValueError, "Alphabet contains duplicate characters."):
            create_cipher_map("aab", "bca")

    def test_create_cipher_map_duplicate_key(self):
        # Mock rationale: Testing error handling for invalid inputs.
        with self.assertRaisesRegex(ValueError, "Key contains duplicate characters."):
            create_cipher_map("abc", "bbc")

    def test_transform_message_encrypt(self):
        message = "Hello, World!"
        expected_encrypted = "Uqppc, 8crpd!"
        # Mock rationale: Using pre-computed maps for deterministic transformation.
        self.assertEqual(transform_message(message, self.encrypt_map), expected_encrypted)

        message_with_unknown_char = "Hello, World! @"
        expected_encrypted_with_unknown = "Uqppc, 8crpd! @" # '@' is not in default alphabet, so it remains unchanged
        self.assertEqual(transform_message(message_with_unknown_char, self.encrypt_map), expected_encrypted_with_unknown)

        self.assertEqual(transform_message("", self.encrypt_map), "")

    def test_transform_message_decrypt(self):
        encrypted_message = "Uqppc, 8crpd!"
        expected_decrypted = "Hello, World!"
        # Mock rationale: Using pre-computed maps for deterministic transformation.
        self.assertEqual(transform_message(encrypted_message, self.decrypt_map), expected_decrypted)

        encrypted_with_unknown_char = "Uqppc, 8crpd! @"
        expected_decrypted_with_unknown = "Hello, World! @"
        self.assertEqual(transform_message(encrypted_with_unknown_char, self.decrypt_map), expected_decrypted_with_unknown)

        self.assertEqual(transform_message("", self.decrypt_map), "")

    def test_round_trip(self):
        original_message = "The quick brown fox jumps over the lazy dog 12345!"
        # Mock rationale: Verifying that encryption followed by decryption restores the original message.
        encrypted = transform_message(original_message, self.encrypt_map)
        decrypted = transform_message(encrypted, self.decrypt_map)
        self.assertEqual(decrypted, original_message)

        original_message_with_all_chars = self.alphabet # Test all characters in the alphabet
        encrypted_all = transform_message(original_message_with_all_chars, self.encrypt_map)
        decrypted_all = transform_message(encrypted_all, self.decrypt_map)
        self.assertEqual(decrypted_all, original_message_with_all_chars)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encrypt(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments and capture stdout/stderr for verification.
        mock_parse_args.return_value = argparse.Namespace(
            encrypt=True, decrypt=False, message="Test message", alphabet=DEFAULT_ALPHABET, key=DEFAULT_KEY
        )
        main()
        self.assertIn("Encrypted message: ", mock_stdout.getvalue())
        self.assertNotIn("Error", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decrypt(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments and capture stdout/stderr for verification.
        mock_parse_args.return_value = argparse.Namespace(
            encrypt=False, decrypt=True, message="Xq00 Fq000uq", alphabet=DEFAULT_ALPHABET, key=DEFAULT_KEY
        )
        main()
        self.assertIn("Decrypted message: ", mock_stdout.getvalue())
        self.assertNotIn("Error", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_action(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments to test error handling for missing --encrypt/--decrypt.
        mock_parse_args.return_value = argparse.Namespace(
            encrypt=False, decrypt=False, message="Test message", alphabet=DEFAULT_ALPHABET, key=DEFAULT_KEY
        )
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2) # argparse exits with 2 for argument errors
        self.assertIn("error: Please specify either --encrypt or --decrypt.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_both_actions(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments to test error handling for both --encrypt and --decrypt.
        mock_parse_args.return_value = argparse.Namespace(
            encrypt=True, decrypt=True, message="Test message", alphabet=DEFAULT_ALPHABET, key=DEFAULT_KEY
        )
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2)
        self.assertIn("error: Cannot specify both --encrypt and --decrypt.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_cipher_map(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulate command-line arguments with an invalid key to test error handling.
        mock_parse_args.return_value = argparse.Namespace(
            encrypt=True, decrypt=False, message="Test", alphabet="abc", key="ab"
        )
        main()
        self.assertIn("Error creating cipher maps: Alphabet and key must be of the same length.", mock_stdout.getvalue())
        self.assertNotIn("error", mock_stderr.getvalue()) # Error is caught and printed, not an argparse error

if __name__ == '__main__':
    unittest.main()
