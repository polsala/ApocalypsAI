import unittest
import sys
from unittest.mock import patch
from io import StringIO

# Mock rationale: We need to test the command-line interface (CLI) of the encoder.
# This involves capturing stdout and simulating command-line arguments (sys.argv).
# Patching sys.stdout allows us to redirect print statements to a StringIO object
# for verification. Patching sys.argv allows us to provide arguments to argparse
# without actually running the script from the command line.

# Import the main function and the cipher logic from the script
# Assuming the script is in src/encoder.py relative to the test file
try:
    from src.encoder import caesar_cipher, main
except ImportError:
    # Adjust import path for direct execution of tests or different environments
    sys.path.append('src')
    from encoder import caesar_cipher, main


class TestCaesarCipher(unittest.TestCase):

    def test_encode_basic(self):
        self.assertEqual(caesar_cipher("Hello", 3, "encode"), "Khoor")
        self.assertEqual(caesar_cipher("World", 5, "encode"), "Bwrlq")

    def test_decode_basic(self):
        self.assertEqual(caesar_cipher("Khoor", 3, "decode"), "Hello")
        self.assertEqual(caesar_cipher("Bwrlq", 5, "decode"), "World")

    def test_encode_wrap_around(self):
        self.assertEqual(caesar_cipher("Zebra", 3, "encode"), "Cheud")
        self.assertEqual(caesar_cipher("apple", 25, "encode"), "zookd") # a-1 = z, p-1 = o, etc.

    def test_decode_wrap_around(self):
        self.assertEqual(caesar_cipher("Cheud", 3, "decode"), "Zebra")
        self.assertEqual(caesar_cipher("zookd", 25, "decode"), "apple")

    def test_mixed_case(self):
        self.assertEqual(caesar_cipher("ApocalypsAI", 1, "encode"), "BqpdqzmqtTBJ")
        self.assertEqual(caesar_cipher("BqpdqzmqtTBJ", 1, "decode"), "ApocalypsAI")
        self.assertEqual(caesar_cipher("MiXeD CaSe", 2, "encode"), "OkXgF EcUg")

    def test_non_alphabetic_characters(self):
        self.assertEqual(caesar_cipher("Hello, World! 123", 3, "encode"), "Khoor, Bwrlq! 123")
        self.assertEqual(caesar_cipher("Khoor, Bwrlq! 123", 3, "decode"), "Hello, World! 123")
        self.assertEqual(caesar_cipher("Base 42 is secure.", 5, "encode"), "Ifxj 42 nx xjhzwj.")

    def test_zero_shift(self):
        self.assertEqual(caesar_cipher("Test", 0, "encode"), "Test")
        self.assertEqual(caesar_cipher("Test", 0, "decode"), "Test")

    def test_empty_string(self):
        self.assertEqual(caesar_cipher("", 5, "encode"), "")
        self.assertEqual(caesar_cipher("", 5, "decode"), "")

    def test_large_shift(self):
        # A shift of 26 is equivalent to a shift of 0
        self.assertEqual(caesar_cipher("Alpha", 26, "encode"), "Alpha")
        self.assertEqual(caesar_cipher("Alpha", 52, "encode"), "Alpha")
        self.assertEqual(caesar_cipher("Alpha", 27, "encode"), "Bmqib") # 27 % 26 = 1
        self.assertEqual(caesar_cipher("Bmqib", 27, "decode"), "Alpha")

    def test_negative_shift(self):
        # Encoding with -1 is like decoding with 1
        self.assertEqual(caesar_cipher("Hello", -1, "encode"), "Gdkkn")
        self.assertEqual(caesar_cipher("Gdkkn", -1, "decode"), "Hello")
        self.assertEqual(caesar_cipher("ApocalypsAI", -1, "encode"), "ZoobkzlorzH")
        self.assertEqual(caesar_cipher("ZoobkzlorzH", -1, "decode"), "ApocalypsAI")


class TestCLI(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encoder.py', '--mode', 'encode', '--message', 'Whisper', '--shift', '2'])
    def test_cli_encode(self, mock_stdout):
        # Mock rationale: See class-level mock rationale.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Yjkuqgt")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encoder.py', '--mode', 'decode', '--message', 'Yjkuqgt', '--shift', '2'])
    def test_cli_decode(self, mock_stdout):
        # Mock rationale: See class-level mock rationale.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Whisper")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encoder.py', '--mode', 'encode', '--message', 'Secret 123!', '--shift', '10'])
    def test_cli_encode_with_special_chars(self, mock_stdout):
        # Mock rationale: See class-level mock rationale.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Csmbo 123!")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['encoder.py', '--mode', 'decode', '--message', 'Csmbo 123!', '--shift', '10'])
    def test_cli_decode_with_special_chars(self, mock_stdout):
        # Mock rationale: See class-level mock rationale.
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Secret 123!")

    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['encoder.py', '--message', 'Test', '--shift', '5']) # Missing mode
    def test_cli_missing_mode_argument(self, mock_exit, mock_stderr):
        # Mock rationale: We need to test how argparse handles missing required arguments.
        # sys.exit is patched to prevent the test runner from exiting prematurely,
        # and sys.stderr is patched to capture the error message printed by argparse.
        with self.assertRaises(SystemExit): # argparse raises SystemExit on error
            main()
        mock_exit.assert_called_with(2) # argparse exits with 2 for argument errors
        self.assertIn("argument --mode is required", mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['encoder.py', '--mode', 'encode', '--message', 'Test', '--shift', 'invalid']) # Invalid shift type
    def test_cli_invalid_shift_type(self, mock_exit, mock_stderr):
        # Mock rationale: See test_cli_missing_mode_argument.
        with self.assertRaises(SystemExit):
            main()
        mock_exit.assert_called_with(2)
        self.assertIn("argument --shift: invalid int value", mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
