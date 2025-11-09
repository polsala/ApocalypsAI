import unittest
from unittest.mock import patch
import io
import sys
from src.whisperer import caesar_cipher, main

class TestWastelandWhisperer(unittest.TestCase):

    def test_caesar_encode_basic(self):
        # Test basic encoding with a positive shift
        self.assertEqual(caesar_cipher("hello", 3, encode=True), "khoor")
        self.assertEqual(caesar_cipher("WORLD", 5, encode=True), "BVSPI")
        self.assertEqual(caesar_cipher("ApocalypsAI", 1, encode=True), "BqpdqmjqtqTj")

    def test_caesar_decode_basic(self):
        # Test basic decoding with a positive shift
        self.assertEqual(caesar_cipher("khoor", 3, encode=False), "hello")
        self.assertEqual(caesar_cipher("BVSPI", 5, encode=False), "WORLD")
        self.assertEqual(caesar_cipher("BqpdqmjqtqTj", 1, encode=False), "ApocalypsAI")

    def test_caesar_encode_wrap_around(self):
        # Test encoding with wrap-around (z -> a)
        self.assertEqual(caesar_cipher("xyz", 3, encode=True), "abc")
        self.assertEqual(caesar_cipher("XYZ", 3, encode=True), "ABC")

    def test_caesar_decode_wrap_around(self):
        # Test decoding with wrap-around (a -> z)
        self.assertEqual(caesar_cipher("abc", 3, encode=False), "xyz")
        self.assertEqual(caesar_cipher("ABC", 3, encode=False), "XYZ")

    def test_caesar_non_alphabetic_characters(self):
        # Test that non-alphabetic characters are unchanged
        self.assertEqual(caesar_cipher("Hello, World! 123", 3, encode=True), "Khoor, Zruog! 123")
        self.assertEqual(caesar_cipher("Khoor, Zruog! 123", 3, encode=False), "Hello, World! 123")
        self.assertEqual(caesar_cipher("!@#$%^&*()", 5, encode=True), "!@#$%^&*()")

    def test_caesar_empty_string(self):
        # Test with an empty string
        self.assertEqual(caesar_cipher("", 5, encode=True), "")
        self.assertEqual(caesar_cipher("", 5, encode=False), "")

    def test_caesar_zero_shift(self):
        # Test with a zero shift (should return original message)
        self.assertEqual(caesar_cipher("Test Message", 0, encode=True), "Test Message")
        self.assertEqual(caesar_cipher("Test Message", 0, encode=False), "Test Message")

    def test_caesar_large_shift(self):
        # Test with a large shift (should behave like shift % 26)
        self.assertEqual(caesar_cipher("abc", 29, encode=True), "def") # 29 % 26 = 3
        self.assertEqual(caesar_cipher("def", 29, encode=False), "abc")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['whisperer.py', 'encode', 'secret', '5'])
    def test_main_encode(self, mock_stdout):
        # Mock rationale: We need to capture stdout to verify the printed output
        # and mock sys.argv to simulate command-line arguments for the main function.
        main()
        self.assertIn("Encoded message: xjhwjy", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['whisperer.py', 'decode', 'xjhwjy', '5'])
    def test_main_decode(self, mock_stdout):
        # Mock rationale: We need to capture stdout to verify the printed output
        # and mock sys.argv to simulate command-line arguments for the main function.
        main()
        self.assertIn("Decoded message: secret", mock_stdout.getvalue())

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['whisperer.py', 'invalid_action', 'message', '1'])
    def test_main_invalid_action(self, mock_exit, mock_stderr):
        # Mock rationale: We need to capture stderr to verify error messages
        # and mock sys.exit to prevent the test runner from exiting prematurely
        # when argparse encounters an invalid argument.
        with self.assertRaises(SystemExit): # argparse raises SystemExit on invalid args
            main()
        self.assertIn("argument action: invalid choice: 'invalid_action'", mock_stderr.getvalue())
        mock_exit.assert_called_with(2)
