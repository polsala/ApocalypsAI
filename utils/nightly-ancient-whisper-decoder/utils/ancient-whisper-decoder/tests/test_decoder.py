import unittest
from unittest.mock import patch
import sys
import io
from src import decoder

class TestDecoder(unittest.TestCase):

    def test_decode_base64_valid(self):
        self.assertEqual(decoder.decode_base64("SGVsbG8sIFdvcmxkIQ=="), "Hello, World!")
        self.assertEqual(decoder.decode_base64("QXBvY2FseXBzQUk="), "ApocalypsAI")

    def test_decode_base64_invalid(self):
        self.assertIsNone(decoder.decode_base64("NotBase64!"))
        self.assertIsNone(decoder.decode_base64("SGVsbG8sIFdvcmxkIQ===")) # Incorrect padding

    def test_decode_rot13(self):
        self.assertEqual(decoder.decode_rot13("Uryyb, Jbeyq!"), "Hello, World!")
        self.assertEqual(decoder.decode_rot13("NcnpnycfNV"), "ApocalypsAI")
        self.assertEqual(decoder.decode_rot13("Hello, World!"), "Uryyb, Jbeyq!") # ROT13 is its own inverse

    def test_reverse_string(self):
        self.assertEqual(decoder.reverse_string("Hello, World!"), "!dlroW ,olleH")
        self.assertEqual(decoder.reverse_string("ApocalypsAI"), "IAsplacyopA")
        self.assertEqual(decoder.reverse_string("racecar"), "racecar")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['decoder.py', 'SGVsbG8sIFdvcmxkIQ=='])
    def test_main_base64_output(self, mock_stdout):
        # Mock rationale: We need to capture stdout to verify the script's output
        # without actually printing to the console during tests.
        # Mock rationale: We need to simulate command-line arguments for the main function.
        decoder.main()
        output = mock_stdout.getvalue()
        self.assertIn("Attempting to decode: 'SGVsbG8sIFdvcmxkIQ=='", output)
        self.assertIn("Base64: Hello, World!", output)
        self.assertNotIn("ROT13:", output) # Should not find ROT13 for this input
        self.assertNotIn("Reverse:", output) # Should not find Reverse for this input

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['decoder.py', 'Uryyb, Jbeyq!'])
    def test_main_rot13_output(self, mock_stdout):
        # Mock rationale: We need to capture stdout to verify the script's output
        # without actually printing to the console during tests.
        # Mock rationale: We need to simulate command-line arguments for the main function.
        decoder.main()
        output = mock_stdout.getvalue()
        self.assertIn("Attempting to decode: 'Uryyb, Jbeyq!'", output)
        self.assertIn("ROT13: Hello, World!", output)
        self.assertNotIn("Base64:", output)
        self.assertNotIn("Reverse:", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['decoder.py', '!dlroW ,olleH'])
    def test_main_reverse_output(self, mock_stdout):
        # Mock rationale: We need to capture stdout to verify the script's output
        # without actually printing to the console during tests.
        # Mock rationale: We need to simulate command-line arguments for the main function.
        decoder.main()
        output = mock_stdout.getvalue()
        self.assertIn("Attempting to decode: '!dlroW ,olleH'", output)
        self.assertIn("Reverse: Hello, World!", output)
        self.assertNotIn("Base64:", output)
        self.assertNotIn("ROT13:", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['decoder.py', 'Plain text message'])
    def test_main_no_decode_output(self, mock_stdout):
        # Mock rationale: We need to capture stdout to verify the script's output
        # without actually printing to the console during tests.
        # Mock rationale: We need to simulate command-line arguments for the main function.
        decoder.main()
        output = mock_stdout.getvalue()
        self.assertIn("Attempting to decode: 'Plain text message'", output)
        self.assertIn("No common encoding/cipher found or message is already plain.", output)
        self.assertNotIn("Base64:", output)
        self.assertNotIn("ROT13:", output)
        self.assertNotIn("Reverse:", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['decoder.py'])
    def test_main_no_args_output(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: We need to capture stdout/stderr to verify the script's output
        # without actually printing to the console during tests.
        # Mock rationale: We need to simulate command-line arguments for the main function.
        # Mock rationale: We need to prevent sys.exit from terminating the test runner.
        decoder.main()
        output_out = mock_stdout.getvalue()
        self.assertIn("Usage: python decoder.py <encoded_message>", output_out)
        mock_exit.assert_called_once_with(1)
