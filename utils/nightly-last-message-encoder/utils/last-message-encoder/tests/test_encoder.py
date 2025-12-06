import unittest
import sys
from unittest.mock import patch
from io import StringIO
from src.encoder import encode, decode, _generate_cipher_map, main

class TestEncoder(unittest.TestCase):

    def test_generate_cipher_map_simple_keyword(self):
        # Mock rationale: This function is pure and deterministic, no mocks needed.
        forward, reverse = _generate_cipher_map("KEY")
        self.assertEqual(forward['A'], 'K')
        self.assertEqual(forward['B'], 'E')
        self.assertEqual(forward['C'], 'Y')
        self.assertEqual(forward['D'], 'A')
        self.assertEqual(reverse['K'], 'A')
        self.assertEqual(reverse['E'], 'B')
        self.assertEqual(reverse['Y'], 'C')
        self.assertEqual(reverse['A'], 'D')

    def test_generate_cipher_map_long_keyword_with_duplicates(self):
        # Mock rationale: This function is pure and deterministic, no mocks needed.
        forward, reverse = _generate_cipher_map("APOCALYPSE")
        # Cipher alphabet: APOCLYSEBDFGHIJKMNQRTUVWXZ
        self.assertEqual(forward['A'], 'A')
        self.assertEqual(forward['B'], 'P')
        self.assertEqual(forward['C'], 'O')
        self.assertEqual(forward['D'], 'C')
        self.assertEqual(forward['E'], 'L') # E maps to L
        self.assertEqual(forward['F'], 'Y') # F maps to Y
        self.assertEqual(forward['G'], 'S') # G maps to S
        self.assertEqual(forward['H'], 'E') # H maps to E

        self.assertEqual(reverse['A'], 'A') # A maps to A
        self.assertEqual(reverse['P'], 'B') # P maps to B
        self.assertEqual(reverse['O'], 'C') # O maps to C
        self.assertEqual(reverse['C'], 'D') # C maps to D
        self.assertEqual(reverse['L'], 'E') # L maps to E
        self.assertEqual(reverse['Y'], 'F') # Y maps to F
        self.assertEqual(reverse['S'], 'G') # S maps to G
        self.assertEqual(reverse['E'], 'H') # E maps to H

    def test_encode_simple_message(self):
        # Mock rationale: This function is pure and deterministic, no mocks needed.
        keyword = "ZULU"
        message = "HELLO WORLD"
        # Expected: EBIIO VMPIA (based on ZULABCDEFGHIJKLMNOPQRSTVWXY cipher alphabet)
        self.assertEqual(encode(message, keyword), "EBIIO VMPIA")

    def test_decode_simple_message(self):
        # Mock rationale: This function is pure and deterministic, no mocks needed.
        keyword = "ZULU"
        encoded_message = "EBIIO VMPIA"
        expected = "HELLO WORLD"
        self.assertEqual(decode(encoded_message, keyword), expected)

    def test_encode_decode_roundtrip(self):
        # Mock rationale: This function is pure and deterministic, no mocks needed.
        keyword = "APOCALYPSE"
        message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 123!@#"
        encoded = encode(message, keyword)
        decoded = decode(encoded, keyword)
        self.assertEqual(decoded, message.upper()) # Note: decode returns uppercase

    def test_handle_non_alpha_characters(self):
        # Mock rationale: This function is pure and deterministic, no mocks needed.
        keyword = "SECRET"
        message = "MESSAGE 123!@#"
        # Expected: JABBAFB 123!@# (based on SECRTABDFGHIJKLMNOUPQVWXYZ cipher alphabet)
        encoded = encode(message, keyword)
        self.assertEqual(encoded, "JABBAFB 123!@#")
        decoded = decode(encoded, keyword)
        self.assertEqual(decoded, message.upper()) # Note: decode returns uppercase

    def test_empty_message(self):
        # Mock rationale: This function is pure and deterministic, no mocks needed.
        keyword = "KEY"
        self.assertEqual(encode("", keyword), "")
        self.assertEqual(decode("", keyword), "")

    def test_cli_encode(self):
        # Mock rationale: We are testing the CLI interface, which involves `sys.argv` and `print`.
        # Patching `sys.argv` allows us to simulate command-line arguments.
        # Patching `sys.stdout` allows us to capture printed output for verification.
        test_args = ["encoder.py", "encode", "HELLO", "ZULU"]
        with patch('sys.argv', test_args),
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Original: HELLO", output)
            self.assertIn("Encoded:  EBIIO", output)

    def test_cli_decode(self):
        # Mock rationale: Similar to `test_cli_encode`, we need to simulate CLI input and capture output.
        test_args = ["encoder.py", "decode", "EBIIO", "ZULU"]
        with patch('sys.argv', test_args),
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Original: EBIIO", output)
            self.assertIn("Decoded:  HELLO", output)

    def test_cli_invalid_action(self):
        # Mock rationale: Testing error handling for invalid CLI arguments.
        # We expect `SystemExit` from `argparse` and capture stderr.
        test_args = ["encoder.py", "invalid_action", "MESSAGE", "KEY"]
        with patch('sys.argv', test_args),
             patch('sys.stderr', new_callable=StringIO) as mock_stderr,
             self.assertRaises(SystemExit) as cm:
            main()
            self.assertEqual(cm.exception.code, 2) # argparse exits with 2 for invalid args
            self.assertIn("argument action: invalid choice: 'invalid_action'", mock_stderr.getvalue())
