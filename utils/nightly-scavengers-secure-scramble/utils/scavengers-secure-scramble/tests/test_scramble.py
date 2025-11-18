import unittest
import sys
from unittest.mock import patch
from io import StringIO
from src.scramble import vigenere_cipher, main

class TestVigenereCipher(unittest.TestCase):

    def test_encrypt_basic(self):
        self.assertEqual(vigenere_cipher("ATTACKATDAWN", "LEMON", "encrypt"), "LXFOPVEFRNHR")
        self.assertEqual(vigenere_cipher("Hello World", "KEY", "encrypt"), "Rijvs Gspqv")
        self.assertEqual(vigenere_cipher("hello world", "key", "encrypt"), "rijvs gspqv")

    def test_decrypt_basic(self):
        self.assertEqual(vigenere_cipher("LXFOPVEFRNHR", "LEMON", "decrypt"), "ATTACKATDAWN")
        self.assertEqual(vigenere_cipher("Rijvs Gspqv", "KEY", "decrypt"), "Hello World")
        self.assertEqual(vigenere_cipher("rijvs gspqv", "key", "decrypt"), "hello world")

    def test_encrypt_decrypt_cycle(self):
        original_text = "The quick brown fox jumps over the lazy dog."
        key = "SECRET"
        encrypted_text = vigenere_cipher(original_text, key, "encrypt")
        decrypted_text = vigenere_cipher(encrypted_text, key, "decrypt")
        self.assertEqual(decrypted_text, original_text)

        original_text_2 = "ApocalypsAI Integrator Agent is online!"
        key_2 = "NIGHTLY"
        encrypted_text_2 = vigenere_cipher(original_text_2, key_2, "encrypt")
        decrypted_text_2 = vigenere_cipher(encrypted_text_2, key_2, "decrypt")
        self.assertEqual(decrypted_text_2, original_text_2)

    def test_non_alphabetic_characters(self):
        text = "Hello, World! 123."
        key = "KEY"
        encrypted = vigenere_cipher(text, key, "encrypt")
        self.assertEqual(encrypted, "Rijvs, Gspqv! 123.")
        decrypted = vigenere_cipher(encrypted, key, "decrypt")
        self.assertEqual(decrypted, text)

    def test_empty_text(self):
        self.assertEqual(vigenere_cipher("", "KEY", "encrypt"), "")
        self.assertEqual(vigenere_cipher("", "KEY", "decrypt"), "")

    def test_key_with_non_alphabetic_chars(self):
        text = "Test"
        key = "K3Y!"
        # The cipher should ignore '3' and '!' in the key
        encrypted = vigenere_cipher(text, key, "encrypt")
        self.assertEqual(encrypted, vigenere_cipher(text, "KEY", "encrypt"))
        decrypted = vigenere_cipher(encrypted, key, "decrypt")
        self.assertEqual(decrypted, text)

    def test_key_with_no_alphabetic_chars(self):
        with self.assertRaises(ValueError) as cm:
            vigenere_cipher("Test", "123", "encrypt")
        self.assertIn("Key must contain at least one alphabetic character.", str(cm.exception))

    def test_invalid_mode(self):
        with self.assertRaises(ValueError) as cm:
            vigenere_cipher("Test", "KEY", "invalid_mode")
        self.assertIn("Mode must be 'encrypt' or 'decrypt'.", str(cm.exception))

class TestMainCLI(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_encrypt(self, mock_stderr, mock_stdout):
        # Mock rationale: We need to simulate command-line arguments and capture stdout/stderr.
        # sys.argv is mocked to provide the arguments as if they were passed from the shell.
        # sys.stdout and sys.stderr are mocked to capture the printed output for assertion.
        test_args = ["scramble.py", "--text", "Hello", "--key", "ABC", "--encrypt"]
        with patch('sys.argv', test_args):
            main()
            self.assertIn("Encrypted: Hfmmp", mock_stdout.getvalue().strip())
            self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_main_decrypt(self, mock_stderr, mock_stdout):
        # Mock rationale: Same as test_main_encrypt, simulating CLI arguments and capturing output.
        test_args = ["scramble.py", "--text", "Hfmmp", "--key", "ABC", "--decrypt"]
        with patch('sys.argv', test_args):
            main()
            self.assertIn("Decrypted: Hello", mock_stdout.getvalue().strip())
            self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_error_no_key_alphabetic(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: Simulating CLI arguments and capturing output.
        # sys.exit is mocked to prevent the test runner from exiting prematurely when main() calls exit(1).
        test_args = ["scramble.py", "--text", "Hello", "--key", "123", "--encrypt"]
        with patch('sys.argv', test_args):
            main()
            self.assertIn("Error: Key must contain at least one alphabetic character.", mock_stdout.getvalue().strip())
            mock_exit.assert_called_with(1)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_error_missing_text(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: Simulating CLI arguments and capturing output.
        # argparse automatically handles missing required arguments by printing to stderr and exiting.
        # We catch SystemExit which argparse raises.
        test_args = ["scramble.py", "--key", "ABC", "--encrypt"]
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit):
                main()
            self.assertIn("argument --text is required", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_error_no_mode(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: Simulating CLI arguments and capturing output.
        # argparse automatically handles missing mutually exclusive arguments by printing to stderr and exiting.
        # We catch SystemExit which argparse raises.
        test_args = ["scramble.py", "--text", "Hello", "--key", "ABC"]
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit):
                main()
            self.assertIn("one of the arguments --encrypt --decrypt is required", mock_stderr.getvalue())
