import unittest
import os
from unittest.mock import patch, mock_open
import sys

# Add the src directory to the path to allow importing cryptographer.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cryptographer import caesar_cipher, encrypt_file, decrypt_file, main
sys.path.pop(0)

class TestCryptographer(unittest.TestCase):

    def test_caesar_cipher_encrypt(self):
        self.assertEqual(caesar_cipher("abc", 1, 'encrypt'), "bcd")
        self.assertEqual(caesar_cipher("xyz", 1, 'encrypt'), "yza")
        self.assertEqual(caesar_cipher("Hello World!", 3, 'encrypt'), "Khoor Zruog!")
        self.assertEqual(caesar_cipher("123", 5, 'encrypt'), "123") # Non-alphabetic characters should remain unchanged
        self.assertEqual(caesar_cipher("", 10, 'encrypt'), "") # Empty string
        self.assertEqual(caesar_cipher("ABC", 1, 'encrypt'), "BCD")
        self.assertEqual(caesar_cipher("XYZ", 1, 'encrypt'), "YZA")
        self.assertEqual(caesar_cipher("Attack at dawn!", 3, 'encrypt'), "Dwwdfn dw gdzq!")

    def test_caesar_cipher_decrypt(self):
        self.assertEqual(caesar_cipher("bcd", 1, 'decrypt'), "abc")
        self.assertEqual(caesar_cipher("yza", 1, 'decrypt'), "xyz")
        self.assertEqual(caesar_cipher("Khoor Zruog!", 3, 'decrypt'), "Hello World!")
        self.assertEqual(caesar_cipher("123", 5, 'decrypt'), "123")
        self.assertEqual(caesar_cipher("", 10, 'decrypt'), "")
        self.assertEqual(caesar_cipher("BCD", 1, 'decrypt'), "ABC")
        self.assertEqual(caesar_cipher("YZA", 1, 'decrypt'), "XYZ")
        self.assertEqual(caesar_cipher("Dwwdfn dw gdzq!", 3, 'decrypt'), "Attack at dawn!")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_encrypt_file(self, mock_exists, mock_file_open):
        # Mock rationale: We don't want to actually read/write to the filesystem during tests.
        # mock_open allows us to simulate file content and check what was written.
        # mock_exists ensures the utility thinks the file exists.
        mock_file_open.return_value.read.return_value = "secret message"
        
        expected_encrypted_content = caesar_cipher("secret message", 3, 'encrypt')
        result = encrypt_file("dummy.txt", 3)
        
        self.assertEqual(result, expected_encrypted_content)
        mock_file_open.assert_called_with("dummy.txt", 'w', encoding='utf-8')
        mock_file_open.return_value.write.assert_called_once_with(expected_encrypted_content)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_decrypt_file(self, mock_exists, mock_file_open):
        # Mock rationale: Similar to encrypt_file, we mock file operations to isolate the test.
        mock_file_open.return_value.read.return_value = caesar_cipher("secret message", 3, 'encrypt')
        
        expected_decrypted_content = "secret message"
        result = decrypt_file("dummy.txt", 3)
        
        self.assertEqual(result, expected_decrypted_content)
        mock_file_open.assert_called_with("dummy.txt", 'w', encoding='utf-8')
        mock_file_open.return_value.write.assert_called_once_with(expected_decrypted_content)

    @patch('cryptographer.encrypt_file')
    @patch('cryptographer.decrypt_file')
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['cryptographer.py', 'encrypt', 'test.txt', '3'])
    @patch('builtins.print') # Mock print to capture output
    def test_main_encrypt(self, mock_print, mock_exists, mock_decrypt, mock_encrypt):
        # Mock rationale: We mock sys.argv to simulate command-line arguments without actually running the script from CLI.
        # We mock encrypt_file/decrypt_file to ensure main calls them correctly and doesn't perform actual file ops.
        # We mock print to verify output messages.
        main()
        mock_encrypt.assert_called_once_with('test.txt', 3)
        mock_decrypt.assert_not_called()
        mock_print.assert_called_with("File 'test.txt' encrypted with shift 3.")

    @patch('cryptographer.encrypt_file')
    @patch('cryptographer.decrypt_file')
    @patch('os.path.exists', return_value=True)
    @patch('sys.argv', ['cryptographer.py', 'decrypt', 'test.txt', '5'])
    @patch('builtins.print')
    def test_main_decrypt(self, mock_print, mock_exists, mock_decrypt, mock_encrypt):
        # Mock rationale: Same as test_main_encrypt, for decrypt mode.
        main()
        mock_decrypt.assert_called_once_with('test.txt', 5)
        mock_encrypt.assert_not_called()
        mock_print.assert_called_with("File 'test.txt' decrypted with shift 5.")

    @patch('os.path.exists', return_value=False)
    @patch('sys.argv', ['cryptographer.py', 'encrypt', 'nonexistent.txt', '1'])
    @patch('builtins.print')
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    def test_main_file_not_found(self, mock_exit, mock_print, mock_exists):
        # Mock rationale: We mock os.path.exists to simulate a missing file.
        # We mock sys.exit to prevent the test runner from terminating.
        main()
        mock_print.assert_called_with("Error: File not found at 'nonexistent.txt'")
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
