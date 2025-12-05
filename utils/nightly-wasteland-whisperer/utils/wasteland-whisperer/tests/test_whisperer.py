import unittest
import sys
import io
from unittest.mock import patch

# Mock rationale: We need to test the CLI functionality which involves stdout and argparse.
# Patching sys.stdout allows us to capture printed output without actual console interaction.
# Patching sys.argv allows us to simulate command-line arguments without running the script directly.
# Patching sys.exit allows us to prevent the test from terminating prematurely when an error occurs
# due to argparse or explicit calls within the script.

# Add the src directory to the path for importing the module
sys.path.insert(0, 'src')
import whisperer
sys.path.pop(0)

class TestWastelandWhisperer(unittest.TestCase):

    def test_encode_basic(self):
        self.assertEqual(whisperer.whisper("abc", 1, 'encode'), "bcd")
        self.assertEqual(whisperer.whisper("xyz", 1, 'encode'), "yza")
        self.assertEqual(whisperer.whisper("ABC", 1, 'encode'), "BCD")
        self.assertEqual(whisperer.whisper("XYZ", 1, 'encode'), "YZA")

    def test_decode_basic(self):
        self.assertEqual(whisperer.whisper("bcd", 1, 'decode'), "abc")
        self.assertEqual(whisperer.whisper("yza", 1, 'decode'), "xyz")
        self.assertEqual(whisperer.whisper("BCD", 1, 'decode'), "ABC")
        self.assertEqual(whisperer.whisper("YZA", 1, 'decode'), "XYZ")

    def test_encode_decode_roundtrip(self):
        original = "Hello, Survivor! This is a test message with numbers 123 and symbols !@#."
        scramble_factor = 5
        encoded = whisperer.whisper(original, scramble_factor, 'encode')
        decoded = whisperer.whisper(encoded, scramble_factor, 'decode')
        self.assertEqual(original, decoded)

    def test_scramble_factor_zero(self):
        text = "No change here."
        self.assertEqual(whisperer.whisper(text, 0, 'encode'), text)
        self.assertEqual(whisperer.whisper(text, 0, 'decode'), text)

    def test_scramble_factor_large(self):
        # A large factor should wrap around correctly (27 is equivalent to 1, -25 is equivalent to 1)
        self.assertEqual(whisperer.whisper("abc", 27, 'encode'), "bcd")
        self.assertEqual(whisperer.whisper("abc", -25, 'encode'), "bcd")
        self.assertEqual(whisperer.whisper("bcd", 27, 'decode'), "abc")

    def test_mixed_case_and_punctuation(self):
        text = "ApocalypsAI is here! 123"
        scramble_factor = 2
        expected_encoded = "CrqocnyrruCK ku jgtg! 123"
        self.assertEqual(whisperer.whisper(text, scramble_factor, 'encode'), expected_encoded)
        self.assertEqual(whisperer.whisper(expected_encoded, scramble_factor, 'decode'), text)

    def test_empty_string(self):
        self.assertEqual(whisperer.whisper("", 5, 'encode'), "")
        self.assertEqual(whisperer.whisper("", 5, 'decode'), "")

    def test_invalid_mode_function_call(self):
        with self.assertRaises(ValueError) as cm:
            whisperer.whisper("test", 1, 'invalid')
        self.assertIn("Mode must be 'encode' or 'decode'.", str(cm.exception))

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['whisperer.py', '--mode', 'encode', '--text', 'test', '--scramble-factor', '1'])
    def test_main_encode_success(self, mock_stdout):
        whisperer.main()
        self.assertEqual(mock_stdout.getvalue().strip(), "uftu")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['whisperer.py', '--mode', 'decode', '--text', 'uftu', '--scramble-factor', '1'])
    def test_main_decode_success(self, mock_stdout):
        whisperer.main()
        self.assertEqual(mock_stdout.getvalue().strip(), "test")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit') # Mock sys.exit to prevent actual program termination
    @patch('sys.argv', ['whisperer.py', '--mode', 'invalid', '--text', 'test', '--scramble-factor', '1'])
    def test_main_invalid_mode_cli_error(self, mock_exit, mock_stderr, mock_stdout):
        # argparse itself handles invalid choices and exits with 2
        whisperer.main()
        mock_exit.assert_called_with(2)
        self.assertIn("argument --mode: invalid choice: 'invalid' (choose from 'encode', 'decode')", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit') # Mock sys.exit to prevent actual program termination
    @patch('sys.argv', ['whisperer.py', '--mode', 'encode', '--text', 'test'])
    def test_main_missing_scramble_factor_cli_error(self, mock_exit, mock_stderr, mock_stdout):
        # argparse handles missing required arguments and exits with 2
        whisperer.main()
        mock_exit.assert_called_with(2)
        self.assertIn("argument --scramble-factor is required", mock_stderr.getvalue())
