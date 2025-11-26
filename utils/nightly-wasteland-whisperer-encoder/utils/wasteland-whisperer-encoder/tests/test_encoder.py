import unittest
import sys
import io
from unittest.mock import patch
from src.encoder import caesar_cipher, main

class TestCaesarCipher(unittest.TestCase):

    def test_encode_basic(self):
        self.assertEqual(caesar_cipher("abc", 1), "bcd")
        self.assertEqual(caesar_cipher("xyz", 1), "yza") # Wrap around
        self.assertEqual(caesar_cipher("Hello", 3), "KHOOR")
        self.assertEqual(caesar_cipher("World", 5), "BwRLD") # Mixed case, different shift

    def test_decode_basic(self):
        self.assertEqual(caesar_cipher("bcd", 1, encode=False), "abc")
        self.assertEqual(caesar_cipher("yza", 1, encode=False), "xyz")
        self.assertEqual(caesar_cipher("KHOOR", 3, encode=False), "HELLO")
        self.assertEqual(caesar_cipher("BwRLD", 5, encode=False), "WORLD")

    def test_non_alphabetic_characters(self):
        self.assertEqual(caesar_cipher("Hello, World! 123", 3), "KHOOR, ZRUOG! 123")
        self.assertEqual(caesar_cipher("KHOOR, ZRUOG! 123", 3, encode=False), "HELLO, WORLD! 123")
        self.assertEqual(caesar_cipher("!@#$%^&*()", 5), "!@#$%^&*()")

    def test_zero_shift(self):
        self.assertEqual(caesar_cipher("Test Message", 0), "Test Message")
        self.assertEqual(caesar_cipher("Test Message", 0, encode=False), "Test Message")

    def test_large_shift(self):
        self.assertEqual(caesar_cipher("abc", 27), "bcd") # Shift 27 is same as shift 1
        self.assertEqual(caesar_cipher("abc", -1), "zab") # Negative shift
        self.assertEqual(caesar_cipher("abc", -27), "zab") # Negative large shift

    def test_mixed_case(self):
        self.assertEqual(caesar_cipher("aBcDeFg", 1), "bCdEfGh")
        self.assertEqual(caesar_cipher("bCdEfGh", 1, encode=False), "aBcDeFg")

class TestMainCLI(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encode_default_shift(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: We need to simulate command-line arguments without actually
        # running the script from the command line. Patching parse_args allows us
        # to inject specific arguments for testing.
        # Patching sys.stdout and sys.stderr allows us to capture the printed output
        # and error messages for verification.
        mock_parse_args.return_value = argparse.Namespace(
            command="encode",
            message="Hello",
            shift=3
        )
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "KHOOR")
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encode_custom_shift(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Same as above, simulating custom shift argument.
        mock_parse_args.return_value = argparse.Namespace(
            command="encode",
            message="Python",
            shift=5
        )
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "UDWKRQ")
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decode_default_shift(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Same as above, simulating decode command.
        mock_parse_args.return_value = argparse.Namespace(
            command="decode",
            message="KHOOR",
            shift=3
        )
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "HELLO")
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decode_custom_shift(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Same as above, simulating decode with custom shift.
        mock_parse_args.return_value = argparse.Namespace(
            command="decode",
            message="UDWKRQ",
            shift=5
        )
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "PYTHON")
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encode_with_spaces_and_symbols(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Testing encoding with non-alphabetic characters via CLI.
        mock_parse_args.return_value = argparse.Namespace(
            command="encode",
            message="Hello, World! 123",
            shift=3
        )
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "KHOOR, ZRUOG! 123")
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decode_with_spaces_and_symbols(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Testing decoding with non-alphabetic characters via CLI.
        mock_parse_args.return_value = argparse.Namespace(
            command="decode",
            message="KHOOR, ZRUOG! 123",
            shift=3
        )
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "HELLO, WORLD! 123")
        self.assertEqual(mock_stderr.getvalue(), "")
