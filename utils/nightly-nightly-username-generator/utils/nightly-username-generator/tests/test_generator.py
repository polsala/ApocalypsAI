import unittest
from utils.nightly-username-generator.src.generator import generate_username

class TestUsernameGenerator(unittest.TestCase):
    def test_deterministic_output(self):
        # Known seeds and their expected usernames (derived from the current pools).
        cases = [
            (0, "fluffy-bunny-whisper"),
            (1, "spiky-dragon-blaze"),
            (5, "fluffy-whisper"),  # seed % 5 == 0 triggers omission of middle part
            (42, "spiky-lynx-ember"),
        ]
        for seed, expected in cases:
            with self.subTest(seed=seed):
                self.assertEqual(generate_username(seed), expected)

    def test_invalid_seed_type(self):
        with self.assertRaises(TypeError):
            generate_username("not-an-int")

    # Mock rationale: No external services are called; the generator is pure.
    # Therefore, tests are fully deterministic and offline.

if __name__ == "__main__":
    unittest.main()
