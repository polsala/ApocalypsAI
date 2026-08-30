import unittest
from src.main import generate_name, ADJECTIVES, CREATURES

class TestCryptidNamer(unittest.TestCase):
    def test_generate_name_components(self):
        name = generate_name()
        # Split into two parts (adjective and creature)
        parts = name.split(" ", 1)
        self.assertEqual(len(parts), 2)
        adj, creature = parts
        self.assertIn(adj, ADJECTIVES)
        self.assertIn(creature, CREATURES)

    def test_multiple_calls_variability(self):
        # Generate a set of names to ensure variability
        names = {generate_name() for _ in range(20)}
        # Expect at least two distinct names in the sample
        self.assertGreater(len(names), 1)

if __name__ == "__main__":
    unittest.main()
