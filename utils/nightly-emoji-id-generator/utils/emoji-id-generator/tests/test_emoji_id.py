import unittest
from src.emoji_id import generate_id

class TestEmojiIdGenerator(unittest.TestCase):
    def test_deterministic_output(self):
        # Same seed yields same result
        id1 = generate_id(length=3, seed=123)
        id2 = generate_id(length=3, seed=123)
        self.assertEqual(id1, id2)

    def test_different_seeds(self):
        id1 = generate_id(length=3, seed=1)
        id2 = generate_id(length=3, seed=2)
        self.assertNotEqual(id1, id2)

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            generate_id(length=0)

    def test_default_parameters(self):
        # Ensure the function works with defaults and returns a non‑empty string
        result = generate_id()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

if __name__ == "__main__":
    unittest.main()
