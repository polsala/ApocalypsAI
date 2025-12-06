'''Tests for the deterministic haiku generator.
All tests run offline and use only the standard library.
'''

import unittest

from src.haiku_generator import generate_haiku


class TestHaikuGenerator(unittest.TestCase):
    def test_known_seed(self):
        # Mock rationale: using a fixed seed ensures the output is deterministic.
        seed = 42
        expected = (
            "Silent moonlight glows\n"
            "Whispers echo through the pine forest\n"
            "Crimson leaves fall"
        )
        self.assertEqual(generate_haiku(seed), expected)

    def test_different_seeds_produce_different_haikus(self):
        haiku_a = generate_haiku(1)
        haiku_b = generate_haiku(2)
        self.assertNotEqual(haiku_a, haiku_b)


if __name__ == "__main__":
    unittest.main()
