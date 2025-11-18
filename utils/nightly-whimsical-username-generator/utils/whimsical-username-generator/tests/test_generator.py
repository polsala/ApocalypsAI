import unittest
from unittest import mock

# Mock rationale: we control randomness via seed, no external I/O needed.
from utils.whimsical-username-generator.src.generator import generate_username

class TestGenerateUsername(unittest.TestCase):
    def test_random_output_is_string(self):
        username = generate_username()
        self.assertIsInstance(username, str)
        self.assertRegex(username, r"^[a-z]+-[a-z]+-\d{2}$")

    def test_deterministic_with_seed(self):
        # Seed 0 should always produce the same username
        expected = generate_username(seed=0)
        for _ in range(5):
            self.assertEqual(generate_username(seed=0), expected)

    def test_different_seeds_produce_different_usernames(self):
        u1 = generate_username(seed=1)
        u2 = generate_username(seed=2)
        self.assertNotEqual(u1, u2)

    def test_number_range(self):
        # Run many times to ensure the numeric suffix stays within 00‑99
        for i in range(100):
            username = generate_username(seed=i)
            number_part = username.split('-')[-1]
            self.assertTrue(0 <= int(number_part) <= 99)

if __name__ == "__main__":
    unittest.main()
