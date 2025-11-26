import unittest
import sys
import io
from unittest.mock import patch
from src.encoder import xor_cipher, xor_decipher, main

class TestWhisperwindEncoder(unittest.TestCase):

    def test_xor_cipher_basic(self):
        message = "Hello World"
        key = "secret"
        encoded = xor_cipher(message, key)
        self.assertEqual(encoded, "0c1a1f1f1c5c261a191f1d") # Pre-calculated hex output for 'Hello World' with key 'secret'

    def test_xor_decipher_basic(self):
        encoded_hex = "0c1a1f1f1c5c261a191f1d"
        key = "secret"
        decoded = xor_decipher(encoded_hex, key)
        self.assertEqual(decoded, "Hello World")

    def test_xor_cipher_empty_message(self):
        message = ""
        key = "secret"
        encoded = xor_cipher(message, key)
        self.assertEqual(encoded, "")

    def test_xor_decipher_empty_encoded(self):
        encoded_hex = ""
        key = "secret"
        decoded = xor_decipher(encoded_hex, key)
        self.assertEqual(decoded, "")

    def test_xor_cipher_long_message_short_key(self):
        message = "This is a much longer message to test key repetition."
        key = "short"
        encoded = xor_cipher(message, key)
        decoded = xor_decipher(encoded, key)
        self.assertEqual(decoded, message)

    def test_xor_cipher_unicode_characters(self):
        message = "Привет, мир! 👋"
        key = "ключ"
        encoded = xor_cipher(message, key)
        decoded = xor_decipher(encoded, key)
        self.assertEqual(decoded, message)

    def test_xor_cipher_empty_key_raises_error(self):
        message = "test"
        key = ""
        with self.assertRaisesRegex(ValueError, "Key cannot be empty."):
            xor_cipher(message, key)

    def test_xor_decipher_empty_key_raises_error(self):
        encoded_hex = "deadbeef"
        key = ""
        with self.assertRaisesRegex(ValueError, "Key cannot be empty."):
            xor_decipher(encoded_hex, key)

    def test_xor_decipher_invalid_hex_raises_error(self):
        invalid_hex = "not_hex_string"
        key = "secret"
        with self.assertRaisesRegex(ValueError, "Invalid hex string provided for decoding."):
            xor_decipher(invalid_hex, key)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encode(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: We need to simulate command-line arguments and capture stdout/stderr
        # without actually running the script as a separate process or affecting the real console.
        mock_parse_args.return_value = argparse.Namespace(
            mode="encode",
            message="Test Message",
            key="mykey"
        )
        main()
        self.assertIn("Encoded (hex):", mock_stdout.getvalue())
        self.assertIn(xor_cipher("Test Message", "mykey"), mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decode(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Same as above, simulating CLI arguments and capturing output.
        encoded_msg = xor_cipher("Secret Info", "pass")
        mock_parse_args.return_value = argparse.Namespace(
            mode="decode",
            message=encoded_msg,
            key="pass"
        )
        main()
        self.assertIn("Decoded: Secret Info", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_error_handling(self, mock_exit, mock_stderr, mock_stdout, mock_parse_args):
        # Mock rationale: Simulating an invalid input scenario (empty key) and verifying
        # that the script prints an error to stderr and exits with code 1.
        mock_parse_args.return_value = argparse.Namespace(
            mode="encode",
            message="Test",
            key=""
        )
        main()
        self.assertIn("Error: Key cannot be empty.", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
