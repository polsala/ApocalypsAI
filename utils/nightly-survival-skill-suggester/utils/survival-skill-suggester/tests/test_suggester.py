import unittest
from unittest.mock import patch
import random
from src.suggester import suggest_skill, SKILLS_DATABASE

class TestSuggester(unittest.TestCase):

    def test_suggest_skill_specific_keyword_match(self):
        # Test with a keyword that should directly match a skill
        skill = suggest_skill("I need water purification tips")
        self.assertEqual(skill["name"], SKILLS_DATABASE["water"]["name"])

        skill = suggest_skill("how to find food")
        self.assertEqual(skill["name"], SKILLS_DATABASE["food"]["name"])
        
        skill = suggest_skill("build a shelter")
        self.assertEqual(skill["name"], SKILLS_DATABASE["shelter"]["name"])

    def test_suggest_skill_case_insensitivity(self):
        # Test that keywords are case-insensitive
        skill = suggest_skill("FIRST AID needed")
        self.assertEqual(skill["name"], SKILLS_DATABASE["first aid"]["name"])

    @patch('random.choice')
    def test_suggest_skill_no_match_random_choice(self, mock_random_choice):
        # Mock rationale: Ensure deterministic testing for random selections.
        # When no specific keyword matches, the function should pick a random skill.
        # We mock random.choice to control which "random" skill is returned.
        
        # Simulate random.choice returning the 'navigation' skill
        mock_random_choice.return_value = SKILLS_DATABASE["navigation"]
        
        skill = suggest_skill("something completely unrelated")
        self.assertEqual(skill["name"], SKILLS_DATABASE["navigation"]["name"])
        mock_random_choice.assert_called_once() # Ensure random.choice was indeed called

        mock_random_choice.reset_mock() # Reset for the next test
        
        # Simulate random.choice returning the 'fire' skill
        mock_random_choice.return_value = SKILLS_DATABASE["fire"]
        skill = suggest_skill("unknown scenario")
        self.assertEqual(skill["name"], SKILLS_DATABASE["fire"]["name"])
        mock_random_choice.assert_called_once()

    @patch('random.choice')
    def test_suggest_skill_empty_input_random_choice(self, mock_random_choice):
        # Mock rationale: Ensure deterministic testing for random selections.
        # When input is empty, the function should pick a random skill.
        
        mock_random_choice.return_value = SKILLS_DATABASE["communication"]
        skill = suggest_skill("")
        self.assertEqual(skill["name"], SKILLS_DATABASE["communication"]["name"])
        mock_random_choice.assert_called_once()

        mock_random_choice.reset_mock()

        mock_random_choice.return_value = SKILLS_DATABASE["defense"]
        skill = suggest_skill("   ") # Test with whitespace
        self.assertEqual(skill["name"], SKILLS_DATABASE["defense"]["name"])
        mock_random_choice.assert_called_once()

    def test_skills_database_integrity(self):
        # Ensure all skills have the required keys
        for key, skill_info in SKILLS_DATABASE.items():
            with self.subTest(skill=key):
                self.assertIn("name", skill_info)
                self.assertIn("description", skill_info)
                self.assertIn("whimsy", skill_info)
                self.assertIsInstance(skill_info["name"], str)
                self.assertIsInstance(skill_info["description"], str)
                self.assertIsInstance(skill_info["whimsy"], str)
