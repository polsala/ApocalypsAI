import unittest
import sys
from unittest.mock import patch
from io import StringIO
from src.encoder import caesar_cipher, main

class TestCaesarCipher(unittest.TestCase):

    def test_encode_basic(self):
        self.assertEqual(caesar_cipher("abc", 1, 'encode'), "bcd")
        self.assertEqual(caesar_cipher("xyz", 3, 'encode'), "abc") # Wrap around
        self.assertEqual(caesar_cipher("Hello World", 3, 'encode'), "Khoor Zruog")
        self.assertEqual(caesar_cipher("APOCALYPSE", 5, 'encode'), "FUQBFQDTXJ")

    def test_decode_basic(self):
        self.assertEqual(caesar_cipher("bcd", 1, 'decode'), "abc")
        self.assertEqual(caesar_cipher("abc", 3, 'decode'), "xyz") # Wrap around
        self.assertEqual(caesar_cipher("Khoor Zruog", 3, 'decode'), "Hello World")
        self.assertEqual(caesar_cipher("FUQBFQDTXJ", 5, 'decode'), "APOCALYPSE")

    def test_non_alphabetic_characters(self):
        self.assertEqual(caesar_cipher("Hello, World! 123", 3, 'encode'), "Khoor, Zruog! 123")
        self.assertEqual(caesar_cipher("Khoor, Zruog! 123", 3, 'decode'), "Hello, World! 123")
        self.assertEqual(caesar_cipher("!@#$%^&*()", 5, 'encode'), "!@#$%^&*()")

    def test_zero_shift(self):
        self.assertEqual(caesar_cipher("Test", 0, 'encode'), "Test")
        self.assertEqual(caesar_cipher("Test", 0, 'decode'), "Test")

    def test_large_shift(self):
        self.assertEqual(caesar_cipher("abc", 27, 'encode'), "bcd") # 27 is same as 1
        self.assertEqual(caesar_cipher("abc", -1, 'encode'), "zab") # Negative shift
        self.assertEqual(caesar_cipher("zab", -1, 'decode'), "abc") # Negative shift decode

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encoder.py', '--message', 'test', '--shift', '1', '--mode', 'encode'])
    def test_main_encode(self, mock_stdout):
        # Mock rationale: We need to capture stdout to verify the printed output of the CLI tool
        # and mock sys.argv to simulate command-line arguments without actually running the script from CLI.
        main()
        expected_output = "Original: test\nShift: 1\nMode: encode\nResult: uftu\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encoder.py', '-m', 'uftu', '-s', '1', '-d', 'decode'])
    def test_main_decode(self, mock_stdout):
        # Mock rationale: Same as above, capturing stdout and mocking sys.argv for CLI simulation.
        main()
        expected_output = "Original: uftu\nShift: 1\nMode: decode\nResult: test\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encoder.py', '-m', 'Hello World', '-s', '3']) # Default mode is encode
    def test_main_default_mode(self, mock_stdout):
        # Mock rationale: Same as above, capturing stdout and mocking sys.argv for CLI simulation.
        main()
        expected_output = "Original: Hello World\nShift: 3\nMode: encode\nResult: Khoor Zruog\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['encoder.py', '-m', 'test']) # Missing --shift
    def test_main_missing_required_arg(self, mock_exit, mock_stderr):
        # Mock rationale: We need to mock sys.exit to prevent the test runner from exiting
        # when argparse encounters an error, and capture stderr to check the error message.
        with self.assertRaises(SystemExit): # argparse.parse_args() raises SystemExit on error
            main()
        mock_exit.assert_called_with(2) # argparse exits with 2 on argument error
        self.assertIn("the following arguments are required: --shift/-s", mock_stderr.getvalue())
