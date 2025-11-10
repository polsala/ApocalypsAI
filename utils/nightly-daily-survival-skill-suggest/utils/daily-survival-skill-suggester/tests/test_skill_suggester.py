import unittest
from unittest.mock import patch
import io
import sys

# Adjust path to import the module from src
sys.path.insert(0, 'utils/daily-survival-skill-suggester/src')
from skill_suggester import get_random_skill, main, SKILLS
sys.path.pop(0) # Clean up path

class TestSkillSuggester(unittest.TestCase):

    @patch('random.choice')
    def test_get_random_skill(self, mock_choice):
        # Mock rationale: random.choice is non-deterministic.
        # We mock it to return a specific skill to ensure the test is deterministic.
        expected_skill = SKILLS[0]
        mock_choice.return_value = expected_skill
        
        skill = get_random_skill()
        self.assertEqual(skill, expected_skill)
        mock_choice.assert_called_once_with(SKILLS)

    @patch('random.choice')
    def test_main_output_format(self, mock_choice):
        # Mock rationale: random.choice is non-deterministic.
        # We mock it to return a specific skill to ensure the test is deterministic.
        expected_skill = {
            "name": "Test Skill",
            "description": "This is a test description.",
            "why_it_matters": "This is why it matters for testing.",
        }
        mock_choice.return_value = expected_skill

        # Mock rationale: sys.stdout is used for printing.
        # We capture stdout to verify the printed output without affecting the console.
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        main()
        
        sys.stdout = sys.__stdout__ # Reset stdout

        output = captured_output.getvalue()
        self.assertIn("--- Your Daily Survival Skill ---", output)
        self.assertIn(f"Skill: {expected_skill['name']}", output)
        self.assertIn(f"Description: {expected_skill['description']}", output)
        self.assertIn(f"Why it matters: {expected_skill['why_it_matters']}", output)
        self.assertIn("---------------------------------", output)
        mock_choice.assert_called_once_with(SKILLS)

    def test_skills_list_not_empty(self):
        self.assertGreater(len(SKILLS), 0, "SKILLS list should not be empty")
        for skill in SKILLS:
            self.assertIsInstance(skill, dict)
            self.assertIn("name", skill)
            self.assertIn("description", skill)
            self.assertIn("why_it_matters", skill)
            self.assertIsInstance(skill["name"], str)
            self.assertIsInstance(skill["description"], str)
            self.assertIsInstance(skill["why_it_matters"], str)
