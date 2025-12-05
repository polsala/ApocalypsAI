import unittest
import string
from src.encryptor import encrypt, decrypt, _generate_cipher_map

class TestWhisperwindEncryptor(unittest.TestCase):

    def test_generate_cipher_map_basic(self):
        # Mock rationale: This is an internal helper function, testing its direct output
        # ensures the core cipher logic is correct without external dependencies.
        keyword = "ZOMBIE"
        forward_map, reverse_map = _generate_cipher_map(keyword)
        
        # Expected cipher alphabet: ZOMBIEACDFGHJKLNPQRSTUVWXY
        self.assertEqual(forward_map['A'], 'Z')
        self.assertEqual(forward_map['B'], 'O')
        self.assertEqual(forward_map['C'], 'M')
        self.assertEqual(forward_map['Z'], 'Y') # Z maps to the last char in the cipher alphabet
        
        self.assertEqual(reverse_map['Z'], 'A')
        self.assertEqual(reverse_map['O'], 'B')
        self.assertEqual(reverse_map['M'], 'C')
        self.assertEqual(reverse_map['Y'], 'Z')

        # Ensure all 26 letters are mapped
        self.assertEqual(len(forward_map), 26)
        self.assertEqual(len(reverse_map), 26)
        self.assertTrue(all(k in string.ascii_uppercase for k in forward_map.keys()))
        self.assertTrue(all(v in string.ascii_uppercase for v in reverse_map.values()))

    def test_generate_cipher_map_short_keyword(self):
        # Mock rationale: Testing with a short keyword ensures the alphabet completion logic works.
        keyword = "CAT"
        forward_map, _ = _generate_cipher_map(keyword)
        # Unique chars: CAT
        # Expected: CATBDEFGHJKLMNPQRSTUVWXYZ
        self.assertEqual(forward_map['A'], 'C')
        self.assertEqual(forward_map['B'], 'A')
        self.assertEqual(forward_map['C'], 'T')
        self.assertEqual(forward_map['D'], 'B') # D maps to the next available char after CAT

    def test_generate_cipher_map_long_keyword_with_duplicates(self):
        # Mock rationale: Testing with a long keyword with duplicates ensures duplicate removal.
        keyword = "MISSISSIPPI"
        forward_map, _ = _generate_cipher_map(keyword)
        # Unique chars: MISP
        # Expected: MISPABCDEFGHJKLNORTUVWQXYZ
        self.assertEqual(forward_map['A'], 'M')
        self.assertEqual(forward_map['B'], 'I')
        self.assertEqual(forward_map['C'], 'S')
        self.assertEqual(forward_map['D'], 'P')
        self.assertEqual(forward_map['E'], 'A') # E maps to the next available char after MISP

    def test_encrypt_decrypt_roundtrip(self):
        # Mock rationale: This is the core functionality test, ensuring encryption and decryption
        # are inverses of each other. No external dependencies are involved.
        message = "The quick brown fox jumps over the lazy dog."
        keyword = "APOCALYPSE"
        
        encrypted = encrypt(message, keyword)
        decrypted = decrypt(encrypted, keyword)
        
        self.assertEqual(decrypted, message)
        self.assertNotEqual(encrypted, message) # Ensure it actually changed

    def test_encrypt_decrypt_with_mixed_case(self):
        # Mock rationale: Verifies case preservation for alphabetic characters.
        message = "Hello World! 123"
        keyword = "RAVEN"
        
        encrypted = encrypt(message, keyword)
        decrypted = decrypt(encrypted, keyword)
        
        self.assertEqual(decrypted, message)
        self.assertNotEqual(encrypted, message)
        self.assertEqual(encrypted[0].isupper(), True) # H -> R (uppercase)
        self.assertEqual(encrypted[6].isupper(), True) # W -> O (uppercase)
        self.assertEqual(encrypted[1].islower(), True) # e -> a (lowercase)

    def test_encrypt_decrypt_with_special_characters_and_numbers(self):
        # Mock rationale: Ensures non-alphabetic characters are passed through unchanged.
        message = "Alert! Code 7-Gamma. Rendezvous @ 0300."
        keyword = "SURVIVAL"
        
        encrypted = encrypt(message, keyword)
        decrypted = decrypt(encrypted, keyword)
        
        self.assertEqual(decrypted, message)
        self.assertIn("!", encrypted)
        self.assertIn("7", encrypted)
        self.assertIn("-", encrypted)
        self.assertIn("@", encrypted)
        self.assertIn("0300", encrypted)

    def test_encrypt_decrypt_empty_message(self):
        # Mock rationale: Edge case test for empty input.
        message = ""
        keyword = "KEY"
        
        encrypted = encrypt(message, keyword)
        decrypted = decrypt(encrypted, keyword)
        
        self.assertEqual(encrypted, "")
        self.assertEqual(decrypted, "")

    def test_encrypt_decrypt_no_keyword(self):
        # Mock rationale: Edge case test for empty keyword, should return original message.
        message = "This should not change."
        keyword = ""
        
        encrypted = encrypt(message, keyword)
        decrypted = decrypt(encrypted, keyword)
        
        self.assertEqual(encrypted, message)
        self.assertEqual(decrypted, message)

    def test_encrypt_decrypt_all_caps_message(self):
        # Mock rationale: Test with an all-uppercase message.
        message = "EMERGENCY BROADCAST SYSTEM"
        keyword = "NIGHTFALL"
        
        encrypted = encrypt(message, keyword)
        decrypted = decrypt(encrypted, keyword)
        
        self.assertEqual(decrypted, message)
        self.assertNotEqual(encrypted, message)

    def test_encrypt_decrypt_all_lowercase_message(self):
        # Mock rationale: Test with an all-lowercase message.
        message = "secret rendezvous point"
        keyword = "SHADOW"
        
        encrypted = encrypt(message, keyword)
        decrypted = decrypt(encrypted, keyword)
        
        self.assertEqual(decrypted, message)
        self.assertNotEqual(encrypted, message)

    def test_encrypt_with_same_keyword_as_alphabet(self):
        # Mock rationale: Test a keyword that is the entire alphabet, should result in no change.
        message = "ABC XYZ"
        keyword = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        encrypted = encrypt(message, keyword)
        decrypted = decrypt(encrypted, keyword)
        
        self.assertEqual(encrypted, message) # Should not change as cipher map is identity
        self.assertEqual(decrypted, message)

    def test_encrypt_with_reverse_alphabet_keyword(self):
        # Mock rationale: Test a keyword that reverses the alphabet.
        message = "HELLO"
        keyword = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
        
        encrypted = encrypt(message, keyword)
        # A->Z, B->Y, C->X ... Z->A
        # H->S, E->V, L->O, L->O, O->L
        self.assertEqual(encrypted, "SVOOL")
        decrypted = decrypt(encrypted, keyword)
        self.assertEqual(decrypted, message)

if __name__ == '__main__':
    unittest.main()
