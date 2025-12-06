import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys
from io import StringIO

# Adjust sys.path to allow importing the tracker module from src/
# Mock rationale: This allows the test suite to import the utility script as a module
# without needing to install it or modify global Python paths.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import tracker
sys.path.pop(0)

class TestSurvivalSkillTracker(unittest.TestCase):

    def setUp(self):
        # Reset SKILLS_FILE path for tests to ensure it's relative to the mock environment.
        # Mock rationale: Ensures that even if `os.path.exists` or `open` were not mocked,
        # the script wouldn't try to access a real `skills.json` in the test directory.
        self.mock_skills_file = os.path.join(os.path.dirname(__file__), 'mock_skills.json')
        tracker.SKILLS_FILE = self.mock_skills_file

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_skill_new(self, mock_stdout, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty skills file and verify a new skill is added with default rating.
        mock_exists.return_value = False
        mock_json_load.return_value = {}

        tracker.add_skill("Foraging")

        mock_json_dump.assert_called_once_with({"Foraging": 1}, mock_open_file(), indent=4)
        self.assertIn("Skill 'Foraging' added with rating 1.", mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_skill_existing(self, mock_stdout, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an existing skills file and verify no new skill is added if it already exists.
        mock_exists.return_value = True
        mock_json_load.return_value = {"First Aid": 3}

        tracker.add_skill("First Aid")

        mock_json_dump.assert_not_called()
        self.assertIn("Skill 'First Aid' already exists.", mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('sys.stdout', new_callable=StringIO)
    def test_rate_skill_existing(self, mock_stdout, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate rating an existing skill and verify the rating is updated.
        mock_exists.return_value = True
        mock_json_load.return_value = {"Shelter Building": 2}

        tracker.rate_skill("Shelter Building", 4)

        mock_json_dump.assert_called_once_with({"Shelter Building": 4}, mock_open_file(), indent=4)
        self.assertIn("Skill 'Shelter Building' rated 4.", mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('sys.stdout', new_callable=StringIO)
    def test_rate_skill_not_found(self, mock_stdout, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate rating a non-existent skill and verify an error message.
        mock_exists.return_value = True
        mock_json_load.return_value = {"Water Purification": 3}

        tracker.rate_skill("Navigation", 5)

        mock_json_dump.assert_not_called()
        self.assertIn("Skill 'Navigation' not found. Add it first.", mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('sys.stdout', new_callable=StringIO)
    def test_rate_skill_invalid_rating(self, mock_stdout, mock_json_dump, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate rating a skill with an out-of-range value and verify an error message.
        mock_exists.return_value = True
        mock_json_load.return_value = {"Cooking": 3}

        tracker.rate_skill("Cooking", 0)
        tracker.rate_skill("Cooking", 6)

        mock_json_dump.assert_not_called()
        self.assertIn("Rating must be between 1 and 5.", mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_skills_empty(self, mock_stdout, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty skills file and verify the correct message is printed.
        mock_exists.return_value = False
        mock_json_load.return_value = {}

        tracker.list_skills()

        self.assertIn("No skills tracked yet. Add some!", mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_skills_populated(self, mock_stdout, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate a populated skills file and verify all skills are listed correctly.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "First Aid": 4,
            "Foraging": 2,
            "Shelter Building": 3
        }

        tracker.list_skills()
        output = mock_stdout.getvalue()

        self.assertIn("--- Your Survival Skills ---", output)
        self.assertIn("- First Aid: 4/5", output)
        self.assertIn("- Foraging: 2/5", output)
        self.assertIn("- Shelter Building: 3/5", output)
        self.assertIn("--------------------------", output)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=StringIO)
    def test_suggest_improvement_empty(self, mock_stdout, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate an empty skills file and verify no suggestion is made.
        mock_exists.return_value = False
        mock_json_load.return_value = {}

        tracker.suggest_improvement()

        self.assertIn("No skills to suggest. Add some first!", mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=StringIO)
    def test_suggest_improvement_single_lowest(self, mock_stdout, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate skills with a clear lowest-rated skill and verify it's suggested.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "First Aid": 4,
            "Foraging": 1,
            "Shelter Building": 3
        }

        tracker.suggest_improvement()

        self.assertIn("Suggestion: Focus on improving 'Foraging' (current rating: 1/5).", mock_stdout.getvalue())

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('sys.stdout', new_callable=StringIO)
    def test_suggest_improvement_multiple_lowest(self, mock_stdout, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate skills with multiple lowest-rated skills and verify the alphabetically first is suggested.
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "First Aid": 2,
            "Foraging": 1,
            "Water Purification": 1,
            "Shelter Building": 3
        }

        tracker.suggest_improvement()

        # 'Foraging' comes before 'Water Purification' alphabetically
        self.assertIn("Suggestion: Focus on improving 'Foraging' (current rating: 1/5).", mock_stdout.getvalue())

    @patch('sys.argv', ['tracker.py', 'add', 'NewSkill'])
    @patch('tracker.add_skill')
    def test_main_add_command(self, mock_add_skill):
        # Mock rationale: Simulate CLI execution of the 'add' command and verify the correct function is called.
        tracker.main()
        mock_add_skill.assert_called_once_with('NewSkill')

    @patch('sys.argv', ['tracker.py', 'rate', 'ExistingSkill', '3'])
    @patch('tracker.rate_skill')
    def test_main_rate_command(self, mock_rate_skill):
        # Mock rationale: Simulate CLI execution of the 'rate' command and verify the correct function is called.
        tracker.main()
        mock_rate_skill.assert_called_once_with('ExistingSkill', 3)

    @patch('sys.argv', ['tracker.py', 'list'])
    @patch('tracker.list_skills')
    def test_main_list_command(self, mock_list_skills):
        # Mock rationale: Simulate CLI execution of the 'list' command and verify the correct function is called.
        tracker.main()
        mock_list_skills.assert_called_once()

    @patch('sys.argv', ['tracker.py', 'suggest'])
    @patch('tracker.suggest_improvement')
    def test_main_suggest_command(self, mock_suggest_improvement):
        # Mock rationale: Simulate CLI execution of the 'suggest' command and verify the correct function is called.
        tracker.main()
        mock_suggest_improvement.assert_called_once()

    @patch('sys.argv', ['tracker.py'])
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_command(self, mock_print_help):
        # Mock rationale: Simulate CLI execution with no command and verify help is printed.
        tracker.main()
        mock_print_help.assert_called_once()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_skills_corrupt_json(self, mock_json_load, mock_open_file, mock_exists):
        # Mock rationale: Simulate a corrupt JSON file and ensure it returns an empty dictionary gracefully.
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        
        skills = tracker.load_skills()
        self.assertEqual(skills, {})

if __name__ == '__main__':
    unittest.main()
