import unittest
from unittest.mock import patch
import sys
from io import StringIO
import os

# Mock rationale: We need to ensure that `random.choice` always returns a predictable value
# for testing purposes, making the test deterministic. Without mocking, the test would
# be non-deterministic as it would pick a different skill each time.

# Add the 'src' directory to the Python path to allow importing 'scrambler'
# This makes the test self-contained and runnable from the utility's root directory.
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '../src')
sys.path.insert(0, src_path)

import scrambler

# Clean up the path after import to avoid affecting other tests/modules
sys.path.pop(0)

class TestScrambler(unittest.TestCase):

    @patch('random.choice')
    def test_get_random_skill_deterministic(self, mock_choice):
        # Mock rationale: Ensure random.choice returns a specific skill for deterministic testing.
        expected_skill = "Practice knot-tying (bowline, square knot, sheet bend)."
        mock_choice.return_value = expected_skill

        skill = scrambler.get_random_skill()
        self.assertEqual(skill, expected_skill)
        mock_choice.assert_called_once_with(scrambler.SKILLS)

    @patch('random.choice')
    def test_run_scrambler_output(self, mock_choice):
        # Mock rationale: Ensure random.choice returns a specific skill for deterministic testing
        # and capture stdout to verify the printed message from `run_scrambler`.
        expected_skill = "Identify 3 edible wild plants in your area (with caution and expert guidance!)."
        mock_choice.return_value = expected_skill

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            scrambler.run_scrambler() # Call the main execution function
            expected_output = f"Your survival task for today: {expected_skill}\n"
            self.assertEqual(captured_output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__ # Restore stdout

    def test_skills_list_not_empty(self):
        self.assertGreater(len(scrambler.SKILLS), 0, "SKILLS list should not be empty.")
        self.assertIsInstance(scrambler.SKILLS, list, "SKILLS should be a list.")
        for skill in scrambler.SKILLS:
            self.assertIsInstance(skill, str, f"All skills must be strings, found: {type(skill)}")
            self.assertGreater(len(skill), 5, f"Skill description too short: '{skill}'") # Ensure skills are descriptive
