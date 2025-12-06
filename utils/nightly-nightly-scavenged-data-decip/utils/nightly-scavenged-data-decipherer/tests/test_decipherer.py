import unittest
import sys
from unittest.mock import patch
from io import StringIO

# Mock rationale: We need to test the command-line interface (CLI) behavior
# which involves reading from sys.argv and writing to sys.stdout. Mocks
# allow us to simulate these interactions deterministically without affecting
# the actual system or requiring user input. For core logic, pure functions
# are tested directly without mocks, ensuring offline and deterministic behavior.

# Add the src directory to the Python path for importing
sys.path.insert(0, 'utils/nightly-scavenged-data-decipherer/src')
import decipherer
sys.path.pop(0)

class TestDecipherer(unittest.TestCase):

    def test_is_base64(self):
        self.assertTrue(decipherer.is_base64("SGVsbG8sIFdvcmxkIQ=="))
        self.assertTrue(decipherer.is_base64("Zm9vYmFy")) # foobar
        self.assertTrue(decipherer.is_base64("SGVsbG8sIFdvcmxkIQ")) # No padding
        self.assertFalse(decipherer.is_base64("not base64"))
        self.assertFalse(decipherer.is_base64("SGVsbG8sIFdvcmxkIQ=")) # Incorrect padding
        self.assertFalse(decipherer.is_base64("SGVsbG8sIFdvcmxkIQ==\n")) # Newline
        self.assertFalse(decipherer.is_base64("SGVsbG8sIFdvcmxkIQ== ")) # Trailing space
        self.assertFalse(decipherer.is_base64("SGVsbG8sIFdvcmxkIQ==A")) # Invalid char
        self.assertFalse(decipherer.is_base64(""))
        self.assertFalse(decipherer.is_base64(None))
        # Test for non-printable characters after decode (should return False)
        self.assertFalse(decipherer.is_base64("AQIDBA==")) # Base64 for binary data (0x01020304)

    def test_decode_base64(self):
        self.assertEqual(decipherer.decode_base64("SGVsbG8sIFdvcmxkIQ=="), "Hello, World!")
        self.assertEqual(decipherer.decode_base64("Zm9vYmFy"), "foobar")
        self.assertEqual(decipherer.decode_base64("SGVsbG8sIFdvcmxkIQ"), "Hello, World!") # No padding
        self.assertIsNone(decipherer.decode_base64("not base64"))
        self.assertIsNone(decipherer.decode_base64("SGVsbG8sIFdvcmxkIQ="))

    def test_is_url_encoded(self):
        self.assertTrue(decipherer.is_url_encoded("Hello%2C%20World%21"))
        self.assertTrue(decipherer.is_url_encoded("foo%20bar"))
        self.assertTrue(decipherer.is_url_encoded("test%2Fpath")) # Contains a slash
        self.assertFalse(decipherer.is_url_encoded("not url encoded"))
        self.assertFalse(decipherer.is_url_encoded("%")) # Not enough chars after %
        self.assertFalse(decipherer.is_url_encoded("Hello% World!")) # Invalid hex after %
        self.assertFalse(decipherer.is_url_encoded(""))
        self.assertFalse(decipherer.is_url_encoded(None))

    def test_decode_url_encoded(self):
        self.assertEqual(decipherer.decode_url_encoded("Hello%2C%20World%21"), "Hello, World!")
        self.assertEqual(decipherer.decode_url_encoded("foo%20bar"), "foo bar")
        self.assertEqual(decipherer.decode_url_encoded("test%2Fpath"), "test/path")
        self.assertIsNone(decipherer.decode_url_encoded("not url encoded"))

    def test_is_hex(self):
        self.assertTrue(decipherer.is_hex("48656c6c6f2c20576f726c6421"))
        self.assertTrue(decipherer.is_hex("666f6f626172")) # foobar
        self.assertTrue(decipherer.is_hex("0123456789abcdefABCDEF"))
        self.assertFalse(decipherer.is_hex("not hex"))
        self.assertFalse(decipherer.is_hex("123")) # Odd length
        self.assertFalse(decipherer.is_hex("123G")) # Invalid hex char
        self.assertFalse(decipherer.is_hex(""))
        self.assertFalse(decipherer.is_hex(None))

    def test_decode_hex(self):
        self.assertEqual(decipherer.decode_hex("48656c6c6f2c20576f726c6421"), "Hello, World!")
        self.assertEqual(decipherer.decode_hex("666f6f626172"), "foobar")
        self.assertIsNone(decipherer.decode_hex("not hex"))
        self.assertIsNone(decipherer.decode_hex("123"))

    def test_decipher_data_base64(self):
        decoded, encoding = decipherer.decipher_data("SGVsbG8sIFdvcmxkIQ==")
        self.assertEqual(decoded, "Hello, World!")
        self.assertEqual(encoding, "Base64")

    def test_decipher_data_url_encoded(self):
        decoded, encoding = decipherer.decipher_data("Hello%2C%20World%21")
        self.assertEqual(decoded, "Hello, World!")
        self.assertEqual(encoding, "URL")

    def test_decipher_data_hex(self):
        decoded, encoding = decipherer.decipher_data("48656c6c6f2c20576f726c6421")
        self.assertEqual(decoded, "Hello, World!")
        self.assertEqual(encoding, "Hex")

    def test_decipher_data_plain_text(self):
        decoded, encoding = decipherer.decipher_data("This is plain text.")
        self.assertEqual(decoded, "This is plain text.")
        self.assertEqual(encoding, "none")

    def test_decipher_data_gibberish(self):
        decoded, encoding = decipherer.decipher_data("Not an encoding, just gibberish!@#")
        self.assertEqual(decoded, "Not an encoding, just gibberish!@#")
        self.assertEqual(encoding, "none")

    def test_decipher_data_empty_string(self):
        decoded, encoding = decipherer.decipher_data("")
        self.assertEqual(decoded, "")
        self.assertEqual(encoding, "none")

    def test_decipher_data_mixed_case_hex(self):
        decoded, encoding = decipherer.decipher_data("48656C6C6F")
        self.assertEqual(decoded, "Hello")
        self.assertEqual(encoding, "Hex")

    def test_decipher_data_url_encoded_false_positive(self):
        # A string that contains '%' but isn't truly URL encoded in a meaningful way
        # The `decipher_data` logic checks if `decoded != input_string` for URL.
        decoded, encoding = decipherer.decipher_data("This is a % test.")
        self.assertEqual(decoded, "This is a % test.")
        self.assertEqual(encoding, "none")

    def test_decipher_data_base64_binary_false_positive(self):
        # Base64 for non-printable binary data, should not be detected as text Base64
        decoded, encoding = decipherer.decipher_data("AQIDBA==")
        self.assertEqual(decoded, "AQIDBA==")
        self.assertEqual(encoding, "none")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['decipherer.py', 'SGVsbG8sIFdvcmxkIQ=='])
    def test_cli_base64(self, mock_stdout):
        decipherer.main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Decoded (Base64): Hello, World!")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['decipherer.py', 'Hello%2C%20World%21'])
    def test_cli_url_encoded(self, mock_stdout):
        decipherer.main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Decoded (URL): Hello, World!")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['decipherer.py', '48656c6c6f2c20576f726c6421'])
    def test_cli_hex(self, mock_stdout):
        decipherer.main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Decoded (Hex): Hello, World!")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['decipherer.py', 'Plain text example.'])
    def test_cli_plain_text(self, mock_stdout):
        decipherer.main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Original: Plain text example.")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['decipherer.py'])
    def test_cli_no_args(self, mock_exit, mock_stderr, mock_stdout):
        decipherer.main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Usage: python src/decipherer.py \"<encoded_string>\"", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
