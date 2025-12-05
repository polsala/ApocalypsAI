import unittest
from src.encoder import encode, decode

class TestWhisperwindEncoder(unittest.TestCase):

    def test_encode_basic(self):
        # Test basic encoding of a lowercase string
        self.assertEqual(encode("hello world"), "svool dliow")

    def test_decode_basic(self):
        # Test basic decoding of a lowercase string
        self.assertEqual(decode("svool dliow"), "hello world")

    def test_encode_case_preservation(self):
        # Test encoding preserves case
        self.assertEqual(encode("Hello World"), "Svool Dliow")

    def test_decode_case_preservation(self):
        # Test decoding preserves case
        self.assertEqual(decode("Svool Dliow"), "Hello World")

    def test_non_alphabetic_characters(self):
        # Test that numbers, symbols, and spaces are passed through unchanged
        message = "Hello, World! 123. How are you?"
        encoded = "Svool, Dliow! 123. Sld ziv blf?"
        self.assertEqual(encode(message), encoded)
        self.assertEqual(decode(encoded), message)

    def test_empty_string(self):
        # Test encoding/decoding an empty string
        self.assertEqual(encode(""), "")
        self.assertEqual(decode(""), "")

    def test_full_alphabet(self):
        # Test encoding the entire alphabet
        self.assertEqual(encode("abcdefghijklmnopqrstuvwxyz"), "zyxwuvtsrqponmlkjihgfedcba")
        self.assertEqual(encode("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), "ZYXWVUTSRQPONMLKJIHGFEDCBA")

    def test_full_cipher_alphabet(self):
        # Test decoding the entire cipher alphabet
        self.assertEqual(decode("zyxwuvtsrqponmlkjihgfedcba"), "abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(decode("ZYXWVUTSRQPONMLKJIHGFEDCBA"), "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_mixed_case_and_symbols(self):
        # Test a complex message with mixed case, numbers, and symbols
        message = "ApocalypsAI is 100% operational! @NightlyIntegrator #ApocalypsAI"
        encoded = "Zkloznbkzhfzr RH 100% lkvizgrlmzo! @MrtsgobRmgvtizglr #Zkloznbkzhfzr"
        self.assertEqual(encode(message), encoded)
        self.assertEqual(decode(encoded), message)

    def test_long_message(self):
        # Test with a longer message to ensure performance and correctness
        long_message = """
        The quick brown fox jumps over the lazy dog. This is a much longer message
        to test the encoder's ability to handle multi-line input and various characters
        without issues. It should maintain all formatting and non-alphabetic content.
        1234567890!@#$%^&*()_+-=[]{}\|;:'\",./<>?`~"
        """
        expected_encoded = """
        Gsv jfrmp yildm ulc qfnkh levi gsv ozab wlt. Gsrh rh z nfcs olmtvi nvhhztv
        gl gvhg gsv vmxlwvi'h zyrorgb gl szmwov nfogr-ormv rmzfg zmw ezirlfh xszizxgvih
        drgslfg rhhfvh. Rg hslfow nzmgrzm zoov uzinfggrmt zmw mlm-zokszyvgrx xlmvmg.
        1234567890!@#$%^&*()_+-=[]{}\|;:'\",./<>?`~"
        """
        self.assertEqual(encode(long_message), expected_encoded)
        self.assertEqual(decode(expected_encoded), long_message)

if __name__ == '__main__':
    unittest.main()
