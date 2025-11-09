import unittest
import sys
import io
from unittest.mock import patch
from src import whisperer

class TestWhispererFunctions(unittest.TestCase):

    # Mock rationale: These tests focus on the core `encode` and `decode` functions,
    # which are pure and deterministic. No external services or non-deterministic
    # behavior needs mocking for these unit tests. If CLI interaction were to be
    # tested, `sys.argv` and `sys.stdout` would be mocked.

    def test_encode_basic(self):
        self.assertEqual(whisperer.encode("Hello", 3), "Khoor")

    def test_decode_basic(self):
        self.assertEqual(whisperer.decode("Khoor", 3), "Hello")

    def test_encode_wrap_around_uppercase(self):
        self.assertEqual(whisperer.encode("XYZ", 3), "ABC")

    def test_decode_wrap_around_uppercase(self):
        self.assertEqual(whisperer.decode("ABC", 3), "XYZ")

    def test_encode_wrap_around_lowercase(self):
        self.assertEqual(whisperer.encode("xyz", 3), "abc")

    def test_decode_wrap_around_lowercase(self):
        self.assertEqual(whisperer.decode("abc", 3), "xyz")

    def test_encode_mixed_case(self):
        self.assertEqual(whisperer.encode("Apocalypse", 1), "Bqpcbmzqt")

    def test_decode_mixed_case(self):
        self.assertEqual(whisperer.decode("Bqpcbmzqt", 1), "Apocalypse")

    def test_non_alphabetic_characters(self):
        self.assertEqual(whisperer.encode("Hello, World! 123", 5), "Mjqqt, Btwqi! 123")
        self.assertEqual(whisperer.decode("Mjqqt, Btwqi! 123", 5), "Hello, World! 123")

    def test_empty_string(self):
        self.assertEqual(whisperer.encode("", 10), "")
        self.assertEqual(whisperer.decode("", 10), "")

    def test_zero_shift(self):
        self.assertEqual(whisperer.encode("Test Message", 0), "Test Message")
        self.assertEqual(whisperer.decode("Test Message", 0), "Test Message")

    def test_large_shift(self):
        # A shift of 26 is equivalent to a shift of 0
        self.assertEqual(whisperer.encode("Test", 26), "Test")
        self.assertEqual(whisperer.decode("Test", 26), "Test")
        self.assertEqual(whisperer.encode("Test", 27), "Uftu") # 27 % 26 = 1
        self.assertEqual(whisperer.decode("Uftu", 27), "Test")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['whisperer.py', 'encode', 'Test Message', '1'])
    def test_main_encode_cli(self, mock_stdout):
        whisperer.main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Uftu Nfssbhf")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['whisperer.py', 'decode', 'Uftu Nfssbhf', '1'])
    def test_main_decode_cli(self, mock_stdout):
        whisperer.main()
        self.assertEqual(mock_stdout.getvalue().strip(), "Test Message")

if __name__ == '__main__':
    unittest.main()
