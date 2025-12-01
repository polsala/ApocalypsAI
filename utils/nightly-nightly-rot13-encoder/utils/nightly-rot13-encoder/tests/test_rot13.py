import sys
import unittest
from unittest import mock

# Import the module under test
from utils.nightly-rot13-encoder.src.rot13 import rot13, main

class TestRot13Function(unittest.TestCase):
    def test_basic_encoding(self):
        self.assertEqual(rot13("Hello, World!"), "Uryyb, Jbeyq!")

    def test_basic_decoding(self):
        # ROT13 is its own inverse
        self.assertEqual(rot13("Uryyb, Jbeyq!"), "Hello, World!")

    def test_empty_string(self):
        self.assertEqual(rot13(""), "")

    def test_non_alpha_characters(self):
        self.assertEqual(rot13("1234!@#$"), "1234!@#$")

class TestRot13CLI(unittest.TestCase):
    def test_cli_encode(self):
        test_args = ["rot13.py", "Hello"]
        with mock.patch.object(sys, "argv", test_args):
            with mock.patch("builtins.print") as mock_print:
                # Mock rationale: simulate command line execution without spawning a subprocess
                main()
                mock_print.assert_called_once_with("Uryyb")

    def test_cli_decode_flag(self):
        test_args = ["rot13.py", "Uryyb", "--decode"]
        with mock.patch.object(sys, "argv", test_args):
            with mock.patch("builtins.print") as mock_print:
                # Mock rationale: ensure the flag does not alter the symmetric operation
                main()
                mock_print.assert_called_once_with("Hello")

if __name__ == "__main__":
    unittest.main()
