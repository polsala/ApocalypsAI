import unittest
import json
import os
from unittest.mock import patch, mock_open
from src.scribe import SurvivalScribe

class TestSurvivalScribe(unittest.TestCase):

    def setUp(self):
        # Mock the data file path for consistent testing
        self.mock_data_file = "mock_skills.json"
        # Ensure no actual file is created/read during setup
        if os.path.exists(self.mock_data_file):
            os.remove(self.mock_data_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_skills_existing_file(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate an existing skills.json file with content.
        # os.path.exists returns True, open reads the content, json.load parses it.
        mock_os_path_exists.return_value = True
        mock_json_load.return_value = {"water purification": {"name": "Water Purification", "description": "Boil water."}}

        scribe = SurvivalScribe(self.mock_data_file)
        self.assertIn("water purification", scribe.skills)
        self.assertEqual(scribe.skills["water purification"]["description"], "Boil water.")
        mock_os_path_exists.assert_called_once_with(self.mock_data_file)
        mock_file_open.assert_called_once_with(self.mock_data_file, 'r')
        mock_json_load.assert_called_once()

    @patch('os.path.exists')
    def test_load_skills_no_file(self, mock_os_path_exists):
        # Mock rationale: Simulate no existing skills.json file.
        # os.path.exists returns False, so no file operations occur.
        mock_os_path_exists.return_value = False

        scribe = SurvivalScribe(self.mock_data_file)
        self.assertEqual(scribe.skills, {})
        mock_os_path_exists.assert_called_once_with(self.mock_data_file)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_skills_malformed_json(self, mock_json_load, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate an existing skills.json file that is malformed.
        # os.path.exists returns True, but json.load raises an error.
        mock_os_path_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        scribe = SurvivalScribe(self.mock_data_file)
        self.assertEqual(scribe.skills, {}) # Should initialize to empty dict
        mock_os_path_exists.assert_called_once_with(self.mock_data_file)
        mock_file_open.assert_called_once_with(self.mock_data_file, 'r')
        mock_json_load.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=False) # Start with no file
    def test_add_skill(self, mock_os_path_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate adding a new skill and saving it.
        # os.path.exists ensures we start fresh. open and json.dump capture the save operation.
        scribe = SurvivalScribe(self.mock_data_file)
        success, message = scribe.add_skill("First Aid", "Basic wound care.")
        self.assertTrue(success)
        self.assertEqual(message, "Skill 'First Aid' added.")
        self.assertIn("first aid", scribe.skills)
        self.assertEqual(scribe.skills["first aid"]["description"], "Basic wound care.")
        mock_file_open.assert_called_once_with(self.mock_data_file, 'w')
        mock_json_dump.assert_called_once_with(
            {"first aid": {"name": "First Aid", "description": "Basic wound care."}},
            mock_file_open(),
            indent=4
        )

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={"first aid": {"name": "First Aid", "description": "Basic wound care."}})
    def test_add_skill_already_exists(self, mock_json_load, mock_os_path_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate trying to add a skill that already exists.
        # json.load provides initial state. The add operation should fail without saving.
        scribe = SurvivalScribe(self.mock_data_file)
        success, message = scribe.add_skill("First Aid", "Advanced wound care.")
        self.assertFalse(success)
        self.assertEqual(message, "Skill 'First Aid' already exists. Use 'update' to modify.")
        # Ensure save was not called
        mock_json_dump.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={"water purification": {"name": "Water Purification", "description": "Boil water."}})
    def test_update_skill(self, mock_json_load, mock_os_path_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate updating an existing skill and saving it.
        # json.load provides initial state. open and json.dump capture the save operation.
        scribe = SurvivalScribe(self.mock_data_file)
        success, message = scribe.update_skill("Water Purification", "Filter and boil water for 3 minutes.")
        self.assertTrue(success)
        self.assertEqual(message, "Skill 'Water Purification' updated.")
        self.assertEqual(scribe.skills["water purification"]["description"], "Filter and boil water for 3 minutes.")
        mock_file_open.assert_called_once_with(self.mock_data_file, 'w')
        mock_json_dump.assert_called_once_with(
            {"water purification": {"name": "Water Purification", "description": "Filter and boil water for 3 minutes."}},
            mock_file_open(),
            indent=4
        )

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=False) # Start with no file
    def test_update_skill_not_found(self, mock_os_path_exists, mock_json_dump, mock_file_open):
        # Mock rationale: Simulate trying to update a non-existent skill.
        # os.path.exists ensures no initial state. The update operation should fail without saving.
        scribe = SurvivalScribe(self.mock_data_file)
        success, message = scribe.update_skill("Non Existent Skill", "Description.")
        self.assertFalse(success)
        self.assertEqual(message, "Skill 'Non Existent Skill' not found. Use 'add' to create it.")
        mock_json_dump.assert_not_called()

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={"fire starting": {"name": "Fire Starting", "description": "Use flint and steel."}})
    def test_get_skill_exists(self, mock_json_load, mock_os_path_exists):
        # Mock rationale: Simulate retrieving an existing skill.
        # json.load provides initial state.
        scribe = SurvivalScribe(self.mock_data_file)
        skill = scribe.get_skill("Fire Starting")
        self.assertIsNotNone(skill)
        self.assertEqual(skill["name"], "Fire Starting")
        self.assertEqual(skill["description"], "Use flint and steel.")

    @patch('os.path.exists', return_value=False)
    def test_get_skill_not_exists(self, mock_os_path_exists):
        # Mock rationale: Simulate retrieving a non-existent skill from an empty scribe.
        # os.path.exists ensures no initial state.
        scribe = SurvivalScribe(self.mock_data_file)
        skill = scribe.get_skill("Non Existent Skill")
        self.assertIsNone(skill)

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={
        "first aid": {"name": "First Aid", "description": "Basic wound care."},
        "water purification": {"name": "Water Purification", "description": "Boil water."},
        "shelter building": {"name": "Shelter Building", "description": "Build a lean-to."}
    })
    def test_list_skills(self, mock_json_load, mock_os_path_exists):
        # Mock rationale: Simulate listing all skills.
        # json.load provides initial state.
        scribe = SurvivalScribe(self.mock_data_file)
        skills = scribe.list_skills()
        self.assertEqual(len(skills), 3)
        self.assertEqual(skills[0]["name"], "First Aid") # Sorted alphabetically
        self.assertEqual(skills[1]["name"], "Shelter Building")
        self.assertEqual(skills[2]["name"], "Water Purification")

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={
        "first aid": {"name": "First Aid", "description": "Basic wound care."},
        "water purification": {"name": "Water Purification", "description": "Boil water for drinking."},
        "shelter building": {"name": "Shelter Building", "description": "Build a lean-to for protection."}
    })
    def test_search_skills(self, mock_json_load, mock_os_path_exists):
        # Mock rationale: Simulate searching for skills by keyword.
        # json.load provides initial state.
        scribe = SurvivalScribe(self.mock_data_file)

        results = scribe.search_skills("water")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Water Purification")

        results = scribe.search_skills("build")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Shelter Building")

        results = scribe.search_skills("care")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "First Aid")

        results = scribe.search_skills("nonexistent")
        self.assertEqual(len(results), 0)

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={
        "first aid": {"name": "First Aid", "description": "Basic wound care."},
        "water purification": {"name": "Water Purification", "description": "Boil water for drinking."},
    })
    def test_search_skills_case_insensitive(self, mock_json_load, mock_os_path_exists):
        # Mock rationale: Test case-insensitivity for search.
        # json.load provides initial state.
        scribe = SurvivalScribe(self.mock_data_file)

        results = scribe.search_skills("Water")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Water Purification")

        results = scribe.search_skills("care")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "First Aid")

    @patch('os.path.exists', return_value=True)
    @patch('json.load', return_value={
        "first aid": {"name": "First Aid", "description": "Basic wound care."},
        "first aid advanced": {"name": "First Aid Advanced", "description": "Advanced wound care."},
    })
    def test_search_multiple_results(self, mock_json_load, mock_os_path_exists):
        # Mock rationale: Test search returning multiple results.
        # json.load provides initial state.
        scribe = SurvivalScribe(self.mock_data_file)

        results = scribe.search_skills("first aid")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["name"], "First Aid")
        self.assertEqual(results[1]["name"], "First Aid Advanced")


if __name__ == '__main__':
    unittest.main()
