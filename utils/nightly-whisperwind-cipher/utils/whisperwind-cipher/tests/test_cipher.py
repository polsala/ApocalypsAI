import unittest
import sys
import io
from unittest.mock import patch

# Mock rationale: The cipher utility is self-contained and performs no external I/O or network requests.
# All functions are pure and deterministic. Therefore, no complex mocking of external systems is required.
# We only mock `sys.stdout` and `sys.stderr` for CLI tests to capture printed output and `sys.exit` to prevent actual exit.

# Add the src directory to the path to allow importing cipher.py
sys.path.insert(0, 'utils/whisperwind-cipher/src')
from cipher import generate_cipher_map, encrypt, decrypt, main, BASE_ALPHABET
sys.path.pop(0)

class TestWhisperwindCipher(unittest.TestCase):

    def test_generate_cipher_map_determinism(self):
        key_phrase = "apocalypsAI"
        map1 = generate_cipher_map(key_phrase)
        map2 = generate_cipher_map(key_phrase)
        self.assertEqual(map1, map2, "Cipher map should be deterministic for the same key phrase.")

        key_phrase_2 = "integrator"
        map3 = generate_cipher_map(key_phrase_2)
        self.assertNotEqual(map1, map3, "Cipher maps should differ for different key phrases.")

    def test_generate_cipher_map_structure(self):
        key_phrase = "test"
        cipher_map = generate_cipher_map(key_phrase)
        self.assertIsInstance(cipher_map, dict)
        self.assertEqual(len(cipher_map), len(BASE_ALPHABET), "Map should cover all base alphabet characters.")
        self.assertTrue(all(k in BASE_ALPHABET for k in cipher_map.keys()))
        self.assertTrue(all(v in BASE_ALPHABET for v in cipher_map.values()))
        self.assertEqual(len(set(cipher_map.values())), len(BASE_ALPHABET), "Cipher map values should be unique (permutation).")

    def test_generate_cipher_map_empty_key_phrase(self):
        with self.assertRaises(ValueError, msg="Empty key phrase should raise ValueError."):
            generate_cipher_map("")

    def test_encrypt_decrypt_roundtrip(self):
        message = "Hello, ApocalypsAI! This is a secret message 123. @#$!"
        key_phrase = "nightly-integrator-agent"

        encrypted_message = encrypt(message, key_phrase)
        decrypted_message = decrypt(encrypted_message, key_phrase)

        self.assertNotEqual(message, encrypted_message, "Message should be encrypted.")
        self.assertEqual(message, decrypted_message, "Decrypted message should match original.")

    def test_encrypt_decrypt_with_different_key(self):
        message = "Top secret data."
        key_phrase_correct = "correct-key"
        key_phrase_wrong = "wrong-key"

        encrypted_message = encrypt(message, key_phrase_correct)
        decrypted_with_wrong_key = decrypt(encrypted_message, key_phrase_wrong)

        self.assertNotEqual(message, decrypted_with_wrong_key, "Wrong key should not decrypt correctly.")

    def test_encrypt_decrypt_empty_message(self):
        message = ""
        key_phrase = "anykey"

        encrypted = encrypt(message, key_phrase)
        decrypted = decrypt(encrypted, key_phrase)

        self.assertEqual(encrypted, "", "Empty message should encrypt to empty string.")
        self.assertEqual(decrypted, "", "Empty message should decrypt to empty string.")

    def test_encrypt_decrypt_unmapped_characters(self):
        # Characters not in BASE_ALPHABET should remain unchanged
        message = "Hello 👋 World!"
        key_phrase = "simple"

        encrypted = encrypt(message, key_phrase)
        decrypted = decrypt(encrypted, key_phrase)

        self.assertIn('👋', encrypted, "Unmapped character should remain in encrypted text.")
        self.assertEqual(message, decrypted, "Unmapped character should roundtrip correctly.")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['cipher.py', 'encrypt', 'Test Message', 'testkey'])
    @patch('sys.exit') # Mock sys.exit to prevent actual program termination
    def test_main_encrypt(self, mock_exit, mock_stdout):
        main()
        output = mock_stdout.getvalue().strip()
        expected_encrypted = encrypt('Test Message', 'testkey')
        self.assertEqual(output, expected_encrypted)
        mock_exit.assert_not_called() # Should not exit on success

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit') # Mock sys.exit to prevent actual program termination
    def test_main_decrypt(self, mock_exit, mock_stdout):
        original_text = 'Original Text'
        encrypted_text = encrypt(original_text, 'testkey')
        
        with patch('sys.argv', ['cipher.py', 'decrypt', encrypted_text, 'testkey']):
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, original_text)
            mock_exit.assert_not_called() # Should not exit on success

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['cipher.py', 'encrypt', 'message', ''])
    def test_main_error_empty_key_phrase(self, mock_exit, mock_stderr):
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Key phrase cannot be empty.", mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
