import unittest
from unittest.mock import patch
import sys
import io
from src.encoder import encode_message, decode_message, calculate_checksum, CHAR_TO_CODE, CODE_TO_CHAR, main

class TestWastelandWhispererEncoderLogic(unittest.TestCase):

    def test_char_to_code_mapping(self):
        self.assertEqual(CHAR_TO_CODE['A'], '01')
        self.assertEqual(CHAR_TO_CODE['Z'], '26')
        self.assertEqual(CHAR_TO_CODE['0'], '27')
        self.assertEqual(CHAR_TO_CODE['9'], '36')
        self.assertEqual(CHAR_TO_CODE[' '], '37')
        self.assertEqual(CHAR_TO_CODE['.'], '38')
        self.assertEqual(CHAR_TO_CODE[','], '39')
        self.assertEqual(CHAR_TO_CODE['!'], '40')
        self.assertEqual(CHAR_TO_CODE['?'], '41')
        self.assertIsNone(CHAR_TO_CODE.get('a')) # Case-insensitivity handled by encoder
        self.assertIsNone(CHAR_TO_CODE.get('@')) # Unsupported character

    def test_code_to_char_mapping(self):
        self.assertEqual(CODE_TO_CHAR['01'], 'A')
        self.assertEqual(CODE_TO_CHAR['26'], 'Z')
        self.assertEqual(CODE_TO_CHAR['27'], '0')
        self.assertEqual(CODE_TO_CHAR['36'], '9')
        self.assertEqual(CODE_TO_CHAR['37'], ' ')
        self.assertEqual(CODE_TO_CHAR['38'], '.')
        self.assertEqual(CODE_TO_CHAR['39'], ',')
        self.assertEqual(CODE_TO_CHAR['40'], '!')
        self.assertEqual(CODE_TO_CHAR['41'], '?')
        self.assertIsNone(CODE_TO_CHAR.get('99')) # Unknown code

    def test_calculate_checksum(self):
        self.assertEqual(calculate_checksum(['01', '02', '03']), 6)
        self.assertEqual(calculate_checksum(['10', '20', '30']), 60)
        self.assertEqual(calculate_checksum([]), 0)
        self.assertEqual(calculate_checksum(['05']), 5)
        self.assertEqual(calculate_checksum(['01', '', '02']), 3) # Empty string from split should be ignored
        self.assertEqual(calculate_checksum(['01', 'XX', '02']), 3) # Non-numeric string should be ignored

    def test_encode_simple_message(self):
        self.assertEqual(encode_message("HI"), "08-09##17")
        self.assertEqual(encode_message("HELLO WORLD"), "08-05-12-12-15-37-23-15-18-12-04##189")
        self.assertEqual(encode_message("123"), "28-29-30##87")
        self.assertEqual(encode_message("SOS!"), "19-15-19-40##93")
        self.assertEqual(encode_message("APOCALYPSAI?"), "01-16-15-03-01-12-25-16-19-01-09-41##144")

    def test_encode_empty_message(self):
        self.assertEqual(encode_message(""), "")
        self.assertEqual(encode_message(" "), "37##37") # Space is a valid char

    def test_encode_unsupported_characters(self):
        # Unsupported characters should be ignored
        self.assertEqual(encode_message("Hello@World"), "08-05-12-12-15-23-15-18-12-04##144")
        self.assertEqual(encode_message("\n\t"), "") # Only space ' ' is supported whitespace

    def test_encode_case_insensitivity(self):
        self.assertEqual(encode_message("hello world"), "08-05-12-12-15-37-23-15-18-12-04##189")
        self.assertEqual(encode_message("Hello World"), "08-05-12-12-15-37-23-15-18-12-04##189")

    def test_decode_simple_message(self):
        decoded, is_ok, expected_cs, actual_cs = decode_message("08-09##17")
        self.assertEqual(decoded, "HI")
        self.assertTrue(is_ok)
        self.assertEqual(expected_cs, 17)
        self.assertEqual(actual_cs, 17)

        decoded, is_ok, expected_cs, actual_cs = decode_message("08-05-12-12-15-37-23-15-18-12-04##189")
        self.assertEqual(decoded, "HELLO WORLD")
        self.assertTrue(is_ok)
        self.assertEqual(expected_cs, 189)
        self.assertEqual(actual_cs, 189)

    def test_decode_message_with_mismatched_checksum(self):
        decoded, is_ok, expected_cs, actual_cs = decode_message("08-09##18") # Checksum should be 17
        self.assertEqual(decoded, "HI")
        self.assertFalse(is_ok)
        self.assertEqual(expected_cs, 18)
        self.assertEqual(actual_cs, 17)

    def test_decode_message_without_checksum(self):
        decoded, is_ok, expected_cs, actual_cs = decode_message("08-09")
        self.assertEqual(decoded, "HI")
        self.assertFalse(is_ok) # No checksum means it can't be 'OK'
        self.assertEqual(expected_cs, -1) # Indicates no checksum provided
        self.assertEqual(actual_cs, 17) # Still calculates actual checksum

    def test_decode_message_with_invalid_checksum_format(self):
        decoded, is_ok, expected_cs, actual_cs = decode_message("08-09##ABC")
        self.assertEqual(decoded, "HI")
        self.assertFalse(is_ok)
        self.assertEqual(expected_cs, -1) # Indicates invalid format
        self.assertEqual(actual_cs, 17)

    def test_decode_message_with_unknown_codes(self):
        decoded, is_ok, expected_cs, actual_cs = decode_message("08-99-09##17") # 99 is unknown, checksum is correct for H_I
        self.assertEqual(decoded, "H[?]I")
        self.assertTrue(is_ok) # Checksum is correct for the valid parts
        self.assertEqual(expected_cs, 17)
        self.assertEqual(actual_cs, 17)

    def test_decode_empty_string(self):
        decoded, is_ok, expected_cs, actual_cs = decode_message("")
        self.assertEqual(decoded, "")
        self.assertFalse(is_ok)
        self.assertEqual(expected_cs, -1)
        self.assertEqual(actual_cs, 0)

    def test_decode_only_checksum(self):
        decoded, is_ok, expected_cs, actual_cs = decode_message("##10")
        self.assertEqual(decoded, "")
        self.assertFalse(is_ok) # Expected 10, Actual 0
        self.assertEqual(expected_cs, 10)
        self.assertEqual(actual_cs, 0)

    def test_decode_only_checksum_matching_empty_message(self):
        decoded, is_ok, expected_cs, actual_cs = decode_message("##0")
        self.assertEqual(decoded, "")
        self.assertTrue(is_ok)
        self.assertEqual(expected_cs, 0)
        self.assertEqual(actual_cs, 0)

    def test_decode_with_leading_trailing_delimiters(self):
        # Test cases where split might produce empty strings
        decoded, is_ok, _, _ = decode_message("-08-09-") # Should ignore empty strings from split
        self.assertEqual(decoded, "HI")
        self.assertFalse(is_ok) # No checksum

        decoded, is_ok, _, _ = decode_message("-08-09-##17")
        self.assertEqual(decoded, "HI")
        self.assertTrue(is_ok)


class TestWastelandWhispererEncoderCLI(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_encode(self, mock_parse_args, mock_stdout):
        # Mock rationale: We are testing the CLI interface of the main function,
        # which prints output to stdout. Mocking sys.stdout allows us to capture
        # and assert the printed output without affecting the actual console.
        # Mocking argparse.ArgumentParser.parse_args allows us to simulate
        # command-line arguments without actually parsing sys.argv.
        mock_parse_args.return_value = argparse.Namespace(encode="TEST", decode=None)
        main()
        self.assertIn("Encoded: 20-05-19-20##64", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decode_ok(self, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, for capturing stdout and simulating CLI args.
        mock_parse_args.return_value = argparse.Namespace(encode=None, decode="20-05-19-20##64")
        main()
        self.assertIn("Decoded: TEST (Checksum OK Expected 64, Got 64)", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decode_mismatch(self, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, for capturing stdout and simulating CLI args.
        mock_parse_args.return_value = argparse.Namespace(encode=None, decode="20-05-19-20##63") # Mismatched checksum
        main()
        self.assertIn("Decoded: TEST (Checksum MISMATCH! Expected 63, Got 64)", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decode_no_checksum_provided(self, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, for capturing stdout and simulating CLI args.
        mock_parse_args.return_value = argparse.Namespace(encode=None, decode="20-05-19-20")
        main()
        self.assertIn("Decoded: TEST (No checksum provided in encoded string)", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_decode_invalid_checksum_format(self, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, for capturing stdout and simulating CLI args.
        mock_parse_args.return_value = argparse.Namespace(encode=None, decode="20-05-19-20##ABC")
        main()
        self.assertIn("Decoded: TEST (Invalid checksum format in encoded string)", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_args(self, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, for capturing stdout and simulating CLI args.
        # argparse.print_help() prints to stderr by default, but often also to stdout.
        # We check for common help output elements.
        mock_parse_args.return_value = argparse.Namespace(encode=None, decode=None)
        main()
        self.assertIn("usage: ", mock_stdout.getvalue())
        self.assertIn("Wasteland Whisperer Encoder/Decoder", mock_stdout.getvalue())
