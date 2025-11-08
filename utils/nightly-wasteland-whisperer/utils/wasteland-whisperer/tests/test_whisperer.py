import unittest
import sys
import io
from unittest.mock import patch
from src.whisperer import encode, decode, main, _normalize_text

class TestWastelandWhisperer(unittest.TestCase):

    def test_normalize_text(self):
        # Mock rationale: Testing an internal helper function directly.
        self.assertEqual(_normalize_text("Hello World! 123"), "HELLOWORLD")
        self.assertEqual(_normalize_text("aBcDeFg"), "ABCDEFG")
        self.assertEqual(_normalize_text(""), "")
        self.assertEqual(_normalize_text("!@#$%^&*()"), "")
        self.assertEqual(_normalize_text("  Test  "), "TEST")

    def test_encode_simple(self):
        # Mock rationale: Testing the core encoding logic with known inputs.
        self.assertEqual(encode("HELLO", "KEY"), "RIJVS")
        self.assertEqual(encode("WORLD", "SECRET"), "NSPXW")
        self.assertEqual(encode("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")

    def test_decode_simple(self):
        # Mock rationale: Testing the core decoding logic with known inputs.
        self.assertEqual(decode("RIJVS", "KEY"), "HELLO")
        self.assertEqual(decode("NSPXW", "SECRET"), "WORLD")
        self.assertEqual(decode("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")

    def test_encode_decode_roundtrip(self):
        # Mock rationale: Verifying that encoding followed by decoding returns the original message.
        message = "The quick brown fox jumps over the lazy dog."
        keyword = "APOCALYPSE"
        encoded = encode(message, keyword)
        decoded = decode(encoded, keyword)
        self.assertEqual(_normalize_text(decoded), _normalize_text(message)) # Normalize for comparison due to non-alpha chars

    def test_preserve_non_alphabetic_chars(self):
        # Mock rationale: Ensuring non-alphabetic characters are not altered.
        message = "Hello, World! 123."
        keyword = "KEY"
        encoded = encode(message, keyword)
        self.assertEqual(encoded, "Rijvs, Nspxw! 123.")
        decoded = decode(encoded, keyword)
        self.assertEqual(decoded, "Hello, World! 123.")

    def test_preserve_case(self):
        # Mock rationale: Ensuring original case of alphabetic characters is preserved.
        message = "HeLlO WoRlD"
        keyword = "KEY"
        encoded = encode(message, keyword)
        self.assertEqual(encoded, "RiJvS NsPxW")
        decoded = decode(encoded, keyword)
        self.assertEqual(decoded, "HeLlO WoRlD")

    def test_keyword_with_non_alphabetic_chars(self):
        # Mock rationale: Testing keyword normalization.
        message = "TEST"
        keyword = "K3Y!"
        encoded = encode(message, keyword)
        self.assertEqual(encoded, "DIBD") # Using "KEY"
        decoded = decode(encoded, keyword)
        self.assertEqual(decoded, "TEST")

    def test_empty_message(self):
        # Mock rationale: Testing behavior with an empty message.
        self.assertEqual(encode("", "KEY"), "")
        self.assertEqual(decode("", "KEY"), "")

    def test_empty_keyword_raises_error(self):
        # Mock rationale: Ensuring an error is raised for an invalid keyword.
        with self.assertRaises(ValueError) as cm:
            encode("HELLO", "")
        self.assertIn("Keyword must contain at least one alphabetic character.", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            decode("RIJVS", "123!@#") # Keyword becomes empty after normalization
        self.assertIn("Keyword must contain at least one alphabetic character.", str(cm.exception))

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encode(self, mock_parse_args, mock_stdout):
        # Mock rationale: Mocking command-line arguments and stdout to test main function behavior without actual CLI interaction.
        mock_parse_args.return_value = argparse.Namespace(
            encode="MEET ME AT THE OLD BRIDGE",
            decode=None,
            keyword="SURVIVAL"
        )
        main()
        expected_output = (
            "Original Message: MEET ME AT THE OLD BRIDGE\n"
            "Keyword: SURVIVAL\n"
            "Encoded Message: EIIF EI AF FHI OLE ZVILGI\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decode(self, mock_parse_args, mock_stdout):
        # Mock rationale: Mocking command-line arguments and stdout to test main function behavior without actual CLI interaction.
        mock_parse_args.return_value = argparse.Namespace(
            encode=None,
            decode="EIIF EI AF FHI OLE ZVILGI",
            keyword="SURVIVAL"
        )
        main()
        expected_output = (
            "Encoded Message: EIIF EI AF FHI OLE ZVILGI\n"
            "Keyword: SURVIVAL\n"
            "Decoded Message: MEET ME AT THE OLD BRIDGE\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_both_encode_decode_error(self, mock_parse_args, mock_stderr):
        # Mock rationale: Mocking command-line arguments and stderr to test error handling in main function.
        mock_parse_args.return_value = argparse.Namespace(
            encode="MSG",
            decode="MSG",
            keyword="KEY"
        )
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2) # argparse exits with 2 for argument errors
        self.assertIn("error: Cannot use --encode and --decode simultaneously. Choose one.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_action_prints_help(self, mock_parse_args, mock_stdout):
        # Mock rationale: Mocking command-line arguments and stdout to test help message display.
        mock_parse_args.return_value = argparse.Namespace(
            encode=None,
            decode=None,
            keyword="KEY"
        )
        with self.assertRaises(SystemExit) as cm: # argparse.print_help() exits
            main()
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("usage: wasteland-whisperer.py", mock_stdout.getvalue())
        self.assertIn("Wasteland Whisperer: A Vigenere cipher utility for cryptic communication.", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
