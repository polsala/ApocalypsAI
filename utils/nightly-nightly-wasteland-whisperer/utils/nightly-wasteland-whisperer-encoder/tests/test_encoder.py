import unittest
import sys
import io
from unittest.mock import patch
from src.encoder import caesar_cipher, main

class TestCaesarCipher(unittest.TestCase):

    def test_encode_basic(self):
        # Test basic encoding with a positive shift
        self.assertEqual(caesar_cipher("abc", 1), "bcd")
        self.assertEqual(caesar_cipher("xyz", 1), "yza") # Wrap around
        self.assertEqual(caesar_cipher("Hello", 3), "Khoor")

    def test_decode_basic(self):
        # Test basic decoding with a positive shift
        self.assertEqual(caesar_cipher("bcd", 1, encode=False), "abc")
        self.assertEqual(caesar_cipher("yza", 1, encode=False), "xyz") # Wrap around
        self.assertEqual(caesar_cipher("Khoor", 3, encode=False), "Hello")

    def test_encode_decode_cycle(self):
        # Test that encoding then decoding returns original text
        original_text = "The quick brown fox jumps over the lazy dog."
        shift = 13 # ROT13
        encoded_text = caesar_cipher(original_text, shift)
        decoded_text = caesar_cipher(encoded_text, shift, encode=False)
        self.assertEqual(decoded_text, original_text)

        original_text = "ApocalypsAI Integrator Agent"
        shift = 5
        encoded_text = caesar_cipher(original_text, shift)
        decoded_text = caesar_cipher(encoded_text, shift, encode=False)
        self.assertEqual(decoded_text, original_text)

    def test_preserve_case(self):
        # Test that case is preserved
        self.assertEqual(caesar_cipher("aBcDeF", 1), "bCdEfG")
        self.assertEqual(caesar_cipher("AbCdEf", 1, encode=False), "ZaBcDe")

    def test_preserve_non_alphabetic(self):
        # Test that non-alphabetic characters are preserved
        self.assertEqual(caesar_cipher("Hello, World! 123", 3), "Khoor, Zruog! 123")
        self.assertEqual(caesar_cipher("!@#$%^&*()", 5), "!@#$%^&*()")
        self.assertEqual(caesar_cipher("12345", 10), "12345")

    def test_zero_shift(self):
        # Test with a zero shift
        self.assertEqual(caesar_cipher("Test", 0), "Test")
        self.assertEqual(caesar_cipher("Test", 0, encode=False), "Test")

class TestMainCLI(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encode(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: We need to simulate command-line arguments and capture stdout/stderr.
        # `argparse.ArgumentParser.parse_args` is mocked to control the arguments passed.
        # `sys.stdout` and `sys.stderr` are mocked to capture the output of the script.
        mock_parse_args.return_value = argparse.Namespace(
            encode=True, decode=False, text="Hello", shift=3
        )
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Khoor")
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decode(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Same as above, simulating CLI arguments and capturing output.
        mock_parse_args.return_value = argparse.Namespace(
            encode=False, decode=True, text="Khoor", shift=3
        )
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello")
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_both_encode_decode_error(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulating an invalid CLI argument combination and checking for error output and exit code.
        # `sys.exit` is mocked to prevent the test runner from exiting.
        mock_parse_args.return_value = argparse.Namespace(
            encode=True, decode=True, text="Test", shift=1
        )
        main()
        self.assertIn("Error: Cannot use both --encode and --decode simultaneously.", mock_stderr.getvalue())
        mock_exit.assert_called_with(1)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_no_encode_decode_error(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Simulating missing required CLI arguments and checking for error output and exit code.
        # `sys.exit` is mocked to prevent the test runner from exiting.
        mock_parse_args.return_value = argparse.Namespace(
            encode=False, decode=False, text="Test", shift=1
        )
        main()
        self.assertIn("Error: Must specify either --encode or --decode.", mock_stderr.getvalue())
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
