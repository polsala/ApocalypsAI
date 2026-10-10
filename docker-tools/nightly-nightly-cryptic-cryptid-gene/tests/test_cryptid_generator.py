import unittest
import random
import sys
import os

# Add the src directory to the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

import cryptid_generator

class TestCryptidGenerator(unittest.TestCase):
    def test_generate_deterministic(self):
        # Mock rationale: fixing the random seed ensures deterministic output for testing.
        random.seed(0)
        result = cryptid_generator.generate()
        expected = "The Radiant Luminox, a mysterious creature that dwells in the misty forests and illuminates the night with bioluminescent breath."
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
