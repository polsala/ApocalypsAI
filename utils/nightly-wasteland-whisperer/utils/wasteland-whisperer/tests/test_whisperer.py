import unittest
import string
from src.whisperer import generate_cipher_alphabet, encode, decode

class TestWastelandWhisperer(unittest.TestCase):

    def test_generate_cipher_alphabet_simple_keyword(self):
        # Mock rationale: Testing the core logic of alphabet generation with a simple, predictable keyword.
        keyword = "KEY"
        expected_alphabet = "KEYABCDFGHILMNOPQRSTUVWXZ"
        self.assertEqual(generate_cipher_alphabet(keyword), expected_alphabet)

    def test_generate_cipher_alphabet_long_keyword(self):
        # Mock rationale: Testing with a longer keyword to ensure unique character handling and correct alphabet completion.
        keyword = "APOCALYPSE"
        expected_alphabet = "APOCLYSEBDFGHIJKMNQRTVWXZ"
        self.assertEqual(generate_cipher_alphabet(keyword), expected_alphabet)

    def test_generate_cipher_alphabet_duplicate_letters_in_keyword(self):
        # Mock rationale: Ensuring duplicate letters in the keyword are handled correctly (only unique ones are used).
        keyword = "BANANA"
        expected_alphabet = "BANCDFGEHIJKLMOPQRSTUVWXZ"
        self.assertEqual(generate_cipher_alphabet(keyword), expected_alphabet)

    def test_generate_cipher_alphabet_non_alpha_keyword(self):
        # Mock rationale: Testing keyword with non-alphabetic characters to ensure they are ignored.
        keyword = "K3Y!W0RD"
        expected_alphabet = "KYWRDABCEFGHIJLMNOPQSTUVXZ"
        self.assertEqual(generate_cipher_alphabet(keyword), expected_alphabet)

    def test_encode_simple_message(self):
        # Mock rationale: Basic encoding test with a known message and keyword.
        message = "HELLO"
        keyword = "APOCALYPSE"
        expected_encoded = "HQFFB"
        self.assertEqual(encode(message, keyword), expected_encoded)

    def test_decode_simple_message(self):
        # Mock rationale: Basic decoding test with a known encoded message and keyword.
        encoded_message = "HQFFB"
        keyword = "APOCALYPSE"
        expected_decoded = "HELLO"
        self.assertEqual(decode(encoded_message, keyword), expected_decoded)

    def test_round_trip_message(self):
        # Mock rationale: Verifying that encoding followed by decoding returns the original message.
        message = "The quick brown fox jumps over the lazy dog."
        keyword = "SURVIVALGUIDE"
        encoded = encode(message, keyword)
        decoded = decode(encoded, keyword)
        self.assertEqual(decoded, message)

    def test_case_preservation(self):
        # Mock rationale: Ensuring that case is preserved during encoding and decoding.
        message = "Hello Survivor"
        keyword = "APOCALYPSE"
        encoded = encode(message, keyword)
        self.assertEqual(encoded, "Hqffb Suxlxbx")
        decoded = decode(encoded, keyword)
        self.assertEqual(decoded, message)

    def test_non_alphabetic_characters(self):
        # Mock rationale: Confirming that numbers, symbols, and spaces are unchanged.
        message = "Message 123! @#$ %^& *()_+"
        keyword = "SECRET"
        encoded = encode(message, keyword)
        # Only alphabetic characters are transformed, so the message should remain unchanged if it contains only non-alpha
        # For a message with mixed chars, only alpha parts change. Here we test if non-alpha parts are untouched.
        self.assertEqual(encoded, "Pqfsqsq 123! @#$ %^& *()_+") # Example: M->P, e->q, s->f, s->f, a->q, g->s, e->q
        decoded = decode(encoded, keyword)
        self.assertEqual(decoded, message)

    def test_empty_message(self):
        # Mock rationale: Testing behavior with an empty input message.
        message = ""
        keyword = "TEST"
        self.assertEqual(encode(message, keyword), "")
        self.assertEqual(decode(message, keyword), "")

    def test_empty_keyword_raises_error(self):
        # Mock rationale: Ensuring that an empty keyword correctly raises a ValueError.
        message = "Hello"
        keyword = ""
        with self.assertRaises(ValueError):
            encode(message, keyword)
        with self.assertRaises(ValueError):
            decode(message, keyword)

    def test_full_alphabet_encoding_decoding(self):
        # Mock rationale: Testing the full range of the alphabet to ensure all letters map correctly.
        message = string.ascii_uppercase + string.ascii_lowercase
        keyword = "ZOMBIE"
        encoded = encode(message, keyword)
        decoded = decode(encoded, keyword)
        self.assertEqual(decoded, message)

    def test_keyword_with_all_letters(self):
        # Mock rationale: Testing a keyword that contains all letters of the alphabet, ensuring it still works.
        message = "TEST MESSAGE"
        keyword = "THEQUICKBROWNFOXJUMPSOVERLAZYDOG"
        encoded = encode(message, keyword)
        decoded = decode(encoded, keyword)
        self.assertEqual(decoded, message)
