import unittest
from src.rot13_encoder import rot13

class TestRot13Encoder(unittest.TestCase):
    def test_basic_lowercase(self):
        self.assertEqual(rot13('hello'), 'uryyb')

    def test_basic_uppercase(self):
        self.assertEqual(rot13('WORLD'), 'JBEYQ')

    def test_mixed_case_and_punctuation(self):
        self.assertEqual(rot13('Apocalypse! 123'), 'Ncbcnpvrf! 123')

    def test_symmetry(self):
        original = 'The quick brown fox jumps over the lazy dog.'
        encoded = rot13(original)
        decoded = rot13(encoded)
        self.assertEqual(decoded, original)

    def test_empty_string(self):
        self.assertEqual(rot13(''), '')

if __name__ == '__main__':
    unittest.main()
