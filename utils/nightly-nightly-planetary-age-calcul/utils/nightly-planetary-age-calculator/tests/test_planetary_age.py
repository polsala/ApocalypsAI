import unittest
import os
import sys

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from planetary_age import age_on_planet

class TestPlanetaryAge(unittest.TestCase):
    def test_known_values(self):
        # 1 Earth year on Mercury ≈ 4.15 years
        self.assertAlmostEqual(age_on_planet(1, "mercury"), 4.15)
        # 30 Earth years on Mars ≈ 15.96 years
        self.assertAlmostEqual(age_on_planet(30, "mars"), 15.96)
        # 0 Earth years on any planet should be 0.0
        self.assertEqual(age_on_planet(0, "jupiter"), 0.0)

    def test_invalid_planet(self):
        with self.assertRaises(ValueError):
            age_on_planet(10, "krypton")

if __name__ == "__main__":
    unittest.main()
