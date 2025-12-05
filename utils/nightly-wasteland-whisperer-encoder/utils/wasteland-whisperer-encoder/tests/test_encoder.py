import unittest
import sys
from io import StringIO
from unittest.mock import patch

# Import the functions from the encoder module
from src.encoder import encode, decode, main

class TestWastelandWhispererEncoder(unittest.TestCase):

    def test_encode_lowercase(self):
        self.assertEqual(encode("hello"), "uryyb")

    def test_decode_lowercase(self):
        self.assertEqual(decode("uryyb"), "hello")

    def test_encode_uppercase(self):
        self.assertEqual(encode("WORLD"), "JBEQW")

    def test_decode_uppercase(self):
        self.assertEqual(decode("JBEQW"), "WORLD")

    def test_encode_mixed_case(self):
        self.assertEqual(encode("Hello World"), "Uryyb JBEQW")

    def test_decode_mixed_case(self):
        self.assertEqual(decode("Uryyb JBEQW"), "Hello World")

    def test_encode_numbers(self):
        # Based on ALPHABET_ORIGINAL = "...0123456789" (indices 52-61)
        # and ALPHABET_CIPHER = "...0123456789abcdefghijklm" (indices 52-61 are 'd' through 'm')
        # So, 0 -> d, 1 -> e, ..., 9 -> m
        self.assertEqual(encode("0123456789"), "defghijklm")

    def test_decode_numbers(self):
        self.assertEqual(decode("defghijklm"), "0123456789")

    def test_encode_mixed_alphanumeric(self):
        self.assertEqual(encode("Secret Message 123"), "Frperg Zrffntr def")

    def test_decode_mixed_alphanumeric(self):
        self.assertEqual(decode("Frperg Zrffntr def"), "Secret Message 123")

    def test_encode_special_characters(self):
        # Special characters should pass through unchanged
        self.assertEqual(encode("!@#$%^&*()_+-=,./<>?;':"[]\\|`~ "), "!@#$%^&*()_+-=,./<>?;':"[]\\|`~ ")

    def test_decode_special_characters(self):
        self.assertEqual(decode("!@#$%^&*()_+-=,./<>?;':"[]\\|`~ "), "!@#$%^&*()_+-=,./<>?;':"[]\\|`~ ")

    def test_encode_empty_string(self):
        self.assertEqual(encode(""), "")

    def test_decode_empty_string(self):
        self.assertEqual(decode(""), "")

    def test_round_trip(self):
        original_message = "The quick brown fox jumps over the lazy dog 12345!"
        encoded = encode(original_message)
        decoded = decode(encoded)
        self.assertEqual(decoded, original_message)

        original_message_2 = "ApocalypsAI Integrator Agent 2024"
        encoded_2 = encode(original_message_2)
        decoded_2 = decode(encoded_2)
        self.assertEqual(decoded_2, original_message_2)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encoder.py', '--encode', 'Secret message 123'])
    def test_main_encode_cli(self, mock_stdout):
        # Mock rationale: We need to simulate command-line arguments and capture stdout
        # without actually running the script in a separate process or affecting the global sys.argv.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Frperg zrffntr def")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encoder.py', '--decode', 'Frperg zrffntr def'])
    def test_main_decode_cli(self, mock_stdout):
        # Mock rationale: Same as above, simulating CLI decode operation.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Secret message 123")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encoder.py'])
    def test_main_no_args_cli(self, mock_stdout):
        # Mock rationale: Simulate running the script without arguments to check help output.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0) # argparse exits with 0 for help
        self.assertIn("usage: encoder.py", mock_stdout.getvalue())
        self.assertIn("Wasteland Whisperer Encoder", mock_stdout.getvalue())
