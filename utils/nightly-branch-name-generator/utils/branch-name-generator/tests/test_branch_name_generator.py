import unittest
import random
import sys
import os

# Add the src directory to the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from branch_name_generator import generate_branch_name

class TestBranchNameGenerator(unittest.TestCase):
    def setUp(self):
        # Deterministic seed for reproducibility
        random.seed(0)  # Mock rationale: fixed seed ensures deterministic output

    def test_default_two_word_name(self):
        name = generate_branch_name()
        # With seed 0, the first adjective is "whispering" and the first noun is "nebula"
        self.assertEqual(name, "whispering-nebula")

    def test_three_word_name(self):
        name = generate_branch_name(3)
        # Sequence: adjective, noun, adjective -> "whispering-nebula-fuzzy"
        self.assertEqual(name, "whispering-nebula-fuzzy")

    def test_length_constraint(self):
        # Generate a long name and ensure it respects the 50‑char limit
        name = generate_branch_name(20)
        self.assertTrue(len(name) <= 50)

    def test_invalid_num_words(self):
        with self.assertRaises(ValueError):
            generate_branch_name(0)

if __name__ == "__main__":
    unittest.main()
