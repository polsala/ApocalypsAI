import unittest
import sys
from unittest.mock import patch
from io import StringIO
import base64
import urllib.parse
import codecs

# Mock rationale: We need to capture stdout to verify the script's output
# when run as a CLI tool, and mock sys.argv to pass arguments programmatically.
# No external network calls or file system operations are involved, so standard
# library mocks are sufficient for deterministic, offline testing.

# Add 'src' to sys.path to allow importing the decryptor module
sys.path.insert(0, 'utils/nightly-data-debris-decryptor/src')
from decryptor import try_decode, main

class TestDataDebrisDecryptor(unittest.TestCase):

    def test_try_decode_base64(self):
        encoded = base64.b64encode(b"Hello, ApocalypsAI!").decode('utf-8')
        decoded, method = try_decode(encoded)
        self.assertEqual(decoded, "Hello, ApocalypsAI!")
        self.assertEqual(method, "Base64")

    def test_try_decode_url_encoded(self):
        encoded = urllib.parse.quote("Data with spaces & symbols!")
        decoded, method = try_decode(encoded)
        self.assertEqual(decoded, "Data with spaces & symbols!")
        self.assertEqual(method, "URL-decode")

    def test_try_decode_rot13(self):
        encoded = codecs.encode("The quick brown fox jumps over the lazy dog.", 'rot13')
        decoded, method = try_decode(encoded)
        self.assertEqual(decoded, "The quick brown fox jumps over the lazy dog.")
        self.assertEqual(method, "ROT13")

    def test_try_decode_multiple_encodings_base64_first(self):
        # Base64 should be tried before URL-decode
        original = "Secret message!"
        encoded_b64 = base64.b64encode(original.encode('utf-8')).decode('utf-8')
        decoded, method = try_decode(encoded_b64)
        self.assertEqual(decoded, original)
        self.assertEqual(method, "Base64")

    def test_try_decode_multiple_encodings_url_first(self):
        # If Base64 fails, URL-decode should be tried
        original = "http://example.com/?q=test%20query"
        decoded, method = try_decode(original)
        self.assertEqual(decoded, "http://example.com/?q=test query")
        self.assertEqual(method, "URL-decode")

    def test_try_decode_no_match(self):
        original = "This is plain text with no special encoding."
        result = try_decode(original)
        self.assertIsNone(result)

    def test_try_decode_invalid_base64(self):
        # Malformed Base64 that might look like something else
        original = "SGVsbG8h" # Valid Base64
        self.assertIsNotNone(try_decode(original))

        invalid_b64 = "SGVsbG8h===" # Extra padding, but b64decode handles it
        decoded, method = try_decode(invalid_b64)
        self.assertEqual(decoded, "Hello!")
        self.assertEqual(method, "Base64")

        non_b64_chars = "SGVsbG8h!" # Invalid char, should not be decoded by Base64
        result = try_decode(non_b64_chars)
        self.assertIsNone(result)

    def test_main_base64_output(self):
        encoded = base64.b64encode(b"CLI Test Message").decode('utf-8')
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            with patch('sys.argv', ['decryptor.py', encoded]):
                main()
                output = fake_stdout.getvalue()
                self.assertIn("Successfully decrypted using Base64:", output)
                self.assertIn("CLI Test Message", output)

    def test_main_url_encoded_output(self):
        encoded = urllib.parse.quote("CLI Test Message with spaces")
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            with patch('sys.argv', ['decryptor.py', encoded]):
                main()
                output = fake_stdout.getvalue()
                self.assertIn("Successfully decrypted using URL-decode:", output)
                self.assertIn("CLI Test Message with spaces", output)

    def test_main_rot13_output(self):
        encoded = codecs.encode("CLI Rot13 Message", 'rot13')
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            with patch('sys.argv', ['decryptor.py', encoded]):
                main()
                output = fake_stdout.getvalue()
                self.assertIn("Successfully decrypted using ROT13:", output)
                self.assertIn("CLI Rot13 Message", output)

    def test_main_no_match_output(self):
        original = "Plain text for CLI"
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            with patch('sys.argv', ['decryptor.py', original]):
                main()
                output = fake_stdout.getvalue()
                self.assertIn("Could not decrypt using known methods. Original string:", output)
                self.assertIn("Plain text for CLI", output)

    def test_main_no_arguments(self):
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            with patch('sys.stderr', new=StringIO()) as fake_stderr:
                with patch('sys.exit') as mock_exit:
                    with patch('sys.argv', ['decryptor.py']): # No arguments provided
                        main()
                        mock_exit.assert_called_with(1)
                        output = fake_stdout.getvalue()
                        self.assertIn("Usage: python decryptor.py <data_string>", output)
