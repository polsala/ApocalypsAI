import unittest
from unittest.mock import patch
import sys
import pathlib

# Ensure the src directory is on the import path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from compliment import get_compliment

class TestCompliment(unittest.TestCase):
    def test_deterministic_compliment(self):
        """# Mock rationale: force the first template to make the test deterministic"""
        with patch('random.choice', lambda seq: seq[0]):
            result = get_compliment("Alice")
            self.assertEqual(result, "You're a shining star, Alice!")

    def test_all_templates(self):
        """# Mock rationale: iterate over each template to ensure formatting works"""
        templates = [
            "You're a shining star, {name}!",
            "Your brilliance lights up the room, {name}.",
            "Keep being awesome, {name}!",
            "Your smile is contagious, {name}.",
            "You make the world better, {name}!",
        ]
        for tmpl in templates:
            with patch('random.choice', lambda seq, t=tmpl: t):
                result = get_compliment("Bob")
                expected = tmpl.format(name="Bob")
                self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
