import unittest
import sys
import io
from unittest.mock import patch
from src import whisperer

class TestWastelandWhisperer(unittest.TestCase):

    def test_encode_simple_message(self):
        message = "HELLO"
        expected_encoded = ".... . ._.. ._.. ___"
        self.assertEqual(whisperer.encode(message), expected_encoded)

    def test_decode_simple_message(self):
        encoded_message = ".... . ._.. ._.. ___"
        expected_decoded = "HELLO"
        self.assertEqual(whisperer.decode(encoded_message), expected_decoded)

    def test_encode_with_space(self):
        message = "HI THERE"
        expected_encoded = ".... .. | _ .... . ._. ."
        self.assertEqual(whisperer.encode(message), expected_encoded)

    def test_decode_with_space(self):
        encoded_message = ".... .. | _ .... . ._. ."
        expected_decoded = "HI THERE"
        self.assertEqual(whisperer.decode(encoded_message), expected_decoded)

    def test_encode_with_numbers_and_punctuation(self):
        message = "ALERT! CODE 7."
        expected_encoded = "._.. . ._. _ ! | _._. ___ _.. . | __... ._._._"
        self.assertEqual(whisperer.encode(message), expected_encoded)

    def test_decode_with_numbers_and_punctuation(self):
        encoded_message = "._.. . ._. _ ! | _._. ___ _.. . | __... ._._._"
        expected_decoded = "ALERT! CODE 7."
        self.assertEqual(whisperer.decode(encoded_message), expected_decoded)

    def test_encode_empty_string(self):
        message = ""
        expected_encoded = ""
        self.assertEqual(whisperer.encode(message), expected_encoded)

    def test_decode_empty_string(self):
        encoded_message = ""
        expected_decoded = ""
        self.assertEqual(whisperer.decode(encoded_message), expected_decoded)

    def test_encode_unsupported_characters(self):
        message = "Hello World @ # $"
        # '@', '#', '$' are unsupported and should be mapped to '~'
        expected_encoded = ".... . ._.. ._.. ___ | .__ ___ ._. ._.. _.. | ~ | ~ | ~"
        self.assertEqual(whisperer.encode(message), expected_encoded)

    def test_decode_unsupported_characters(self):
        encoded_message = ".... . ._.. ._.. ___ | .__ ___ ._. ._.. _.. | ~ | ~ | ~"
        # '~' should be decoded to '?'
        expected_decoded = "HELLO WORLD ? ? ?"
        self.assertEqual(whisperer.decode(encoded_message), expected_decoded)

    def test_decode_unknown_sequences(self):
        encoded_message = ".... . ._.. ._.. ___ | UNKNOWN_SEQ | .__ ___ ._. ._.. _.. | ANOTHER_BAD_SEQ"
        # UNKNOWN_SEQ and ANOTHER_BAD_SEQ should be decoded to '?'
        expected_decoded = "HELLO?WORLD?"
        self.assertEqual(whisperer.decode(encoded_message), expected_decoded)

    def test_cli_encode(self):
        # Mock rationale: We need to capture stdout to verify the CLI output.
        # We also mock sys.argv to simulate command-line arguments.
        test_message = "TEST CLI"
        expected_output = "_. ._.._ ... _ | _._. ._.. ._.."
        
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            with patch('sys.argv', ['whisperer.py', 'encode', test_message]):
                whisperer.main()
            self.assertEqual(fake_stdout.getvalue().strip(), expected_output)

    def test_cli_decode(self):
        # Mock rationale: We need to capture stdout to verify the CLI output.
        # We also mock sys.argv to simulate command-line arguments.
        test_encoded_message = "_. ._.._ ... _ | _._. ._.. ._.."
        expected_output = "TEST CLI"
        
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            with patch('sys.argv', ['whisperer.py', 'decode', test_encoded_message]):
                whisperer.main()
            self.assertEqual(fake_stdout.getvalue().strip(), expected_output)

    def test_cli_invalid_action(self):
        # Mock rationale: We need to capture stderr to verify error messages
        # and sys.exit to prevent the test runner from exiting.
        with patch('sys.stderr', new=io.StringIO()) as fake_stderr:
            with self.assertRaises(SystemExit) as cm:
                with patch('sys.argv', ['whisperer.py', 'invalid_action', 'message']):
                    whisperer.main()
            self.assertEqual(cm.exception.code, 2) # argparse exits with 2 for invalid arguments
            self.assertIn("argument action: invalid choice: 'invalid_action'", fake_stderr.getvalue())
